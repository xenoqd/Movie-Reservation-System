from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from backend.repositories.showtime_seat_repository import ShowtimeSeatRepository
from backend.repositories.showtime_repository import ShowtimeRepository
from backend.schemas.seat import SeatAvailabilitySchema
from backend.core.exceptions import DomainError


class ShowtimeSeatService:
    @staticmethod
    async def get_hall_schema(
        session: AsyncSession,
        showtime_id: int,
    ) -> List[SeatAvailabilitySchema]:
        showtime = await ShowtimeRepository.get_by_id(session, showtime_id)
        if not showtime:
            raise DomainError(404, "Showtime not found")


        showtime_seats = await ShowtimeSeatRepository.get_all_seats_for_showtime(
            session, showtime_id
        )

        if not showtime_seats:
            raise DomainError(500, f"No seats initialized for showtime {showtime_id}")


        return [
            SeatAvailabilitySchema(
                seat_id=ss.seat_id,
                row=ss.seat.row,
                number=ss.seat.number,
                is_reserved=ss.is_reserved,
            )
            for ss in showtime_seats
        ]

    @staticmethod
    async def get_available_seats(
        session: AsyncSession,
        showtime_id: int
    ):
        showtime = await ShowtimeRepository.get_by_id(session, showtime_id)
        if not showtime:
            raise DomainError(404, "Showtime not found")
        
        showtime_seats = await ShowtimeSeatRepository.get_available_seats_for_showtime(session, showtime_id)

        return showtime_seats