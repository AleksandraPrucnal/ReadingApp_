import pytest
from databases import Database


DATABASE_URL = "postgresql+asyncpg://user:password@db:5432/test_db"
database = Database(DATABASE_URL)

@pytest.fixture(scope="function")
async def setup_database():
    await database.connect()
    yield database
    await database.disconnect()
