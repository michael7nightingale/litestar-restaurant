from litestar import Controller, post
from litestar.enums import RequestEncodingType
from litestar.exceptions import HTTPException
from litestar.params import Body

from typing import Annotated

from schemas.users import UserRegisterSchema, UserLoginSchema
from db.services import login_user, create_user
from internal.core.auth import encode_jwt_token


class UsersController(Controller):
    path = "/users"

    @post("/register")
    async def register(
            self,
            data: Annotated[UserRegisterSchema, Body()]
    ) -> dict:
        user = await create_user(**data.dict())
        if user is None:
            raise HTTPException(
                detail="Data is invalid or not unique.",
                status_code=400
            )
        return {"detail": "User created successfully."}

    @post("/login")
    async def login(
            self,
            data: Annotated[UserLoginSchema, Body()]
    ) -> dict:
        user = await login_user(data.phone)
        if not user:
            raise HTTPException(
                detail="User is not found.",
                status_code=404
            )
        return {"access-token": encode_jwt_token(user['id'])}
