from typing import Annotated

from litestar import get, Controller, post
from litestar.params import Body
from litestar.enums import RequestEncodingType
from litestar.response import Template, Redirect

from db.services import create_table_reservation
from schemas.main import Reservation


class MainController(Controller):
    path = "/"

    @get(name="homepage")
    async def homepage(self) -> Template:
        context = {
            "title": "Хотей Тавда"
        }
        return Template("index.html", context=context)


class ContactController(Controller):
    path = "/contact"

    @get(name='contact')
    async def contact_get(self) -> Template:
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

    @post(name='contact_post', status_code=303)
    async def contact_create(
            self,
            data: Annotated[Reservation, Body(media_type=RequestEncodingType.URL_ENCODED)]
    ) -> Redirect:
        await create_table_reservation(**data.dict())
        return Redirect("/contact")
