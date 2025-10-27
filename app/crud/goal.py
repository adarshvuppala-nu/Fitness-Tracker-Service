from typing import Optional, List
from uuid import UUID

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.goal import Goal
from app.schemas.goal import GoalCreate, GoalUpdate


class CRUDGoal(CRUDBase[Goal, GoalCreate, GoalUpdate]):
    def get_by_user(
        self,
        db: Session,
        *,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None
    ) -> List[Goal]:
        query = db.query(Goal).filter(Goal.user_id == user_id)

        if status:
            query = query.filter(Goal.status == status)

        return query.offset(skip).limit(limit).all()


goal = CRUDGoal(Goal)
