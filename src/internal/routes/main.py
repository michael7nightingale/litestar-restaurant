from litestar import get, Controller
from litestar.response import Template


class MainController(Controller):
    path = "/"

    @get()
    async def homepage(self) -> Template:
        return Template("index.html")
