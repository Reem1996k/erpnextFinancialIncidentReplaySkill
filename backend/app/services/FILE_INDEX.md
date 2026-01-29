"""
FINANCIAL INCIDENT ANALYZER - FILE INDEX & QUICK NAVIGATION
============================================================

This file serves as a navigation guide for all Financial Incident Analyzer files.
"""

# ============================================================================
# FILE INDEX
# ============================================================================

"""
SERVICE IMPLEMENTATION FILES
============================

1. erp_data_extractor.py
   Purpose: Extracts ERP data (Invoice, Sales Order, Customer)
   Main Class: ERPDataExtractor
   Key Method: extract_incident_data(invoice_id)
   Use When: Need to fetch ERP data for analysis
   
   Example:
       extractor = ERPDataExtractor(erp_client)
       snapshot = extractor.extract_incident_data("INV-001")


2. financial_incident_analyzer.py
   Purpose: Orchestrates complete incident analysis workflow
   Main Class: FinancialIncidentAnalyzer
   Key Method: analyze_incident(incident, db=None)
   Use When: Need full analysis (extract + AI + rules)
   
   Example:
       analyzer = FinancialIncidentAnalyzer(erp_client, ai_client)
       result = analyzer.analyze_incident(incident, db=session)


3. financial_incident_analyzer_integration.py
   Purpose: Integration functions for controllers and services
   Main Functions:
       - analyze_incident_with_ai(incident, db)
       - analyze_incident_with_ai_no_persist(incident)
       - get_erp_snapshot_for_incident(incident)
       - update_incident_from_analysis(incident, result, db)
   Use When: Integrating into existing controller
   
   Example:
       from app.services.financial_incident_analyzer_integration import analyze_incident_with_ai
       result = analyze_incident_with_ai(incident, db=session)


DOCUMENTATION FILES
===================

4. QUICK_START.md (START HERE)
   What: 5-minute getting started guide
   Contains: Basic usage, common patterns, expected results
   Read Time: 5 minutes
   Best For: New users, quick integration


5. FINANCIAL_INCIDENT_ANALYZER_GUIDE.md
   What: Complete technical reference
   Contains: Architecture, detailed API, business rules, data flow
   Read Time: 20 minutes
   Best For: Understanding internals, debugging


6. IMPLEMENTATION_SUMMARY.md
   What: Implementation details and status
   Contains: What was built, architecture diagram, integration checklist
   Read Time: 10 minutes
   Best For: Deployment planning, system integration


7. CONTROLLER_INTEGRATION_EXAMPLES.py
   What: Real code examples for integration
   Contains: 7 different integration patterns, error handling
   Read Time: 15 minutes
   Best For: Implementing in your controller


TESTING & VALIDATION
====================

8. financial_incident_analyzer_validation.py
   What: Comprehensive test suite
   Contains: Unit tests, integration tests, mock data generators
   Run: from app.services.financial_incident_analyzer_validation import run_all_tests
        success = run_all_tests()
   Best For: Testing, validation, learning


THIS FILE (Index)
=================

9. FILE_INDEX.md (This File)
   What: Navigation guide for all files
   Purpose: Quick reference for finding what you need


RECOMMENDED READING ORDER
=========================

New Users:
    1. QUICK_START.md (5 min)
    2. FINANCIAL_INCIDENT_ANALYZER_GUIDE.md (20 min)
    3. CONTROLLER_INTEGRATION_EXAMPLES.py (15 min)

Integration:
    1. QUICK_START.md
    2. CONTROLLER_INTEGRATION_EXAMPLES.py
    3. IMPLEMENTATION_SUMMARY.md

Debugging:
    1. FINANCIAL_INCIDENT_ANALYZER_GUIDE.md (Troubleshooting section)
    2. financial_incident_analyzer_validation.py
    3. Server logs with debug enabled

Architecture Review:
    1. IMPLEMENTATION_SUMMARY.md
    2. FINANCIAL_INCIDENT_ANALYZER_GUIDE.md (Architecture section)
    3. Source code: erp_data_extractor.py, financial_incident_analyzer.py
"""


