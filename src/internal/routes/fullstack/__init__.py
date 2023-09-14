from litestar import Router

from .users import UsersController
from .main import MainController, ContactController
from .menu import MenuController


fullstack_router = Router(
    route_handlers=[
        UsersController,
        MainController,
        MenuController,
        ContactController,

    ],
    path="/"
)
