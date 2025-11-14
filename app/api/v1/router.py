from fastapi import APIRouter

from app.api.v1 import users, workouts, goals, progress, ai, analytics, health

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(workouts.router, prefix="/workouts", tags=["Workouts"])
api_router.include_router(goals.router, prefix="/goals", tags=["Goals"])
api_router.include_router(progress.router, prefix="/progress", tags=["Progress"])
api_router.include_router(ai.router, prefix="/ai", tags=["AI Assistant"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
