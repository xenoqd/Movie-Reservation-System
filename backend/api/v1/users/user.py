from fastapi import APIRouter, Depends

from backend.core.security.dependencies import get_current_user
from backend.schemas.user import UserRead

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.get("/me", response_model=UserRead)
async def me(user=Depends(get_current_user)):
    return user
