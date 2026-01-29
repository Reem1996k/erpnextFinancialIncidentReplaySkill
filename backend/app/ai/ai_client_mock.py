"""
Mock AI client for testing without API calls.

This module provides a mock AI implementation that returns realistic
but hardcoded responses. Perfect for:
- Unit testing without external dependencies
- Local development without API keys
- Testing error scenarios
- Demonstrating AI functionality without costs
"""

from typing import Dict, Any
from app.ai.ai_client_base import AIClientBase


class AIClientMock(AIClientBase):
    """
    Mock AI client returning realistic test data.
    
    Implements the same interface as real AI clients but returns
    hardcoded responses that demonstrate typical AI analysis results.
    
    Why mock?
    - Enables testing without OpenAI API calls
    - No API costs during development
    - Deterministic responses for reproducible tests
    - Easy to test error scenarios
    """
    
    def __init__(self, fail: bool = False):
        """
        Initialize mock AI client.
        
        Args:
            fail: If True, simulate API failure for error handling tests
        """
        self.fail = fail
    
    def is_available(self) -> bool:
        """Mock is always available."""
        return True
    
    def analyze(self, prompt: str) -> Dict[str, Any]:
        """
        Return mock analysis response.
        
        Args:
            prompt: Analysis prompt (ignored by mock)
        
        Returns:
            Realistic mock analysis result
        
        Raises:
            RuntimeError: If fail=True was set in __init__
        """
        if self.fail:
            raise RuntimeError("Mock AI failure - simulating API error")
        
        # Determine response based on incident type in prompt
        if "duplicate" in prompt.lower():
            return {
                "root_cause": "Duplicate invoice entry detected - same SO and invoice number already exists",
                "recommended_actions": [
                    "Cancel the duplicate invoice",
                    "Verify with sales team on original entry",
                    "Update customer records if needed"
                ],
                "customer_message": "We detected a duplicate invoice entry in our system and have cancelled it. No payment is required.",
                "confidence_score": 0.95
            }
        
        elif "amount" in prompt.lower() or "mismatch" in prompt.lower():
            return {
                "root_cause": "Invoice amount does not match sales order - possible calculation error or unauthorized amendments",
                "recommended_actions": [
                    "Review calculation details",
                    "Check for unapproved price amendments",
                    "Contact customer for verification"
                ],
                "customer_message": "We identified an amount discrepancy on your invoice. Our finance team will contact you within 24 hours.",
                "confidence_score": 0.87
            }
        
        elif "late" in prompt.lower() or "overdue" in prompt.lower():
            return {
                "root_cause": "Invoice significantly overdue - payment not received within standard terms",
                "recommended_actions": [
                    "Send payment reminder",
                    "Review credit limit and customer history",
                    "Escalate to sales team for relationship review"
                ],
                "customer_message": "This invoice is overdue. Please arrange payment at your earliest convenience.",
                "confidence_score": 0.92
            }
        
        else:
            # Generic response for unknown incident types
            return {
                "root_cause": "Processing anomaly detected in financial transaction",
                "recommended_actions": [
                    "Review transaction details with customer",
                    "Verify data integrity in source systems",
                    "Update transaction records if correction needed"
                ],
                "customer_message": "We detected an issue with your transaction. Our team is investigating and will contact you shortly.",
                "confidence_score": 0.75
            }
