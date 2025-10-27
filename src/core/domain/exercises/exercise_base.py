from typing import List
from pydantic import BaseModel,ConfigDict
from src.core.domain.enums import ExerciseType


class ExerciseIn(BaseModel):
    type: ExerciseType
    level: int
    topics: List[int] = []

class Exercise(ExerciseIn):
    id_exercise: int
    model_config = ConfigDict(from_attributes=True)