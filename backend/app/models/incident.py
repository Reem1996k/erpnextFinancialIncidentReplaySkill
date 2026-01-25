"""
Create Pydantic models for Incident API.

Models:
1. IncidentCreate:
   - erp_reference: string
   - incident_type: string
   - description: string

2. IncidentResponse:
   - id: int
   - erp_reference: string
   - incident_type: string
   - status: string
   - description: string
   - created_at: datetime


"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class IncidentCreate(BaseModel):
    """Schema for creating a new incident."""
    erp_reference: str
    incident_type: str
    description: str


class IncidentResponse(BaseModel):
    """ Extend IncidentResponse to include replay fields:
- replay_summary
- replay_details
- replay_conclusion
- replayed_at
All fields should be optional.
"""
    """Schema for incident API response."""
    id: int
    erp_reference: str
    incident_type: str
    status: str
    description: str
    created_at: datetime
    replay_summary: Optional[str] = None
    replay_details: Optional[str] = None
    replay_conclusion: Optional[str] = None
    replayed_at: Optional[datetime] = None
    #config is a part of the pydantic this helps to convert the orm object to pydantic model (json serializable)
    class Config:
        from_attributes = True