from litestar.contrib.piccolo import PiccoloDTO
from pydantic import BaseModel

from db.tables import User


UserDTO = PiccoloDTO[User]


class UserCreate(BaseModel):
    name: str
    phone: str


class UserLogin(BaseModel):
    phone: str
