from typing import List, Optional
from pydantic import BaseModel,ConfigDict, field_validator


class QuestionIn(BaseModel):
    question: str
    answers: List[str]
    correct_index: int

    @field_validator("correct_index")
    @classmethod
    def validate_correct_index(cls, v, info):
        answers = info.data.get("answers") or []
        if not (0 <= v < len(answers)):
            raise ValueError("correct_index must be within answers range")
        return v


class Question(QuestionIn):
    id_question: int
    exercise_id: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")