"""
Create a controller function to create a new Incident.

Requirements:
- Accept IncidentCreate schema
- Create Incident SQLAlchemy object
- Set status to "OPEN"
- Save to database using SQLAlchemy session
- Return the created Incident

"""

from datetime import datetime
from sqlalchemy.orm import Session
from app.db.models import Incident
from app.models.incident import IncidentCreate
from app.services.replay_engine import ReplayEngine
from fastapi import HTTPException, status


def create_incident(incident_data: IncidentCreate, db: Session) -> Incident:
    """
    Create a new incident in the database.
    
    Args:
        incident_data: IncidentCreate schema with incident details
        db: SQLAlchemy database session
    
    Returns:
        Created Incident object
    """
    existing = (
        db.query(Incident)
        .filter(Incident.erp_reference == incident_data.erp_reference)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Incident with ERP reference '{incident_data.erp_reference}' already exists"
        )
    db_incident = Incident(
        erp_reference=incident_data.erp_reference,
        incident_type=incident_data.incident_type,
        description=incident_data.description,
        status="OPEN"
    )
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident


def get_incident_by_id(incident_id: int, db: Session) -> Incident | None:
    """
    Get an incident by ID from the database.
    
    Args:
        incident_id: The ID of the incident to retrieve
        db: SQLAlchemy database session
    
    Returns:
        Incident object if found, None otherwise
    """
    return db.query(Incident).filter(Incident.id == incident_id).first()


def get_all_incidents(db: Session) -> list[Incident]:
    """
    Get all incidents from the database.
    
    Args:
        db: SQLAlchemy database session
    
    Returns:
        List of all Incident objects
    """
    return db.query(Incident).all()


def run_replay_for_incident(incident_id: int, db: Session) -> Incident | None:
    """
    Run replay analysis for an incident.
    
    Args:
        incident_id: The ID of the incident to replay
        db: SQLAlchemy database session
    
    Returns:
        Updated Incident object if found, None otherwise
    """
    incident = get_incident_by_id(incident_id, db)
    if incident is None:
        return None
    
    # Initialize ReplayEngine (it will handle ERP client selection via factory)
    replay_engine = ReplayEngine()
    
    # Use ReplayEngine to analyze the incident
    analysis = replay_engine.analyze_incident(incident)
    
    # Populate replay fields from analysis
    incident.replay_summary = analysis["summary"]
    incident.replay_details = analysis["details"]
    incident.replay_conclusion = analysis["conclusion"]
    incident.status = "ANALYZED"
    incident.replayed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(incident)
    return incident


