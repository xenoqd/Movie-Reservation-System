from fastapi import FastAPI
from backend.api.v1.auth import auth_router
from backend.api.v1.user import user_router

from backend.db.session import init_db

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/")
def root():
    return {"Hello": "World"}


app.include_router(auth_router)
app.include_router(user_router)
