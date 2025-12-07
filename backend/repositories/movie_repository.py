from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.movie import Movie


class MovieRepository:
    @staticmethod
    async def get_by_id(session: AsyncSession, movie_id: int):
        return await session.get(Movie, movie_id)

    @staticmethod
    async def create(session: AsyncSession, movie: Movie):
        session.add(movie)
        await session.commit()
        await session.refresh(movie)
        return movie

    @staticmethod
    async def delete(session: AsyncSession, movie: Movie):
        await session.delete(movie)
        await session.commit()
