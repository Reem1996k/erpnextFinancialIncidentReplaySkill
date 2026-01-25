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
from unittest.mock import Mock
from app.db.models import Incident
from app.services.replay_engine import ReplayEngine
from app.integrations.erpnext_client import ERPNextClient


class MockERPNextClient:
    """Mock ERPNextClient for testing without real HTTP requests."""
    
    def __init__(self, invoice_data: dict = None, order_data: dict = None):
        """
        Initialize mock client with predefined data.
        
        Args:
            invoice_data: Mock invoice data to return
            order_data: Mock order data to return
        """
        self.invoice_data = invoice_data or {
            "invoice_id": "INV-001",
            "total_amount": 5750.00,
            "currency": "USD",
            "status": "Submitted",
            "customer": "Test Customer",
            "linked_sales_order": "SO-001"
        }
        self.order_data = order_data or {
            "order_id": "SO-001",
            "expected_amount": 5000.00,
            "currency": "USD",
            "status": "Submitted",
            "customer": "Test Customer"
        }
    
    def get_invoice(self, invoice_id: str) -> dict:
        """Return mock invoice data."""
        return self.invoice_data
    
    def get_sales_order(self, order_id: str) -> dict:
        """Return mock order data."""
        return self.order_data


def test_replay_engine_pricing_issue_acceptable_variance():
    """
    Test ReplayEngine for Pricing_Issue with acceptable variance (15%).
    
    Scenario:
    - Expected amount: $5,000
    - Invoice amount: $5,750
    - Variance: 15%
    - Expected decision: APPROVED_WITH_RISK
    """
    # Create mock client with acceptable variance
    mock_client = MockERPNextClient(
        invoice_data={
            "invoice_id": "INV-001",
            "total_amount": 5750.00,
            "currency": "USD",
            "status": "Submitted",
            "customer": "Acme Corp",
            "linked_sales_order": "SO-001"
        },
        order_data={
            "order_id": "SO-001",
            "expected_amount": 5000.00,
            "currency": "USD",
            "status": "Submitted",
            "customer": "Acme Corp"
        }
    )
    
    # Create incident and ReplayEngine with mock client
    incident = Incident(
        id=1,
        erp_reference="ERR-PRICING-001",
        incident_type="Pricing_Issue",
        status="OPEN",
        description="Invoice exceeds purchase order",
        created_at=None
    )
    
    replay_engine = ReplayEngine(mock_client)
    analysis = replay_engine.analyze_incident(incident)
    
    # Verify decision
    assert analysis["decision"] == "APPROVED_WITH_RISK"
    
    # Verify summary
    assert "15.0%" in analysis["summary"]
    assert "exceeds" in analysis["summary"].lower()
    
    # Verify details contain amounts
    assert "5,000.00" in analysis["details"]
    assert "5,750.00" in analysis["details"]
    assert "15.0%" in analysis["details"]
    assert "INV-001" in analysis["details"]
    assert "SO-001" in analysis["details"]
    
    # Verify conclusion
    assert "APPROVED_WITH_RISK" in analysis["conclusion"]
    assert "within" in analysis["conclusion"].lower()
    assert "manual review" in analysis["conclusion"].lower()


def test_replay_engine_pricing_issue_high_variance():
    """
    Test ReplayEngine for Pricing_Issue with high variance (40%).
    
    Scenario:
    - Expected amount: $5,000
    - Invoice amount: $7,000
    - Variance: 40%
    - Expected decision: REJECTED
    """
    # Create mock client with high variance
    mock_client = MockERPNextClient(
        invoice_data={
            "invoice_id": "INV-002",
            "total_amount": 7000.00,
            "currency": "USD",
            "status": "Submitted",
            "customer": "BigCorp Inc",
            "linked_sales_order": "SO-002"
        },
        order_data={
            "order_id": "SO-002",
            "expected_amount": 5000.00,
            "currency": "USD",
            "status": "Submitted",
            "customer": "BigCorp Inc"
        }
    )
    
    # Create incident and ReplayEngine with mock client
    incident = Incident(
        id=2,
        erp_reference="ERR-PRICING-002",
        incident_type="Pricing_Issue",
        status="OPEN",
        description="Invoice significantly exceeds purchase order",
        created_at=None
    )
    
    replay_engine = ReplayEngine(mock_client)
    analysis = replay_engine.analyze_incident(incident)
    
    # Verify decision is REJECTED for high variance
    assert analysis["decision"] == "REJECTED"
    
    # Verify summary contains percentage
    assert "40.0%" in analysis["summary"]
    
    # Verify details
    assert "5,000.00" in analysis["details"]
    assert "7,000.00" in analysis["details"]
    assert "40.0%" in analysis["details"]
    
    # Verify conclusion explains rejection
    assert "REJECTED" in analysis["conclusion"]
    assert "outside" in analysis["conclusion"].lower()
    assert "manual review" in analysis["conclusion"].lower()


