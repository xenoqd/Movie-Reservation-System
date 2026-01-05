from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.seat import Seat


class SeatRepository:
    @staticmethod
    async def get_all(session: AsyncSession) -> List[Seat]:
        query = select(Seat).order_by(Seat.row, Seat.number)
        result = await session.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def count(session: AsyncSession):
        query = select(Seat)
        result = await session.execute(query)
        return len(result.scalars().all())

    @staticmethod
    async def get_by_id(session: AsyncSession, seat_id: int):
        return await session.get(Seat, seat_id)
