"""
Create a controller function to create a new Incident.

Requirements:
- Accept IncidentCreate schema
- Create Incident SQLAlchemy object
- Set status to "OPEN"
- Save to database using SQLAlchemy session
- Return the created Incident

"""

from datetime import datetime
import os
import json
import logging
from sqlalchemy.orm import Session
from app.db.models import Incident
from app.models.incident import IncidentCreate
from app.services.replay_engine import ReplayEngine
from app.ai.ai_resolver import AIResolver
from app.ai.ai_factory import get_ai_client
from app.integrations.client_factory import get_erp_client
from fastapi import HTTPException, status
import json


def create_incident(incident_data: IncidentCreate, db: Session) -> Incident:
    """
    Create a new incident in the database.
    
    Args:
        incident_data: IncidentCreate schema with incident details
        db: SQLAlchemy database session
    
    Returns:
        Created Incident object
    """
    existing = (
        db.query(Incident)
        .filter(Incident.erp_reference == incident_data.erp_reference)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Incident with ERP reference '{incident_data.erp_reference}' already exists"
        )
    db_incident = Incident(
        erp_reference=incident_data.erp_reference,
        incident_type=incident_data.incident_type,
        description=incident_data.description,
        status="OPEN"
    )
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident


def get_incident_by_id(incident_id: int, db: Session) -> Incident | None:
    """
    Get an incident by ID from the database.
    
    Args:
        incident_id: The ID of the incident to retrieve
        db: SQLAlchemy database session
    
    Returns:
        Incident object if found, None otherwise
    """
    return db.query(Incident).filter(Incident.id == incident_id).first()


def get_all_incidents(db: Session) -> list[Incident]:
    """
    Get all incidents from the database.
    
    Args:
        db: SQLAlchemy database session
    
    Returns:
        List of all Incident objects
    """
    return db.query(Incident).all()


def run_replay_for_incident(incident_id: int, db: Session) -> Incident | None:
    """
    Run replay analysis for an incident.
    
    Args:
        incident_id: The ID of the incident to replay
        db: SQLAlchemy database session
    
    Returns:
        Updated Incident object if found, None otherwise
    """
    incident = get_incident_by_id(incident_id, db)
    if incident is None:
        return None
    
    # Initialize ReplayEngine (it will handle ERP client selection via factory)
    replay_engine = ReplayEngine()
    
    # Use ReplayEngine to analyze the incident
    analysis = replay_engine.analyze_incident(incident)
    
    # Populate replay fields from analysis
    incident.replay_summary = analysis["summary"]
    incident.replay_details = analysis["details"]
    incident.replay_conclusion = analysis["conclusion"]
    incident.analysis_source = analysis.get("analysis_source", "RULE")
    incident.confidence_score = analysis.get("confidence", 0.0)
    incident.status = "ANALYZED"
    incident.replayed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(incident)
    return incident


def resolve_incident(incident_id: int, db: Session) -> Incident | None:
    """
    Resolve an incident using STRICT AI-ONLY or RULE-ONLY path.
    
    CRITICAL GUARANTEES:
    1. If AI_ENABLED=true → AI ONLY (no rule execution)
    2. If AI_ENABLED=false → RULE ONLY (no AI execution)
    3. If AI fails → status = UNDER_REVIEW, analysis_source = AI_FAILED
    4. NEVER mark RESOLVED if AI failed
    5. analysis_source = "AI" only when AI succeeds
    6. analysis_source = "RULE" only when rule path taken
    7. NO fallback between paths. NO merging of results.
    
    Args:
        incident_id: The ID of the incident to resolve
        db: SQLAlchemy database session
    
    Returns:
        Updated Incident object if found, None otherwise
    """
    logger = logging.getLogger(__name__)
    
    incident = get_incident_by_id(incident_id, db)
    if incident is None:
        return None
    
    # Parse AI_ENABLED as boolean (strict: "true"/"1"/"yes"/"on" → True)
    ai_enabled = os.getenv("AI_ENABLED", "").strip().lower() in ("true", "1", "yes", "on")
    
    if ai_enabled:
        # === PATH 1: AI ANALYSIS ONLY ===
        logger.info(f"resolve_incident: AI path for incident {incident_id}")
        return _resolve_with_ai(incident, incident_id, db)
    else:
        # === PATH 2: RULE-BASED ANALYSIS ONLY ===
        logger.info(f"resolve_incident: RULE path for incident {incident_id}")
        return _resolve_with_rules(incident, incident_id, db)


