from backend.models.movie import Genre

from pydantic import BaseModel
from typing import Optional


class MovieCreate(BaseModel):
    title: str
    description: str
    poster_url: Optional[str] = None
    genre: Genre


class MovieRead(BaseModel):
    id: int
    title: str
    description: str
    poster_url: Optional[str]
    genre: Genre


class MovieEdit(BaseModel):
    title: str
    description: str
    poster_url: Optional[str] = None
    genre: Genre
