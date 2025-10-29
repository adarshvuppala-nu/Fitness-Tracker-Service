from fastapi import APIRouter

from app.api.v1 import users, workouts, goals, progress, ai, analytics

api_router = APIRouter()

# Day 1: Core CRUD endpoints
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(workouts.router, prefix="/workout-sessions", tags=["Workout Sessions"])
api_router.include_router(goals.router, prefix="/fitness-goals", tags=["Fitness Goals"])
api_router.include_router(progress.router, prefix="/progress-metrics", tags=["Progress Metrics"])

# Day 2: AI Agent endpoints
api_router.include_router(ai.router, prefix="/ai", tags=["AI Assistant"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
