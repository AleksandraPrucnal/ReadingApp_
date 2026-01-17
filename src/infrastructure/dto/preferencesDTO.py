from typing import List, Dict
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from src.core.domain.enums import UiMode


class PreferencesDTO(BaseModel):
    id_user: UUID
    topics: List[int] = []
    favourite_names: List[str] = []
    family_names: Dict[str, str] = {}
    ui_mode: UiMode
    level: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")