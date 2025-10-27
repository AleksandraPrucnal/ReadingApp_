from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict

class TokenDTO(BaseModel):
    access_token: str
    token_type: Literal["Bearer"]
    expires: datetime
    model_config = ConfigDict(from_attributes=True, extra="ignore")