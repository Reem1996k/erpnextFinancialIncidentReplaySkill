"""
Build a FastAPI application skeleton.

Requirements:
- Create a FastAPI app instance
- Health check endpoint: GET /health
- No business logic
- Ready for future routers
- Clean, minimal, production-ready structure
"""
import os
import sys

cwd = os.getcwd() + "/backend"
if cwd not in sys.path:
    sys.path.insert(0, cwd)
# Initialize database on startup
# Import Base and engine and create all tables

from dotenv import load_dotenv #env loader
from pathlib import Path

# Load .env from backend directory
backend_dir = Path(__file__).parent.parent
env_path = backend_dir / ".env"
load_dotenv(dotenv_path=env_path)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware #give access to frontend apps
from app.db.database import Base, engine
# Import models to register them with SQLAlchemy
from app.api.incidents import router as incidents_router

# Try to import UI router, but don't fail if templates are missing
from app.api.analysis import router as analysis_router

#these metadata are used to generate swagger documentation
app = FastAPI(
    title="ERPNext Financial Incident Replay",
    description="API for replaying financial incidents in ERPNext",
    version="1.0.0"
)

# Add CORS middleware
#connect frontend apps to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create all database tables on startup
Base.metadata.create_all(bind=engine)

# Include routers
#connect all the  endpoints to the main app
app.include_router(incidents_router)
app.include_router(analysis_router)

@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)