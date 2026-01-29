"""
Create FastAPI route for POST /incidents.

Requirements:
- Use APIRouter
- Accept IncidentCreate request body
- Call controller to create incident
- Return IncidentResponse
- Set HTTP status code 201

"""

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.models.incident import IncidentCreate, IncidentResponse
from app.controllers.incident_controller import create_incident, get_incident_by_id, run_replay_for_incident, get_all_incidents, resolve_incident
from app.db.database import SessionLocal


#before every route the is a /incidents prefix 
#the tags is used for swagger documentation grouping
router = APIRouter(prefix="/incidents", tags=["incidents"])


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#response_model is a decorator parameter that helps to convert the orm object to pydantic model (json serializable)
@router.post("/", response_model=IncidentResponse, status_code=status.HTTP_201_CREATED)
async def create_new_incident(
    incident: IncidentCreate,
    db: Session = Depends(get_db)
) -> IncidentResponse:
    """
    Create a new incident.
    
    Args:
        incident: Incident data from request body
        db: Database session (injected)
    
    Returns:
        Created incident with HTTP 201 status
    """
    db_incident = create_incident(incident, db)
    return db_incident


@router.get("/", response_model=list[IncidentResponse])
async def list_incidents(
    db: Session = Depends(get_db)
) -> list[IncidentResponse]:
    """
    Get all incidents.
    
    Args:
        db: Database session (injected)
    
    Returns:
        List of all incidents
    """
    incidents = get_all_incidents(db)
    return incidents


@router.get("/{incident_id}", response_model=IncidentResponse)
async def get_incident(
    incident_id: int,
    db: Session = Depends(get_db)
) -> IncidentResponse:
    """
    Get an incident by ID.
    
    Args:
        incident_id: The ID of the incident to retrieve
        db: Database session (injected)
    
    Returns:
        Incident details if found
    
    Raises:
        HTTPException: 404 if incident not found
    """
    db_incident = get_incident_by_id(incident_id, db)
    if db_incident is None:
        raise HTTPException(status_code=404, detail=f"Incident {incident_id} not found")
    return db_incident


@router.post("/{incident_id}/replay", response_model=IncidentResponse, status_code=status.HTTP_200_OK)
async def replay_incident(
    incident_id: int,
    db: Session = Depends(get_db)
) -> IncidentResponse:
    """
    Run replay analysis for an incident.
    Uses rule-based or AI analysis depending on configuration.
    """
    incident = run_replay_for_incident(incident_id, db)
    if incident is None:
        raise HTTPException(status_code=404, detail=f"Incident {incident_id} not found")
    return incident
