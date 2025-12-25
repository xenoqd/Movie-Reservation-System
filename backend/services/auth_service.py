from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.user import User, UserRole
from backend.db.session import get_session
from backend.repositories.user_repository import user_repo
from backend.core.exceptions import DomainError
from backend.core.security.jwt import create_access_token, create_refresh_token
from backend.core.security.password import (
    get_password_hash,
    verify_password,
)


class AuthService:
    @staticmethod
    async def register(user_data, session: AsyncSession):
        if session is None:
            session = await get_session()

        existing = await user_repo.get_by_email(session, user_data.email)
        if existing:
            raise DomainError(400, "User already exists")

        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=get_password_hash(user_data.password),
            role=UserRole.USER,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

        return user

    @staticmethod
    async def login(user_data, session: AsyncSession):
        if session is None:
            session = await get_session()

        login = user_data.login

        if "@" in login:
            user = await user_repo.get_by_email(session, login)
        else:
            user = await user_repo.get_by_username(session, login)

        if not user:
            raise DomainError(400, "User not found")

        if not verify_password(user_data.password, user.hashed_password):
            raise DomainError(401, "Invalid password or login")

        access_token = create_access_token(
            {
                "sub": str(user.id),
                "role": user.role,
            }
        )
        refresh_token = create_refresh_token(
            {
                "sub": str(user.id),
                "role": user.role,
            }
        )

        return {"access_token": access_token, "refresh_token": refresh_token}
