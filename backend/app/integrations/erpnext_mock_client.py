"""
Mock ERPNext Client for Testing & Development

Returns hardcoded financial data for testing replay engine
without needing a real ERPNext instance.
"""

from typing import Dict, Any, Optional
from .erpnext_client_base import BaseERPNextClient


class ERPNextMockClient(BaseERPNextClient):
    """
    Mock ERPNext client that returns hardcoded test data.
    
    Used for testing, development, and demonstration without requiring
    a real ERPNext connection.
    """

    def get_invoice(self, invoice_id: str) -> Optional[Dict[str, Any]]:
        """
        Return mock invoice data for testing.
        
        Test scenarios:
        - INV-001: Normal invoice matching sales order
        - INV-002: Pricing issue (invoice higher than SO)
        - INV-003: Duplicate invoice
        - ACC-SINV-2026-00009: Real test case with linked SO and additional charges
        """
        invoices = {
            "INV-001": {
                "name": "INV-001",
                "doctype": "Sales Invoice",
                "customer": "CUST-001",
                "customer_name": "Acme Corp",
                "posting_date": "2024-01-15",
                "sales_order": "SO-001",
                "grand_total": 5000.00,
                "total_qty": 10,
                "items": [
                    {
                        "item_code": "ITEM-A",
                        "item_name": "Widget A",
                        "qty": 10,
                        "rate": 500.00,
                        "amount": 5000.00
                    }
                ]
            },
            "INV-002": {
                "name": "INV-002",
                "doctype": "Sales Invoice",
                "customer": "CUST-002",
                "customer_name": "Beta Inc",
                "posting_date": "2024-01-16",
                "sales_order": "SO-002",
                "grand_total": 10500.00,
                "total_qty": 10,
                "items": [
                    {
                        "item_code": "ITEM-B",
                        "item_name": "Widget B",
                        "qty": 10,
                        "rate": 1050.00,
                        "amount": 10500.00
                    }
                ]
            },
            "INV-003": {
                "name": "INV-003",
                "doctype": "Sales Invoice",
                "customer": "CUST-001",
                "customer_name": "Acme Corp",
                "posting_date": "2024-01-17",
                "sales_order": "SO-001",
                "grand_total": 5000.00,
                "total_qty": 10,
                "items": [
                    {
                        "item_code": "ITEM-A",
                        "item_name": "Widget A",
                        "qty": 10,
                        "rate": 500.00,
                        "amount": 5000.00
                    }
                ]
            },
            "ACC-SINV-2026-00009": {
                "name": "ACC-SINV-2026-00009",
                "doctype": "Sales Invoice",
                "customer": "Test Customer",
                "customer_name": "Test Customer",
                "posting_date": "2026-01-28",
                "sales_order": "SO-2026-00005",
                "net_total": 10000.00,
                "currency": "ILS",
                "docstatus": 1,
                "items": [
                    {
                        "item_code": "ITEM-001",
                        "item_name": "Item 001",
                        "qty": 10,
                        "rate": 500.00,
                        "amount": 5000.00
                    },
                    {
                        "item_code": "ITEM-002",
                        "item_name": "Item 002",
                        "qty": 10,
                        "rate": 500.00,
                        "amount": 5000.00
                    }
                ],
                "taxes": [
                    {
                        "tax_type": "VAT",
                        "rate": 20.0,
                        "tax_amount": 2000.00
                    }
                ],
                "charges": [
                    {
                        "charge_type": "Shipping",
                        "amount": 1000.00
                    }
                ],
                "rounding_adjustment": 0.0,
                "grand_total": 12000.00
            }
        }
        return invoices.get(invoice_id)

    def get_sales_order(self, order_id: str) -> Optional[Dict[str, Any]]:
        """Return mock sales order data."""
        orders = {
            "SO-001": {
                "name": "SO-001",
                "doctype": "Sales Order",
                "customer": "CUST-001",
                "customer_name": "Acme Corp",
                "creation": "2024-01-10",
                "total_qty": 10,
                "total_amount": 5000.00,
                "items": [
                    {
                        "item_code": "ITEM-A",
                        "item_name": "Widget A",
                        "qty": 10,
                        "rate": 500.00,
                        "amount": 5000.00
                    }
                ]
            },
            "SO-002": {
                "name": "SO-002",
                "doctype": "Sales Order",
                "customer": "CUST-002",
                "customer_name": "Beta Inc",
                "creation": "2024-01-11",
                "total_qty": 10,
                "total_amount": 10000.00,
                "items": [
                    {
                        "item_code": "ITEM-B",
                        "item_name": "Widget B",
                        "qty": 10,
                        "rate": 1000.00,
                        "amount": 10000.00
                    }
                ]
            },
            "SO-2026-00005": {
                "name": "SO-2026-00005",
                "doctype": "Sales Order",
                "customer": "Test Customer",
                "customer_name": "Test Customer",
                "creation": "2026-01-20",
                "posting_date": "2026-01-20",
                "transaction_date": "2026-01-20",
                "currency": "ILS",
                "docstatus": 1,
                "net_total": 10000.00,
                "grand_total": 11700.00,
                "items": [
                    {
                        "item_code": "RK2910",
                        "item_name": "Item RK2910",
                        "qty": 10,
                        "rate": 500.00,
                        "amount": 5000.00,
                        "description": "Sales Order Item"
                    },
                    {
                        "item_code": "ITEM-002",
                        "item_name": "Item 002",
                        "qty": 10,
                        "rate": 500.00,
                        "amount": 5000.00,
                        "description": "Sales Order Item"
                    }
                ],
                "taxes": [
                    {
                        "tax_type": "VAT",
                        "rate": 17.0,
                        "tax_amount": 1700.00,
                        "description": "VAT"
                    }
                ],
                "total_qty": 20,
                "remarks": "Linked Sales Order"
            }
        }
        return orders.get(order_id)

    def get_customer(self, customer_id: str) -> Optional[Dict[str, Any]]:
        """Return mock customer data."""
        customers = {
            "CUST-001": {
                "name": "CUST-001",
                "doctype": "Customer",
                "customer_name": "Acme Corp",
                "email": "contact@acme.com",
                "country": "United States",
                "credit_limit": 50000.00
            },
            "CUST-002": {
                "name": "CUST-002",
                "doctype": "Customer",
                "customer_name": "Beta Inc",
                "email": "sales@beta.com",
                "country": "Canada",
                "credit_limit": 75000.00
            }
        }
        return customers.get(customer_id)



