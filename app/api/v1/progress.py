from datetime import date
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud import progress as crud_progress
from app.crud import user as crud_user
from app.schemas.progress import ProgressCreate, ProgressUpdate, ProgressResponse

router = APIRouter()


@router.post("/", response_model=ProgressResponse, status_code=status.HTTP_201_CREATED)
def create_progress(progress_in: ProgressCreate, db: Session = Depends(get_db)):
    user = crud_user.get(db=db, id=progress_in.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return crud_progress.create(db=db, obj_in=progress_in)


@router.get("/{progress_id}", response_model=ProgressResponse)
def get_progress(progress_id: int, db: Session = Depends(get_db)):
    db_progress = crud_progress.get(db=db, id=progress_id)
    if not db_progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progress not found"
        )
    return db_progress


@router.get("/", response_model=List[ProgressResponse])
def list_progress(
    user_id: Optional[int] = None,
    metric: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    if user_id:
        return crud_progress.get_by_user(
            db=db,
            user_id=user_id,
            skip=skip,
            limit=limit,
            metric=metric,
            date_from=date_from,
            date_to=date_to
        )
    return crud_progress.get_multi(db=db, skip=skip, limit=limit)


@router.put("/{progress_id}", response_model=ProgressResponse)
def update_progress(progress_id: int, progress_in: ProgressUpdate, db: Session = Depends(get_db)):
    db_progress = crud_progress.get(db=db, id=progress_id)
    if not db_progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progress not found"
        )
    return crud_progress.update(db=db, db_obj=db_progress, obj_in=progress_in)


@router.delete("/{progress_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_progress(progress_id: int, db: Session = Depends(get_db)):
    db_progress = crud_progress.get(db=db, id=progress_id)
    if not db_progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progress not found"
        )
    crud_progress.delete(db=db, id=progress_id)
