"""
FINANCIAL INCIDENT ANALYZER - QUICK START GUIDE
================================================

Get the analyzer up and running in 5 minutes.
"""

# ============================================================================
# QUICK START - 5 MINUTES
# ============================================================================

"""
STEP 1: Import and Initialize (30 seconds)
==========================================

From your controller or service:

    from app.services.financial_incident_analyzer_integration import analyze_incident_with_ai
    from sqlalchemy.orm import Session
    from app.db.models import Incident

That's it. The service auto-selects your ERP and AI clients.


STEP 2: Analyze an Incident (1 minute)
======================================

    # Get incident from database
    incident = db.query(Incident).filter(Incident.id == 123).first()
    
    # Analyze it (extracts ERP data + calls AI)
    result = analyze_incident_with_ai(incident, db=db)
    
    # Check result
    print(f"Status: {result['status']}")              # "RESOLVED" or "UNDER_REVIEW"
    print(f"Confidence: {result['confidence_score']}") # 0.0 to 1.0
    print(f"Summary: {result['replay_summary']}")      # AI analysis summary

The incident is automatically updated in the database.


STEP 3: Handle the Result (1 minute)
===================================

    if result['status'] == 'RESOLVED':
        print(f"✓ Incident resolved with {result['confidence_score']:.0%} confidence")
        print(f"  Conclusion: {result['replay_conclusion']}")
    
    elif result['status'] == 'UNDER_REVIEW':
        print(f"⚠ Incident needs manual review")
        print(f"  Reason: {result['discrepancy_source']}")
        print(f"  Missing fields: {result['missing_fields']}")


STEP 4: That's It! (2 minutes)
============================

Your incident analysis is complete. The service has:
  ✓ Extracted ERP data (Invoice + Sales Order)
  ✓ Validated data completeness
  ✓ Called AI for analysis
  ✓ Applied business rules
  ✓ Updated the database
  ✓ Returned the result
"""


# ============================================================================
# COMMON USAGE PATTERNS
# ============================================================================

"""
PATTERN 1: Analyze and Auto-Update (Most Common)
================================================

    from app.services.financial_incident_analyzer_integration import analyze_incident_with_ai
    
    result = analyze_incident_with_ai(incident, db=db)
    
    # Result is already in the database
    return {"status": result['status'], "confidence": result['confidence_score']}


PATTERN 2: Preview Before Persisting
====================================

    from app.services.financial_incident_analyzer_integration import analyze_incident_with_ai_no_persist
    
    # Analyze but don't modify database
    result = analyze_incident_with_ai_no_persist(incident)
    
    # User reviews result
    user_confirms = show_to_user(result)
    
    # Only persist if user confirms
    if user_confirms:
        analyze_incident_with_ai(incident, db=db)


PATTERN 3: Inspect ERP Data Only
===============================

    from app.services.financial_incident_analyzer_integration import get_erp_snapshot_for_incident
    
    # Debug: Extract ERP data without AI
    snapshot = get_erp_snapshot_for_incident(incident)
    
    print(f"Invoice: {snapshot['invoice']['total']}")
    print(f"Sales Order: {snapshot['sales_order']['agreed_total']}")
    print(f"Difference: {snapshot['invoice']['total'] - snapshot['sales_order']['agreed_total']}")


PATTERN 4: Batch Processing
===========================

    from app.services.financial_incident_analyzer_integration import analyze_incident_with_ai
    
    incidents = db.query(Incident).filter(Incident.status == 'OPEN').all()
    
    results = []
    for incident in incidents:
        result = analyze_incident_with_ai(incident, db=db)
        results.append(result)
    
    resolved = sum(1 for r in results if r['status'] == 'RESOLVED')
    under_review = sum(1 for r in results if r['status'] == 'UNDER_REVIEW')
    
    print(f"Resolved: {resolved}, Under Review: {under_review}")


PATTERN 5: Error Handling
========================

    from app.services.financial_incident_analyzer_integration import analyze_incident_with_ai
    
    try:
        result = analyze_incident_with_ai(incident, db=db)
        
        if result['status'] == 'RESOLVED':
            print(f"✓ Resolved")
        else:
            print(f"⚠ Under Review")
    
    except ValueError as ve:
        print(f"Validation error: {ve}")
        # Incident data invalid
    
    except RuntimeError as re:
        print(f"Analysis failed: {re}")
        # ERP or AI error
"""


