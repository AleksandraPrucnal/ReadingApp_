from abc import abstractmethod

from src.core.domain.exercises.exercise_base import (
    Exercise,
)


class ExerciseService:

    @abstractmethod
    async def check_answer(self, exercise: Exercise, answer: str | int) -> bool:
        pass