from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class ProgressIn(BaseModel):
    user_id: UUID
    id_exercise: int
    rate: int
    completed_at: datetime = Field(default_factory=datetime.utcnow)

class Progress(ProgressIn):
    id_event: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")
