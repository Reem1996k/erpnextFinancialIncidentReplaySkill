"""
Complete ERPNext Client Base Class

Abstract base class defining the interface for all ERPNext integrations.
Implementations must provide methods for fetching financial data from ERP.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseERPNextClient(ABC):
    """
    Abstract base class for ERPNext client implementations.
    
    This class defines the contract for interacting with the ERPNext system.
    All implementations must provide methods for fetching financial data.
    """

    @abstractmethod
    def get_invoice(self, invoice_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve invoice data from the ERPNext system.
        
        Args:
            invoice_id: The unique identifier of the invoice
        
        Returns:
            Dict with invoice data or None if not found.
            Should include: name, customer, items, grand_total, posting_date, etc.
        """
        pass

    @abstractmethod
    def get_sales_order(self, order_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve sales order data from the ERPNext system.
        
        Args:
            order_id: The unique identifier of the sales order
        
        Returns:
            Dict with sales order data or None if not found.
            Should include: name, customer, items, total_amount, creation, etc.
        """
        pass

    @abstractmethod
    def get_customer(self, customer_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve customer data from the ERPNext system.
        
        Args:
            customer_id: The unique identifier of the customer
        
        Returns:
            Dict with customer data or None if not found.
            Should include: name, email, credit_limit, country, etc.
        """
        pass
