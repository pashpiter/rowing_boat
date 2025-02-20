from fastapi import FastAPI
from contextlib import asynccontextmanager
from db.database import create_table_and_boat
from api.v1.routers import router as v1_router


@asynccontextmanager
async def lifespan(app):
    create_table_and_boat()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(v1_router)
