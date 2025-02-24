from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.v1.routers import router as v1_router
from db.database import create_table_and_boat


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_table_and_boat()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(v1_router)
