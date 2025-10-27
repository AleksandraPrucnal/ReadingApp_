from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Dict, List
from src.core.domain.enums import UiMode

class Preferences(BaseModel):
    id_user: UUID
    topics: List[int]
    favourite_names: List[str]
    family_names: Dict[str, str]
    ui_mode: UiMode
    level: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")
