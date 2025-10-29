"""Advanced Analytics API Endpoints"""

from typing import Optional, List, Dict, Any
from datetime import datetime, date, timedelta
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel

from app.api.deps import get_db
from app import crud, models

router = APIRouter()


class AnalyticsResponse(BaseModel):
    total_workouts: int
    total_duration: int
    total_calories: float
    avg_duration: float
    avg_calories: float
    workout_by_type: Dict[str, int]
    weekly_trend: List[Dict[str, Any]]
    streak: int
    achievements: List[Dict[str, str]]


class WorkoutStreak(BaseModel):
    current_streak: int
    longest_streak: int
    last_workout_date: Optional[str]


@router.get("/analytics/{user_id}", response_model=AnalyticsResponse)
def get_user_analytics(
    user_id: str,
    days: int = 30,
    db: Session = Depends(get_db)
):
    """
    Get comprehensive analytics for a user
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    start_date = date.today() - timedelta(days=days)
    workouts = crud.workout.get_by_user(
        db, user_id=user_id, date_from=start_date, skip=0, limit=1000
    )

    total_workouts = len(workouts)
    total_duration = sum(w.duration for w in workouts)
    total_calories = sum(w.calories_burned for w in workouts)

    avg_duration = total_duration / total_workouts if total_workouts > 0 else 0
    avg_calories = total_calories / total_workouts if total_workouts > 0 else 0

    workout_by_type = {}
    for w in workouts:
        workout_by_type[w.type] = workout_by_type.get(w.type, 0) + 1

    weekly_trend = calculate_weekly_trend(workouts)
    streak = calculate_streak(workouts)
    achievements = calculate_achievements(workouts)

    return AnalyticsResponse(
        total_workouts=total_workouts,
        total_duration=total_duration,
        total_calories=total_calories,
        avg_duration=round(avg_duration, 2),
        avg_calories=round(avg_calories, 2),
        workout_by_type=workout_by_type,
        weekly_trend=weekly_trend,
        streak=streak,
        achievements=achievements
    )


@router.get("/streak/{user_id}", response_model=WorkoutStreak)
def get_workout_streak(user_id: str, db: Session = Depends(get_db)):
    """
    Calculate current and longest workout streak
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    workouts = crud.workout.get_by_user(db, user_id=user_id, skip=0, limit=1000)

    if not workouts:
        return WorkoutStreak(current_streak=0, longest_streak=0, last_workout_date=None)

    workout_dates = sorted(set(w.date for w in workouts), reverse=True)

    current_streak = 0
    longest_streak = 0
    temp_streak = 1

    for i, workout_date in enumerate(workout_dates):
        if i == 0:
            if workout_date >= date.today() - timedelta(days=1):
                current_streak = 1
        else:
            diff = (workout_dates[i-1] - workout_date).days
            if diff == 1:
                temp_streak += 1
                if i <= len(workout_dates) - 1 and current_streak > 0:
                    current_streak = temp_streak
            else:
                longest_streak = max(longest_streak, temp_streak)
                temp_streak = 1

    longest_streak = max(longest_streak, temp_streak, current_streak)

    return WorkoutStreak(
        current_streak=current_streak,
        longest_streak=longest_streak,
        last_workout_date=str(workout_dates[0]) if workout_dates else None
    )


@router.get("/export/{user_id}")
def export_user_data(user_id: str, db: Session = Depends(get_db)):
    """
    Export user data as CSV format
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    workouts = crud.workout.get_by_user(db, user_id=user_id, skip=0, limit=10000)

    csv_lines = ["Date,Type,Duration (min),Calories,Notes"]
    for workout in workouts:
        csv_lines.append(
            f"{workout.date},{workout.type},{workout.duration},"
            f"{workout.calories_burned},{workout.notes or ''}"
        )

    return {
        "user_id": user_id,
        "username": user.username,
        "total_records": len(workouts),
        "csv_data": "\n".join(csv_lines)
    }


def calculate_weekly_trend(workouts: List) -> List[Dict[str, Any]]:
    """Calculate weekly workout trends"""
    weekly_data = {}

    for workout in workouts:
        week_start = workout.date - timedelta(days=workout.date.weekday())
        week_key = week_start.strftime("%Y-%m-%d")

        if week_key not in weekly_data:
            weekly_data[week_key] = {"count": 0, "calories": 0, "duration": 0}

        weekly_data[week_key]["count"] += 1
        weekly_data[week_key]["calories"] += workout.calories_burned
        weekly_data[week_key]["duration"] += workout.duration

    return [
        {
            "week": week,
            "workouts": data["count"],
            "calories": round(data["calories"], 2),
            "duration": data["duration"]
        }
        for week, data in sorted(weekly_data.items())[-8:]
    ]


def calculate_streak(workouts: List) -> int:
    """Calculate current workout streak"""
    if not workouts:
        return 0

    workout_dates = sorted(set(w.date for w in workouts), reverse=True)

    streak = 0
    expected_date = date.today()

    for workout_date in workout_dates:
        if workout_date == expected_date or workout_date == expected_date - timedelta(days=1):
            streak += 1
            expected_date = workout_date - timedelta(days=1)
        else:
            break

    return streak


def calculate_achievements(workouts: List) -> List[Dict[str, str]]:
    """Calculate user achievements based on workout data"""
    achievements = []

    total_workouts = len(workouts)
    total_calories = sum(w.calories_burned for w in workouts)
    workout_types = set(w.type for w in workouts)

    if total_workouts >= 10:
        achievements.append({"title": "Dedicated", "description": "10+ workouts completed"})
    if total_workouts >= 50:
        achievements.append({"title": "Committed", "description": "50+ workouts completed"})
    if total_workouts >= 100:
        achievements.append({"title": "Champion", "description": "100+ workouts completed"})

    if total_calories >= 5000:
        achievements.append({"title": "Calorie Crusher", "description": "5000+ calories burned"})
    if total_calories >= 10000:
        achievements.append({"title": "Fat Burner", "description": "10000+ calories burned"})

    if len(workout_types) >= 3:
        achievements.append({"title": "Versatile", "description": "3+ different workout types"})

    streak = calculate_streak(workouts)
    if streak >= 7:
        achievements.append({"title": "Week Warrior", "description": "7-day workout streak"})
    if streak >= 30:
        achievements.append({"title": "Month Master", "description": "30-day workout streak"})

    return achievements
