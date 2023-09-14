from litestar import Litestar
from litestar.exceptions import HTTPException
from litestar.template.config import TemplateConfig
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.static_files import StaticFilesConfig
from litestar.middleware import DefineMiddleware

from pathlib import Path

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
            exception_handlers={
                HTTPException: auth_exception_handler,
            }

        )

        for router in routers:
            self.app.register(router)

        print([i.path for i in self.app.routes])

    async def on_startup(self, app):
        await create_superuser()
