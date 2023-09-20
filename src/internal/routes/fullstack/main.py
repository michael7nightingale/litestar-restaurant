from litestar import get, Controller, post, Request
from litestar.params import Body
from litestar.enums import RequestEncodingType
from litestar.response import Template, Redirect

from typing import Annotated

from repositories.table_reservation import create_table_reservation
from repositories.reviews import create_review, get_reviews
from schemas.main import Reservation, Review


class MainController(Controller):
    path = "/"

    @get(name="homepage")
    async def homepage(self) -> Template:
        context = {
            "title": "Хотей Тавда"
        }
        return Template("index.html", context=context)

    @get("/contact", name='contact')
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


class TableReservationController(Controller):
    path = "/table-reservation"

    @get(name="table_reservation")
    async def table_reservation(self) -> Template:
        return Template("table-reservation.html")

    @post(name='table_reservation_post', status_code=303)
    async def table_reservation_create(
            self,
            request: Request,
            data: Annotated[Reservation, Body(media_type=RequestEncodingType.URL_ENCODED)]
    ) -> Redirect:
        await create_table_reservation(**data.dict())
        return Redirect(request.app.route_reverse("table_reservation"))


class ReviewsController(Controller):
    path = "/reviews"

    @get(name="reviews")
    async def reviews(self) -> Template:
        context = {
            "reviews": await get_reviews()
        }
        return Template("reviews.html", context=context)

    @post(name='reviews_post', status_code=303)
    async def reviews_create(
            self,
            request: Request,
            data: Annotated[Review, Body(media_type=RequestEncodingType.URL_ENCODED)]
    ) -> Redirect:
        if not request.user:
            return Redirect(request.app.route_reverse("login"))
        await create_review(user_id=request.user.id, **data.dict())
        return Redirect(request.app.route_reverse("reviews"))
