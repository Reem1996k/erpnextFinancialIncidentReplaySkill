"""
Create FastAPI route for POST /incidents.

Requirements:
- Use APIRouter
- Accept IncidentCreate request body
- Call controller to create incident
- Return IncidentResponse
- Set HTTP status code 201

"""

from fastapi import APIRouter, Depends, status, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.models.incident import IncidentCreate, IncidentResponse
from app.controllers.incident_controller import create_incident, get_incident_by_id, run_replay_for_incident
from app.db.database import SessionLocal
import os

# Set up templates
templates_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
templates = Jinja2Templates(directory=templates_dir)
#before every route the is a /incidents prefix 
#the tags is used for swagger documentation grouping
router = APIRouter(prefix="/incidents", tags=["incidents"])

# UI Router for HTML responses
ui_router = APIRouter(prefix="/ui/incidents", tags=["ui"])


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
    
    Args:
        incident_id: The ID of the incident to replay
        db: Database session (injected)
    
    Returns:
        Updated incident with replay analysis results
    
    Raises:
        HTTPException: 404 if incident not found
    """
    db_incident = run_replay_for_incident(incident_id, db)
    if db_incident is None:
        raise HTTPException(status_code=404, detail=f"Incident {incident_id} not found")
    return db_incident


@ui_router.get("/{incident_id}", response_class=HTMLResponse)
async def view_incident_replay(
    incident_id: int,
    request: Request,
    db: Session = Depends(get_db)
) -> str:
    """
    Display incident replay analysis in HTML format.
    
    Args:
        incident_id: The ID of the incident to display
        request: The HTTP request object
        db: Database session (injected)
    
    Returns:
        Rendered HTML template with incident details
    
    Raises:
        HTTPException: 404 if incident not found
    """
    db_incident = get_incident_by_id(incident_id, db)
    if db_incident is None:
        raise HTTPException(status_code=404, detail=f"Incident {incident_id} not found")
    
    return templates.TemplateResponse("incident_replay.html", {
        "request": request,
        "incident": db_incident
    })