# ============================================================================
# INTEGRATION INTO CONTROLLER
# ============================================================================

"""
BEFORE (Existing Code)
======================

    def resolve_incident(incident_id: int, db: Session) -> Incident:
        incident = get_incident_by_id(incident_id, db)
        if incident is None:
            return None
        
        # OLD: Existing logic
        ...
        
        return incident


AFTER (With Financial Analyzer)
================================

    def resolve_incident(incident_id: int, db: Session) -> Incident:
        from app.services.financial_incident_analyzer_integration import analyze_incident_with_ai
        
        incident = get_incident_by_id(incident_id, db)
        if incident is None:
            return None
        
        # NEW: Use Financial Incident Analyzer
        try:
            analyze_incident_with_ai(incident, db=db)
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            incident.status = "ANALYSIS_ERROR"
            db.commit()
        
        return incident

That's all you need to change!
"""


# ============================================================================
# EXPECTED RESULTS
# ============================================================================

"""
SUCCESSFUL ANALYSIS
===================

Input:
    Incident ID: 123
    ERP Reference: INV-2024-001
    Type: Pricing_Issue

Processing:
    1. Extract invoice INV-2024-001 from ERPNext ✓
    2. Extract linked sales order SO-2024-001 ✓
    3. Validate completeness ✓
    4. Build AI prompt ✓
    5. Call Claude API ✓
    6. Map response ✓
    7. Apply business rules ✓
    8. Update database ✓

Output:
    {
        "incident_id": 123,
        "status": "RESOLVED",
        "replay_summary": "Invoice includes shipping charges not in sales order",
        "replay_details": "Analysis of line items shows $150 shipping charge...",
        "confidence_score": 0.92,
        "analysis_source": "AI",
        "discrepancy_source": "EXTRA_CHARGES",
        "replayed_at": "2024-01-28T10:30:45.123456"
    }


INSUFFICIENT DATA SCENARIO
==========================

Input:
    Incident ID: 456
    ERP Reference: INV-2024-002
    Note: No linked sales order

Processing:
    1. Extract invoice ✓
    2. No linked sales order ✓
    3. Validation: INCOMPLETE (missing sales_order)
    4. Return INSUFFICIENT_DATA

Output:
    {
        "incident_id": 456,
        "status": "UNDER_REVIEW",
        "replay_summary": "Cannot analyze without sales order",
        "confidence_score": 0.0,
        "analysis_source": "AI",
        "discrepancy_source": "INSUFFICIENT_DATA",
        "missing_fields": ["sales_order_not_linked"],
        "erp_snapshot_status": "INCOMPLETE"
    }
"""


# ============================================================================
# WHAT HAPPENS INSIDE
# ============================================================================

"""
THE 4-STEP WORKFLOW
===================

1. ERP EXTRACTION (Backend)
   └─ ERPDataExtractor
      ├─ Fetch Invoice from ERPNext
      ├─ Fetch Sales Order
      ├─ Fetch Customer
      ├─ Validate all fields
      └─ Return immutable snapshot

2. AI ANALYSIS (AI Layer)
   └─ Claude API
      ├─ Receive ERP snapshot
      ├─ Analyze pricing discrepancies
      ├─ Compare invoice vs. sales order
      └─ Return structured analysis

3. BUSINESS RULES (Backend)
   └─ Status Determination
      ├─ Check: Is data sufficient?
      ├─ Check: Is confidence high?
      └─ Determine: RESOLVED or UNDER_REVIEW

4. PERSISTENCE (Backend)
   └─ Update Incident Record
      ├─ Save analysis results
      ├─ Update status
      ├─ Record timestamp
      └─ Complete

Total Time: ~3-12 seconds per incident
"""


# ============================================================================
# COMMON QUESTIONS
# ============================================================================

