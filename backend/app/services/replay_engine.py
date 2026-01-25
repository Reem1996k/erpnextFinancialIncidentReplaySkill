"""
Create a ReplayEngine service.

Requirements:
- Function analyze_incident(incident)
- Behavior depends on incident_type
- For Pricing_Issue:
  - Assume expected amount is 5000
  - Assume invoice amount is 5750
  - Calculate percentage difference
  - If difference <= 20%, decision is APPROVED_WITH_RISK
  - Return structured analysis:
    summary, details, conclusion
- Return a dictionary with:
  summary, details, conclusion, decision
"""

from typing import Dict, Any
from app.db.models import Incident


class ReplayEngine:
    """Service for analyzing financial incidents."""
    
    @staticmethod
    def analyze_incident(incident: Incident) -> Dict[str, Any]:
        """
        Analyze an incident based on its type.
        
        Args:
            incident: The Incident object to analyze
        
        Returns:
            Dictionary containing summary, details, conclusion, and decision
        """
        if incident.incident_type == "Pricing_Issue":
            return ReplayEngine._analyze_pricing_issue(incident)
        else:
            return ReplayEngine._analyze_generic(incident)
    
    @staticmethod
    def _analyze_pricing_issue(incident: Incident) -> Dict[str, Any]:
        """
        Analyze a pricing issue incident.
        
        Args:
            incident: The Incident object
        
        Returns:
            Analysis dictionary
        """
        # Define baseline values
        expected_amount = 5000
        invoice_amount = 5750
        
        # Calculate percentage difference
        difference = invoice_amount - expected_amount
        percentage_difference = (difference / expected_amount) * 100
        
        # Determine decision based on percentage
        if percentage_difference <= 20:
            decision = "APPROVED_WITH_RISK"
        else:
            decision = "REJECTED"
        
        summary = f"Invoice exceeds expected amount by {percentage_difference:.1f}%"
        details = (
            f"Expected amount: ${expected_amount:,.2f}\n"
            f"Invoice amount: ${invoice_amount:,.2f}\n"
            f"Difference: ${difference:,.2f} ({percentage_difference:.1f}%)"
        )
        conclusion = (
            f"Decision: {decision}. "
            f"The invoice amount is within acceptable variance threshold (20%). "
            f"Requires manual review for compliance."
        )
        
        return {
            "summary": summary,
            "details": details,
            "conclusion": conclusion,
            "decision": decision
        }
    
    @staticmethod
    def _analyze_generic(incident: Incident) -> Dict[str, Any]:
        """
        Analyze a generic incident.
        
        Args:
            incident: The Incident object
        
        Returns:
            Analysis dictionary
        """
        return {
            "summary": f"Analysis for {incident.incident_type}",
            "details": incident.description,
            "conclusion": "Generic analysis completed. Manual review recommended.",
            "decision": "PENDING_REVIEW"
        }
