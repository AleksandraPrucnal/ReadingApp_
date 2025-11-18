from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List


class ChartPointDTO(BaseModel):
    date: str   # Formatowanie daty jako string
    points: int


class UserProgressDTO(BaseModel):
    total_points: int
    current_level: int
    points_to_next_level: int
    next_level_threshold: int
    history: List[ChartPointDTO]

    model_config = ConfigDict(from_attributes=True)