import pytest
from src.infrastructure.repositories.exercise_repository import ExerciseRepository
from src.core.domain.exercises.exercise_match import ExerciseMatchIn
from src.core.domain.enums import ExerciseType
from databases import Database


DATABASE_URL = "postgresql+asyncpg://user:password@db:5432/test_db"
database = Database(DATABASE_URL)

@pytest.fixture(scope="function")
async def setup_database():
    await database.connect()
    yield database
    await database.disconnect()


@pytest.fixture
def repo() -> ExerciseRepository:
    """Fixture dla repozytorium ExerciseRepository."""
    return ExerciseRepository()

@pytest.fixture
def topic_ids():
    """Fixture dla przykładowych topic_ids."""
    return [1, 2]

@pytest.mark.asyncio
async def test_add_and_get_match_ok(repo: ExerciseRepository, topic_ids):
    data = ExerciseMatchIn(
        type=ExerciseType.MATCH, level=1, topics=topic_ids,
        text="x", image_urls=["a.png", "b.png"], correct_index=1
    )
    saved = await repo.add_exercise_match(data)
    got = await repo.get_by_id(saved.id_exercise)

    assert got.id_exercise == saved.id_exercise
