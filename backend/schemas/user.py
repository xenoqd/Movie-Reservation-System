from pydantic import BaseModel, EmailStr
from backend.models.user import UserRole


class UserRead(BaseModel):
    id: int
    username: str
    email: str
    role: UserRole


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    login: str
    password: str
