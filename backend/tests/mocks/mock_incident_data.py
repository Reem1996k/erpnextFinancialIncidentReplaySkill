"""
Mock data for Incidents API tests.

This module contains ONLY mock data and helper functions
that return predefined incident payloads and expected responses.

No test logic, no assertions, no pytest imports.
"""


# =========================
# POST /incidents payloads
# =========================

def get_valid_incident_payload():
    """Valid incident payload (happy path)."""
    return {
        "erp_reference": "ACC-SINV-TEST-001",
        "incident_type": "Pricing_Issue",
        "description": "Invoice total does not match sales order total"
    }


def get_second_valid_incident_payload():
    """Another valid incident payload (used for list tests)."""
    return {
        "erp_reference": "ACC-SINV-TEST-002",
        "incident_type": "Duplicate_Invoice",
        "description": "Duplicate invoice detected for same customer"
    }


def get_duplicate_incident_payload():
    """Duplicate incident payload (same ERP reference as first)."""
    return {
        "erp_reference": "ACC-SINV-TEST-001",
        "incident_type": "Pricing_Issue",
        "description": "Trying to create duplicate incident"
    }


def get_invalid_incident_missing_erp_reference():
    """Invalid payload: missing erp_reference."""
    return {
        "incident_type": "Pricing_Issue",
        "description": "ERP reference is missing"
    }


def get_invalid_incident_empty_type():
    """Invalid payload: empty incident_type."""
    return {
        "erp_reference": "ACC-SINV-TEST-003",
        "incident_type": "",
        "description": "Incident type is empty"
    }


# =========================
# Expected response helpers
# =========================

def get_expected_incident_status():
    """Default status for newly created incidents."""
    return "OPEN"


def get_expected_error_duplicate():
    """Expected error message for duplicate incident."""
    return {
        "detail": "Incident with ERP reference 'ACC-SINV-TEST-001' already exists"
    }


def get_expected_not_found_error(incident_id: int):
    """Expected error message for incident not found."""
    return {
        "detail": f"Incident {incident_id} not found"
    }


# =========================
# IDs for GET tests
# =========================

def get_existing_incident_id():
    """Example existing incident ID (used after creation)."""
    return 1


def get_non_existing_incident_id():
    """Incident ID that does not exist."""
    return 9999


# =========================
# data for analysis tests
# ========================= 

def get_incident_for_analysis():
    """
    Incident object as returned from DB before analysis.
    """
    return {
        "id": 1,
        "erp_reference": "ACC-SINV-2026-00009",
        "incident_type": "Pricing_Issue",
        "description": "Customer claims invoice amount is higher than agreed",
        "status": "OPEN"
    }


def get_expected_analysis_response_fields():
    """
    Expected fields in successful analysis response.
    """
    return [
        "success",
        "incident_id",
        "incident"
    ]


def get_expected_incident_fields_after_analysis():
    """
    Expected fields in the incident object after analysis.
    """
    return [
        "id",
        "erp_reference",
        "status",
        "analysis_source",
        "confidence_score",
        "replay_summary",
        "replay_conclusion"
    ]


def get_expected_status_after_successful_analysis():
    """
    Expected status after successful AI analysis.
    """
    return "RESOLVED"


def get_expected_status_after_failed_analysis():
    """
    Expected status after failed AI analysis.
    """
    return "UNDER_REVIEW"


def get_expected_analysis_source_ai():
    """
    Expected analysis source for successful AI analysis.
    """
    return "AI"


def get_expected_analysis_source_failed():
    """
    Expected analysis source for failed AI analysis.
    """
    return "AI_FAILED"

