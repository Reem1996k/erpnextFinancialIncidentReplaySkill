"""
Mock AI Client for Testing

Provides a configurable mock AI client that simulates AI analysis
without making actual API calls. Supports success and failure scenarios.
"""

from typing import Dict, Any
from app.ai.ai_client_base import AIClientBase


class MockAIClient(AIClientBase):
    """
    Mock AI client for testing incident analysis.

    IMPORTANT:
    This mock strictly follows the AIResultMapper contract.
    """

    def __init__(self, should_succeed: bool = True, raise_exception: bool = False):
        self.should_succeed = should_succeed
        self.raise_exception = raise_exception

    def analyze(self, prompt: str) -> Dict[str, Any]:
        if self.raise_exception:
            raise Exception("Mock AI service unavailable")

        if self.should_succeed:
            # ✅ FULL SUCCESS CONTRACT (REQUIRED FIELDS)
            return {
                "replay_summary": "Invoice includes an additional freight charge not present in sales order",
                "replay_details": "SO subtotal: 10000 + tax: 2000 = invoice total 12000",
                "replay_conclusion": "Remove or correct the freight charge",
                "confidence_score": 0.95,
            }

        # ❌ FAILURE BUT VALID STRUCTURE (NO EXCEPTION)
        return {
            "replay_summary": "",
            "replay_details": "",
            "replay_conclusion": "",
            "confidence_score": 0.0,
        }

    def is_available(self) -> bool:
        return True


# =========================
# Factory helpers
# =========================

def get_mock_ai_client_success():
    return MockAIClient(should_succeed=True, raise_exception=False)


def get_mock_ai_client_failure():
    return MockAIClient(should_succeed=False, raise_exception=False)


def get_mock_ai_client_exception():
    return MockAIClient(should_succeed=True, raise_exception=True)
