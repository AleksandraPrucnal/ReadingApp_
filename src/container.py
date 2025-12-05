from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

# Repozytoria
from src.infrastructure.repositories.exercise_repository import ExerciseRepository
from src.infrastructure.repositories.topic_repository import TopicRepository
from src.infrastructure.repositories.user_repository import UserRepository
from src.infrastructure.repositories.progress_repository import ProgressRepository

# Serwisy
from src.infrastructure.services.exercise import ExerciseService
from src.infrastructure.services.topic import TopicService
from src.infrastructure.services.user import UserService
from src.infrastructure.services.progress import ProgressService
from src.infrastructure.services.inflection import InflectionService


class Container(DeclarativeContainer):
    # --- REPOZYTORIA ---
    exercise_repository = Singleton(ExerciseRepository)
    topic_repository = Singleton(TopicRepository)
    user_repository = Singleton(UserRepository)
    progress_repository = Singleton(ProgressRepository)

    # --- SERWISY ---

    # ExerciseService
    exercise_service = Factory(
        ExerciseService,
        repository=exercise_repository,
        progress_repo=progress_repository,
    )

    # UserService
    user_service = Factory(
        UserService,
        user_repo=user_repository,
    )

    # TopicService
    topic_service = Factory(
        TopicService,
        repository=topic_repository,
    )

    # ProgressService
    progress_service = Factory(
        ProgressService,
        repository=progress_repository
    )

    inflection_service = Factory(
        InflectionService,
    )