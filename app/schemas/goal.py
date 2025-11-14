from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class GoalBase(BaseModel):
    goal_type: str
    target_value: float
    unit: str
    deadline: date


class GoalCreate(GoalBase):
    user_id: int
    current_value: float = 0.0
    status: str = "active"


class GoalUpdate(BaseModel):
    goal_type: Optional[str] = None
    target_value: Optional[float] = None
    current_value: Optional[float] = None
    unit: Optional[str] = None
    deadline: Optional[date] = None
    status: Optional[str] = None


class GoalResponse(GoalBase):
    id: int
    user_id: int
    current_value: float
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
