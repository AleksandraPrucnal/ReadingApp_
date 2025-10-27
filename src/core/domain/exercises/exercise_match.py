# src/core/domain/exercises/exercise_match.py
from pydantic import BaseModel, ConfigDict
from typing import List
from src.core.domain.enums import ExerciseType

class ExerciseMatchIn(BaseModel):
    type: ExerciseType  # "match_image"
    level: int
    topics: List[int] = []
    text: str
    image_urls: List[str]
    correct_index: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")



"""from typing import List

from pydantic import field_validator
from src.core.domain.exercises.exercise_base import ExerciseIn, Exercise


class ExerciseMatchIn(ExerciseIn):
    text: str
    image_urls: List[str]
    correct_index: int

    @field_validator("correct_index")
    @classmethod
    def validate_correct_index(cls, v, info):
        urls = info.data.get("image_urls") or []
        if not (0 <= v < len(urls)):
            raise ValueError("correct_index must be within image_urls range")
        return v


class ExerciseMatch(Exercise, ExerciseMatchIn):
    pass
"""