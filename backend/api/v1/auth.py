from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from backend.services.auth_service import AuthService
from backend.schemas.user import UserRead, UserCreate, UserLogin
from backend.schemas.auth import TokenResponse

from backend.db.session import get_session

auth_router= APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register/", response_model=UserRead)
async def register(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    user = await AuthService.register(user_data, session)
    return user


@auth_router.post("/login/", response_model=TokenResponse)
async def login(
    user_data: UserLogin,
    response: Response,
    session: AsyncSession = Depends(get_session),
):
    token = await AuthService.login(user_data, session)

    # Ставим HttpOnly куку
    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,
        max_age=3600,  # 1 час
        secure=False,  # HTTPS
        samesite="lax",
        path="/",
    )
    return TokenResponse(access_token=token, token_type="bearer")
