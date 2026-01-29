"""
ERP Data Extractor - Fetches and validates financial data from ERPNext.

ARCHITECTURE RULE:
- Backend owns ALL data extraction from ERP
- Extracts complete financial snapshots (Invoice + Sales Order)
- Validates data completeness
- Marks missing fields explicitly
- Returns read-only, immutable ERP snapshots
- No business logic, pure extraction and validation

This module ensures AI receives authoritative, validated ERP data.
"""

import logging
from typing import Dict, Any, Optional, List
from decimal import Decimal
from app.integrations.erpnext_client_base import BaseERPNextClient

logger = logging.getLogger(__name__)


class ERPDataExtractor:
    """
    Extracts and validates financial data from ERPNext system.
    
    Responsibilities:
    1. Fetch Invoice with all items and calculations
    2. Fetch linked Sales Order
    3. Validate data completeness
    4. Mark insufficient/missing data
    5. Return immutable ERP snapshot
    """
    
    def __init__(self, erp_client: BaseERPNextClient):
        """
        Initialize extractor with ERP client.
        
        Args:
            erp_client: ERPNext client implementation
        """
        if not erp_client:
            raise ValueError("ERPDataExtractor requires erp_client (cannot be None)")
        self.erp_client = erp_client
    
    def extract_incident_data(self, incident_reference: str) -> Dict[str, Any]:
        """
        Extract complete financial data for an incident.
        
        This is the main entry point. It treats the incident_reference
        as an Invoice ID and extracts the full financial context.
        
        Args:
            incident_reference: The invoice ID (ERP reference)
        
        Returns:
            ERP snapshot containing:
            {
                "status": "SUCCESS" | "INCOMPLETE" | "ERROR",
                "invoice": {...full invoice data...},
                "sales_order": {...full sales order data or null...},
                "customer": {...customer data or null...},
                "missing_fields": [list of missing critical fields],
                "extraction_notes": [list of data quality notes],
                "extracted_at": ISO timestamp
            }
        
        Raises:
            ValueError: If incident_reference is None or empty
            RuntimeError: If ERP client fails
        """
        if not incident_reference or not incident_reference.strip():
            raise ValueError("incident_reference cannot be None or empty")
        
        logger.info(f"ERPDataExtractor: Starting extraction for invoice {incident_reference}")
        
        try:
            # Step 1: Fetch Invoice
            invoice = self.erp_client.get_invoice(incident_reference)
            if not invoice:
                logger.error(f"ERPDataExtractor: Invoice {incident_reference} not found")
                return self._error_response(
                    f"Invoice {incident_reference} not found in ERP",
                    missing_fields=["invoice"]
                )
            
            logger.info(f"ERPDataExtractor: Invoice {incident_reference} fetched successfully")
            
            # Step 2: Extract and validate invoice data
            invoice_snapshot = self._extract_invoice(invoice)
            
            # Step 3: Resolve and fetch Sales Order
            sales_order = None
            so_reference = self._resolve_sales_order_reference(invoice)
            logger.info(f"ERPDataExtractor: SO reference resolved to: {so_reference}")
            
            if so_reference:
                logger.info(f"ERPDataExtractor: Attempting to fetch SO {so_reference} from ERP")
                try:
                    sales_order = self.erp_client.get_sales_order(so_reference)
                    if sales_order:
                        logger.info(f"ERPDataExtractor: SO {so_reference} fetched successfully with data")
                    else:
                        logger.warning(f"ERPDataExtractor: SO {so_reference} fetch returned empty/None")
                except Exception as e:
                    logger.exception(f"ERPDataExtractor: Error fetching SO {so_reference}: {str(e)}")
            else:
                logger.info("ERPDataExtractor: No SO reference found in invoice direct fields")
            
            # If SO not found via direct reference, try from invoice items
            if not sales_order:
                logger.info("ERPDataExtractor: SO not found via direct reference, trying from items")
                sales_order = self.get_sales_order_for_items(invoice.get("items", []))
                if sales_order:
                    logger.info("ERPDataExtractor: SO fetched successfully from invoice items")
                else:
                    logger.warning("ERPDataExtractor: Could not fetch SO from invoice items either")
            
            sales_order_snapshot = self._extract_sales_order(sales_order) if sales_order else None
            
            # Step 4: Fetch customer
            customer = None
            customer_id = invoice.get("customer")
            if customer_id:
                customer = self.erp_client.get_customer(customer_id)
            
            customer_snapshot = self._extract_customer(customer) if customer else None
            
            # Step 5: Validate completeness
            missing_fields = self._validate_completeness(invoice, sales_order)
            status = "INCOMPLETE" if missing_fields else "SUCCESS"
            
            logger.info(
                f"ERPDataExtractor: Extraction complete - "
                f"status={status}, missing_fields={missing_fields}"
            )
            
            return {
                "status": status,
                "invoice": invoice_snapshot,
                "sales_order": sales_order_snapshot,
                "customer": customer_snapshot,
                "missing_fields": missing_fields,
                "extraction_notes": [
                    f"Invoice: {invoice_snapshot.get('name', 'N/A')}",
                    f"Sales Order: {sales_order_snapshot.get('name', 'N/A') if sales_order_snapshot else 'NOT_LINKED'}",
                    f"Customer: {customer_snapshot.get('name', 'N/A') if customer_snapshot else 'N/A'}"
                ]
            }
        
        except Exception as e:
            logger.exception(f"ERPDataExtractor: Error extracting data for {incident_reference}")
            return self._error_response(f"Extraction error: {str(e)}")
    
    def _extract_invoice(self, invoice: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract invoice with all relevant financial fields.
        
        Args:
            invoice: Raw invoice data from ERP
        
        Returns:
            Validated invoice snapshot
        """
        items = invoice.get("items", [])
        items_snapshot = [
            {
                "item_code": item.get("item_code"),
                "item_name": item.get("item_name"),
                "quantity": self._safe_float(item.get("qty")),
                "rate": self._safe_float(item.get("rate")),
                "amount": self._safe_float(item.get("amount")),
                "description": item.get("description")
            }
            for item in items
        ]
        
        # Extract taxes
        taxes = invoice.get("taxes", [])
        taxes_snapshot = [
            {
                "tax_type": tax.get("tax_type"),
                "tax_rate": self._safe_float(tax.get("rate")),
                "tax_amount": self._safe_float(tax.get("tax_amount")),
                "description": tax.get("description")
            }
            for tax in taxes
        ]
        
        # Extract charges and adjustments
        charges = invoice.get("charges", [])
        charges_snapshot = [
            {
                "charge_type": charge.get("charge_type"),
                "charge_amount": self._safe_float(charge.get("amount")),
                "description": charge.get("description")
            }
            for charge in charges
        ]
        
        return {
            "name": invoice.get("name"),
            "customer": invoice.get("customer"),
            "posting_date": invoice.get("posting_date"),
            "due_date": invoice.get("due_date"),
            "currency": invoice.get("currency"),
            "items": items_snapshot,
            "subtotal": self._safe_float(invoice.get("net_total")),
            "taxes": taxes_snapshot,
            "extra_charges": charges_snapshot,
            "rounding_adjustment": self._safe_float(invoice.get("rounding_adjustment")),
            "total": self._safe_float(invoice.get("grand_total")),
            "status": invoice.get("docstatus"),  # 0=draft, 1=submitted, 2=cancelled
            "remarks": invoice.get("remarks"),
            "raw_data": invoice  # Keep raw for reference
        }
    
    def _extract_sales_order(self, sales_order: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Extract sales order with all relevant fields.
        
        Args:
            sales_order: Raw sales order data from ERP (or None)
        
        Returns:
            Sales order snapshot or None
        """
        if not sales_order:
            return None
        
        items = sales_order.get("items", [])
        items_snapshot = [
            {
                "item_code": item.get("item_code"),
                "item_name": item.get("item_name"),
                "quantity": self._safe_float(item.get("qty")),
                "agreed_rate": self._safe_float(item.get("rate")),
                "amount": self._safe_float(item.get("amount")),
                "description": item.get("description")
            }
            for item in items
        ]
        
        # Extract SO taxes if any
        taxes = sales_order.get("taxes", [])
        taxes_snapshot = [
            {
                "tax_type": tax.get("tax_type"),
                "tax_rate": self._safe_float(tax.get("rate")),
                "tax_amount": self._safe_float(tax.get("tax_amount")),
                "description": tax.get("description")
            }
            for tax in taxes
        ]
        
        return {
            "name": sales_order.get("name"),
            "customer": sales_order.get("customer"),
            "creation_date": sales_order.get("creation"),
            "transaction_date": sales_order.get("transaction_date"),
            "currency": sales_order.get("currency"),
            "items": items_snapshot,
            "subtotal": self._safe_float(sales_order.get("net_total")),
            "taxes": taxes_snapshot,
            "agreed_total": self._safe_float(sales_order.get("grand_total")),
            "status": sales_order.get("docstatus"),
            "remarks": sales_order.get("remarks"),
            "raw_data": sales_order
        }
    
    def _extract_customer(self, customer: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Extract customer information.
        
        Args:
            customer: Raw customer data from ERP (or None)
        
        Returns:
            Customer snapshot or None
        """
        if not customer:
            return None
        
        return {
            "name": customer.get("name"),
            "customer_name": customer.get("customer_name"),
            "email": customer.get("email_id"),
            "credit_limit": self._safe_float(customer.get("credit_limit")),
            "outstanding": self._safe_float(customer.get("outstanding")),
            "country": customer.get("country"),
            "territory": customer.get("territory"),
            "payment_terms": customer.get("payment_terms"),
            "raw_data": customer
        }
    
    def _validate_completeness(
        self, 
        invoice: Dict[str, Any],
        sales_order: Optional[Dict[str, Any]]
    ) -> List[str]:
        """
        Validate that critical data is present.
        
        Args:
            invoice: Invoice data
            sales_order: Sales order data (may be None)
        
        Returns:
            List of missing critical fields
        """
        missing = []
        
        # Invoice validations
        if not invoice.get("items"):
            missing.append("invoice.items")
        if invoice.get("grand_total") is None:
            missing.append("invoice.grand_total")
        if not invoice.get("customer"):
            missing.append("invoice.customer")
        
        # Sales Order validations (if linked)
        if sales_order:
            if not sales_order.get("items"):
                missing.append("sales_order.items")
            if sales_order.get("grand_total") is None:
                missing.append("sales_order.grand_total")
        else:
            missing.append("sales_order_not_linked")
        
        return missing
    
    def _safe_float(self, value: Any) -> Optional[float]:
        """
        Safely convert value to float.
        
        Args:
            value: Value to convert
        
        Returns:
            Float value or None
        """
        if value is None:
            return None
        try:
            if isinstance(value, (int, float)):
                return float(value)
            if isinstance(value, Decimal):
                return float(value)
            if isinstance(value, str):
                return float(value.strip())
            return None
        except (TypeError, ValueError):
            return None
    
    def _error_response(
        self,
        error_message: str,
        missing_fields: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create an error response.
        
        Args:
            error_message: Error description
            missing_fields: List of missing fields
        
        Returns:
            Error response object
        """
        if missing_fields is None:
            missing_fields = []
        
        return {
            "status": "ERROR",
            "error": error_message,
            "invoice": None,
            "sales_order": None,
            "customer": None,
            "missing_fields": missing_fields,
            "extraction_notes": [error_message]
        }
    def _resolve_sales_order_reference(self, invoice: Dict[str, Any]) -> Optional[str]:
        """
        Resolve the Sales Order reference from invoice.
        
        Tries multiple approaches to find the linked Sales Order:
        1. Direct sales_order field on invoice
        2. sales_order field on first invoice item
        3. sales_order_list field (some ERPNext versions)
        4. Linked document references
        5. Search in invoice_against_sales_order
        
        Args:
            invoice: Invoice data
        
        Returns:
            Sales Order ID or None
        """
        logger.debug(f"_resolve_sales_order_reference: Starting resolution for invoice {invoice.get('name')}")
        
        # 1. Direct invoice field
        if invoice.get("sales_order"):
            logger.debug(f"_resolve_sales_order_reference: Found SO via direct field: {invoice['sales_order']}")
            return invoice["sales_order"]

        # 2. From invoice items
        for item in invoice.get("items", []):
            if item.get("sales_order"):
                logger.debug(f"_resolve_sales_order_reference: Found SO via item: {item['sales_order']}")
                return item["sales_order"]
        
        # 3. Check for sales_order_list (some ERPNext versions)
        if invoice.get("sales_order_list"):
            so_list = invoice.get("sales_order_list", [])
            if so_list:
                logger.debug(f"_resolve_sales_order_reference: Found SO via list: {so_list[0]}")
                return so_list[0]
        
        # 4. Check for linked documents
        linked_docs = invoice.get("linked_document", [])
        for doc in linked_docs:
            if doc.get("doctype") == "Sales Order":
                logger.debug(f"_resolve_sales_order_reference: Found SO via linked_document: {doc.get('name')}")
                return doc.get("name")
        
        # 5. Check for invoice_against_sales_order field
        if invoice.get("invoice_against_sales_order"):
            logger.debug(f"_resolve_sales_order_reference: Found SO via invoice_against_sales_order: {invoice['invoice_against_sales_order']}")
            return invoice["invoice_against_sales_order"]

        logger.debug(f"_resolve_sales_order_reference: No SO reference found for invoice {invoice.get('name')}")
        return None
    
    def get_sales_order_for_items(self, invoice_items: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Try to fetch Sales Order data from invoice items.
        
        If invoice items have sales_order references, fetch and consolidate them.
        
        Args:
            invoice_items: List of invoice line items
        
        Returns:
            Consolidated sales order data or None
        """
        if not invoice_items:
            return None
        
        # Collect all unique SO references from items
        so_references = set()
        for item in invoice_items:
            if item.get("sales_order"):
                so_references.add(item["sales_order"])
                logger.debug(f"get_sales_order_for_items: Found SO reference in item: {item['sales_order']}")
        
        if not so_references:
            logger.debug("get_sales_order_for_items: No SO references found in invoice items")
            return None
        
        # For now, fetch the first one
        # In a real scenario, handle multiple SOs per invoice
        try:
            so_ref = list(so_references)[0]
            logger.info(f"get_sales_order_for_items: Attempting to fetch SO {so_ref}")
            so_data = self.erp_client.get_sales_order(so_ref)
            if so_data:
                logger.info(f"get_sales_order_for_items: Successfully fetched SO {so_ref}")
                return so_data
            else:
                logger.warning(f"get_sales_order_for_items: SO {so_ref} returned empty result")
                return None
        except Exception as e:
            logger.exception(f"get_sales_order_for_items: Failed to fetch sales order {so_ref}: {str(e)}")
            return None
