from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton, Resource

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


# Importujemy sesję bazy danych (jeśli Twoje repozytoria jej używają w __init__,
# ale w naszym przypadku używamy globalnego obiektu 'database' z src.db,
# więc repozytoria nie potrzebują wstrzykiwania sesji w kontenerze).

class Container(DeclarativeContainer):
    # --- REPOZYTORIA ---
    # Tworzymy je jako Singletony (jedna instancja na całą aplikację)
    exercise_repository = Singleton(ExerciseRepository)
    topic_repository = Singleton(TopicRepository)
    user_repository = Singleton(UserRepository)
    progress_repository = Singleton(ProgressRepository)

    # --- SERWISY ---

    # ExerciseService
    # Zakładam, że w __init__ masz argumenty: repository i progress_repo
    exercise_service = Factory(
        ExerciseService,
        repository=exercise_repository,
        progress_repo=progress_repository,
    )

    # UserService
    # POPRAWKA: Zmieniono 'repository' na 'user_repo', aby pasowało do __init__ w UserService
    user_service = Factory(
        UserService,
        user_repo=user_repository,
    )

    # TopicService
    # Zakładam, że w __init__ masz argument: repository
    topic_service = Factory(
        TopicService,
        repository=topic_repository,
    )

    # ProgressService
    # (Dodałem to, bo zaimportowałeś klasę, ale nie zdefiniowałeś fabryki w swoim kodzie)
    # Jeśli masz ProgressService, prawdopodobnie wygląda tak:
    progress_service = Factory(
        ProgressService,
        repository=progress_repository
    )