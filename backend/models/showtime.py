from typing import Optional
from datetime import datetime
from sqlalchemy import Column, TIMESTAMP
from sqlmodel import SQLModel, Field, Relationship


class Showtime(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    movie_id: int = Field(foreign_key="movie.id")
    starts_at: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True))
    )
    ends_at: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True))
    )
    hall_number: int
    capacity: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None, nullable=True)

    movie: Optional["Movie"] = Relationship(back_populates="showtimes")
