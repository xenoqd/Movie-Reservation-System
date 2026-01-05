from backend.models.showtime import ShowtimeStatus
from datetime import datetime, timezone
from pydantic import BaseModel
from typing import Optional
from sqlmodel import Field

class ShowtimeCreate(BaseModel):
    movie_id: int
    starts_at: datetime = datetime.now(timezone.utc)
    ends_at: datetime = datetime.now(timezone.utc)
    hall_number: int
    capacity: int = Field(default=60)


class ShowtimeUpdate(BaseModel):
    movie_id: Optional[int] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None
    hall_number: Optional[int] = None
    capacity: Optional[int] = None


class ShowtimeRead(BaseModel):
    id: int
    movie_id: int
    starts_at: datetime
    ends_at: datetime
    hall_number: int
    capacity: int
    created_at: datetime
    updated_at: Optional[datetime] = None

