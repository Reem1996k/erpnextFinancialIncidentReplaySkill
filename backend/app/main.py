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
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.db.database import Base, engine
from app.api.incidents import router as incidents_router
from app.ui.router import router as ui_router


app = FastAPI(
    title="ERPNext Financial Incident Replay",
    description="API for replaying financial incidents in ERPNext",
    version="1.0.0"
)

# Add CORS middleware
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
app.include_router(incidents_router)
app.include_router(ui_router)

@app.get("/health")
def health():
    return {"status": "ok"}
