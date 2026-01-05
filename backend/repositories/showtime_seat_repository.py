from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import joinedload
from sqlalchemy import update

from backend.models.showtime_seat import ShowtimeSeat


class ShowtimeSeatRepository:
    @staticmethod
    async def get_all_seats_for_showtime(
        session: AsyncSession,
        showtime_id: int
    ) -> List[ShowtimeSeat]:
        query = (
            select(ShowtimeSeat)
            .options(joinedload(ShowtimeSeat.seat))
            .where(ShowtimeSeat.showtime_id == showtime_id)
        )
        result = await session.execute(query)
        seats = list(result.scalars().unique().all())
        return sorted(seats, key=lambda s: (s.seat.row, s.seat.number))

    @staticmethod
    async def get_multiple_for_reservation(
        session: AsyncSession,
        showtime_id: int,
        seat_ids: List[int],
    ):
        query = (
            select(ShowtimeSeat)
            .where(
                ShowtimeSeat.showtime_id == showtime_id,
                ShowtimeSeat.seat_id.in_(seat_ids)
            )
            .with_for_update()
        )
        result = await session.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def mark_as_reserved(
        session: AsyncSession,
        showtime_seats: List[ShowtimeSeat],
    ):
        if not showtime_seats:
            return

        seat_ids = [ss.seat_id for ss in showtime_seats]
        showtime_id = showtime_seats[0].showtime_id  # все одинаковые

        query = (
            update(ShowtimeSeat)
            .where(
                ShowtimeSeat.showtime_id == showtime_id,
                ShowtimeSeat.seat_id.in_(seat_ids)
            )
            .values(is_reserved=True)
        )
        await session.execute(query)

    @staticmethod
    async def create_many(
        session: AsyncSession,
        showtime_seats: List[ShowtimeSeat]
    ):
        session.add_all(showtime_seats)
        await session.commit()

    @staticmethod
    async def get_reserved_count_for_showtime(
        session: AsyncSession,
        showtime_id: int
    ) -> int:
        query = (
            select(func.count())
            .select_from(ShowtimeSeat)
            .where(
                and_(
                    ShowtimeSeat.showtime_id == showtime_id,
                    ShowtimeSeat.is_reserved == True
                )
            )
        )
        result = await session.execute(query)
        return result.scalar_one()

    @staticmethod
    async def get_by_showtime_and_seat(
        session: AsyncSession,
        showtime_id: int,
        seat_id: int
    ) -> Optional[ShowtimeSeat]:
        query = select(ShowtimeSeat).where(
            and_(
                ShowtimeSeat.showtime_id == showtime_id,
                ShowtimeSeat.seat_id == seat_id
            )
        )
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_available_seats_for_showtime(
        session: AsyncSession,
        showtime_id: int
    ) -> List[ShowtimeSeat]:
        query = (
            select(ShowtimeSeat)
            .options(joinedload(ShowtimeSeat.seat))
            .where(
                ShowtimeSeat.showtime_id == showtime_id,
                ShowtimeSeat.is_reserved == False
            )
        )
        result = await session.execute(query)
        seats = list(result.scalars().unique().all())

        return sorted(seats, key=lambda s: (s.seat.row, s.seat.number))