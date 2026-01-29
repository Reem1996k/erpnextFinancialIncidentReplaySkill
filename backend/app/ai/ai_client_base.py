"""
Abstract base class for AI service providers.

This module defines the interface that all AI implementations must follow.
It enables flexible provider switching (OpenAI, Claude, custom LLMs, mocks)
without changing the core business logic.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class AIClientBase(ABC):
    """
    Abstract base class for AI incident analysis providers.
    
    This interface ensures all AI implementations provide consistent
    structured responses for incident analysis. Implementations handle
    their own authentication, rate limiting, and error handling.
    
    Why separate AI clients?
    - Enables testing without API calls (use mock)
    - Supports provider switching (OpenAI → Claude → Custom LLM)
    - Keeps API keys and credentials separate
    - Follows dependency injection principles
    """
    
    @abstractmethod
    def analyze(self, prompt: str) -> Dict[str, Any]:
        """
        Analyze a financial incident using AI.
        
        Args:
            prompt: Detailed analysis prompt containing:
                - Incident description and context
                - ERP data (invoice, sales order, customer)
                - Current rule-based decision
                - Business context
        
        Returns:
            Structured analysis result:
            {
                "root_cause": str,          # Why the incident occurred
                "recommended_actions": [   # What to do about it
                    "action 1",
                    "action 2",
                    ...
                ],
                "customer_message": str,   # How to communicate to customer
                "confidence_score": float  # 0.0-1.0, how confident is this analysis
            }
        
        Raises:
            Exception: Any error should raise with descriptive message.
                      Caller will handle fallback to manual review.
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the AI service is properly configured and available.
        
        Returns:
            True if service can be used, False if misconfigured
        """
        pass
