"""
Create FastAPI route for POST /incidents.

Requirements:
- Use APIRouter
- Accept IncidentCreate request body
- Call controller to create incident
- Return IncidentResponse
- Set HTTP status code 201

"""

import os
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.models.incident import IncidentCreate, IncidentResponse
from app.controllers.incident_controller import create_incident, get_incident_by_id, get_all_incidents
from app.db.dependencies import get_db



#before every route the is a /incidents prefix 
#the tags is used for swagger documentation grouping
router = APIRouter(prefix="/incidents", tags=["incidents"])
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

@router.get("/debug/ai")
def debug_ai():
    return {
        "AI_ENABLED_RAW": os.getenv("AI_ENABLED"),
        "AI_PROVIDER_RAW": os.getenv("AI_PROVIDER"),
        "CLAUDE_API_KEY_SET": bool(os.getenv("CLAUDE_API_KEY")),
        "AI_VALIDATION": {
            "ai_enabled": os.getenv("AI_ENABLED", "").lower() == "true",
            "provider_valid": os.getenv("AI_PROVIDER", "").lower() == "claude",
            "api_key_present": bool(os.getenv("CLAUDE_API_KEY")),
        }
    }

