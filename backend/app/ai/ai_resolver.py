"""
AI Resolver - Call Claude API and return result (no merging).

ARCHITECTURE RULE: This resolver ONLY calls AI.
- Does NOT merge with rules
- Does NOT have fallback logic
- On error → raises exception (controller catches)
- Returns clean AI response or failure status
"""

import logging
from typing import Dict, Any, Optional
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
    
    def _run_rule_analysis(self, incident: Incident) -> Dict[str, Any]:
        """
        Run the rule-based analyzer for the incident type.
        
        Args:
            incident: Incident to analyze
        
        Returns:
            Rule analysis result
        """
        try:
            analyzer = IncidentAnalyzerFactory.get_analyzer(
                incident.incident_type
            )
            analysis = analyzer.analyze(incident)
            return {
                "decision": analysis.decision,
                "summary": analysis.summary,
                "details": analysis.details,
                "conclusion": analysis.conclusion,
                "confidence": analysis.confidence,
                "source": "RULE"
            }
        except Exception as e:
            return {
                "decision": "UNDETERMINED",
                "summary": "Rule analyzer failed",
                "details": str(e),
                "conclusion": "Manual review needed",
                "confidence": 0.0,
                "source": "RULE_FAILED"
            }
    
    def _run_ai_analysis(
        self,
        incident: Incident,
        erp_data: Dict[str, Any],
        rule_analysis: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Run AI analysis for additional insights.
        
        Args:
            incident: Incident to analyze
            erp_data: ERP context data
            rule_analysis: Rule-based analysis for context
        
        Returns:
            AI analysis result, or None if AI fails
        """
        try:
            if not self.ai_client or not self.ai_client.is_available():
                return None
            
            # Build comprehensive prompt with context
            invoice = erp_data.get("invoice", {})
            sales_order = erp_data.get("sales_order", {})
            incident_description = incident.description or ""
            
            prompt = build_financial_analysis_prompt(
                invoice=invoice,
                sales_order=sales_order,
                incident_description=incident_description
            )
            
            # Call AI client
            ai_response = self.ai_client.analyze(prompt)
            
            return {
                "root_cause": ai_response.get("root_cause", ""),
                "recommended_actions": ai_response.get("recommended_actions", []),
                "customer_message": ai_response.get("customer_message", ""),
                "confidence": float(ai_response.get("confidence_score", 0.0)),
                "source": "AI",
                "raw_response": ai_response
            }
        
        except Exception as e:
            # AI analysis failed, but don't break - we have rules as fallback
            return {
                "error": str(e),
                "source": "AI_FAILED",
                "confidence": 0.0
            }
    
    def _merge_analyses(
        self,
        rule_analysis: Dict[str, Any],
        ai_analysis: Optional[Dict[str, Any]],
        incident: Incident
    ) -> Dict[str, Any]:
        """
        Merge rule and AI analyses into final resolution.
        
        Logic:
        - If rule confidence >= 0.85, trust rules (AI is supplementary)
        - If rule confidence < 0.85 and AI succeeded, prefer AI
        - If both failed, return manual review
        
        Args:
            rule_analysis: Rule-based analysis result
            ai_analysis: AI analysis result (may be None)
            incident: Original incident
        
        Returns:
            Merged resolution with metadata
        """
        # Determine which analysis to prioritize
        use_ai = (
            ai_analysis and
            ai_analysis.get("source") == "AI" and
            ai_analysis.get("confidence", 0.0) > rule_analysis.get("confidence", 0.0)
        )
        
        if use_ai:
            # AI has higher confidence - use it
            primary = ai_analysis
            analysis_source = "AI"
            confidence = ai_analysis.get("confidence", 0.0)
        else:
            # Use rule analysis (it's reliable or AI failed)
            primary = rule_analysis
            analysis_source = "RULE"
            confidence = rule_analysis.get("confidence", 0.0)
        
        # Build final resolution
        resolution = {
            "summary": primary.get("summary", ""),
            "details": primary.get("details", ""),
            "conclusion": primary.get("conclusion", ""),
            "decision": primary.get("decision", "UNDETERMINED"),
            "analysis_source": analysis_source,
            "confidence": confidence,
            "analyzed_at": datetime.utcnow().isoformat()
        }
        
        # Add AI insights if available (for transparency)
        if ai_analysis and ai_analysis.get("source") == "AI":
            resolution["ai_insights"] = {
                "root_cause": ai_analysis.get("root_cause", ""),
                "recommended_actions": ai_analysis.get("recommended_actions", []),
                "customer_message": ai_analysis.get("customer_message", ""),
                "confidence": ai_analysis.get("confidence", 0.0)
            }
        
        return resolution
