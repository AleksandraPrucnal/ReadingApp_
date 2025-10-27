from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict


class TopicDTO(BaseModel):
    id_topic: int
    name: str

    model_config = ConfigDict(from_attributes=True, extra="ignore")