# ============================================================================
# QUICK REFERENCE BY USE CASE
# ============================================================================

"""
USE CASE: "I want to integrate into my controller"
==================================================

Files to Read:
    1. QUICK_START.md - Get the basics
    2. CONTROLLER_INTEGRATION_EXAMPLES.py - See how to do it
    
Quick Code:
    from app.services.financial_incident_analyzer_integration import analyze_incident_with_ai
    
    result = analyze_incident_with_ai(incident, db=db)

Integration Checklist in: IMPLEMENTATION_SUMMARY.md


USE CASE: "I want to understand the architecture"
==================================================

Files to Read:
    1. IMPLEMENTATION_SUMMARY.md - Overview
    2. FINANCIAL_INCIDENT_ANALYZER_GUIDE.md - Details
    
Key Sections:
    - Architecture Overview
    - Data Flow Diagram
    - Separation of Concerns


USE CASE: "I'm getting an error"
=================================

Files to Read:
    1. FINANCIAL_INCIDENT_ANALYZER_GUIDE.md - Troubleshooting
    2. financial_incident_analyzer_validation.py - Test with mock data
    
Debug Steps:
    1. Check logs: logger.debug(...)
    2. Inspect ERP: get_erp_snapshot_for_incident(incident)
    3. Run tests: run_all_tests()


USE CASE: "I want to test it first"
====================================

Files to Read:
    1. QUICK_START.md - See what it does
    2. financial_incident_analyzer_validation.py - Run tests
    
Run Tests:
    from app.services.financial_incident_analyzer_validation import run_all_tests
    success = run_all_tests()


USE CASE: "I want to customize it"
===================================

Files to Read:
    1. FINANCIAL_INCIDENT_ANALYZER_GUIDE.md - Business rules section
    2. Source code: financial_incident_analyzer.py
    
Key Methods to Override:
    - _determine_status() - Change status rules
    - _extract_invoice() - Add/remove fields
    - _build_ai_prompt() - Change AI instructions


USE CASE: "I need API documentation"
====================================

Files to Read:
    1. FINANCIAL_INCIDENT_ANALYZER_GUIDE.md - Detailed API Reference
    
API Entry Points:
    - ERPDataExtractor.extract_incident_data()
    - FinancialIncidentAnalyzer.analyze_incident()
    - analyze_incident_with_ai()


USE CASE: "I want production deployment checklist"
===================================================

Files to Read:
    1. IMPLEMENTATION_SUMMARY.md - Integration Checklist
    2. FINANCIAL_INCIDENT_ANALYZER_GUIDE.md - Environment Variables
    
Checklist:
    [ ] Run all tests passing
    [ ] Update controller
    [ ] Test with staging data
    [ ] Enable logging
    [ ] Configure AI credentials
    [ ] Monitor first deployments
"""


# ============================================================================
# CODE SNIPPETS BY FILE
# ============================================================================

