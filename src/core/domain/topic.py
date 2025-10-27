from pydantic import BaseModel

class TopicIn(BaseModel):
    name: str

class Topic(TopicIn):
    id_topic: int
