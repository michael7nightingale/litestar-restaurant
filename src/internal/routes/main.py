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
        context = {
            "phone_numbers": [
                {
                    'number': "+7 (993) 774-08-34",
                    "description": "Администратор"
                }
            ],
            "emails": [
                {
                    "email": "hotei@tave.com",
                    "description": ""
                }
            ],

        }
        return Template("contact.html", context=context)
