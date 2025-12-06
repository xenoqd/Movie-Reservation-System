from fastapi import FastAPI
from backend.api.v1.auth.auth import auth_router
from backend.api.v1.users.user import user_router

from backend.api.v1.users.user_admin import user_admin_router

from backend.db import session as db_session
from backend.db.seed import create_initial_admin

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await db_session.init_db()

    async with db_session.async_session() as session:
        await create_initial_admin(session)


@app.get("/")
def root():
    return {"Hello": "World"}

app.include_router(user_admin_router)


app.include_router(auth_router)
app.include_router(user_router)
