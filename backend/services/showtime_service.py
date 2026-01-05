from typing import List, Optional
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from backend.repositories.showtime_seat_repository import ShowtimeSeatRepository
from backend.repositories.showtime_repository import ShowtimeRepository
from backend.repositories.movie_repository import MovieRepository
from backend.repositories.seat_repository import SeatRepository

from backend.schemas.showtime import ShowtimeCreate, ShowtimeUpdate
from backend.core.exceptions import DomainError

from backend.models.showtime import Showtime, ShowtimeStatus
from backend.models.showtime_seat import ShowtimeSeat


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

        created_showtime = await ShowtimeRepository.create(session, showtime)

        all_seats = await SeatRepository.get_all(session)

        if len(all_seats) != created_showtime.capacity:
            await session.delete(created_showtime)
            await session.commit()
            raise DomainError(
                500,
                f"Capacity mismatch: expected {created_showtime.capacity} seats, "
                f"but found {len(all_seats)}. Check init_seats()."
            )

        showtime_seats = [
            ShowtimeSeat(
                showtime_id=created_showtime.id,
                seat_id=seat.id,
                is_reserved=False
            )
            for seat in all_seats
        ]

        await ShowtimeSeatRepository.create_many(session, showtime_seats)

        await session.refresh(created_showtime)

        return created_showtime

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
    async def cancel_showtime(
        session: AsyncSession,
        showtime_id: int,
    ):
        showtime = await ShowtimeRepository.get_by_id(session, showtime_id)

        if not showtime:
            raise DomainError(404, "Showtime not found")

        if showtime.status.CANCELLED:
            raise DomainError(400, "Showtime already Cancelled")

        showtime.status = ShowtimeStatus.CANCELLED

        await ShowtimeRepository.create(session, showtime)

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
