from backend.models.user import User, UserRole
from backend.core.security.password import get_password_hash

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select


async def create_initial_admin(session: AsyncSession):
    result = await session.execute(
        select(User).where(User.email == "admin@example.com")
    )
    admin = result.scalar_one_or_none()

    if not admin:
        hashed_pw = get_password_hash("admin123")
        admin = User(
            username="Admin",
            email="admin@example.com",
            hashed_password=hashed_pw,
            role=UserRole.ADMIN,
        )
        session.add(admin)
        await session.commit()
