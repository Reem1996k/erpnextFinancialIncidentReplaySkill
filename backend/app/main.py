"""
Build a FastAPI application skeleton.

Requirements:
- Create a FastAPI app instance
- Health check endpoint: GET /health
- No business logic
- Ready for future routers
- Clean, minimal, production-ready structure
"""
# Initialize database on startup
# Import Base and engine and create all tables

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.db.database import Base, engine
from app.api.incidents import router as incidents_router
app = FastAPI(
    title="ERPNext Financial Incident Replay",
    description="API for replaying financial incidents in ERPNext",
    version="1.0.0"
)

# Create all database tables on startup
Base.metadata.create_all(bind=engine)

app.include_router(incidents_router)

@app.get("/health")
def health():
    return {"status": "ok"}
