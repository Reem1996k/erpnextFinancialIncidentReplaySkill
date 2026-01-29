"""
Incident Analysis Service with ERP Data Extraction

Coordinates ERP data extraction, AI analysis, and database persistence.
Validates data completeness before calling AI.
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime
import json

from app.db.database import SessionLocal
from app.db.models import Incident
from app.services.erp_financial_extractor import (
    ERPNextFinancialExtractor,
    ERPSnapshotValidator
)
from app.integrations.client_factory import get_erp_client
from app.ai.ai_factory import get_ai_client
from app.ai.prompt_builder_financial import build_financial_analysis_prompt

logger = logging.getLogger(__name__)


class IncidentAnalysisService:
    """
    Orchestrates complete incident analysis workflow.
    
    Flow:
    1. Extract ERP snapshot (invoice + sales order)
    2. Validate completeness
    3. If incomplete: mark UNDER_REVIEW with BACKEND_DATA_INCOMPLETE
    4. If complete: call AI for analysis
    5. Save results to database
    """

    def __init__(self):
        """Initialize with ERP and AI clients."""
        self.erp_client = get_erp_client()
        try:
            self.ai_client = get_ai_client()
            self.ai_enabled = True
        except:
            self.ai_client = None
            self.ai_enabled = False
        self.extractor = ERPNextFinancialExtractor(self.erp_client)

    def analyze_incident(self, incident: Incident, db: Optional[Any] = None) -> Dict[str, Any]:
        """
        Perform complete incident analysis.
        
        Args:
            incident: Incident model instance
            db: Database session
        
        Returns:
            Analysis result with status, confidence, and conclusions
        """
        if db is None:
            db = SessionLocal()
            close_session = True
        else:
            close_session = False

        try:
            # Step 1: Extract ERP snapshot
            logger.info(f"Extracting ERP data for incident {incident.id}")
            snapshot = self.extractor.extract_invoice_snapshot(incident.erp_reference)

            # Step 2: Validate completeness
            is_complete = ERPSnapshotValidator.is_complete(snapshot)
            
            if not is_complete:
                # Data incomplete - no AI analysis
                logger.warning(f"Incomplete ERP data for incident {incident.id}")
                result = self._handle_incomplete_data(incident, snapshot, db)
            else:
                # Data complete - call AI
                logger.info(f"Complete ERP data for incident {incident.id}, calling AI")
                result = self._perform_ai_analysis(incident, snapshot, db)

            return result

        except Exception as e:
            logger.exception(f"Error analyzing incident {incident.id}")
            return self._handle_error(incident, str(e), db)

        finally:
            if close_session:
                db.close()

    def _perform_rule_based_analysis(
        self,
        incident: Incident,
        snapshot: Dict[str, Any],
        db: Any
    ) -> Dict[str, Any]:
        """
        Perform rule-based analysis on complete ERP snapshot.
        """
        invoice = snapshot.get("invoice", {})
        sales_order = snapshot.get("sales_order", {})
        
        inv_total = invoice.get("grand_total", 0)
        so_total = sales_order.get("grand_total", 0)
        
        if so_total == 0:
            variance_pct = 0
        else:
            variance_pct = ((inv_total - so_total) / so_total) * 100
        
        # Determine status based on variance
        if abs(variance_pct) <= 20:
            status = "RESOLVED"
        else:
            status = "UNDER_REVIEW"
        
        summary = f"Invoice total {inv_total} vs agreed {so_total} ({variance_pct:+.1f}%)"
        conclusion = f"Variance {abs(variance_pct):.1f}% is {'within' if abs(variance_pct) <= 20 else 'outside'} ±20% threshold"
        
        incident.status = status
        incident.analysis_source = "RULE_BASED_WITH_ERP_SNAPSHOT"
        incident.replay_summary = summary
        incident.replay_details = f"Invoice: {invoice.get('id')}, SO: {sales_order.get('id')}"
        incident.replay_conclusion = conclusion
        incident.confidence_score = 0.85
        incident.replayed_at = datetime.utcnow()
        
        db.commit()
        db.refresh(incident)
        
        logger.info(f"Incident {incident.id} analyzed by rules: {summary}")
        
        return {
            "incident_id": incident.id,
            "status": incident.status,
            "analysis_source": incident.analysis_source,
            "confidence": incident.confidence_score,
            "summary": incident.replay_summary,
            "details": incident.replay_details,
            "conclusion": incident.replay_conclusion
        }

    def _perform_ai_analysis(
    self,
    incident: Incident,
    snapshot: Dict[str, Any],
    db: Any
) -> Dict[str, Any]:

        if not self.ai_enabled or not self.ai_client:
            return self._perform_rule_based_analysis(incident, snapshot, db)

        try:
            prompt = self._build_analysis_prompt(snapshot)

            ai_response = self.ai_client.analyze(prompt)

            # --- הגנה מוחלטת על DB ---
            replay_summary = str(ai_response.get("replay_summary", "AI analysis completed"))
            replay_details = ai_response.get("replay_details", "")
            replay_conclusion = str(ai_response.get("replay_conclusion", ""))

            confidence = ai_response.get("confidence_score", 0.5)
            try:
                confidence = float(confidence)
            except:
                confidence = 0.5

            incident.status = "RESOLVED"
            incident.analysis_source = "AI_WITH_ERP_SNAPSHOT"
            incident.replay_summary = replay_summary

            # SQLite לא תומך dict
            incident.replay_details = (
                json.dumps(replay_details, ensure_ascii=False)
                if isinstance(replay_details, (dict, list))
                else str(replay_details)
            )

            incident.replay_conclusion = replay_conclusion
            incident.confidence_score = confidence

            # תמיד JSON string
            incident.ai_analysis_json = json.dumps(ai_response, ensure_ascii=False)

            incident.replayed_at = datetime.utcnow()

            db.commit()
            db.refresh(incident)

            return {
                "incident_id": incident.id,
                "status": incident.status,
                "analysis_source": incident.analysis_source,
                "confidence": incident.confidence_score,
                "summary": incident.replay_summary,
                "details": incident.replay_details,
                "conclusion": incident.replay_conclusion
            }

        except Exception as e:
            db.rollback()
            logger.exception(f"AI analysis failed for incident {incident.id}")
            return self._handle_error(incident, f"AI analysis error: {str(e)}", db)

    def _handle_incomplete_data(
        self,
        incident: Incident,
        snapshot: Dict[str, Any],
        db: Any
    ) -> Dict[str, Any]:
        """
        Handle cases where ERP data is incomplete.
        Mark incident and don't call AI.
        """
        reason = ERPSnapshotValidator.get_completeness_reason(snapshot)
        missing = ERPSnapshotValidator.get_missing_fields(snapshot)

        incident.status = "UNDER_REVIEW"
        incident.analysis_source = "BACKEND_DATA_INCOMPLETE"
        incident.replay_summary = f"Cannot analyze: {reason}"
        incident.replay_details = f"Missing: {', '.join(missing)}"
        incident.replay_conclusion = (
            "Waiting for complete Sales Order data. "
            "Once linked Sales Order is available in ERP, analysis can proceed."
        )
        incident.confidence_score = 0.0
        incident.replayed_at = datetime.utcnow()

        db.commit()
        db.refresh(incident)

        logger.info(f"Incident {incident.id} marked UNDER_REVIEW: {reason}")

        return {
            "incident_id": incident.id,
            "status": incident.status,
            "analysis_source": incident.analysis_source,
            "confidence": incident.confidence_score,
            "reason": reason,
            "missing_fields": missing
        }

    def _handle_error(
    self,
    incident: Incident,
    error_message: str,
    db: Any
) -> Dict[str, Any]:

        try:
            db.rollback()
        except:
            pass

        incident.status = "ERROR"
        incident.analysis_source = "ANALYSIS_ERROR"
        incident.replay_summary = "Analysis error occurred"
        incident.replay_details = ""
        incident.replay_conclusion = error_message
        incident.confidence_score = 0.0
        incident.replayed_at = datetime.utcnow()

        try:
            db.commit()
        except:
            pass

        logger.error(f"Incident {incident.id} analysis error: {error_message}")

        return {
            "incident_id": incident.id,
            "status": incident.status,
            "error": error_message
        }


    def _build_analysis_prompt(self, snapshot: Dict[str, Any]) -> str:
        """
        Build AI analysis prompt using generic financial analysis prompt builder.
        
        Uses the new generic prompt that works for ANY invoice/SO pair
        and provides data-driven discrepancy analysis.
        """
        invoice = snapshot.get("invoice", {})
        sales_order = snapshot.get("sales_order", {})
        incident_description = (
            f"Financial discrepancy detected between invoice {invoice.get('id')} "
            f"and sales order {sales_order.get('id')}. "
            f"Invoice total: {invoice.get('grand_total')} vs SO total: {sales_order.get('grand_total')}"
        )
        
        # Use the new generic prompt builder
        prompt = build_financial_analysis_prompt(
            invoice=invoice,
            sales_order=sales_order,
            incident_description=incident_description
        )
        
        return prompt

    def _structure_ai_response(self, ai_response: str) -> Dict[str, Any]:
        """
        Structure AI response into standardized incident fields.
        
        Expects JSON response from the prompt builder with fields:
        - root_cause
        - difference_breakdown
        - recommended_resolution
        - confidence_score
        """
        try:
            # Parse Claude's JSON response
            parsed = json.loads(ai_response)
            
            # Extract fields from new prompt format
            root_cause = parsed.get("root_cause", "Unable to determine root cause")
            difference_breakdown = parsed.get("difference_breakdown", "")
            recommendation = parsed.get("recommended_resolution", "")
            confidence = parsed.get("confidence_score", 0.5)
            
            # Ensure confidence is a float between 0 and 1
            try:
                confidence = float(confidence)
                confidence = max(0.0, min(1.0, confidence))
            except (ValueError, TypeError):
                confidence = 0.5
            
            # Build structured response
            return {
                "summary": root_cause,
                "details": difference_breakdown,
                "conclusion": recommendation,
                "confidence": confidence,
                "status": "RESOLVED" if confidence >= 0.7 else "UNDER_REVIEW",
                "raw_response": ai_response
            }
        except json.JSONDecodeError:
            # Fallback if response is not valid JSON
            logger.warning(f"Could not parse AI response as JSON: {ai_response[:200]}")
            return {
                "summary": "Analysis completed",
                "details": ai_response,
                "conclusion": "See details above",
                "confidence": 0.5,
                "status": "UNDER_REVIEW",
                "raw_response": ai_response
            }