"""
FROM: erp_data_extractor.py
===========================

Extract complete ERP snapshot:
    from app.services.erp_data_extractor import ERPDataExtractor
    
    extractor = ERPDataExtractor(erp_client)
    snapshot = extractor.extract_incident_data("INV-001")
    
    if snapshot['status'] == 'SUCCESS':
        print(f"Invoice Total: {snapshot['invoice']['total']}")
        print(f"SO Total: {snapshot['sales_order']['agreed_total']}")
    else:
        print(f"Missing: {snapshot['missing_fields']}")


FROM: financial_incident_analyzer.py
====================================

Full incident analysis:
    from app.services.financial_incident_analyzer import FinancialIncidentAnalyzer
    
    analyzer = FinancialIncidentAnalyzer(erp_client, ai_client)
    result = analyzer.analyze_incident(incident, db=session)
    
    print(f"Status: {result['status']}")
    print(f"Confidence: {result['confidence_score']}")
    print(f"Conclusion: {result['replay_conclusion']}")


FROM: financial_incident_analyzer_integration.py
=================================================

Integration into controller:
    from app.services.financial_incident_analyzer_integration import analyze_incident_with_ai
    
    result = analyze_incident_with_ai(incident, db=db)
    
    return {
        "status": result["status"],
        "summary": result["replay_summary"],
        "confidence": result["confidence_score"]
    }

Preview without persistence:
    from app.services.financial_incident_analyzer_integration import analyze_incident_with_ai_no_persist
    
    result = analyze_incident_with_ai_no_persist(incident)

Inspect ERP data:
    from app.services.financial_incident_analyzer_integration import get_erp_snapshot_for_incident
    
    snapshot = get_erp_snapshot_for_incident(incident)


FROM: financial_incident_analyzer_validation.py
================================================

Run all tests:
    from app.services.financial_incident_analyzer_validation import run_all_tests
    
    success = run_all_tests()

Create mock data:
    from app.services.financial_incident_analyzer_validation import (
        create_mock_invoice,
        create_mock_sales_order,
        create_mock_customer,
        create_mock_incident,
        create_mock_erp_client,
        create_mock_ai_client
    )
    
    invoice = create_mock_invoice(invoice_id="INV-001")
    erp_client = create_mock_erp_client(invoice=invoice)
"""


# ============================================================================
# ARCHITECTURE OVERVIEW
# ============================================================================

"""
4-STEP WORKFLOW
===============

     USER/CONTROLLER
            ↓
     [analyze_incident_with_ai]
            ↓
     [FinancialIncidentAnalyzer]
            ↓
     ┌─────────────────────┐
     │ 1. ERP EXTRACTION   │ (ERPDataExtractor)
     │ ├─ Fetch Invoice    │
     │ ├─ Fetch SO         │
     │ └─ Validate         │
     └─────────────────────┘
            ↓
     ┌─────────────────────┐
     │ 2. AI ANALYSIS      │ (Claude API)
     │ ├─ Receive snapshot │
     │ ├─ Analyze          │
     │ └─ Return result    │
     └─────────────────────┘
            ↓
     ┌─────────────────────┐
     │ 3. BUSINESS RULES   │ (Backend)
     │ ├─ Check confidence │
     │ ├─ Check data       │
     │ └─ Determine status │
     └─────────────────────┘
            ↓
     ┌─────────────────────┐
     │ 4. PERSISTENCE      │ (Database)
     │ └─ Update incident  │
     └─────────────────────┘
            ↓
     [Return Result]
            ↓
     USER/CONTROLLER


KEY PRINCIPLES
==============

✓ Backend owns ERP extraction
✓ AI owns analysis only
✓ Backend owns business rules
✓ ERPNext is single source of truth
✓ Clear error handling
✓ Immutable ERP snapshots
✓ No assumptions, explicit validation
"""


# ============================================================================
# ENVIRONMENT VARIABLES
# ============================================================================

"""
CONFIGURATION
=============

AI_ENABLED=true
    - Enable/disable AI analysis
    - Default: true

AI_CLIENT_MODE=anthropic
    - Select AI client: anthropic or mock
    - Default: anthropic

ERP_CLIENT_MODE=real
    - Select ERP client: real or mock
    - Default: real

ANTHROPIC_API_KEY
    - Claude API key (required if using real AI)

ERPNEXT_API_KEY
    - ERPNext API credentials

ERPNEXT_URL
    - ERPNext server URL


For Details See: FINANCIAL_INCIDENT_ANALYZER_GUIDE.md
"""


# ============================================================================
# COMMON TASKS CHECKLIST
# ============================================================================

