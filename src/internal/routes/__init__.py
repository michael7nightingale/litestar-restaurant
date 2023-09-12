from .users import UsersController
from .main import MainController, ContactController
from .menu import MenuController


route_handlers = [UsersController, MainController, MenuController, ContactController]
