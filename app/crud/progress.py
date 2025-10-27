from datetime import date
from typing import Optional, List
from uuid import UUID

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.progress import Progress
from app.schemas.progress import ProgressCreate, ProgressUpdate


class CRUDProgress(CRUDBase[Progress, ProgressCreate, ProgressUpdate]):
    def get_by_user(
        self,
        db: Session,
        *,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
        metric: Optional[str] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> List[Progress]:
        query = db.query(Progress).filter(Progress.user_id == user_id)

        if metric:
            query = query.filter(Progress.metric == metric)
        if date_from:
            query = query.filter(Progress.date >= date_from)
        if date_to:
            query = query.filter(Progress.date <= date_to)

        return query.offset(skip).limit(limit).all()


progress = CRUDProgress(Progress)
