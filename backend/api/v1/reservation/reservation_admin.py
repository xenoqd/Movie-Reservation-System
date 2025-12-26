from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from backend.services.reservation_service import ReservationService
from backend.core.security.dependencies import get_admin_user
from backend.db.session import get_session
from backend.models.user import User

reservation_admin_router = APIRouter(
    prefix="/admin", tags=["admin", "reservation_admin"]
)


@reservation_admin_router.get("/showtime/{showtime_id}/reservations")
async def showtime_reservations(
    showtime_id: int,
    session: AsyncSession = Depends(get_session),
    _: User = Depends(get_admin_user),
):
    reservations = await ReservationService.get_showtime_reservations(
        session, showtime_id
    )
    return reservations


@reservation_admin_router.get("/users/{user_id}/reservations")
async def get_user_reservations(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    _: User = Depends(get_admin_user),
):
    reservations = await ReservationService.get_user_reservation(session, user_id)
    return reservations
