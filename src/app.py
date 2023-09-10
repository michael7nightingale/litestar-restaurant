from litestar import Litestar
from internal.routes import route_handlers


create_app = Litestar(route_handlers=route_handlers)
