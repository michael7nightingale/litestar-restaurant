from litestar import Router

from .users import UsersController
from .main import MainController, TableReservationController, ReviewsController
from .menu import MenuController
from .cart import CartController


fullstack_router = Router(
    route_handlers=[
        UsersController,
        MainController,
        MenuController,
        TableReservationController,
        ReviewsController,
        CartController,

    ],
    path="/"
)
