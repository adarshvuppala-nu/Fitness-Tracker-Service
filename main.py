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

# Configure CORS - restrict to known origins for security
# For production, update with your actual domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "http://localhost:3001",  # Vite dev server (alternate port)
        "http://localhost:5173",  # Vite dev server
        # Add production domain here: "https://yourdomain.com"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
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
    # This must be registered AFTER all API routes to avoid conflicts
    from fastapi import Request
    from fastapi.exceptions import HTTPException

    @app.exception_handler(404)
    async def custom_404_handler(request: Request, exc: HTTPException):
        """
        Custom 404 handler that serves the SPA for non-API routes.
        API routes get normal 404 JSON responses.
        """
        # If it's an API request, return JSON 404
        if request.url.path.startswith("/api/"):
            return exc

        # For all other routes, serve the React SPA
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
