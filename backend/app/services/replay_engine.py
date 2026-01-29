"""
Replay Engine service for analyzing financial incidents (RULE-BASED ONLY).

ARCHITECTURE RULE: ReplayEngine ONLY does rule-based analysis.
- No AI fallback (AI is handled separately via AIResolver)
- Pure deterministic analysis
- Returns AnalysisResult with decision, confidence, and reasoning

This keeps rule engine independent from AI.
"""

from typing import Dict, Any, Optional
import logging
from app.db.models import Incident
from app.integrations.erpnext_client_base import BaseERPNextClient
from app.integrations.client_factory import get_erp_client
from app.services.incident_analyzers import IncidentAnalyzerFactory, AnalysisResult

logger = logging.getLogger(__name__)


class ReplayEngine:
    """
    Rule-based incident analyzer (NO AI).
    
    This class orchestrates ONLY rule-based incident analysis:
    1. Fetch ERP data
    2. Select analyzer for incident type
    3. Run deterministic rules
    4. Return result (even if UNDETERMINED - no fallback)
    
    For AI analysis, use AIResolver separately in controller.
    """
    
    def __init__(
        self, 
        erp_client: Optional[BaseERPNextClient] = None
    ):
        """
        Initialize ReplayEngine with ERP client.
        
        Args:
            erp_client: ERP client implementation.
                If None, automatically selected based on ERP_CLIENT_MODE env var.
        """
        self.erp_client = erp_client if erp_client is not None else get_erp_client()
    
    def analyze_incident(self, incident: Incident) -> Dict[str, Any]:
        """
        Analyze incident using RULE-BASED ANALYSIS ONLY.
        
        No AI, no fallback. Pure deterministic rules.
        
        Args:
            incident: The Incident object to analyze
        
        Returns:
            Dictionary containing analysis results:
            {
                "summary": str,
                "details": str,
                "conclusion": str,
                "confidence": float,
                "analysis_source": "RULE"
            }
        """
        try:
            logger.info(f"ReplayEngine: Analyzing incident {incident.id} (RULE-BASED ONLY)")
            
            # Run rule-based analysis
            rule_result = self._run_rule_based_analysis(incident)
            
            logger.info(
                f"ReplayEngine: Analysis complete - "
                f"decision={rule_result.decision}, confidence={rule_result.confidence}"
            )
            
            return rule_result.to_dict()
        
        except Exception as e:
            logger.error(f"ReplayEngine: Error analyzing incident {incident.id}: {e}")
            # Return error result (not undetermined, explicit error)
            from app.services.incident_analyzers import AnalysisResult
            return AnalysisResult(
                decision="UNDETERMINED",
                summary="Rule analysis error",
                details=f"Error: {str(e)}",
                conclusion="Manual review required",
                confidence=0.0,
                analysis_source="RULE"
            ).to_dict()
    
    def _run_rule_based_analysis(self, incident: Incident) -> AnalysisResult:
        """
        Run rule-based analyzer for incident type.
        
        Args:
            incident: Incident to analyze
        
        Returns:
            AnalysisResult (may be UNDETERMINED if rules don't apply)
        """
        try:
            logger.info(
                f"ReplayEngine._run_rule_based_analysis: "
                f"Incident {incident.id}, type={incident.incident_type}"
            )
            
            # Get analyzer for incident type
            analyzer = IncidentAnalyzerFactory.get_analyzer(
                incident.incident_type,
                self.erp_client
            )
            
            if analyzer is None:
                logger.warning(
                    f"ReplayEngine: No analyzer for type '{incident.incident_type}'"
                )
                return AnalysisResult(
                    decision="UNDETERMINED",
                    summary=f"Unknown incident type: {incident.incident_type}",
                    details=f"No rule-based analyzer for type '{incident.incident_type}'",
                    conclusion="Manual review required",
                    confidence=0.0,
                    analysis_source="RULE"
                )
            
            # Run analyzer
            logger.info(f"ReplayEngine: Running analyzer for incident {incident.id}")
            result = analyzer.analyze(incident)
            return result
        
        except Exception as e:
            logger.error(
                f"ReplayEngine: Error in _run_rule_based_analysis: {e}", 
                exc_info=True
            )
            return AnalysisResult(
                decision="UNDETERMINED",
                summary="Rule-based analysis error",
                details=f"Error during rule analysis: {str(e)}",
                conclusion="Manual review required",
                confidence=0.0,
                analysis_source="RULE"
            )
