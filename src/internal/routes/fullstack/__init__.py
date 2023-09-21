from litestar import Router
from litestar.exceptions import NotAuthorizedException
from litestar.middleware import DefineMiddleware

from .users import UsersController
from .main import MainController, TableReservationController, ReviewsController
from .menu import MenuController
from .cart import CartController
from .orders import OrderController

from internal.core.middleware import PaginationMiddleware
from internal.core.auth import auth_exception_handler


fullstack_router = Router(
    route_handlers=[
        UsersController,
        MainController,
        MenuController,
        TableReservationController,
        ReviewsController,
        CartController,
        OrderController,

    ],
    path="/",
    middleware=[DefineMiddleware(PaginationMiddleware)],
    exception_handlers={
        NotAuthorizedException: auth_exception_handler,
    },

)
