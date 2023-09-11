from litestar import Litestar
from litestar.template.config import TemplateConfig
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.static_files import StaticFilesConfig

from pathlib import Path

from internal.routes import route_handlers
from .admin import admin_app, create_superuser


class App:
    def __init__(self):
        handlers = route_handlers.copy()
        handlers.append(admin_app)

        self.app = Litestar(
            route_handlers=handlers,
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
            on_startup=[self.on_startup]

        )

    async def on_startup(self, app):
        await create_superuser()