def _resolve_with_ai(incident: Incident, incident_id: int, db: Session) -> Incident:
    """
    Resolve using AI analysis only.
    
    If AI fails → status = UNDER_REVIEW, analysis_source = AI_FAILED
    If AI succeeds → status = RESOLVED, analysis_source = AI
    
    NEVER marks RESOLVED on AI failure.
    """
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"_resolve_with_ai: Getting Claude client for incident {incident_id}")
        ai_client = get_ai_client()
        
        logger.info(f"_resolve_with_ai: Running AI analysis for incident {incident_id}")
        ai_result = _run_ai_analysis_for_incident(incident, ai_client)
        
        if not ai_result:
            raise RuntimeError("AI analysis returned empty result")
        
        # AI succeeded - persist AI result
        logger.info(f"_resolve_with_ai: AI succeeded for incident {incident_id}")
        incident.replay_summary = ai_result.get("summary", "")
        incident.replay_details = ai_result.get("details", "")
        incident.replay_conclusion = ai_result.get("conclusion", "")
        incident.confidence_score = ai_result.get("confidence_score", 0.0)
        incident.analysis_source = "AI"
        incident.status = "RESOLVED"
        incident.replayed_at = datetime.utcnow()
        
        if "ai_raw_response" in ai_result:
            incident.ai_analysis_json = json.dumps(ai_result["ai_raw_response"])
        
        db.commit()
        db.refresh(incident)
        return incident
    
    except Exception as e:
        # AI FAILED - mark as UNDER_REVIEW, NOT RESOLVED
        logger.error(f"_resolve_with_ai: AI FAILED for incident {incident_id}: {str(e)}")
        incident.status = "UNDER_REVIEW"
        incident.replay_summary = "AI analysis failed"
        incident.replay_details = f"AI Error: {str(e)}"
        incident.replay_conclusion = "Manual review required - AI could not complete analysis"
        incident.confidence_score = 0.0
        incident.analysis_source = "AI_FAILED"
        incident.replayed_at = datetime.utcnow()
        
        db.commit()
        db.refresh(incident)
        return incident


def _resolve_with_rules(incident: Incident, incident_id: int, db: Session) -> Incident:
    """
    Resolve using rule-based analysis only.
    
    No AI involved. Pure rule-based.
    """
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"_resolve_with_rules: Running rule-based analysis for incident {incident_id}")
        
        replay_engine = ReplayEngine()
        rule_analysis = replay_engine.analyze_incident(incident)
        
        # Persist rule result
        incident.replay_summary = rule_analysis.get("summary", "")
        incident.replay_details = rule_analysis.get("details", "")
        incident.replay_conclusion = rule_analysis.get("conclusion", "")
        incident.confidence_score = rule_analysis.get("confidence", 0.0)
        incident.analysis_source = "RULE"
        incident.status = "RESOLVED"
        incident.replayed_at = datetime.utcnow()
        
        logger.info(f"_resolve_with_rules: Rule analysis succeeded for incident {incident_id}")
        
        db.commit()
        db.refresh(incident)
        return incident
    
    except Exception as e:
        # Rule analysis failed - still mark as error (not AI_FAILED)
        logger.error(f"_resolve_with_rules: Rule analysis FAILED for incident {incident_id}: {str(e)}")
        incident.status = "UNDER_REVIEW"
        incident.replay_summary = "Rule analysis error"
        incident.replay_details = f"Error: {str(e)}"
        incident.replay_conclusion = "Manual review required"
        incident.confidence_score = 0.0
        incident.analysis_source = "RULE_FAILED"
        incident.replayed_at = datetime.utcnow()
        
        db.commit()
        db.refresh(incident)
        return incident


