from typing import Optional, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud import goal as crud_goal
from app.crud import user as crud_user
from app.schemas.goal import GoalCreate, GoalUpdate, GoalResponse

router = APIRouter()


@router.post("/", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
def create_goal(goal_in: GoalCreate, db: Session = Depends(get_db)):
    user = crud_user.get(db=db, id=goal_in.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return crud_goal.create(db=db, obj_in=goal_in)


@router.get("/{goal_id}", response_model=GoalResponse)
def get_goal(goal_id: UUID, db: Session = Depends(get_db)):
    db_goal = crud_goal.get(db=db, id=goal_id)
    if not db_goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )
    return db_goal


@router.get("/", response_model=List[GoalResponse])
def list_goals(
    user_id: Optional[UUID] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    if user_id:
        return crud_goal.get_by_user(
            db=db,
            user_id=user_id,
            skip=skip,
            limit=limit,
            status=status
        )
    return crud_goal.get_multi(db=db, skip=skip, limit=limit)


@router.put("/{goal_id}", response_model=GoalResponse)
def update_goal(goal_id: UUID, goal_in: GoalUpdate, db: Session = Depends(get_db)):
    db_goal = crud_goal.get(db=db, id=goal_id)
    if not db_goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )
    return crud_goal.update(db=db, db_obj=db_goal, obj_in=goal_in)


@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_goal(goal_id: UUID, db: Session = Depends(get_db)):
    db_goal = crud_goal.get(db=db, id=goal_id)
    if not db_goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )
    crud_goal.delete(db=db, id=goal_id)
