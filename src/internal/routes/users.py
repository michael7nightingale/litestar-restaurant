from litestar import Controller, get, post, Request
from litestar.exceptions import HTTPException
from litestar.enums import RequestEncodingType
from litestar.response import Template, Redirect

from litestar.params import Body
from typing import Annotated

from db.services import login_user, create_user
from schemas.users import UserLogin, UserCreate
from internal.core.auth import login_user as login_user_cookies, login_required, logout_user


class UsersController(Controller):
    path = "/users"

    @get("/login", name="login")
    async def get_login(self) -> Template:
        return Template("login.html")

    @get("/logout", name="logout", status_code=303)
    async def logout(self, request: Request) -> Redirect:
        logout_user(request)
        return Redirect(request.app.route_reverse("homepage"))

    @post("/login", name="login_post", status_code=303)
    async def post_login(
            self,
            request: Request,
            data: Annotated[UserLogin, Body(media_type=RequestEncodingType.URL_ENCODED)]
    ) -> Redirect:
        user = await login_user(data.phone)
        if user is None:
            return Redirect(request.app.route_reverse("login"))
        login_user_cookies(request, user['id'])
        return Redirect(request.app.route_reverse("homepage"))

    @get("/register", name="register")
    async def get_register(self) -> Template:
        return Template("register.html")

    @post("/register", name="register_post", status_code=303)
    async def post_register(
            self,
            request: Request,
            data: Annotated[UserCreate, Body(media_type=RequestEncodingType.URL_ENCODED)]
    ) -> Redirect:
        try:
            user = await create_user(**data.dict())
        except Exception:
            return Redirect(request.app.route_reverse("register"))
        return Redirect(request.app.route_reverse("login"))

    @get("/account", name="account")
    async def get_account(self, request: Request) -> list:
        if request.user is None:
            raise HTTPException(status_code=303)

        return []
