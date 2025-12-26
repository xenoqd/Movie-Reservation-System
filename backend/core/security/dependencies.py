from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError, ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.security.jwt import decode_access_token
from backend.repositories.user_repository import user_repo
from backend.db.session import get_session
from backend.core.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM


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


def get_admin_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        role: str = payload.get("role")

        if role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions"
            )

        return payload

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
