from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from backend.services.auth_service import AuthService
from backend.schemas.user import UserRead, UserCreate, UserLogin
from backend.schemas.auth import TokenResponse

from backend.db.session import get_session

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register/", response_model=UserRead)
async def register(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    user = await AuthService.register(user_data, session)
    return user


@auth_router.post("/login/")
async def login(
    user_data: UserLogin,
    response: Response,
    session: AsyncSession = Depends(get_session),
):
    tokens = await AuthService.login(user_data, session)

    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=3600,
        secure=False,
        samesite="lax",
        path="/",
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=60 * 60 * 24 * 7,
        secure=True,
        samesite="lax",
        path="/auth/refresh",
    )
    return {"message": "Login successful"}
