from sqlmodel import SQLModel
from pydantic import EmailStr
from backend.models.user import UserRole


class UserRead(SQLModel):
    id: int
    username: str
    email: str
    role: UserRole


class UserCreate(SQLModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(SQLModel):
    login: str
    password: str
