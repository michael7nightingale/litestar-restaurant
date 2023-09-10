from litestar import Controller, get

from db.tables import User
from schemas.users import UserDTO


class UsersController(Controller):
    path = "/users"

    @get(dto=UserDTO)
    async def get_users(self) -> list[User]:
        return await User.select()