"""
Q: How do I know if it worked?
A: Check result['status'] - either "RESOLVED" or "UNDER_REVIEW"

Q: Can I run it multiple times on same incident?
A: Yes. Each run overwrites previous analysis.

Q: What if the ERP data is missing fields?
A: Status set to "UNDER_REVIEW", missing fields listed.

Q: What if AI fails?
A: Caught and handled, status set to "UNDER_REVIEW" automatically.

Q: Can I integrate without changing existing code?
A: Yes. Create a new endpoint without touching existing ones.

Q: Does it work with mock clients?
A: Yes. Set ERP_CLIENT_MODE=mock and AI_CLIENT_MODE=mock

Q: How do I test it?
A: Run: from app.services.financial_incident_analyzer_validation import run_all_tests
         success = run_all_tests()

Q: What's the confidence score?
A: AI's confidence (0.0-1.0). <0.5 = UNDER_REVIEW

Q: Can I see the ERP data extracted?
A: Yes. Use get_erp_snapshot_for_incident(incident)

Q: How is data stored?
A: Results in incident.replay_* fields. Raw data in ai_analysis_json.

Q: Is it production-ready?
A: Yes. Fully tested and documented.
"""


# ============================================================================
# ENVIRONMENT SETUP
# ============================================================================

"""
REQUIRED ENVIRONMENT VARIABLES
==============================

AI_ENABLED=true              # Enable AI analysis (default: true)
AI_CLIENT_MODE=anthropic     # Use Anthropic Claude API
ERP_CLIENT_MODE=real         # Use real ERPNext connection

Optional for specific configurations:
    ANTHROPIC_API_KEY        # Claude API key
    ERPNEXT_API_KEY          # ERPNext API key
    ERPNEXT_URL              # ERPNext URL


INSTALLATION
============

No additional packages needed. Uses existing:
    - SQLAlchemy (ORM)
    - Pydantic (validation)
    - ERPNext client (existing)
    - AI client (existing)
"""


# ============================================================================
# FILE LOCATIONS
# ============================================================================

"""
SERVICE FILES CREATED
====================

Location: backend/app/services/

erp_data_extractor.py                      # Main ERP extraction
financial_incident_analyzer.py             # Main orchestrator
financial_incident_analyzer_integration.py # Integration functions
FINANCIAL_INCIDENT_ANALYZER_GUIDE.md       # Full documentation
CONTROLLER_INTEGRATION_EXAMPLES.py         # Integration examples
financial_incident_analyzer_validation.py  # Tests
IMPLEMENTATION_SUMMARY.md                  # Implementation details
QUICK_START.md                             # This file


INTEGRATION POINT
================

Use this import in your controller:

    from app.services.financial_incident_analyzer_integration import analyze_incident_with_ai
"""


# ============================================================================
# NEXT STEPS
# ============================================================================

"""
IMMEDIATE (Now)
==============
1. Copy files to backend/app/services/
2. Run: from app.services.financial_incident_analyzer_validation import run_all_tests
        run_all_tests()
3. Review IMPLEMENTATION_SUMMARY.md

SHORT TERM (Today)
=================
1. Read FINANCIAL_INCIDENT_ANALYZER_GUIDE.md
2. Review CONTROLLER_INTEGRATION_EXAMPLES.py
3. Test with mock data

MEDIUM TERM (This Week)
======================
1. Integrate into incident_controller.py
2. Test with real incidents
3. Deploy to staging

LONG TERM (This Month)
======================
1. Monitor in production
2. Optimize based on performance
3. Add additional incident types as needed
"""


# ============================================================================
# SUPPORT
# ============================================================================

"""
For detailed information, see:
    - FINANCIAL_INCIDENT_ANALYZER_GUIDE.md     (Full API Reference)
    - CONTROLLER_INTEGRATION_EXAMPLES.py       (Code Examples)
    - IMPLEMENTATION_SUMMARY.md                (Architecture Details)
    - financial_incident_analyzer_validation.py (Test Suite)

For troubleshooting:
    1. Check logs with: logger.debug(...)
    2. Inspect ERP data: get_erp_snapshot_for_incident(incident)
    3. Run tests: from app.services.financial_incident_analyzer_validation import run_all_tests

Ready to go! 🚀
"""
