import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api.v1 import api_router
from app.core.config import settings
from app.core.database import engine
from app.models.base import Base

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes first (higher priority)
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

# Determine if we're running in production (with built frontend)
STATIC_DIR = Path(__file__).parent / "app" / "static"
STATIC_EXISTS = STATIC_DIR.exists() and (STATIC_DIR / "index.html").exists()

# Mount static files only if they exist (Docker deployment)
if STATIC_EXISTS:
    # Mount static assets (JS, CSS, images, etc.)
    app.mount("/assets", StaticFiles(directory=STATIC_DIR / "assets"), name="assets")

    # Serve any other static files from the static directory
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    @app.get("/")
    async def serve_frontend():
        """Serve the React frontend index.html"""
        return FileResponse(STATIC_DIR / "index.html")

    # Catch-all route for React Router (SPA support)
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        """
        Catch-all route to serve React SPA for client-side routing.
        Returns index.html for any route that doesn't match /api/v1/*
        """
        # Don't catch API routes
        if full_path.startswith("api/"):
            return {"detail": "Not Found"}

        # Check if the requested file exists in static directory
        file_path = STATIC_DIR / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)

        # Otherwise, serve index.html for client-side routing
        return FileResponse(STATIC_DIR / "index.html")
else:
    # Development mode - API only
    @app.get("/")
    def root():
        return {
            "message": "Fitness Tracker API",
            "version": settings.VERSION,
            "docs": f"{settings.API_V1_PREFIX}/docs",
            "note": "Frontend not built. Run 'cd frontend && npm run build' to build frontend."
        }


@app.on_event("startup")
def startup_event():
    if STATIC_EXISTS:
        print(f"✓ Serving frontend from {STATIC_DIR}")
    else:
        print(f"✗ Frontend not found at {STATIC_DIR}")
        print("  Running in API-only mode")


@app.on_event("shutdown")
def shutdown_event():
    pass
