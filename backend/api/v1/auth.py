from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.services.auth_service import AuthService
from backend.schemas.user import UserRead, UserCreate, UserLogin
from backend.schemas.auth import TokenResponse

from backend.db.session import get_session

auth_service = APIRouter(prefix="/auth", tags=["auth"])

@auth_service.post("/register/", response_model=UserRead)
async def register(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session)
    ):
    user = await AuthService.register(user_data, session)
    return user


@auth_service.post("/login/", response_model=TokenResponse)
async def login(
    user_data: UserLogin,
    session: AsyncSession = Depends(get_session)
    ):
    user = await AuthService.login(user_data, session)
    return user