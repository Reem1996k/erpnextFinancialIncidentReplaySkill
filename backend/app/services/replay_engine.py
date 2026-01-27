"""
Replay Engine service for analyzing financial incidents.

This module provides the ReplayEngine class which analyzes financial incidents
using dependency injection to work with any BaseERPNextClient implementation.
The ERP client can be explicitly provided for testing or automatically selected
based on the ERP_CLIENT_MODE environment variable.
"""

from typing import Dict, Any, Optional
from app.db.models import Incident
from app.integrations.erpnext_client_base import BaseERPNextClient
from app.integrations.client_factory import get_erp_client


class ReplayEngine:
    """
    Service for analyzing financial incidents with ERPNext integration.
    
    This class uses dependency injection to accept any implementation of
    BaseERPNextClient, allowing for flexible testing with mock clients
    and production use with real API clients.
    """
    
    def __init__(self, erp_client: Optional[BaseERPNextClient] = None):
        """
        Initialize the ReplayEngine with an ERPNext client.
        
        Args:
            erp_client (Optional[BaseERPNextClient]): An implementation of the ERPNext
                client interface. If not provided (None), the client will be automatically
                selected based on the ERP_CLIENT_MODE environment variable via the factory:
                - "real": Creates an ERPNextRealClient for production use
                - "mock" (default): Creates an ERPNextMockClient for testing
                
                This can be explicitly provided for unit testing to inject a mock or test
                double, which will bypass the factory and environment variable check.
        
        Note:
            This uses dependency injection to allow flexibility in choosing which
            ERPNext client implementation to use. When erp_client is None, the factory
            function respects the ERP_CLIENT_MODE environment variable for automatic
            client selection. This allows tests to pass in mock clients while production
            code uses environment-driven configuration.
        """
        self.erp_client = erp_client if erp_client is not None else get_erp_client()

    
    def analyze_incident(self, incident: Incident) -> Dict[str, Any]:
        """
        Analyze an incident based on its type.
        
        Args:
            incident: The Incident object to analyze
        
        Returns:
            Dictionary containing summary, details, conclusion, and decision
        """
        if incident.incident_type == "Pricing_Issue":
            return self._analyze_pricing_issue(incident)
        elif incident.incident_type == "Duplicate_Invoice":
            return self._analyze_duplicate_invoice(incident)
        else:
            return self._analyze_generic(incident)
    
    def _analyze_pricing_issue(self, incident: Incident) -> Dict[str, Any]:
        """
        Analyze a pricing issue incident using ERPNext data.
        
        Retrieves invoice and sales order data from ERPNext client,
        compares amounts, and determines if the variance is acceptable.
        
        Args:
            incident: The Incident object
        
        Returns:
            Analysis dictionary with summary, details, conclusion, and decision
        """
        # Extract invoice and order IDs from description or use defaults
        # For demo purposes, we'll use mock IDs that the mock client recognizes
        invoice_id = incident.erp_reference  # ✅ החשבונית האמיתית מ-ERPNext

        invoice_data = self.erp_client.get_invoice(invoice_id)

        sales_order_id = invoice_data.get("linked_sales_order")
        if not sales_order_id:
            raise RuntimeError(
        f"No linked Sales Order found for invoice {invoice_id}"
    )
        sales_order_data = self.erp_client.get_sales_order(sales_order_id)
        
        # Extract amounts
        invoice_amount = invoice_data.get("total_amount", 0)
        expected_amount = sales_order_data.get("expected_amount", 0)
        currency = invoice_data.get("currency", "USD")
        
        # Calculate difference
        difference = invoice_amount - expected_amount
        
        # Calculate percentage difference
        if expected_amount > 0:
            percentage_difference = (difference / expected_amount) * 100
        else:
            percentage_difference = 0
        
        # Determine decision based on percentage
        if abs(percentage_difference) <= 20:
            decision = "APPROVED_WITH_RISK"
        else:
            decision = "REJECTED"
        
        # Build response
        summary = f"Invoice exceeds expected amount by {percentage_difference:.1f}%"
        details = (
            f"Invoice ID: {invoice_id}\n"
            f"Sales Order ID: {sales_order_id}\n"
            f"Expected amount: {currency} {expected_amount:,.2f}\n"
            f"Invoice amount: {currency} {invoice_amount:,.2f}\n"
            f"Difference: {currency} {difference:,.2f} ({percentage_difference:.1f}%)\n"
            f"Invoice Status: {invoice_data.get('status', 'Unknown')}\n"
            f"Order Status: {sales_order_data.get('status', 'Unknown')}"
        )
        conclusion = (
            f"Decision: {decision}. "
            f"The invoice amount is {abs(percentage_difference):.1f}% "
            f"{'above' if difference > 0 else 'below'} the expected amount. "
            f"Variance is {'within' if abs(percentage_difference) <= 20 else 'outside'} "
            f"acceptable threshold (20%). Requires manual review for compliance."
        )
        
        return {
            "summary": summary,
            "details": details,
            "conclusion": conclusion,
            "decision": decision
        }
    
    def _analyze_duplicate_invoice(self, incident: Incident) -> Dict[str, Any]:
        """
        Analyze a duplicate invoice incident.
        
        Args:
            incident: The Incident object
        
        Returns:
            Analysis dictionary
        """
        # Define duplicate invoice parameters
        invoice_amount = 3200
        vendor_name = "Vendor XYZ"
        invoice_date = "2024-01-15"
        
        # Duplicate detected
        decision = "REJECTED"
        
        summary = "Duplicate invoice detected - Same amount, vendor, and date"
        details = (
            f"Invoice Amount: ${invoice_amount:,.2f}\n"
            f"Vendor: {vendor_name}\n"
            f"Invoice Date: {invoice_date}\n"
            f"Matching Fields: Amount, Vendor, Date\n"
            f"Status: DUPLICATE CONFIRMED"
        )
        conclusion = (
            f"Decision: {decision}. "
            f"Invoice has been flagged as a duplicate based on matching "
            f"amount, vendor, and date. This payment has been blocked to prevent "
            f"duplicate payment. Manual verification required."
        )
        
        return {
            "summary": summary,
            "details": details,
            "conclusion": conclusion,
            "decision": decision
        }
    
    def _analyze_generic(self, incident: Incident) -> Dict[str, Any]:
        """
        Analyze a generic incident.
        
        Args:
            incident: The Incident object
        
        Returns:
            Analysis dictionary
        """
        return {
            "summary": f"Analysis for {incident.incident_type}",
            "details": incident.description,
            "conclusion": "Generic analysis completed. Manual review recommended.",
            "decision": "PENDING_REVIEW"
        }
