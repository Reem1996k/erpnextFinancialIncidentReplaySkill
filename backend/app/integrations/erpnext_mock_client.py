"""
Mock ERPNext client implementation for testing and development.

This module provides a mock implementation of the BaseERPNextClient interface
that simulates ERPNext API responses without making real HTTP requests.
It returns hardcoded (mock) financial data for testing purposes.

NOTE: This is a mock implementation. In production, this should be replaced with
a real ERPNext API client that makes actual HTTP requests.
"""

from typing import Dict, Any
from .erpnext_client_base import BaseERPNextClient


class ERPNextMockClient(BaseERPNextClient):
    """
    Mock ERPNext client for testing and development.
    
    This class provides a mock implementation of the BaseERPNextClient interface.
    It simulates communication with ERPNext without making real HTTP requests,
    returning hardcoded (mock) data for testing and development purposes.
    
    This implementation is intended for use in test environments only.
    In production, replace this with a real ERPNext API client.
    """
    
    def __init__(self):
        """Initialize the mock ERPNext client."""
        pass
    
    def get_invoice(self, invoice_id: str) -> Dict[str, Any]:
        """
        Retrieve invoice data from ERPNext (mock implementation).
        
        Args:
            invoice_id (str): The unique identifier of the invoice to retrieve.
        
        Returns:
            dict: A dictionary containing mock invoice details:
                - invoice_id (str): The invoice identifier
                - total_amount (float): Total invoice amount
                - currency (str): Currency code (e.g., USD, EUR)
                - status (str): Invoice status (Draft, Submitted, Paid, etc.)
                - customer (str): Customer name
                - linked_sales_order (str): Associated sales order ID or None
        
        Note:
            This is a mock implementation that returns hardcoded data.
            For testing purposes only.
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
        Retrieve sales order data from ERPNext (mock implementation).
        
        Args:
            order_id (str): The unique identifier of the sales order to retrieve.
        
        Returns:
            dict: A dictionary containing mock sales order details:
                - order_id (str): The order identifier
                - expected_amount (float): Expected order amount
                - currency (str): Currency code (e.g., USD, EUR)
                - status (str): Order status (Draft, Submitted, Delivered, etc.)
                - customer (str): Customer name
        
        Note:
            This is a mock implementation that returns hardcoded data.
            For testing purposes only.
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