"""
TASK: Get Started in 5 Minutes
[ ] 1. Read QUICK_START.md
[ ] 2. Copy service files to backend/app/services/
[ ] 3. Test: run_all_tests()
[ ] 4. Integrate: Follow QUICK_START.md example

TASK: Integrate into Existing Controller
[ ] 1. Read CONTROLLER_INTEGRATION_EXAMPLES.py
[ ] 2. Update incident_controller.py
[ ] 3. Test with real incidents
[ ] 4. Deploy to staging

TASK: Deploy to Production
[ ] 1. Run full test suite
[ ] 2. Test with staging data
[ ] 3. Enable debug logging
[ ] 4. Configure AI credentials
[ ] 5. Monitor first deployments
[ ] 6. Check: IMPLEMENTATION_SUMMARY.md Integration Checklist

TASK: Debug Issues
[ ] 1. Check logs
[ ] 2. Inspect ERP data: get_erp_snapshot_for_incident()
[ ] 3. Run tests with mock data
[ ] 4. Review: FINANCIAL_INCIDENT_ANALYZER_GUIDE.md Troubleshooting

TASK: Understand Architecture
[ ] 1. Read: IMPLEMENTATION_SUMMARY.md
[ ] 2. Study: Architecture Diagram in this file
[ ] 3. Review: Data Flow Diagram in FINANCIAL_INCIDENT_ANALYZER_GUIDE.md
[ ] 4. Examine: Source code files

TASK: Customize for Your Needs
[ ] 1. Review: FINANCIAL_INCIDENT_ANALYZER_GUIDE.md Business Rules
[ ] 2. Modify: financial_incident_analyzer.py methods
[ ] 3. Test: Run validation suite with new logic
[ ] 4. Verify: No breaking changes
"""


# ============================================================================
# TROUBLESHOOTING DECISION TREE
# ============================================================================

"""
I have a problem... What do I read?
===================================

"The analyzer won't start"
  └─ Check: QUICK_START.md - Step 1 (Imports)
     Check: FINANCIAL_INCIDENT_ANALYZER_GUIDE.md - Errors & Troubleshooting

"Analysis fails"
  └─ Check: FINANCIAL_INCIDENT_ANALYZER_GUIDE.md - Troubleshooting
     Check: Server logs
     Run: get_erp_snapshot_for_incident() to inspect data

"Results don't look right"
  └─ Check: financial_incident_analyzer_validation.py
     Run: run_all_tests()
     Check: Mock data scenarios

"I need to modify behavior"
  └─ Check: FINANCIAL_INCIDENT_ANALYZER_GUIDE.md - Business Rules
     Review: Source code methods to override
     Run: Tests after changes

"Performance is slow"
  └─ Check: FINANCIAL_INCIDENT_ANALYZER_GUIDE.md - Performance Notes
     Monitor: ERP response times
     Check: AI API latency

"I want to add new features"
  └─ Check: CONTROLLER_INTEGRATION_EXAMPLES.py - Patterns
     Check: financial_incident_analyzer_validation.py - Testing patterns
     Run: Tests after additions
"""


# ============================================================================
# QUICK COPY-PASTE CODE
# ============================================================================

