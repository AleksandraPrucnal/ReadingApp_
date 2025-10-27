from typing import Optional, Iterable, Sequence
from abc import ABC, abstractmethod
from src.core.domain.enums import ExerciseType
from src.core.domain.exercises.exercise_base import ExerciseIn
from src.core.domain.exercises.exercise_match import ExerciseMatchIn
from src.core.domain.exercises.exercise_question import ExerciseQuestionIn
from src.core.domain.exercises.question import Question, QuestionIn
from src.infrastructure.dto.exerciseDTO import (
    ExerciseBaseDTO,
    ExerciseMatchDTO,
    ExerciseQuestionDTO,
    QuestionDTO,
)


class IExerciseService(ABC):

    @abstractmethod
    async def get_all_exercises(self) -> Iterable[ExerciseBaseDTO]:
        pass

    @abstractmethod
    async def get_by_id(self, id_exercise: int) -> ExerciseMatchDTO:
        pass

    @abstractmethod
    async def get_by_level(self, level: int) -> Iterable[ExerciseBaseDTO]:
        pass

    @abstractmethod
    async def get_by_type(self, ex_type: ExerciseType) -> Iterable[ExerciseBaseDTO]:
        pass

    @abstractmethod
    async def get_by_topics(
            self,
            topic_ids: Sequence[int],
            *,
            match_all: bool = False,
            limit: int = 50,
            offset: int = 0,
    ) -> Iterable[ExerciseBaseDTO]:
        pass

    @abstractmethod
    async def list_questions(self, id_exercise: int) -> Iterable[QuestionDTO]:
        pass

    @abstractmethod
    async def get_question(self, id_question: int) -> Optional[QuestionDTO]:
        pass

    @abstractmethod
    async def add_exercise_match(self, data: ExerciseMatchIn) -> None:
        pass

    @abstractmethod
    async def add_exercise_question(self, data: ExerciseQuestionIn) -> None:
        pass

    @abstractmethod
    async def add_question(self, id_exercise: int, data: QuestionIn) -> Question:
        pass

    @abstractmethod
    async def update_exercise_match(self, id_exercise: int, data: ExerciseMatchIn) -> None:
        pass

    @abstractmethod
    async def update_exercise_question(self, id_exercise: int, data: ExerciseQuestionIn) -> None:
        pass

    @abstractmethod
    async def update_question(self, id_question: int, data: QuestionIn) -> Question | None:
        pass

    @abstractmethod
    async def delete_exercise(self, id_exercise: int) -> bool:
        pass

    @abstractmethod
    async def delete_question(self, id_question: int) -> bool:
        pass

    @abstractmethod
    async def check_answer_match(
        self,
        id_exercise: int,
        selected_index: int,
    ) -> tuple[int, bool]:
        pass

    @abstractmethod
    async def check_answer_question_single(
        self,
        id_exercise: int,
        id_question: int,
        selected_index: int,
    ) -> tuple[int, int, bool]:
        pass