def test_replay_engine_pricing_issue_low_variance():
    """
    Test ReplayEngine for Pricing_Issue with low variance (5%).
    
    Scenario:
    - Expected amount: $5,000
    - Invoice amount: $5,250
    - Variance: 5%
    - Expected decision: APPROVED_WITH_RISK (within 20% threshold)
    """
    # Create mock client with low variance
    mock_client = MockERPNextClient(
        invoice_data={
            "invoice_id": "INV-003",
            "total_amount": 5250.00,
            "currency": "USD",
            "status": "Submitted",
            "customer": "MidSize Co",
            "linked_sales_order": "SO-003"
        },
        order_data={
            "order_id": "SO-003",
            "expected_amount": 5000.00,
            "currency": "USD",
            "status": "Submitted",
            "customer": "MidSize Co"
        }
    )
    
    # Create incident and ReplayEngine with mock client
    incident = Incident(
        id=3,
        erp_reference="ERR-PRICING-003",
        incident_type="Pricing_Issue",
        status="OPEN",
        description="Small invoice variance",
        created_at=None
    )
    
    replay_engine = ReplayEngine(mock_client)
    analysis = replay_engine.analyze_incident(incident)
    
    # Verify decision
    assert analysis["decision"] == "APPROVED_WITH_RISK"
    
    # Verify summary contains percentage
    assert "5.0%" in analysis["summary"]
    
    # Verify details
    assert "5,000.00" in analysis["details"]
    assert "5,250.00" in analysis["details"]


def test_replay_engine_generic_incident():
    """
    Test ReplayEngine for generic (non-Pricing, non-Duplicate) incident type.
    
    Expected decision: PENDING_REVIEW
    """
    # Create mock client (not used for generic incidents)
    mock_client = MockERPNextClient()
    
    # Create generic incident
    incident = Incident(
        id=4,
        erp_reference="ERR-AUDIT-001",
        incident_type="Audit_Finding",
        status="OPEN",
        description="Missing supporting documentation",
        created_at=None
    )
    
    replay_engine = ReplayEngine(mock_client)
    analysis = replay_engine.analyze_incident(incident)
    
    # Verify decision is PENDING_REVIEW
    assert analysis["decision"] == "PENDING_REVIEW"
    
    # Verify summary mentions incident type
    assert "Audit_Finding" in analysis["summary"]
    
    # Verify conclusion recommends manual review
    assert "manual review" in analysis["conclusion"].lower()
    
    # Verify all fields are populated
    assert analysis["summary"]
    assert analysis["details"]
    assert analysis["conclusion"]


def test_replay_engine_duplicate_invoice_analysis():
    """Test ReplayEngine analysis for Duplicate_Invoice incident type."""
    # Create mock client
    mock_client = MockERPNextClient()
    
    # Create a duplicate invoice incident
    incident = Incident(
        id=5,
        erp_reference="ERR-DUPLICATE-001",
        incident_type="Duplicate_Invoice",
        status="OPEN",
        description="Duplicate invoice from vendor XYZ",
        created_at=None
    )
    
    replay_engine = ReplayEngine(mock_client)
    analysis = replay_engine.analyze_incident(incident)
    
    # Verify decision is REJECTED
    assert analysis["decision"] == "REJECTED"
    
    # Verify summary mentions duplicate
    assert "duplicate" in analysis["summary"].lower()
    
    # Verify conclusion explains duplicate risk
    assert "duplicate" in analysis["conclusion"].lower()
    assert "blocked" in analysis["conclusion"].lower() or "flagged" in analysis["conclusion"].lower()
    assert "manual" in analysis["conclusion"].lower()
    
    # Verify details
    assert "$3,200.00" in analysis["details"]
    assert "Vendor XYZ" in analysis["details"]
    assert "DUPLICATE CONFIRMED" in analysis["details"]


def test_replay_engine_analysis_structure():
    """Verify ReplayEngine returns correct analysis structure for all fields."""
    # Create mock client
    mock_client = MockERPNextClient()
    
    # Create incident
    incident = Incident(
        id=6,
        erp_reference="ERR-STRUCT-001",
        incident_type="Pricing_Issue",
        status="OPEN",
        description="Test structure",
        created_at=None
    )
    
    replay_engine = ReplayEngine(mock_client)
    analysis = replay_engine.analyze_incident(incident)
    
    # Verify all required keys are present
    assert "summary" in analysis
    assert "details" in analysis
    assert "conclusion" in analysis
    assert "decision" in analysis
    
    # Verify values are strings and not empty
    assert isinstance(analysis["summary"], str)
    assert len(analysis["summary"]) > 0
    assert isinstance(analysis["details"], str)
    assert len(analysis["details"]) > 0
    assert isinstance(analysis["conclusion"], str)
    assert len(analysis["conclusion"]) > 0
    assert isinstance(analysis["decision"], str)
    assert len(analysis["decision"]) > 0


def test_replay_engine_with_different_currencies():
    """Test ReplayEngine handles different currencies correctly."""
    # Create mock client with EUR currency
    mock_client = MockERPNextClient(
        invoice_data={
            "invoice_id": "INV-EUR-001",
            "total_amount": 5750.00,
            "currency": "EUR",
            "status": "Submitted",
            "customer": "European Corp",
            "linked_sales_order": "SO-EUR-001"
        },
        order_data={
            "order_id": "SO-EUR-001",
            "expected_amount": 5000.00,
            "currency": "EUR",
            "status": "Submitted",
            "customer": "European Corp"
        }
    )
    
    # Create incident
    incident = Incident(
        id=7,
        erp_reference="ERR-EUR-001",
        incident_type="Pricing_Issue",
        status="OPEN",
        description="EUR pricing issue",
        created_at=None
    )
    
    replay_engine = ReplayEngine(mock_client)
    analysis = replay_engine.analyze_incident(incident)
    
    # Verify decision is correct regardless of currency
    assert analysis["decision"] == "APPROVED_WITH_RISK"
    
    # Verify currency is included in details
    assert "EUR" in analysis["details"]
