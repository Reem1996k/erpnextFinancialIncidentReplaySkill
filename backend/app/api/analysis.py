"""
Incident Analysis API Endpoint

Provides endpoint to trigger incident analysis with ERP data extraction.
"""

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
import logging
from app.db.database import SessionLocal
from app.db.models import Incident
from app.controllers.incident_controller import resolve_incident

logger = logging.getLogger(__name__)
router = APIRouter(tags=["analysis"])


def get_db():
    """Dependency for database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/incidents/{incident_id}/analyze")
def analyze_incident(incident_id: int, db: Session = Depends(get_db)):
    """
    Trigger complete analysis for an incident.
    
    - Extracts ERP data (Invoice + Sales Order)
    - Runs rule-based or AI analysis based on configuration
    - Saves results
    
    Returns: Updated incident with analysis results
    """
    try:
        incident = db.query(Incident).filter(Incident.id == incident_id).first()
        
        if not incident:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Incident {incident_id} not found"
            )

        # Use the controller function to resolve/analyze the incident
        updated_incident = resolve_incident(incident_id, db)
        
        if updated_incident is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Incident {incident_id} not found after analysis"
            )
        
        return {
            "success": True,
            "incident_id": incident_id,
            "incident": {
                "id": updated_incident.id,
                "erp_reference": updated_incident.erp_reference,
                "status": updated_incident.status,
                "analysis_source": updated_incident.analysis_source,
                "confidence_score": updated_incident.confidence_score,
                "replay_summary": updated_incident.replay_summary,
                "replay_conclusion": updated_incident.replay_conclusion
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Analysis error for incident {incident_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


