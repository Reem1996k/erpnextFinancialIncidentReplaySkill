"""
AI Resolver - Call Claude API and return result (no merging).

ARCHITECTURE RULE: This resolver ONLY calls AI.
- Does NOT merge with rules
- Does NOT have fallback logic
- On error → raises exception (controller catches)
- Returns clean AI response or failure status
"""

import logging
from typing import Dict, Any
from app.db.models import Incident
from app.ai.ai_client_base import AIClientBase
from app.ai.prompt_builder_financial import build_financial_analysis_prompt
from app.ai.ai_result_mapper import AIResultMapper

logger = logging.getLogger(__name__)


class AIResolver:
    """
    Calls Claude API for incident analysis.
    
    Does NOT:
    - Merge with rule results
    - Have fallback logic
    - Make decisions about which analysis is "better"
    
    Does:
    - Build prompt from ERP data
    - Call AI client
    - Map response to standard format
    - Raise exceptions on failure (let controller handle)
    """
    
    def __init__(self, ai_client: AIClientBase):
        """
        Initialize resolver with AI client.
        
        Args:
            ai_client: AIClientAnthropic instance (required, not optional)
        """
        self.ai_client = ai_client
        if not ai_client:
            raise ValueError("AIResolver requires ai_client (cannot be None)")
    #in use
    def resolve_incident(
        self,
        incident: Incident,
        erp_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Call Claude API for incident analysis.
        
        CRITICAL: Raises exception on ANY failure. No fallback.
        
        Args:
            incident: Incident object
            erp_data: ERP context (invoice, SO, customer)
        
        Returns:
            Mapped AI response:
            {
                "replay_summary": str,
                "replay_details": str,
                "replay_conclusion": str,
                "confidence_score": float,
                "analysis_source": "AI"
            }
        
        Raises:
            RuntimeError: On ANY API failure or response parsing error
            ValueError: On invalid response from Claude
        """
        logger.info(
            f"AIResolver: Building prompt for incident {incident.id} "
            f"(type: {incident.incident_type})"
        )
        
        # Step 1: Build prompt with ERP data
        # Extract invoice and sales order from erp_data
        invoice = erp_data.get("invoice", {})
        sales_order = erp_data.get("sales_order", {})
        incident_description = incident.description or ""
        
        prompt = build_financial_analysis_prompt(
            invoice=invoice,
            sales_order=sales_order,
            incident_description=incident_description
        )
        
        logger.debug(f"Prompt built: {len(prompt)} chars")
        
        # Step 2: Call Claude API (NO try-catch, let exception propagate)
        logger.info(f"AIResolver: Calling Claude API for incident {incident.id}")
        ai_response = self.ai_client.analyze(prompt)
        
        logger.info(f"AIResolver: Claude returned response")
        logger.debug(f"Claude response: {ai_response}")
        
        # Step 3: Map response using AIResultMapper
        logger.info(f"AIResolver: Mapping Claude response")
        mapped_result = AIResultMapper.map_ai_response(ai_response)
        
        logger.info(
            f"AIResolver: Analysis complete - confidence={mapped_result.get('confidence_score')}"
        )
        
        return mapped_result
    
   