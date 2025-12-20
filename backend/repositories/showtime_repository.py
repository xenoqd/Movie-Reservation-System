from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from backend.models.showtime import Showtime


class ShowtimeRepository:
    @staticmethod
    async def get_by_id(session: AsyncSession, showtime_id: int):
        return await session.get(Showtime, showtime_id)

    @staticmethod
    async def create(session: AsyncSession, showtime: Showtime):
        session.add(showtime)
        await session.commit()
        await session.refresh(showtime)
        return showtime

    @staticmethod
    async def delete(session: AsyncSession, showtime: Showtime):
        await session.delete(showtime)
        await session.commit()

    @staticmethod
    async def read_showtime_by_filters(
        session: AsyncSession,
        movie_id: int = None,
        hall_number: int = None,
        starts_at: datetime = None,
    ):
        query = select(Showtime)
        if movie_id is not None:
            query = query.where(Showtime.movie_id == movie_id)
        if hall_number is not None:
            query = query.where(Showtime.hall_number == hall_number)
        if starts_at is not None:
            query = query.where(Showtime.starts_at == starts_at)

        result = await session.execute(query)
        return result.scalars().all()
