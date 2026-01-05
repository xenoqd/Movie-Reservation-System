from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.security.dependencies import get_admin_user
from backend.services.showtime_service import ShowtimeService
from backend.schemas.showtime import ShowtimeCreate, ShowtimeUpdate
from backend.db.session import get_session
from backend.models.user import User

showtime_admin_router = APIRouter(prefix="/admin/showtime", tags=["admin", "showtime_admin"])


@showtime_admin_router.post("")
async def create_showtime(
    showtime_data: ShowtimeCreate,
    _: User  = Depends(get_admin_user),
    session: AsyncSession = Depends(get_session),
):

    showtime = await ShowtimeService.create_showtime(session, showtime_data)

    return showtime

@showtime_admin_router.patch("/{showtime_id}")
async def update_showtime(
    showtime_id: int,
    showtime_data: ShowtimeUpdate,
    _: User = Depends(get_admin_user),
    session: AsyncSession = Depends(get_session),
):
    showtime = await ShowtimeService.update_showtime(session, showtime_id, showtime_data)

    if not showtime:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Showtime not found")

    return showtime


@showtime_admin_router.post("/{showtime_id}")
async def cancel_showtime(
    showtime_id: int,
    _: User = Depends(get_admin_user),
    session: AsyncSession = Depends(get_session),
):
    showtime = await ShowtimeService.cancel_showtime(session, showtime_id)

    if not showtime:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    return {"detail": "Showtime canceled successfully"}