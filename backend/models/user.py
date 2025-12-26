from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    role: UserRole = Field(default=UserRole.USER)

    reservations: List["Reservation"] = Relationship(back_populates="user")
