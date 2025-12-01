from fastapi import Depends, Request, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.session import get_session
from backend.core.security.jwt import decode_access_token
from backend.repositories.user_repository import user_repo
from backend.models.user import User


async def get_current_user(
    request: Request, session: AsyncSession = Depends(get_session)
):
    # Достаём токен из header/cookie
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token missing"
        )

    if isinstance(token, str) and token.lower().startswith("bearer "):
        token = token.split(" ", 1)[1]

    payload = decode_access_token(token)
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(401, "Invalid token payload")

    user_id = int(payload.get("sub"))
    user = await user_repo.get_by_user_id(session, user_id)

    if not user:
        raise HTTPException(404, "User not found")

    return user


async def get_current_admin(
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    return current_user
