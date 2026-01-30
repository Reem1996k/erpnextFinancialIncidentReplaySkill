"""
AI Result Mapper - Map Claude response only, NO defaults.

ARCHITECTURE RULE: Never inject default summaries.
- If Claude didn't provide a field, return empty string (not a default)
- Raises ValueError on invalid response
- Pure mapping, no guessing
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class AIResultMapper:
    """
    Maps Claude API response to incident database fields.
    
    STRICT RULES:
    - Only maps fields that Claude actually provided
    - Never invents summaries or conclusions
    - Raises ValueError on missing required fields
    - Empty string if field missing (not default text)
    """
    
    @staticmethod
    def map_ai_response(api_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map Claude API response to incident fields.
        
        Args:
            api_response: Response from AIClientAnthropic.analyze()
        
        Returns:
            {
                "replay_summary": str,
                "replay_details": str,
                "replay_conclusion": str,
                "confidence_score": float (0.0-1.0)
            }
        
        Raises:
            ValueError: If missing required fields
        """
        if not api_response or not isinstance(api_response, dict):
            raise ValueError("Invalid API response: empty or non-dict")
        
        # Extract required fields from Claude response
        summary = api_response.get("replay_summary", "").strip()
        details = api_response.get("replay_details", "").strip()
        conclusion = api_response.get("replay_conclusion", "").strip()
        confidence = api_response.get("confidence_score")
        
        # Validate required fields are present
        if not summary:
            raise ValueError("Claude response missing replay_summary")
        if not details:
            raise ValueError("Claude response missing replay_details")
        if not conclusion:
            raise ValueError("Claude response missing replay_conclusion")
        
        # Validate confidence
        try:
            conf_float = float(confidence or 0.0)
            if not (0.0 <= conf_float <= 1.0):
                raise ValueError(f"Confidence out of range: {conf_float}")
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid confidence_score: {confidence}") from e
        
        logger.info(
            f"AIResultMapper: Mapped Claude response "
            f"(summary_len={len(summary)}, confidence={conf_float})"
        )
        
        return {
            "replay_summary": summary,
            "replay_details": details,
            "replay_conclusion": conclusion,
            "confidence_score": conf_float
        }
    
