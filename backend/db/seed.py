from backend.core.security.password import get_password_hash
from backend.models.user import User, UserRole
from backend.models.seat import Seat

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

async def create_initial_seats(session: AsyncSession):
    result = await session.execute(select(Seat))
    if result.first():
        return  # уже созданы

    rows = 6
    seats_per_row = 10

    for row in range(1, rows + 1):
        for number in range(1, seats_per_row + 1):
            session.add(
                Seat(row=row, number=number)
            )

    await session.commit()