"""
Real ERPNext REST API client implementation.

This module provides a concrete implementation of the BaseERPNextClient interface
that communicates with a real ERPNext system via REST API.

Environment variables required:
- ERPNEXT_BASE_URL: The base URL of the ERPNext instance (e.g., https://erpnext.example.com)
- ERPNEXT_API_TOKEN: The API token in format "API_KEY:API_SECRET"
"""

import os
import logging
from typing import Dict, Any
import requests
from pathlib import Path
from dotenv import load_dotenv

from .erpnext_client_base import BaseERPNextClient

logger = logging.getLogger(__name__)

# Ensure .env is loaded
backend_dir = Path(__file__).parent.parent.parent
env_path = backend_dir / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)


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
        logger.debug(f"ERPNextRealClient: Making request to {url}")

        try:
            response = requests.get(url, headers=self._get_headers(), timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                # Resource not found - return empty response
                logger.warning(f"ERPNextRealClient: Resource not found at {url}")
                return {"data": {}}
            logger.error(f"ERPNextRealClient: HTTP error {response.status_code} at {url}")
            raise RuntimeError(
                f"Failed to fetch data from ERPNext. "
                f"Status code: {response.status_code}. "
                f"Response: {response.text}"
            ) from e
        except requests.exceptions.RequestException as e:
            logger.error(f"ERPNextRealClient: Request error at {url}: {str(e)}")
            raise RuntimeError(
                f"Error connecting to ERPNext at {url}: {str(e)}"
            ) from e
        except ValueError as e:
            logger.error(f"ERPNextRealClient: JSON parse error at {url}: {str(e)}")
            raise RuntimeError(
                f"Failed to parse JSON response from ERPNext: {str(e)}"
            ) from e

    def get_invoice(self, invoice_id: str) -> Dict[str, Any]:
        """
        Retrieve invoice data from the ERPNext system.
        
        Args:
            invoice_id (str): The unique identifier of the invoice to retrieve.
        
        Returns:
            dict: Raw invoice data from ERPNext API including all fields.
        
        Raises:
            RuntimeError: If the API request fails.
        """
        endpoint = f"/api/resource/Sales Invoice/{invoice_id}"
        response = self._make_request(endpoint)
        data = response.get("data", {})
        
        # Debug: Log the actual fields returned by real API
        logger.debug(f"ERPNextRealClient: Invoice {invoice_id} raw keys: {list(data.keys())}")
        if data:
            logger.debug(f"ERPNextRealClient: Invoice {invoice_id} full data: {data}")
        
        # Return raw data for financial extractor to process
        return data

    def get_sales_order(self, order_id: str) -> Dict[str, Any]:
        """
        Retrieve sales order data from the ERPNext system.
        
        Args:
            order_id (str): The unique identifier of the sales order to retrieve.
        
        Returns:
            dict: Raw sales order data from ERPNext API including all fields, or empty dict if not found.
        
        Raises:
            RuntimeError: If the API request fails.
        """
        logger.info(f"ERPNextRealClient: Fetching Sales Order {order_id}")
        endpoint = f"/api/resource/Sales Order/{order_id}"
        response = self._make_request(endpoint)
        data = response.get("data", {})
        
        # Return raw data for financial extractor to process
        if isinstance(data, list):
            if not data:
                logger.warning(f"ERPNextRealClient: Sales Order {order_id} returned empty list")
                return {}
            logger.info(f"ERPNextRealClient: Sales Order {order_id} fetched successfully")
            return data[0]
        
        if data:
            logger.info(f"ERPNextRealClient: Sales Order {order_id} fetched successfully")
        else:
            logger.warning(f"ERPNextRealClient: Sales Order {order_id} not found or empty")
        return data

    def get_customer(self, customer_id: str) -> Dict[str, Any]:
        """
        Retrieve customer data from the ERPNext system.
        
        Args:
            customer_id (str): The unique identifier of the customer to retrieve.
        
        Returns:
            dict: Raw customer data from ERPNext API.
        
        Raises:
            RuntimeError: If the API request fails.
        """
        endpoint = f"/api/resource/Customer/{customer_id}"
        response = self._make_request(endpoint)
        data = response.get("data", {})
        
        # Return raw data
        if isinstance(data, list):
            if not data:
                return {}
            return data[0]
        
        return data

