from litestar import get, Controller, post, Request
from litestar.params import Body
from litestar.enums import RequestEncodingType

from typing import Annotated

from schemas.main import Reservation
from repositories.table_reservation import create_table_reservation


class ContactController(Controller):
    path = "/contact"

    @get()
    async def contact_get(self) -> dict:
        return {
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

    @post(status_code=303)
    async def contact_create(
            self,
            request: Request,
            data: Annotated[Reservation, Body(media_type=RequestEncodingType.JSON)]
    ) -> dict:
        reservation = await create_table_reservation(**data.dict())
        return {"detail": "Table reserved successfully."}
