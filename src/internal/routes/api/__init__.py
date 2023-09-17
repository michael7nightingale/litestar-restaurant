from litestar.router import Router

from .main import ContactController
from .menu import MenuController
from .cart import is_in_user_cart, CartController


api_router = Router(
    route_handlers=[
        ContactController,
        MenuController,
        is_in_user_cart,
        CartController,

    ],
    path="/api"
)
