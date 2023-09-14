from litestar.router import Router

from .main import ContactController
from .menu import MenuController


api_router = Router(
    route_handlers=[
        ContactController,
        MenuController,

    ],
    path="/api"
)
