from pydantic import BaseModel


class UserRegisterSchema(BaseModel):
    name: str
    phone: str


class UserLoginSchema(BaseModel):
    phone: str
