from fastapi import FastAPI
from backend.api.v1.auth import auth_service
from backend.db.session import init_db

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/")
def root():
    return {"Hello": "World"}


app.include_router(auth_service)
