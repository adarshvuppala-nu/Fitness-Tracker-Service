from datetime import date
from typing import Optional, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud import workout as crud_workout
from app.crud import user as crud_user
from app.schemas.workout import WorkoutCreate, WorkoutUpdate, WorkoutResponse

router = APIRouter()


@router.post("/", response_model=WorkoutResponse, status_code=status.HTTP_201_CREATED)
def create_workout(workout_in: WorkoutCreate, db: Session = Depends(get_db)):
    user = crud_user.get(db=db, id=workout_in.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return crud_workout.create(db=db, obj_in=workout_in)


@router.get("/{workout_id}", response_model=WorkoutResponse)
def get_workout(workout_id: UUID, db: Session = Depends(get_db)):
    db_workout = crud_workout.get(db=db, id=workout_id)
    if not db_workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout not found"
        )
    return db_workout


@router.get("/", response_model=List[WorkoutResponse])
def list_workouts(
    user_id: Optional[UUID] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    if user_id:
        return crud_workout.get_by_user(
            db=db,
            user_id=user_id,
            skip=skip,
            limit=limit,
            date_from=date_from,
            date_to=date_to
        )
    return crud_workout.get_multi(db=db, skip=skip, limit=limit)


@router.put("/{workout_id}", response_model=WorkoutResponse)
def update_workout(workout_id: UUID, workout_in: WorkoutUpdate, db: Session = Depends(get_db)):
    db_workout = crud_workout.get(db=db, id=workout_id)
    if not db_workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout not found"
        )
    return crud_workout.update(db=db, db_obj=db_workout, obj_in=workout_in)


@router.delete("/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workout(workout_id: UUID, db: Session = Depends(get_db)):
    db_workout = crud_workout.get(db=db, id=workout_id)
    if not db_workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout not found"
        )
    crud_workout.delete(db=db, id=workout_id)
