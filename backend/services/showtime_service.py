from typing import List, Optional
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from backend.repositories.movie_repository import MovieRepository
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
        movie = await MovieRepository.get_by_id(session, showtime_data.movie_id)
        if not movie:
            raise DomainError(404, "Movie not found")

        duration = showtime_data.ends_at - showtime_data.starts_at

        if duration.total_seconds() <= 0:
            raise DomainError(400, "Showtime end must be after start")

        if duration < timedelta(minutes=30):
            raise DomainError(400, "Showtime is too short")

        if duration > timedelta(hours=6):
            raise DomainError(400, "Showtime is too long")

        overlap = await ShowtimeRepository.find_overlap(
            session,
            hall_number=showtime_data.hall_number,
            starts_at=showtime_data.starts_at,
            ends_at=showtime_data.ends_at,
        )
        if overlap:
            raise DomainError(400,"Showtime overlaps with another showtime in this hall")

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
        session: AsyncSession, showtime_id: int, showtime_data: ShowtimeUpdate
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
    async def get_showtime_by_id(session: AsyncSession, showtime_id: int):
        showtime = await ShowtimeRepository.get_by_id(session, showtime_id)
        if not showtime:
            raise DomainError(404, "Showtime not found")

        return showtime

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
