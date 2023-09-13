from litestar import Controller, get, post, Request
from litestar.response import Template, Redirect


class UsersController(Controller):
    path = "/users"

    @get(path="/login", name="login")
    async def get_login(self) -> Template:
        return Template("login.html")

    @post(path="/login", name="login_post")
    async def post_login(self, request: Request) -> Redirect:
        return Redirect(request.app.route_reverse("homepage"))

    @get(path="/register", name="register")
    async def get_register(self) -> Template:
        return Template("register.html")

    @get(path="/account", name="account")
    async def get_account(self) -> list:
        return []
