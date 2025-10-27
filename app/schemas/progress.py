from datetime import datetime, date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class ProgressBase(BaseModel):
    metric: str
    value: float
    unit: str
    date: date
    notes: Optional[str] = None


class ProgressCreate(ProgressBase):
    user_id: UUID


class ProgressUpdate(BaseModel):
    metric: Optional[str] = None
    value: Optional[float] = None
    unit: Optional[str] = None
    date: Optional[date] = None
    notes: Optional[str] = None


class ProgressResponse(ProgressBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
