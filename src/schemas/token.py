from datetime import datetime

from pydantic import BaseModel


class Token(BaseModel):
    user_id: int
    exp: datetime


class ScopeUser(BaseModel):
    name: str
