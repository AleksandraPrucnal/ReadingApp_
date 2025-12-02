from typing import Iterable, Sequence, Optional
from uuid import UUID
from datetime import datetime
from src.core.domain.enums import ExerciseType
from src.core.domain.exercises.exercise_match import ExerciseMatchIn
from src.core.domain.exercises.exercise_question import ExerciseQuestionIn
from src.core.domain.exercises.question import Question, QuestionIn
from src.core.repositories.iexercise_repository import IExerciseRepository
from src.core.repositories.iprogress_repository import IProgressRepository
from src.infrastructure.services.iexercise import IExerciseService
from src.infrastructure.dto.exerciseDTO import (
    QuestionDTO,
    ExerciseMatchDTO,
    ExerciseQuestionDTO,
    ExerciseBaseDTO,
)

from src.core.domain.progress import ProgressIn
from src.infrastructure.repositories.progress_repository import ProgressRepository


class ExerciseService(IExerciseService):
    """Exercise service delegating to the repository."""

    _repository: IExerciseRepository
    _progress_repo: IProgressRepository

    def __init__(self, repository: IExerciseRepository, progress_repo: ProgressRepository) -> None:
        self._repository = repository
        self._progress_repo = progress_repo

    # --- Read ---
    async def get_all_exercises(self, limit: int = 50, offset: int = 0) -> Iterable[ExerciseBaseDTO]:
        return await self._repository.get_all_exercises(limit=limit, offset=offset)

    async def get_by_id(self, id_exercise: int) -> Optional[ExerciseBaseDTO]:
        return await self._repository.get_by_id(id_exercise)

    async def get_by_level(self, level: int, limit: int = 50, offset: int = 0) -> Iterable[ExerciseBaseDTO]:
        return await self._repository.get_by_level(level, limit=limit, offset=offset)

    async def get_by_type(self, ex_type: ExerciseType, limit: int = 50, offset: int = 0) -> Iterable[ExerciseBaseDTO]:
        return await self._repository.get_by_type(ex_type, limit=limit, offset=offset)

    async def get_by_topics(
            self,
            topic_ids: Sequence[int],
            *,
            match_all: bool = False,
            limit: int = 50,
            offset: int = 0,
    ) -> Iterable[ExerciseBaseDTO]:
        return await self._repository.get_by_topics(
            topic_ids,
            match_all=match_all,
            limit=limit,
            offset=offset,
        )

    async def list_questions(self, id_exercise: int) -> Iterable[QuestionDTO]:
        return await self._repository.list_questions(id_exercise)

    async def get_question(self, id_question: int) -> Optional[QuestionDTO]:
        return await self._repository.get_question(id_question)

    # --- Create ---
    async def add_exercise_match(self, data: ExerciseMatchIn) -> ExerciseMatchDTO | None:
        return await self._repository.add_exercise_match(data)

    async def add_exercise_question(self, data: ExerciseQuestionIn) -> ExerciseQuestionDTO | None:
        return await self._repository.add_exercise_question(data)

    async def add_question(self, id_exercise: int, data: QuestionIn) -> QuestionDTO | None:
        return await self._repository.add_question(id_exercise, data)

    # --- Update ---
    async def update_exercise_match(self, id_exercise: int, data: ExerciseMatchIn) -> ExerciseMatchDTO | None:
        return await self._repository.update_exercise_match(id_exercise, data)

    async def update_exercise_question(self, id_exercise: int, data: ExerciseQuestionIn) -> ExerciseQuestionDTO | None:
        return await self._repository.update_exercise_question(id_exercise, data)

    async def update_question(self, id_question: int, data: QuestionIn) -> QuestionDTO | None:
        return await self._repository.update_question(id_question, data)

    # --- Delete ---
    async def delete_exercise(self, id_exercise: int) -> bool:
        return await self._repository.delete_exercise(id_exercise)

    async def delete_question(self, id_question: int) -> bool:
        return await self._repository.delete_question(id_question)

    # --- PUNKTY I SPRAWDZANIE ---

    async def check_answer_match(
            self,
            id_exercise: int,
            selected_index: int,
            *,
            user_id: Optional[UUID] = None,
    ) -> tuple[int, bool]:
        ex_id, ok = await self._repository.check_answer_match(
            id_exercise=id_exercise,
            selected_index=selected_index,
        )

        # Zapis postępu
        if user_id is not None:
            points = 10 if ok else 0

            await self._progress_repo.add_progress(
                ProgressIn(
                    user_id=user_id,
                    id_exercise=ex_id,
                    rate=points,
                    completed_at=datetime.utcnow(),
                )
            )
        return ex_id, ok

    async def check_answer_question_single(
            self,
            id_exercise: int,
            id_question: int,
            selected_index: int,
            *,
            user_id: Optional[UUID] = None,
    ) -> tuple[int, int, bool]:
        ex_id, q_id, ok = await self._repository.check_answer_question_single(
            id_exercise=id_exercise,
            id_question=id_question,
            selected_index=selected_index,
        )

        if user_id is not None:
            points = 5 if ok else 0

            await self._progress_repo.add_progress(
                ProgressIn(
                    user_id=user_id,
                    id_exercise=ex_id,
                    rate=points,
                    completed_at=datetime.utcnow(),
                )
            )
        return ex_id, q_id, ok