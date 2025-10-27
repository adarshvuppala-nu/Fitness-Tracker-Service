from datetime import date
from typing import Optional, List
from uuid import UUID

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.workout import Workout
from app.schemas.workout import WorkoutCreate, WorkoutUpdate


class CRUDWorkout(CRUDBase[Workout, WorkoutCreate, WorkoutUpdate]):
    def get_by_user(
        self,
        db: Session,
        *,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> List[Workout]:
        query = db.query(Workout).filter(Workout.user_id == user_id)

        if date_from:
            query = query.filter(Workout.date >= date_from)
        if date_to:
            query = query.filter(Workout.date <= date_to)

        return query.offset(skip).limit(limit).all()


workout = CRUDWorkout(Workout)
