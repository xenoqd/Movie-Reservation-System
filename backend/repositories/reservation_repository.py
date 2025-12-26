from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from backend.models.reservation import Reservation


class ReservationRepository:
    @staticmethod
    async def create(session: AsyncSession, reservation: Reservation):
        session.add(reservation)
        await session.commit()
        await session.refresh(reservation)
        return reservation

    @staticmethod
    async def delete(session: AsyncSession, reservation: Reservation):
        await session.delete(reservation)
        await session.commit()

    @staticmethod
    async def get_by_id(session: AsyncSession, reservation_id: int):
        return await session.get(Reservation, reservation_id)

    @staticmethod
    async def get_by_user(session: AsyncSession, user_id: int):
        query = select(Reservation).where(Reservation.user_id == user_id)
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_by_showtime(session: AsyncSession, showtime_id: int):
        query = select(Reservation).where(Reservation.showtime_id == showtime_id)
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def count_reserved_seats(session: AsyncSession, showtime_id: int):
        query = select(func.coalesce(func.sum(Reservation.seats_reserved), 0)).where(
            Reservation.showtime_id == showtime_id
        )
        result = await session.execute(query)
        return result.scalar() or 0