def _run_ai_analysis_for_incident(incident: Incident, ai_client) -> dict:
    """
    Run AI analysis with STRICT validation.

    Calls AIResolver which:
    - Calls Claude API (via AIClientAnthropic)
    - Maps response using AIResultMapper (strict validation)
    - Raises RuntimeError on ANY failure (no fallback)

    Args:
        incident: Incident object to analyze
        ai_client: AI client implementation (AIClientAnthropic)

    Returns:
        Dict with validated AI result or raises RuntimeError

    Raises:
        RuntimeError: On ANY failure (API error, validation error, etc.)
    """
    logger = logging.getLogger(__name__)

    try:
        logger.info(f"_run_ai_analysis_for_incident: Gathering ERP context for incident {incident.id}")
        erp_client = get_erp_client()
        erp_data = _gather_erp_data_for_incident(incident, erp_client)

        logger.info(f"_run_ai_analysis_for_incident: Calling AIResolver for incident {incident.id}")
        resolver = AIResolver(ai_client=ai_client)
        ai_resolution = resolver.resolve_incident(incident, erp_data)

        if not ai_resolution:
            raise RuntimeError("AIResolver returned empty response")

        logger.info(f"_run_ai_analysis_for_incident: AIResolver succeeded for incident {incident.id}")
        
        # Return the mapped result from AIResolver
        return {
            "summary": ai_resolution.get("replay_summary", ""),
            "details": ai_resolution.get("replay_details", ""),
            "conclusion": ai_resolution.get("replay_conclusion", ""),
            "confidence_score": ai_resolution.get("confidence_score", 0.0),
            "ai_raw_response": ai_resolution
        }

    except Exception as e:
        logger.error(f"_run_ai_analysis_for_incident: FAILED for incident {incident.id}: {str(e)}", exc_info=True)
        # Let exception propagate to controller (which will mark as UNDER_REVIEW)
        raise RuntimeError(f"AI analysis failed: {str(e)}") from e


def _gather_erp_data_for_incident(incident: Incident, erp_client) -> dict:
    """
    Gather ERP data for AI analysis context.
    
    Args:
        incident: Incident object
        erp_client: ERP client for data retrieval
    
    Returns:
        Dictionary with invoice, sales_order, and customer data
    """
    logger = logging.getLogger(__name__)
    
    try:
        invoice_id = incident.erp_reference
        
        # Fetch invoice
        invoice_data = erp_client.get_invoice(invoice_id) or {}
        logger.debug(f"Invoice {invoice_id} fetched: {list(invoice_data.keys())}")
        
        # Fetch linked sales order from invoice header
        sales_order_data = {}
        
        # Try multiple field names (ERPNext API uses different field names)
        sales_order_id = (
            invoice_data.get("sales_order") or
            invoice_data.get("so_no") or
            invoice_data.get("linked_sales_order")
        )
        
        logger.debug(f"Invoice {invoice_id} SO ID attempt: {sales_order_id}")
        
        # If not found at header level, try from first item (fallback)
        if not sales_order_id:
            items = invoice_data.get("items", [])
            if items and isinstance(items, list) and len(items) > 0:
                first_item = items[0]
                sales_order_id = (
                    first_item.get("sales_order") or
                    first_item.get("so_no") or
                    first_item.get("linked_sales_order")
                )
                logger.debug(f"Invoice {invoice_id} SO ID from first item: {sales_order_id}")
        
        # Fetch sales order if found
        if sales_order_id:
            logger.info(f"Fetching Sales Order {sales_order_id} for invoice {invoice_id}")
            sales_order_data = erp_client.get_sales_order(sales_order_id) or {}
            logger.info(f"Sales Order {sales_order_id} fetched successfully")
        else:
            logger.warning(f"No sales order linked to invoice {invoice_id}")
        
        # Fetch customer data
        customer_data = {}
        customer_name = invoice_data.get("customer_name")
        if customer_name:
            customer_data = erp_client.get_customer(customer_name) or {}
        
        return {
            "invoice": invoice_data,
            "sales_order": sales_order_data,
            "customer": customer_data
        }
    
    except Exception as e:
        logger.error(f"Error gathering ERP data for incident {incident.erp_reference}: {str(e)}", exc_info=True)
        # Return empty data structure on error
        return {
            "invoice": {"error": str(e)},
            "sales_order": {},
            "customer": {}
        }