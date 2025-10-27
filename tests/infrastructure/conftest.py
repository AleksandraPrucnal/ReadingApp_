import pytest
from src.infrastructure.repositories.exercise_repository import ExerciseRepository
from src.db import database
from src.core.repositories.iexercise_repository import IExerciseRepository
from src.core.domain.enums import ExerciseType
from src.core.domain.exercises.exercise_match import ExerciseMatchIn

@pytest.fixture
async def repo() -> IExerciseRepository:
    exercise_repo = ExerciseRepository()
    return exercise_repo

@pytest.fixture
async def topic_ids():
    return [1, 2]
