from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from backend.repositories.showtime_seat_repository import ShowtimeSeatRepository
from backend.repositories.reservation_repository import ReservationRepository
from backend.repositories.showtime_repository import ShowtimeRepository
from backend.schemas.reservation import ReservationCreate
from backend.core.exceptions import DomainError
from backend.models.reservation import Reservation, ReservationStatus

class ReservationService:
    @staticmethod
    async def create_reservation(
        session: AsyncSession,
        data: ReservationCreate,
        user_id: int,
    ):
        showtime = await ShowtimeRepository.get_by_id_with_lock(session, data.showtime_id)
        if not showtime:
            raise DomainError(404, "Showtime not found")

        if showtime.starts_at <= datetime.now(timezone.utc):
            raise DomainError(400, "Showtime has already started")

        seat_ids = data.seat_ids
        requested_count = len(seat_ids)

        if requested_count == 0:
            raise DomainError(400, "At least one seat must be selected")
        if len(set(seat_ids)) != requested_count:
            raise DomainError(400, "Duplicate seat IDs are not allowed")

        reserved_count = await ShowtimeSeatRepository.get_reserved_count_for_showtime(
            session, data.showtime_id
        )
        if reserved_count + requested_count > showtime.capacity:
            raise DomainError(
                400,
                f"Only {showtime.capacity - reserved_count} seat(s) available"
            )

        showtime_seats = await ShowtimeSeatRepository.get_multiple_for_reservation(
            session, data.showtime_id, seat_ids
        )

        found_ids = {ss.seat_id for ss in showtime_seats}
        if len(found_ids) != requested_count:
            missing = sorted(set(seat_ids) - found_ids)
            raise DomainError(404, f"Seats not available: {missing}")

        already_reserved = [ss.seat_id for ss in showtime_seats if ss.is_reserved]
        if already_reserved:
            raise DomainError(400, f"Seats already reserved: {sorted(already_reserved)}")

        await ShowtimeSeatRepository.mark_as_reserved(session, showtime_seats)

        reservation = Reservation(
            user_id=user_id,
            showtime_id=data.showtime_id,
            seats_reserved=len(data.seat_ids),
            status=ReservationStatus.ACTIVE,
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
