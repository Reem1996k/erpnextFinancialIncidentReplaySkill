"""
Factory for creating ERPNext client instances.

This module provides a factory function that creates the appropriate ERPNext
client based on the environment configuration. It supports both mock clients
for testing and real API clients for production use.
"""

import os
from .erpnext_client_base import BaseERPNextClient
from .erpnext_real_client import ERPNextRealClient


def get_erp_client() -> BaseERPNextClient:
    """
    Factory function to create an ERPNext client instance.
    
    The client type is determined by the ERP_CLIENT_MODE environment variable:
    - "real": Creates an ERPNextRealClient that makes actual HTTP requests to ERPNext
    
    Environment Variables:
        ERP_CLIENT_MODE: Controls which client implementation to use.
            Accepts: "real", "mock" (default if not set or unrecognized)
    
    Returns:
        BaseERPNextClient: An instance of either ERPNextRealClient or ERPNextMockClient
    
    Raises:
        ValueError: If ERP_CLIENT_MODE is set to an invalid value
    
    Examples:
        >>> # Use real client (for production)
        >>> os.environ["ERP_CLIENT_MODE"] = "real"
        >>> client = get_erp_client()
        >>> isinstance(client, ERPNextRealClient)
        True
    """
    mode = os.getenv("ERP_CLIENT_MODE", "mock").lower().strip()

    if mode == "real":
        return ERPNextRealClient()
    else:
        raise ValueError(
            f"Invalid ERP_CLIENT_MODE value: '{mode}'. "
            f"Supported values are: 'real' (for production ERPNext API), "
            f"'mock' (for testing with hardcoded data). "
            f"Defaults to 'mock' if not set."
        )
