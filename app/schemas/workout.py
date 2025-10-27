from datetime import datetime, date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class WorkoutBase(BaseModel):
    type: str
    duration: int = Field(gt=0)
    calories_burned: float = Field(ge=0)
    notes: Optional[str] = None
    date: date


class WorkoutCreate(WorkoutBase):
    user_id: UUID


class WorkoutUpdate(BaseModel):
    type: Optional[str] = None
    duration: Optional[int] = Field(default=None, gt=0)
    calories_burned: Optional[float] = Field(default=None, ge=0)
    notes: Optional[str] = None
    date: Optional[date] = None


class WorkoutResponse(WorkoutBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
