from pydantic import BaseModel


class OrderCreateScheme(BaseModel):
    home: str
    street: str
    comment: str
