import logging
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers.exercise import router as exercise_router
from src.api.routers.user import router as user_router # <-- Zmieniony import
from src.api.routers.topic import router as topic_router
from src.api.routers.progress import router as progress_router
from src.config import config
from src.container import Container
from src.db import database, init_db
from src.db_wait import wait_for_db

logging.basicConfig(level=logging.INFO)

print("Reading database configuration...")
print(f"Host: {config.DB_HOST}")
print(f"Name: {config.DB_NAME}")
print(f"User: {config.DB_USER}")

container = Container()
container.wire(modules=[
    "src.api.routers.exercise",
    "src.api.routers.user", # <-- Zmieniony moduł
    "src.api.routers.topic",
    "src.api.routers.progress",
])

# Usunęliśmy pierwszą, zduplikowaną definicję lifespan

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    """Lifespan function working on app startup."""
    logging.info("Application startup...")
    logging.info("Waiting for database...")
    await wait_for_db(
        host=os.getenv("DB_HOST", "db"),
        port=int(os.getenv("DB_PORT", "5432")),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
        database=os.getenv("DB_NAME", "app"),
    )
    logging.info("Database is ready. Initializing tables...")
    await init_db()
    logging.info("Connecting to database pool...")
    await database.connect()
    logging.info("Dziala, dziala. Nie boj nic. (Startup complete)")
    yield
    # Kod po `yield` wykona się przy zamykaniu aplikacji
    logging.info("Application shutdown...")
    await database.disconnect()
    logging.info("Database connection pool closed.")


app = FastAPI(lifespan=lifespan)

# --- Konfiguracja CORS (Poprawiona) ---
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Używamy konkretnych originów
    allow_credentials=True,    # To jest teraz bezpieczne
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Dołączanie routerów (Poprawione) ---
# Prefiksy są już zdefiniowane wewnątrz samych plików routerów
app.include_router(exercise_router, prefix="/exercise")
app.include_router(user_router) # <-- Usunięto prefix /user
app.include_router(progress_router, prefix="/progress")
app.include_router(topic_router, prefix="/topic")


@app.exception_handler(HTTPException)
async def http_exception_handle_logging(
    request: Request,
    exception: HTTPException,
) -> Response:
    # Tutaj możesz dodać logowanie błędu, np.:
    # logging.error(f"HTTP Exception: {exception.status_code} {exception.detail} for {request.url}")
    return await http_exception_handler(request, exception)

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}