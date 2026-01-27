"""
UI Router for HTML rendering using Jinja2 templates.

Provides HTML views for incident details and analysis results.
"""

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.controllers.incident_controller import get_incident_by_id

# Initialize Jinja2 environment with template directory
jinja_env = Environment(loader=FileSystemLoader("app/templates"))

# Create router with /ui prefix
router = APIRouter(prefix="/ui", tags=["ui"])


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/incidents/{incident_id}", response_class=HTMLResponse)
def get_incident_ui(incident_id: int, db: Session = Depends(get_db)):
    """
    Render incident details as HTML page.
    
    Args:
        incident_id: ID of the incident to display
        db: Database session dependency
    
    Returns:
        HTML response with incident details
    
    Raises:
        HTTPException: 404 if incident not found
    """
    # Fetch incident from database
    incident = get_incident_by_id(incident_id, db)
    
    # If not found, raise 404 error
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    # Load and render template
    template = jinja_env.get_template("incident_replay.html")
    html = template.render(incident=incident)
    
    return HTMLResponse(content=html)
