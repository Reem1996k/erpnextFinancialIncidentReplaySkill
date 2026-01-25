# Define the Incident model using SQLAlchemy ORM
# Table name: incidents
# Fields:
# - id (primary key)
# - erp_reference (string)
# - incident_type (string)
# - status (string)
# - created_at (datetime)

"""
Add replay-related fields to the Incident model:
- replay_summary (string, nullable)
- replay_details (string, nullable)
- replay_conclusion (string, nullable)
- replayed_at (datetime, nullable)
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.db.database import Base


class Incident(Base):
    __tablename__ = "incidents"
    
    id = Column(Integer, primary_key=True, index=True)
    erp_reference = Column(String, unique=True, index=True)
    incident_type = Column(String)
    status = Column(String)
    description = Column(String)
    replay_summary = Column(String, nullable=True)
    replay_details = Column(String, nullable=True)
    replay_conclusion = Column(String, nullable=True)
    replayed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)