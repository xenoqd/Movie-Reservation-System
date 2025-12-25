from sqlalchemy.ext.asyncio import AsyncSession

from backend.repositories.movie_repository import MovieRepository
from backend.schemas.movie import MovieCreate, MovieEdit
from backend.core.exceptions import DomainError
from backend.models.movie import Movie


class MovieService:
    @staticmethod
    async def create_movie(
        session: AsyncSession, 
        movie_data: MovieCreate
    ):
        movie = Movie(
            title=movie_data.title,
            description=movie_data.description,
            genre=movie_data.genre.value,
            poster_url=movie_data.poster_url,
        )
        return await MovieRepository.create(session, movie)

    @staticmethod
    async def edit_movie(
        session: AsyncSession,
        movie_id: int,
        movie_data: MovieEdit,
    ):
        movie = await MovieRepository.get_by_id(session, movie_id)
        if not movie:
            raise DomainError(404, "Movie not found")

        movie.title = movie_data.title
        movie.description = movie_data.description
        movie.genre = movie_data.genre
        movie.poster_url = movie_data.poster_url

        await session.commit()
        await session.refresh(movie)

        return movie

    @staticmethod
    async def delete_movie(
        session: AsyncSession,
        movie_id: int,
    ):
        movie = await MovieRepository.get_by_id(session, movie_id)

        if not movie:
            raise DomainError(404, "Movie not found")


        await MovieRepository.delete(session, movie)
        return True
