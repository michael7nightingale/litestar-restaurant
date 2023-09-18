from litestar import Litestar
from litestar.exceptions.http_exceptions import NotAuthorizedException
from litestar.template.config import TemplateConfig
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.static_files import StaticFilesConfig
from litestar.middleware import DefineMiddleware

from pathlib import Path

from db.load_data import load_data
from internal.routes import routers
from .admin import admin_app, create_superuser
from .auth import AuthenticationMiddleware, auth_exception_handler


class App:
    def __init__(self):
        self.app = Litestar(
            route_handlers=[admin_app],
            template_config=TemplateConfig(
                directory=Path("internal/templates"),
                engine=JinjaTemplateEngine
            ),
            static_files_config=[
                StaticFilesConfig(
                    directories=['internal/static'],
                    path="/static"
                )
            ],
            on_startup=[self.on_startup],
            middleware=[
                DefineMiddleware(AuthenticationMiddleware),

            ],

        )

        for router in routers:
            self.app.register(router)

    async def on_startup(self, app):
        await load_data()
        await create_superuser()
