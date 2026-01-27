"""
Abstract base class for ERPNext integration.

This module defines the interface that all ERPNext client implementations
must follow. Subclasses should provide concrete implementations for
retrieving data from the ERP system.
"""

from abc import ABC, abstractmethod


class BaseERPNextClient(ABC):
    """
    Abstract base class for ERPNext client implementations.
    
    This class defines the contract for interacting with the ERPNext system.
    Subclasses must implement all abstract methods to provide concrete
    functionality for retrieving data from the ERP system.
    """

    @abstractmethod
    def get_invoice(self, invoice_id: str) -> dict:
        """
        Retrieve invoice data from the ERPNext system.
        
        Args:
            invoice_id (str): The unique identifier of the invoice to retrieve.
        
        Returns:
            dict: A dictionary containing the invoice data from the ERP system.
                 The structure and content depend on the ERPNext system's data model.
        
        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def get_sales_order(self, order_id: str) -> dict:
        """
        Retrieve sales order data from the ERPNext system.
        
        Args:
            order_id (str): The unique identifier of the sales order to retrieve.
        
        Returns:
            dict: A dictionary containing the sales order data from the ERP system.
                 The structure and content depend on the ERPNext system's data model.
        
        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        pass
