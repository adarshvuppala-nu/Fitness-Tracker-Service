from fastapi import APIRouter

from app.api.v1 import users, workouts, goals, progress

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(workouts.router, prefix="/workout-sessions", tags=["Workout Sessions"])
api_router.include_router(goals.router, prefix="/fitness-goals", tags=["Fitness Goals"])
api_router.include_router(progress.router, prefix="/progress-metrics", tags=["Progress Metrics"])
