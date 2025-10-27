from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from src.infrastructure.repositories.exercise_repository import ExerciseRepository
from src.infrastructure.repositories.topic_repository import TopicRepository
from src.infrastructure.repositories.user_repository import UserRepository
from src.infrastructure.repositories.progress_repository import ProgressRepository

from src.infrastructure.services.exercise import ExerciseService
from src.infrastructure.services.topic import TopicService
from src.infrastructure.services.user import UserService
from src.infrastructure.services.progress import ProgressService


class Container(DeclarativeContainer):
    exercise_repository = Singleton(ExerciseRepository)
    topic_repository = Singleton(TopicRepository)
    user_repository = Singleton(UserRepository)
    progress_repository = Singleton(ProgressRepository)

    exercise_service = Factory(
        ExerciseService,
        repository=exercise_repository,
        progress_repo=progress_repository,
    )

    user_service = Factory(
        UserService,
        repository=user_repository,
    )

    topic_service = Factory(
        TopicService,
        repository=topic_repository,
    )


"""To nizej chyba niepotrzebne?
    progress_service = Factory(
        ProgressService,
        repository=progress_repository,
    )
    """
