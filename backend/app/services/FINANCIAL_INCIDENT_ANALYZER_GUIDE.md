"""
FINANCIAL INCIDENT ANALYZER - IMPLEMENTATION GUIDE

This document describes the Financial Incident Analyzer backend service implementation.

ARCHITECTURE OVERVIEW
====================

The analyzer follows a strict separation of concerns:

1. ERP DATA EXTRACTION (Backend)
   ├─ Fetches Invoice from ERPNext
   ├─ Fetches linked Sales Order
   ├─ Validates completeness
   └─ Returns immutable ERP snapshot

2. AI ANALYSIS (AI Layer)
   ├─ Receives ERP snapshot only
   ├─ Performs numeric comparisons
   ├─ Analyzes discrepancies
   └─ Returns analysis in JSON format

3. BUSINESS RULES (Backend)
   ├─ Evaluates AI response
   ├─ Applies status decision rules
   ├─ Persists results to incident
   └─ Returns final analysis result

CRITICAL GUARANTEES:
- AI MUST NOT fetch ERP data
- AI MUST NOT ask for input
- ERPNext is single source of truth
- Backend owns all data extraction
- All ERP data is validated before AI sees it


SERVICES CREATED
===============

1. ERPDataExtractor (erp_data_extractor.py)
   - Class: ERPDataExtractor
   - Primary method: extract_incident_data(incident_reference)
   - Returns: Complete ERP snapshot with all financial details
   - Responsibilities:
     * Fetch invoice with items, taxes, charges
     * Fetch linked sales order
     * Extract customer information
     * Validate data completeness
     * Mark missing fields explicitly

2. FinancialIncidentAnalyzer (financial_incident_analyzer.py)
   - Class: FinancialIncidentAnalyzer
   - Primary method: analyze_incident(incident, db=None)
   - Returns: Complete analysis result with status and reasoning
   - Workflow:
     * Extract ERP data
     * Build AI prompt
     * Call AI analysis
     * Apply business rules
     * Persist results (if db provided)

3. Integration Functions (financial_incident_analyzer_integration.py)
   - Function: analyze_incident_with_ai(incident, db)
   - Function: analyze_incident_with_ai_no_persist(incident)
   - Function: get_erp_snapshot_for_incident(incident)
   - Function: update_incident_from_analysis(incident, result, db)
   - Responsibilities: Connect analyzer to existing codebase


DETAILED API REFERENCE
=====================

1. ERPDataExtractor.extract_incident_data(invoice_id)

   Extracts complete financial data for analysis.

   Args:
       invoice_id (str): The invoice ID from ERP reference

   Returns:
       Dict with structure:
       {
           "status": "SUCCESS" | "INCOMPLETE" | "ERROR",
           "invoice": {
               "name": str,
               "customer": str,
               "posting_date": str,
               "due_date": str,
               "currency": str,
               "items": [
                   {
                       "item_code": str,
                       "quantity": float,
                       "rate": float,
                       "amount": float
                   },
                   ...
               ],
               "subtotal": float,
               "taxes": [
                   {
                       "tax_type": str,
                       "tax_rate": float,
                       "tax_amount": float
                   },
                   ...
               ],
               "extra_charges": [
                   {
                       "charge_type": str,
                       "charge_amount": float
                   },
                   ...
               ],
               "rounding_adjustment": float,
               "total": float,
               "status": int,
               "remarks": str
           },
           "sales_order": {
               "name": str,
               "customer": str,
               "creation_date": str,
               "currency": str,
               "items": [
                   {
                       "item_code": str,
                       "quantity": float,
                       "agreed_rate": float,
                       "amount": float
                   },
                   ...
               ],
               "subtotal": float,
               "taxes": [...],
               "agreed_total": float,
               "status": int,
               "remarks": str
           } | null,
           "customer": {
               "name": str,
               "customer_name": str,
               "email": str,
               "credit_limit": float,
               "outstanding": float,
               "country": str,
               "territory": str,
               "payment_terms": str
           } | null,
           "missing_fields": [
               "sales_order_not_linked",  # Example
               ...
           ],
           "extraction_notes": [str, ...]
       }

   Raises:
       ValueError: If invoice_id is None/empty
       RuntimeError: If ERP client fails


2. FinancialIncidentAnalyzer.analyze_incident(incident, db=None)

   Main entry point for incident analysis.

   Args:
       incident (Incident): The incident database record
       db (Session): Optional SQLAlchemy session for persistence

   Returns:
       Dict with structure:
       {
           "incident_id": int,
           "incident_type": str,
           "incident_reference": str,
           "status": "RESOLVED" | "UNDER_REVIEW",
           "replay_summary": str,
           "replay_details": str,
           "discrepancy_source": str,
           "difference_breakdown": Dict,
           "replay_conclusion": str,
           "confidence_score": float,
           "analysis_source": "AI" | "EXTRACTION_ERROR" | "AI_FAILED",
           "erp_snapshot_status": "SUCCESS" | "INCOMPLETE" | "ERROR",
           "erp_extraction_notes": [str, ...],
           "missing_fields": [str, ...],
           "erp_data": {
               "invoice": {...},
               "sales_order": {...},
               "customer": {...}
           },
           "replayed_at": ISO datetime string
       }

   Status Decision Rules:
       - If discrepancy_source == "INSUFFICIENT_DATA" → "UNDER_REVIEW"
       - If confidence_score < 0.5 → "UNDER_REVIEW"
       - Otherwise → "RESOLVED"

   Raises:
       ValueError: If incident data invalid
       RuntimeError: If extraction or AI fails


3. analyze_incident_with_ai(incident, db=None)

   Integration function for controllers. Handles setup and orchestration.

   Args:
       incident (Incident): Incident to analyze
       db (Session): Optional database session for persistence

   Returns:
       Complete analysis result (same as FinancialIncidentAnalyzer.analyze_incident)

   Usage:
       from app.services.financial_incident_analyzer_integration import analyze_incident_with_ai
       
       result = analyze_incident_with_ai(incident, db=session)
       print(f"Status: {result['status']}")
       print(f"Confidence: {result['confidence_score']}")


4. get_erp_snapshot_for_incident(incident)

   Extract just ERP data for debugging/review (no AI analysis).

   Args:
       incident (Incident): Incident to extract data for

   Returns:
       ERP snapshot (see ERPDataExtractor.extract_incident_data return type)

   Usage:
       snapshot = get_erp_snapshot_for_incident(incident)
       print(f"Invoice: {snapshot['invoice']['name']}")
       print(f"Sales Order: {snapshot['sales_order']['name']}")


USAGE EXAMPLES
==============

Example 1: Basic incident analysis with persistence

    from sqlalchemy.orm import Session
    from app.services.financial_incident_analyzer_integration import analyze_incident_with_ai
    from app.db.models import Incident

    def resolve_incident_endpoint(incident_id: int, db: Session):
        incident = db.query(Incident).filter(Incident.id == incident_id).first()
        if not incident:
            return {"error": "Not found"}
        
        # Analyze and persist
        result = analyze_incident_with_ai(incident, db=db)
        
        return {
            "status": result["status"],
            "summary": result["replay_summary"],
            "confidence": result["confidence_score"]
        }


Example 2: Analysis preview without persistence

    from app.services.financial_incident_analyzer_integration import analyze_incident_with_ai_no_persist

    def preview_incident_analysis(incident_id: int, db: Session):
        incident = db.query(Incident).filter(Incident.id == incident_id).first()
        
        # Analyze but don't modify database
        result = analyze_incident_with_ai_no_persist(incident)
        
        return result


Example 3: Debug ERP data extraction

    from app.services.financial_incident_analyzer_integration import get_erp_snapshot_for_incident

    def debug_incident_data(incident_id: int, db: Session):
        incident = db.query(Incident).filter(Incident.id == incident_id).first()
        
        # Extract ERP data only
        snapshot = get_erp_snapshot_for_incident(incident)
        
        if snapshot["status"] == "ERROR":
            return {
                "error": snapshot.get("error"),
                "missing_fields": snapshot.get("missing_fields")
            }
        
        return {
            "invoice_total": snapshot["invoice"]["total"],
            "sales_order_total": snapshot["sales_order"]["agreed_total"],
            "difference": snapshot["invoice"]["total"] - snapshot["sales_order"]["agreed_total"]
        }


Example 4: Manual AI analysis call

    from app.services.financial_incident_analyzer import FinancialIncidentAnalyzer
    from app.integrations.client_factory import get_erp_client
    from app.ai.ai_factory import get_ai_client

    analyzer = FinancialIncidentAnalyzer(
        erp_client=get_erp_client(),
        ai_client=get_ai_client()
    )
    
    result = analyzer.analyze_incident(incident, db=session)
    print(f"Conclusion: {result['replay_conclusion']}")


INTEGRATION WITH EXISTING CONTROLLER
====================================

To integrate with incident_controller.py, modify resolve_incident():

    # OLD CODE
    def resolve_incident(incident_id: int, db: Session) -> Incident | None:
        incident = get_incident_by_id(incident_id, db)
        if incident is None:
            return None
        
        # OLD: Single analysis path
        ...

    # NEW CODE
    def resolve_incident(incident_id: int, db: Session) -> Incident | None:
        incident = get_incident_by_id(incident_id, db)
        if incident is None:
            return None
        
        from app.services.financial_incident_analyzer_integration import analyze_incident_with_ai
        
        try:
            result = analyze_incident_with_ai(incident, db=db)
            return incident
        except Exception as e:
            logger.error(f"Financial analysis failed: {e}")
            incident.status = "ANALYSIS_ERROR"
            db.commit()
            return incident


BUSINESS RULES
==============

Status Determination:

    INSUFFICIENT_DATA:
        - Any critical ERP field missing
        - Sales order not linked
        → Status: UNDER_REVIEW (requires manual review)
        → Confidence: 0.0

    LOW_CONFIDENCE (confidence < 0.5):
        - AI uncertain about analysis
        → Status: UNDER_REVIEW (requires manual review)

    HIGH_CONFIDENCE (confidence >= 0.5):
        - AI confident in analysis
        → Status: RESOLVED
        → Results persisted to incident


DATA FLOW DIAGRAM
================

    ERPNext System
         ↓
    ERPDataExtractor.extract_incident_data()
         ├─ Fetch Invoice
         ├─ Fetch Sales Order
         ├─ Fetch Customer
         └─ Validate completeness
         ↓
    ERP Snapshot (immutable)
         ↓
    PromptBuilder.build_analysis_prompt()
         ├─ Format ERP data
         ├─ Build business context
         └─ Create AI prompt
         ↓
    AI Analysis Layer (Claude/Anthropic)
         ├─ Receive ERP snapshot
         ├─ Analyze discrepancies
         └─ Return JSON response
         ↓
    AIResultMapper.map_ai_response()
         └─ Validate and map fields
         ↓
    Business Rules Engine
         ├─ Check discrepancy_source
         ├─ Evaluate confidence
         └─ Determine status
         ↓
    Incident Record (Database)
         └─ Persist results


TESTING & VALIDATION
===================

To test the analyzer:

    from app.services.financial_incident_analyzer import FinancialIncidentAnalyzer
    from app.db.models import Incident
    from app.integrations.erpnext_mock_client import MockERPNextClient
    from app.ai.ai_client_mock import MockAIClient

    # Use mock clients for testing
    mock_erp = MockERPNextClient()
    mock_ai = MockAIClient()

    analyzer = FinancialIncidentAnalyzer(
        erp_client=mock_erp,
        ai_client=mock_ai
    )

    # Create test incident
    incident = Incident(
        id=1,
        erp_reference="INV-001",
        incident_type="Pricing_Issue",
        description="Test incident",
        status="OPEN"
    )

    # Analyze
    result = analyzer.analyze_incident(incident, db=None)

    # Verify
    assert result["status"] in ["RESOLVED", "UNDER_REVIEW"]
    assert result["confidence_score"] >= 0.0
    assert "replay_summary" in result


KEY DESIGN PRINCIPLES
===================

1. SEPARATION OF CONCERNS
   - ERP extraction (backend only)
   - AI analysis (AI layer only)
   - Business rules (backend only)

2. IMMUTABILITY
   - ERP snapshots are read-only
   - AI receives complete data
   - No partial or incomplete ERP data to AI

3. TRACEABILITY
   - Every field has source tracking
   - Missing fields marked explicitly
   - AI response fully mapped
   - Confidence scores always present

4. FAILURE HANDLING
   - Clear error states (EXTRACTION_ERROR, AI_FAILED)
   - Explicit INSUFFICIENT_DATA tracking
   - Graceful degradation to UNDER_REVIEW

5. BACKWARD COMPATIBILITY
   - Integration functions work with existing code
   - Optional persistence
   - No breaking changes to Incident model


ENVIRONMENT VARIABLES
====================

AI_ENABLED
    Controls whether AI analysis is used
    Values: "true"/"false" (default: true)

ERP_CLIENT_MODE
    Selects ERP client implementation
    Values: "real"/"mock" (default: real)

AI_CLIENT_MODE
    Selects AI client implementation
    Values: "anthropic"/"mock" (default: anthropic)


ERRORS & TROUBLESHOOTING
=======================

Error: "Invoice not found"
    Cause: incident_reference doesn't match ERP invoice ID
    Solution: Verify ERP reference in incident record

Error: "Sales Order not linked"
    Cause: Invoice has no sales_order field
    Solution: Mark as UNDER_REVIEW (expected scenario)

Error: "Missing confidence_score"
    Cause: AI response incomplete
    Solution: Check AI client response mapping

Error: "AI analysis failed"
    Cause: AI service error
    Solution: Status set to UNDER_REVIEW automatically

Error: "Insufficient ERP data"
    Cause: Critical fields missing from Invoice
    Solution: Verify ERP data quality

For more info, check logs with:
    import logging
    logging.basicConfig(level=logging.DEBUG)
"""

# This is a documentation module - no executable code
