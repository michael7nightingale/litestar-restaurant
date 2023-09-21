from pydantic import BaseModel, Field
from datetime import datetime


class Token(BaseModel):
    user_id: int
    exp: datetime


class ScopeUser(BaseModel):
    id: int
    name: str
    phone: str
    cart_id: int = Field(alias="cart")
