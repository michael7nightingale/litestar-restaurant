from litestar import Controller, get, post, Request
from litestar.enums import RequestEncodingType
from litestar.response import Template, Redirect

from litestar.params import Body
from typing import Annotated

from db.services import login_user, create_user
from schemas.users import UserLoginSchema, UserRegisterSchema
from internal.core.auth import login_user as login_user_cookies, logout_user


def get_previous_url(request: Request) -> str:
    previous_url = request.cookies.get("previous-url")
    if previous_url is None:
        previous_url = request.app.route_reverse("homepage")
    return previous_url


class UsersController(Controller):
    path = "/users"

    @get("/login", name="login")
    async def get_login(self) -> Template:
        return Template("login.html")

    @get("/logout", name="logout", status_code=303)
    async def logout(self, request: Request) -> Redirect:
        logout_user(request)
        return Redirect(get_previous_url(request))

    @post("/login", name="login_post", status_code=303)
    async def post_login(
            self,
            request: Request,
            data: Annotated[UserLoginSchema, Body(media_type=RequestEncodingType.URL_ENCODED)]
    ) -> Redirect:
        user = await login_user(data.phone)
        if user is None:
            return Redirect(request.app.route_reverse("login"))
        login_user_cookies(request, user['id'])
        return Redirect(get_previous_url(request))

    @get("/register", name="register")
    async def get_register(self) -> Template:
        return Template("register.html")

    @post("/register", name="register_post", status_code=303)
    async def post_register(
            self,
            request: Request,
            data: Annotated[UserRegisterSchema, Body(media_type=RequestEncodingType.URL_ENCODED)]
    ) -> Redirect:
        user = await create_user(**data.dict())
        if user is None:
            return Redirect(request.app.route_reverse("register"))
        return Redirect(request.app.route_reverse("login"))
