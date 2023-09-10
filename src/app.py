from litestar import Litestar
from litestar.template.config import TemplateConfig
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.static_files import StaticFilesConfig

from pathlib import Path

from internal.routes import route_handlers


create_app = Litestar(
    route_handlers=route_handlers,
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

)
