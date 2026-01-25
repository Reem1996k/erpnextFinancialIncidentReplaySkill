"""
Write unit tests for ReplayEngine.

Test case:
- incident_type = Pricing_Issue
- Verify:
  - decision is APPROVED_WITH_RISK
  - summary contains percentage difference
  - conclusion explains why approval was allowed

"""

import pytest
from app.db.models import Incident
from app.services.replay_engine import ReplayEngine


def test_replay_engine_pricing_issue_analysis():
    """Test ReplayEngine analysis for Pricing_Issue incident type."""
    # Create a mock incident
    incident = Incident(
        id=1,
        erp_reference="ERR-PRICING-001",
        incident_type="Pricing_Issue",
        status="OPEN",
        description="Invoice exceeds purchase order",
        created_at=None
    )
    
    # Analyze the incident
    analysis = ReplayEngine.analyze_incident(incident)
    
    # Verify decision is APPROVED_WITH_RISK
    assert analysis["decision"] == "APPROVED_WITH_RISK"
    
    # Verify summary contains percentage difference
    assert "15.0%" in analysis["summary"]
    assert "exceeds" in analysis["summary"].lower()
    
    # Verify conclusion explains approval
    assert "APPROVED_WITH_RISK" in analysis["conclusion"]
    assert "manual review" in analysis["conclusion"].lower()
    assert "compliance" in analysis["conclusion"].lower()
    
    # Verify details contain amount information
    assert "$5,000.00" in analysis["details"]
    assert "$5,750.00" in analysis["details"]
    assert "15.0%" in analysis["details"]


def test_replay_engine_generic_incident():
    """Test ReplayEngine analysis for generic incident type."""
    # Create a mock incident with generic type
    incident = Incident(
        id=2,
        erp_reference="ERR-GENERIC-001",
        incident_type="Audit_Finding",
        status="OPEN",
        description="Test generic incident",
        created_at=None
    )
    
    # Analyze the incident
    analysis = ReplayEngine.analyze_incident(incident)
    
    # Verify decision is PENDING_REVIEW for generic types
    assert analysis["decision"] == "PENDING_REVIEW"
    
    # Verify summary mentions incident type
    assert "Audit_Finding" in analysis["summary"]
    
    # Verify conclusion recommends manual review
    assert "manual review" in analysis["conclusion"].lower()


def test_replay_engine_analysis_structure():
    """Test ReplayEngine returns correct analysis structure."""
    # Create a mock incident
    incident = Incident(
        id=3,
        erp_reference="ERR-STRUCT-001",
        incident_type="Pricing_Issue",
        status="OPEN",
        description="Test structure",
        created_at=None
    )
    
    # Analyze the incident
    analysis = ReplayEngine.analyze_incident(incident)
    
    # Verify all required keys are present
    assert "summary" in analysis
    assert "details" in analysis
    assert "conclusion" in analysis
    assert "decision" in analysis
    
    # Verify values are not empty
    assert isinstance(analysis["summary"], str)
    assert len(analysis["summary"]) > 0
    assert isinstance(analysis["details"], str)
    assert len(analysis["details"]) > 0
    assert isinstance(analysis["conclusion"], str)
    assert len(analysis["conclusion"]) > 0
    assert isinstance(analysis["decision"], str)
    assert len(analysis["decision"]) > 0
