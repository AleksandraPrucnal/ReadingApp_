from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import JSONResponse

from datetime import date, time, datetime

from src.api.routers.exercise import router as exercise_router
from src.api.routers.user import router as user_router
from src.api.routers.topic import router as topic_router

from src.container import Container
from src.db import database, init_db
from src.config import config

import logging
logging.basicConfig(level=logging.INFO)
import os
from src.db_wait import wait_for_db

print("Connecting to database...")
print(f"Host: {config.DB_HOST}")
print(f"Name: {config.DB_NAME}")
print(f"User: {config.DB_USER}")


container = Container()
container.wire(modules=[
    "src.api.routers.exercise",
    "src.api.routers.user",
    "src.api.routers.topic",
])


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Connecting to database...")
    await wait_for_db(
        host=os.getenv("DB_HOST", "db"),
        port=int(os.getenv("DB_PORT", "5432")),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
        database=os.getenv("DB_NAME", "app"),
    )
    await init_db()
    await database.connect()
    yield
    await database.disconnect()

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    """Lifespan function working on app startup."""
    print("Connecting to database...")
    await wait_for_db(
        host=os.getenv("DB_HOST", "db"),
        port=int(os.getenv("DB_PORT", "5432")),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
        database=os.getenv("DB_NAME", "app"),
    )
    await init_db()
    await database.connect()
    logging.info("Dziala, dziala. Nie boj nic.")
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(exercise_router, prefix="/exercise")
app.include_router(user_router, prefix="/user")
app.include_router(topic_router, prefix="/topic")


@app.exception_handler(HTTPException)
async def http_exception_handle_logging(
    request: Request,
    exception: HTTPException,
) -> Response:

    return await http_exception_handler(request, exception)