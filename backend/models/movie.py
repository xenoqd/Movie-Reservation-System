from typing import Optional, List
from datetime import datetime
from enum import Enum

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import func


class Genre(str, Enum):
    ACTION = "action"
    DRAMA = "drama"
    COMEDY = "comedy"
    HORROR = "horror"
    ROMANCE = "romance"
    THRILLER = "Thriller"


class Movie(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, nullable=False)
    description: Optional[str] = Field(default=None, nullable=True)
    poster_url: Optional[str] = Field(default=None, nullable=True)
    genre: Genre = Field(sa_column_kwargs={"nullable": False})
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=func.now())
    updated_at: Optional[datetime] = Field(default=None, nullable=True)


#    showtimes: List["Showtime"] = Relationship(back_populates="movie")
