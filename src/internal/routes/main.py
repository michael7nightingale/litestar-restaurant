from litestar import get, Controller
from litestar.response import Template


class MainController(Controller):
    path = "/"

    @get(name="homepage")
    async def homepage(self) -> Template:
        context = {
            "title": "Хотей Тавда"
        }
        return Template("index.html", context=context)

    @get(path="/contact", name='contact')
    async def contact(self) -> Template:
        return Template("contact.html")