"""
MINIMAL EXAMPLE (Copy & Paste)
==============================

from app.services.financial_incident_analyzer_integration import analyze_incident_with_ai
from sqlalchemy.orm import Session
from app.db.models import Incident

def analyze_my_incident(incident_id: int, db: Session):
    # Get incident
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    
    # Analyze
    result = analyze_incident_with_ai(incident, db=db)
    
    # Return
    return result


COMPLETE EXAMPLE (Copy & Paste)
===============================

from app.services.financial_incident_analyzer_integration import (
    analyze_incident_with_ai,
    get_erp_snapshot_for_incident
)
from sqlalchemy.orm import Session
from app.db.models import Incident
from fastapi import HTTPException, status

def resolve_incident_endpoint(incident_id: int, db: Session):
    # Fetch incident
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Not found")
    
    # Check existing status
    if incident.status == "RESOLVED":
        return {"status": "Already resolved"}
    
    try:
        # Analyze
        result = analyze_incident_with_ai(incident, db=db)
        
        # Return result
        return {
            "status": result["status"],
            "confidence": result["confidence_score"],
            "summary": result["replay_summary"],
            "conclusion": result["replay_conclusion"]
        }
    
    except Exception as e:
        # Log error
        logger.error(f"Analysis failed: {e}")
        
        # Try to see ERP data
        try:
            snapshot = get_erp_snapshot_for_incident(incident)
            missing = snapshot.get("missing_fields", [])
            return {
                "error": "Analysis failed",
                "missing_fields": missing
            }
        except:
            return {
                "error": "Analysis failed: " + str(e)
            }


ERROR HANDLING EXAMPLE (Copy & Paste)
====================================

try:
    result = analyze_incident_with_ai(incident, db=db)
    
    if result['status'] == 'RESOLVED':
        print(f"✓ Resolved with {result['confidence_score']:.0%} confidence")
    else:
        print(f"⚠ Under review - {result['discrepancy_source']}")
        print(f"  Missing: {result['missing_fields']}")

except ValueError as ve:
    print(f"Validation error: {ve}")
    # Incident data invalid

except RuntimeError as re:
    print(f"Analysis failed: {re}")
    # ERP or AI error

except Exception as e:
    print(f"Unexpected error: {e}")
    # Something else went wrong
"""


# ============================================================================
# SUMMARY TABLE
# ============================================================================

"""
FILE SUMMARY TABLE
==================

┌──────────────────────────────┬──────────┬────────────────────────┐
│ FILE NAME                    │ TYPE     │ WHEN TO USE            │
├──────────────────────────────┼──────────┼────────────────────────┤
│ QUICK_START.md               │ GUIDE    │ Getting started        │
│ FINANCIAL_INCIDENT_..._GUIDE │ DOCS     │ Reference              │
│ IMPLEMENTATION_SUMMARY.md    │ DOCS     │ Architecture           │
│ CONTROLLER_INTEGRATION_...   │ CODE     │ Integration patterns   │
│ erp_data_extractor.py        │ SERVICE  │ Extract ERP data       │
│ financial_incident_...py     │ SERVICE  │ Orchestrate analysis   │
│ financial_incident_...int... │ SERVICE  │ Integration functions  │
│ financial_incident_...val... │ TESTS    │ Testing               │
└──────────────────────────────┴──────────┴────────────────────────┘

LEGEND:
  GUIDE  = Documentation (read to understand)
  DOCS   = Technical reference (read for details)
  CODE   = Example code (read to implement)
  SERVICE = Implementation (use in your code)
  TESTS  = Testing (run to validate)
"""


# ============================================================================
# NEXT STEPS
# ============================================================================

"""
RECOMMENDED NEXT STEP:

1. If you're new: Read QUICK_START.md (5 minutes)
2. If you're integrating: Read CONTROLLER_INTEGRATION_EXAMPLES.py
3. If you're debugging: Read FINANCIAL_INCIDENT_ANALYZER_GUIDE.md
4. If you're deploying: Check IMPLEMENTATION_SUMMARY.md


QUICK LINK COMMANDS

Get started:
    See: QUICK_START.md

Understand internals:
    See: FINANCIAL_INCIDENT_ANALYZER_GUIDE.md

Find code examples:
    See: CONTROLLER_INTEGRATION_EXAMPLES.py

Run tests:
    from app.services.financial_incident_analyzer_validation import run_all_tests
    run_all_tests()

Inspect ERP data:
    from app.services.financial_incident_analyzer_integration import get_erp_snapshot_for_incident
    snapshot = get_erp_snapshot_for_incident(incident)

Analyze incident:
    from app.services.financial_incident_analyzer_integration import analyze_incident_with_ai
    result = analyze_incident_with_ai(incident, db=db)
"""

# ============================================================================
# END OF FILE INDEX
# ============================================================================
