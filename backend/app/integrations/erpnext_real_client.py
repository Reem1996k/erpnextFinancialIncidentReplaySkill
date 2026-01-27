"""
Real ERPNext REST API client implementation.

This module provides a concrete implementation of the BaseERPNextClient interface
that communicates with a real ERPNext system via REST API.

Environment variables required:
- ERPNEXT_BASE_URL: The base URL of the ERPNext instance (e.g., https://erpnext.example.com)
- ERPNEXT_API_TOKEN: The API token in format "API_KEY:API_SECRET"
"""

import os
from typing import Dict, Any
import requests

from .erpnext_client_base import BaseERPNextClient


class ERPNextRealClient(BaseERPNextClient):
    """
    Real ERPNext REST API client.
    
    This class provides a concrete implementation of the BaseERPNextClient interface
    that makes actual HTTP requests to an ERPNext system via the REST API.
    
    It is part of an ERPNext Financial Incident Replay skill that communicates with
    a running ERPNext instance.
    
    Configuration:
        The client reads configuration from environment variables:
        - ERPNEXT_BASE_URL: Base URL of the ERPNext instance
        - ERPNEXT_API_TOKEN: API token in format "API_KEY:API_SECRET"
    
    Authentication:
        Uses Bearer token authentication with the format:
        Authorization: token API_KEY:API_SECRET
    """

    def __init__(self):
        """
        Initialize the ERPNext real client.
        
        Raises:
            RuntimeError: If required environment variables are not set.
        """
        self.base_url = os.getenv("ERPNEXT_BASE_URL")
        self.api_token = os.getenv("ERPNEXT_API_TOKEN")

        if not self.base_url:
            raise RuntimeError(
                "ERPNEXT_BASE_URL environment variable is not set. "
                "Please set it to the base URL of your ERPNext instance (e.g., https://erpnext.example.com)."
            )

        if not self.api_token:
            raise RuntimeError(
                "ERPNEXT_API_TOKEN environment variable is not set. "
                "Please set it to your API token in the format 'API_KEY:API_SECRET'."
            )

        # Ensure base_url doesn't end with a trailing slash
        self.base_url = self.base_url.rstrip("/")

    def _get_headers(self) -> Dict[str, str]:
        """
        Generate HTTP headers for API requests.
        
        Returns:
            dict: Headers dictionary with authorization token.
        """
        return {
            "Authorization": f"token {self.api_token}",
            "Content-Type": "application/json",
        }

    def _make_request(self, endpoint: str) -> Dict[str, Any]:
        """
        Make an HTTP GET request to the ERPNext API.
        
        Args:
            endpoint (str): The API endpoint path (e.g., /api/resource/Sales Invoice/INV-001)
        
        Returns:
            dict: The parsed JSON response from the API.
        
        Raises:
            RuntimeError: If the HTTP request fails or returns an error status code.
        """
        url = f"{self.base_url}{endpoint}"

        try:
            response = requests.get(url, headers=self._get_headers(), timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            raise RuntimeError(
                f"Failed to fetch data from ERPNext. "
                f"Status code: {response.status_code}. "
                f"Response: {response.text}"
            ) from e
        except requests.exceptions.RequestException as e:
            raise RuntimeError(
                f"Error connecting to ERPNext at {url}: {str(e)}"
            ) from e
        except ValueError as e:
            raise RuntimeError(
                f"Failed to parse JSON response from ERPNext: {str(e)}"
            ) from e

    def get_invoice(self, invoice_id: str) -> Dict[str, Any]:
        """
        Retrieve invoice data from the ERPNext system.
        
        Args:
            invoice_id (str): The unique identifier of the invoice to retrieve.
        
        Returns:
            dict: A dictionary containing normalized invoice details:
                - invoice_id (str): The invoice identifier
                - total_amount (float): Total invoice amount
                - currency (str): Currency code
                - status (str): Invoice status
                - customer (str): Customer name
                - linked_sales_order (str): Associated sales order ID or None
        
        Raises:
            RuntimeError: If the API request fails.
        """
        endpoint = f"/api/resource/Sales Invoice/{invoice_id}"
        response = self._make_request(endpoint)

        # Extract data from the API response
        data = response.get("data", {})
        items = data.get("items", [])
        sales_order_id = None
        for item in items:
            if item.get("sales_order"):
                sales_order_id = item["sales_order"]
                break


        # Normalize and return the invoice data
        return {
            "invoice_id": data.get("name"),
            "total_amount": float(data.get("grand_total", 0)),
            "currency": data.get("currency", "USD"),
            "status": data.get("docstatus", "Draft"),
            "customer": data.get("customer_name", ""),
            "linked_sales_order": sales_order_id,
        }

    def get_sales_order(self, order_id: str) -> Dict[str, Any]:
        """
        Retrieve sales order data from the ERPNext system.
        
        Args:
            order_id (str): The unique identifier of the sales order to retrieve.
        
        Returns:
            dict: A dictionary containing normalized sales order details:
                - order_id (str): The order identifier
                - expected_amount (float): Expected order amount
                - currency (str): Currency code
                - status (str): Order status
                - customer (str): Customer name
        
        Raises:
            RuntimeError: If the API request fails.
        """
        endpoint = f"/api/resource/Sales Order/{order_id}"
        response = self._make_request(endpoint)

        # Extract data from the API response
        data = response.get("data", {})
        if isinstance(data, list):
            if not data:
                raise RuntimeError(f"Sales Order {order_id} not found in ERPNext")
            data = data[0]
        # Normalize and return the sales order data
        return {
            "order_id": data.get("name"),
            "expected_amount": float(data.get("grand_total", 0)),
            "currency": data.get("currency", "USD"),
            "status": data.get("docstatus", "Draft"),
            "customer": data.get("customer_name", ""),
        }