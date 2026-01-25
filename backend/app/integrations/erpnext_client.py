"""
Create a mock ERPNext client for integration testing.

Requirements:
- Create a class named ERPNextClient
- This class simulates communication with ERPNext REST API
- Do NOT perform real HTTP requests
- Return hardcoded (mock) data

Methods to implement:

1. get_invoice(invoice_id: str) -> dict
   - Return a dictionary with:
     - invoice_id
     - total_amount
     - currency
     - status
     - customer
     - linked_sales_order

2. get_sales_order(order_id: str) -> dict
   - Return a dictionary with:
     - order_id
     - expected_amount
     - currency
     - status
     - customer

Additional notes:
- Add clear docstrings explaining that this is a mock client
- This client will be replaced later with a real ERPNext API integration
- Keep the code simple and readable
"""

from typing import Dict, Any


class ERPNextClient:
    """
    Mock ERPNext REST API client for integration testing.
    
    This class simulates communication with ERPNext without making real HTTP requests.
    It returns hardcoded (mock) data for testing and development purposes.
    
    NOTE: This is a mock implementation. In production, this should be replaced with
    a real ERPNext API client that makes actual HTTP requests.
    """
    
    def __init__(self):
        """Initialize the mock ERPNext client."""
        pass
    
    def get_invoice(self, invoice_id: str) -> Dict[str, Any]:
        """
        Retrieve invoice data from ERPNext (mock).
        
        Args:
            invoice_id: The invoice ID to retrieve
        
        Returns:
            Dictionary containing invoice details:
            - invoice_id: str - The invoice identifier
            - total_amount: float - Total invoice amount
            - currency: str - Currency code (e.g., USD)
            - status: str - Invoice status (Draft, Submitted, Paid, etc.)
            - customer: str - Customer name
            - linked_sales_order: str - Associated sales order ID
        
        Note: This is a mock implementation that returns hardcoded data.
        """
        # Mock invoice data
        mock_invoices = {
            "INV-001": {
                "invoice_id": "INV-001",
                "total_amount": 5750.00,
                "currency": "USD",
                "status": "Submitted",
                "customer": "Acme Corporation",
                "linked_sales_order": "SO-001"
            },
            "INV-002": {
                "invoice_id": "INV-002",
                "total_amount": 3200.00,
                "currency": "USD",
                "status": "Submitted",
                "customer": "Vendor XYZ",
                "linked_sales_order": "SO-002"
            },
            "INV-003": {
                "invoice_id": "INV-003",
                "total_amount": 8500.00,
                "currency": "EUR",
                "status": "Paid",
                "customer": "Global Industries",
                "linked_sales_order": "SO-003"
            }
        }
        
        # Return mock data for the requested invoice or a default
        return mock_invoices.get(invoice_id, {
            "invoice_id": invoice_id,
            "total_amount": 0.00,
            "currency": "USD",
            "status": "Draft",
            "customer": "Unknown",
            "linked_sales_order": None
        })
    
    def get_sales_order(self, order_id: str) -> Dict[str, Any]:
        """
        Retrieve sales order data from ERPNext (mock).
        
        Args:
            order_id: The sales order ID to retrieve
        
        Returns:
            Dictionary containing sales order details:
            - order_id: str - The order identifier
            - expected_amount: float - Expected order amount
            - currency: str - Currency code (e.g., USD)
            - status: str - Order status (Draft, Submitted, Delivered, etc.)
            - customer: str - Customer name
        
        Note: This is a mock implementation that returns hardcoded data.
        """
        # Mock sales order data
        mock_orders = {
            "SO-001": {
                "order_id": "SO-001",
                "expected_amount": 5000.00,
                "currency": "USD",
                "status": "Submitted",
                "customer": "Acme Corporation"
            },
            "SO-002": {
                "order_id": "SO-002",
                "expected_amount": 3200.00,
                "currency": "USD",
                "status": "Submitted",
                "customer": "Vendor XYZ"
            },
            "SO-003": {
                "order_id": "SO-003",
                "expected_amount": 8000.00,
                "currency": "EUR",
                "status": "Delivered",
                "customer": "Global Industries"
            }
        }
        
        # Return mock data for the requested order or a default
        return mock_orders.get(order_id, {
            "order_id": order_id,
            "expected_amount": 0.00,
            "currency": "USD",
            "status": "Draft",
            "customer": "Unknown"
        })


