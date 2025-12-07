from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.schemas.movie import MovieCreate, MovieEdit
from backend.services.movie_service import MovieService
from backend.db.session import get_session
from backend.core.security.dependencies import get_admin_user

movie_admin_router = APIRouter(prefix="/admin", tags=["admin"])


@movie_admin_router.post("/movies/create_movie")
async def create_movie(
    movie_data: MovieCreate,
    user=Depends(get_admin_user),
    session: AsyncSession = Depends(get_session),
):

    movie = await MovieService.create_movie(session, movie_data)

    return movie


@movie_admin_router.patch("/movies/{movie_id}")
async def edit_movie(
    movie_id: int,
    movie_data: MovieEdit,
    user=Depends(get_admin_user),
    session: AsyncSession = Depends(get_session),
):

    movie = await MovieService.edit_movie(session, movie_id, movie_data)

    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    return movie


@movie_admin_router.delete("/movies/{movie_id}")
async def delet_movie(
    movie_id: int,
    user=Depends(get_admin_user),
    session: AsyncSession = Depends(get_session),
):

    movie = await MovieService.delete_movie(session, movie_id)

    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    return {"detail": "Movie deleted successfully"}
