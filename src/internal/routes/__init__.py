from .users import UsersController
from .main import MainController
from .menu import MenuController


route_handlers = [UsersController, MainController, MenuController]
