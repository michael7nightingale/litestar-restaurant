from typing import Annotated

from litestar import Controller, get, post, Request
from litestar.params import Body
from litestar.enums import RequestEncodingType
from litestar.response import Template, Redirect

from internal.core.auth import login_required
from schemas.orders import OrderCreateScheme
from repositories.order import get_order, create_order


class OrderController(Controller):
    path = "/orders"

    @get(name="create_order")
    @login_required
    async def create_order(self, request: Request) -> Template | Redirect:
        order = await get_order(request.user.cart_id)
        if order is not None:
            return Redirect(request.app.route_reverse("current_order"), status_code=303)
        return Template("create_order.html")

    @post(name="create_order_post", status_code=303)
    @login_required
    async def create_order_post(
            self,
            request: Request,
    ) -> Redirect:
        new_order = await create_order(
            user_id=request.user.id,
            cart_id=request.user.cart_id,
            **{k: v[0] for k, v in (await request.form()).dict().items()}
        )
        return Redirect(request.app.route_reverse("current_order"))

    @get(path="/current", name="current_order")
    @login_required
    async def current_order(self, request: Request) -> Template:
        order = await get_order(request.user.cart_id)
        context = {"order": order}
        return Template("order.html", context=context)
