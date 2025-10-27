# src/core/domain/exercises/exercise_question.py
from pydantic import BaseModel, ConfigDict
from typing import List
from src.core.domain.enums import ExerciseType

class ExerciseQuestionIn(BaseModel):
    type: ExerciseType  # "text_question"
    level: int
    topics: List[int] = []
    text: str
    image_url: str
    model_config = ConfigDict(from_attributes=True, extra="ignore")


"""
from typing import List, Optional

from pydantic import field_validator
from src.core.domain.exercises.exercise_base import ExerciseIn, Exercise
from src.core.domain.exercises.question import QuestionIn

class ExerciseQuestionIn(ExerciseIn):
    text: str
    image_url: str
    questions: Optional[List[QuestionIn]] = None

    @field_validator("questions")
    @classmethod
    def validate_questions(cls, v):
        if v is not None and len(v) == 0:
            raise ValueError("questions list cannot be empty if provided")
        return v

class ExerciseQuestion(Exercise, ExerciseQuestionIn):
    pass
"""