from typing import List, Optional
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from backend.repositories.showtime_repository import ShowtimeRepository
from backend.schemas.showtime import ShowtimeCreate, ShowtimeUpdate
from backend.core.exceptions import DomainError
from backend.models.showtime import Showtime


class ShowtimeService:
    @staticmethod
    async def create_showtime(
        session: AsyncSession,
        showtime_data: ShowtimeCreate,
    ):
        showtime = Showtime(
            movie_id=showtime_data.movie_id,
            starts_at=showtime_data.starts_at,
            ends_at=showtime_data.ends_at,
            hall_number=showtime_data.hall_number,
            capacity=showtime_data.capacity,
        )
        return await ShowtimeRepository.create(session, showtime)

    @staticmethod
    async def update_showtime(
        session: AsyncSession,
        showtime_id: int,
        showtime_data: ShowtimeUpdate
    ):
        showtime = await ShowtimeRepository.get_by_id(session, showtime_id)

        if not showtime:
            raise DomainError(404, "Showtime not found")

        for field, value in showtime_data.dict(exclude_unset=True).items():
            setattr(showtime, field, value)

        showtime.updated_at = datetime.utcnow()

        await session.commit()
        await session.refresh(showtime)

        return showtime

    @staticmethod
    async def delete_showtime(
        session: AsyncSession,
        showtime_id: int,
    ):

        showtime = await ShowtimeRepository.get_by_id(session, showtime_id)

        if not showtime:
            raise DomainError(404, "Showtime not found")

        await ShowtimeRepository.delete(session, showtime)

        return showtime

    @staticmethod
    async def get_showtime_by_id(
        session: AsyncSession,
        showtime_id: int
    ):
        return await ShowtimeRepository.get_by_id(session, showtime_id)

    @staticmethod
    async def get_showtimes_by_filters(
        session: AsyncSession,
        movie_id: Optional[int] = None,
        hall_number: Optional[int] = None,
        starts_at: Optional[datetime] = None,
    ):
        return await ShowtimeRepository.read_showtime_by_filters(
            session=session,
            movie_id=movie_id,
            hall_number=hall_number,
            starts_at=starts_at,
        )
