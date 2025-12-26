from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from typing import List

from backend.services.reservation_service import ReservationService
from backend.core.security.dependencies import get_current_user
from backend.db.session import get_session
from backend.models.user import User
from backend.schemas.reservation import ReservationRead, ReservationCreate

reservation_router = APIRouter(prefix="/reservation", tags=["reservation"])


@reservation_router.get("/me", response_model=List[ReservationRead])
async def get_user_reservation(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):

    reservation = await ReservationService.get_user_reservation(
        session=session, user_id=current_user.id
    )

    return reservation


@reservation_router.post("/reserve", response_model=ReservationRead)
async def reserve_seat(
    data: ReservationCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):

    reservation = await ReservationService.create_reservation(
        session=session, data=data, user_id=current_user.id
    )

    return reservation


@reservation_router.post("/cancel")
async def cancel_reservation(
    reservation_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):

    is_admin = current_user.role

    await ReservationService.cancel_reservation(
        session=session,
        reservation_id=reservation_id,
        current_user_id=current_user.id,
        is_admin=is_admin,
    )

    return {"status": "ok"}
