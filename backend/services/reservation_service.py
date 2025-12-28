from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from backend.repositories.reservation_repository import ReservationRepository
from backend.repositories.showtime_repository import ShowtimeRepository
from backend.schemas.reservation import ReservationCreate
from backend.core.exceptions import DomainError
from backend.models.reservation import Reservation, ReservationStatus


class ReservationService:
    @staticmethod
    async def create_reservation(
        session: AsyncSession, data: ReservationCreate, user_id: int
    ):  
        showtime = await ShowtimeRepository.get_by_id_with_lock(session, data.showtime_id)

        if not showtime:
            raise DomainError(404, "Showtime not found")
        
        if showtime.starts_at <= datetime.now(timezone.utc):
            raise DomainError(400, "Showtime already started")

        reserved = await ReservationRepository.count_reserved_seats(
            session, data.showtime_id
        )

        available = showtime.capacity - reserved

        if data.seats > available:
            raise DomainError(400, "Not enough seats available")

        if data.seats < 1:
            raise DomainError(400, "Value must be positive")

        reservation = Reservation(
            user_id=user_id, showtime_id=data.showtime_id, seats_reserved=data.seats
        )

        return await ReservationRepository.create(session, reservation)

    @staticmethod
    async def cancel_reservation(
        session: AsyncSession,
        reservation_id: int,
        current_user_id: int,
        is_admin: bool = False,
    ):
        reservation = await ReservationRepository.get_by_id(session, reservation_id)

        if not reservation:
            raise DomainError(404, "Reservation not found")

        if not is_admin and reservation.user_id != current_user_id:
            raise DomainError(400, "You can't cancel this reservation")

        if reservation.status != ReservationStatus.ACTIVE:
            raise DomainError(400, "Reservation not active")

        if reservation.showtime.starts_at <= datetime.now(timezone.utc):
            raise DomainError(400, "Cannot cancel started showtime")

        reservation.status = ReservationStatus.CANCELLED

        await ReservationRepository.create(session, reservation)

    @staticmethod
    async def get_user_reservation(session: AsyncSession, user_id: int):
        return await ReservationRepository.get_by_user(session, user_id)

    @staticmethod
    async def get_showtime_reservations(session: AsyncSession, showtime_id: int):
        showtime = await ShowtimeRepository.get_by_id(session, showtime_id)
        if not showtime:
            raise DomainError(404, "Showtime not found")

        return await ReservationRepository.get_by_showtime(session, showtime_id)
