from litestar import Controller, get, Request
from litestar.response import Template, Redirect

from db.services import get_cart


class CartController(Controller):
    path = "/cart"

    @get(name="cart")
    async def cart(self, request: Request) -> Template | Redirect:
        if not request.user:
            return Redirect(request.app.route_reverse("login"))
        context = {
            "cart": await get_cart(request.user.id)
        }
        return Template("cart.html", context=context)

