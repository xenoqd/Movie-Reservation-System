from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from backend.api.v1.auth.auth import auth_router
from backend.api.v1.users.user import user_router
from backend.api.v1.showtime.showtime import showtime_router
from backend.api.v1.reservation.reservation import reservation_router

from backend.api.v1.users.user_admin import user_admin_router
from backend.api.v1.movie.movie_admin import movie_admin_router
from backend.api.v1.showtime.showtime_admin import showtime_admin_router
from backend.api.v1.reservation.reservation_admin import reservation_admin_router

from backend.db import session as db_session
from backend.db.seed import create_initial_admin,  create_initial_seats

from backend.core.exceptions import DomainError


app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await db_session.init_db()

    async with db_session.async_session() as session:
        await create_initial_admin(session)
        await create_initial_seats(session)


@app.get("/")
def root():
    return {"Hello": "World"}


@app.exception_handler(DomainError)
async def domain_exception_handler(request: Request, exc: DomainError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )


app.include_router(user_admin_router)
app.include_router(movie_admin_router)
app.include_router(showtime_admin_router)
app.include_router(reservation_router)
app.include_router(reservation_admin_router)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(showtime_router)
