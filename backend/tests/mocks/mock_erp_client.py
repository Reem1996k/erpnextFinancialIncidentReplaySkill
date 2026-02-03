"""
Mock ERP Client for Testing

Provides mock ERPNext data without making actual API calls.
"""

from typing import Dict, Any, Optional
from app.integrations.erpnext_client_base import BaseERPNextClient


def get_invoice_data():
    return {
        "id": "ACC-SINV-2026-00009",
        "currency": "ILS",
        "subtotal": 10000.0,
        "grand_total": 12000.0,
        "items": [
            {
                "item_code": "ITEM-001",
                "qty": 1,
                "rate": 10000.0,
                "amount": 10000.0
            }
        ],
        "taxes": [
            {
                "account_head": "Freight and Forwarding Charges - DCD",
                "rate": 0,
                "tax_amount": 2000.0
            }
        ],
        "charges": []
    }


def get_sales_order_data():
    return {
        "id": "SO-0009",
        "currency": "ILS",
        "subtotal": 10000.0,
        "grand_total": 10000.0,
        "items": [
            {
                "item_code": "ITEM-001",
                "qty": 1,
                "rate": 10000.0,
                "amount": 10000.0
            }
        ]
    }


def get_full_erp_context():
    """
    ERP context passed to analysis / AI resolver.
    """
    return {
        "invoice": get_invoice_data(),
        "sales_order": get_sales_order_data(),
        "customer": {
            "name": "ACME Ltd",
            "credit_limit": 50000
        }
    }


class MockERPNextClient(BaseERPNextClient):
    """
    Mock ERPNext client for testing.
    
    Returns predefined invoice and sales order data without
    making actual API calls to ERPNext.
    """

    def get_invoice(self, invoice_id: str) -> Optional[Dict[str, Any]]:
        """
        Return mock invoice data.
        
        Args:
            invoice_id: Invoice ID (ignored in mock)
        
        Returns:
            Mock invoice data
        """
        return get_invoice_data()

    def get_sales_order(self, order_id: str) -> Optional[Dict[str, Any]]:
        """
        Return mock sales order data.
        
        Args:
            order_id: Sales order ID (ignored in mock)
        
        Returns:
            Mock sales order data
        """
        return get_sales_order_data()

    def get_customer(self, customer_id: str) -> Optional[Dict[str, Any]]:
        """
        Return mock customer data.
        
        Args:
            customer_id: Customer ID (ignored in mock)
        
        Returns:
            Mock customer data
        """
        return {
            "name": "ACME Ltd",
            "credit_limit": 50000
        }


def get_mock_erp_client():
    """Get a mock ERP client for testing."""
    return MockERPNextClient()
