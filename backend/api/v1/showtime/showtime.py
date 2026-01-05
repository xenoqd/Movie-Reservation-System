from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from datetime import datetime

from backend.db.session import get_session
from backend.schemas.showtime import ShowtimeRead
from backend.services.showtime_service import ShowtimeService
from backend.services.showtime_seat_service import ShowtimeSeatService

showtime_router = APIRouter(prefix="/showtime", tags=["showtime"])

@showtime_router.get("/{showtime_id}/seats")
async def get_showtime_seats(
    showtime_id: int,
    session: AsyncSession = Depends(get_session),
):
    seats = await ShowtimeSeatService.get_hall_schema(session, showtime_id)
    return seats

@showtime_router.get("/{showtime_id}/seats/available")
async def get_available_seats(
    showtime_id: int,
    session: AsyncSession = Depends(get_session),
):
    seats = await ShowtimeSeatService.get_available_seats(session, showtime_id)
    return seats

@showtime_router.get("/{showtime_id}", response_model=ShowtimeRead)
async def get_showtime(
    showtime_id: int,
    session: AsyncSession = Depends(get_session),
):
    showtime = await ShowtimeService.get_showtime_by_id(session, showtime_id)

    if not showtime:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Showtime not found"
        )

    return showtime


@showtime_router.get("", response_model=List[ShowtimeRead])
async def get_showtimes(
    movie_id: Optional[int] = Query(None),
    hall_number: Optional[int] = Query(None),
    starts_at: Optional[datetime] = Query(None),
    session: AsyncSession = Depends(get_session),
):
    return await ShowtimeService.get_showtimes_by_filters(
        session=session,
        movie_id=movie_id,
        hall_number=hall_number,
        starts_at=starts_at,
    )
