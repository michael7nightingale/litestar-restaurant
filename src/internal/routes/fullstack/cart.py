from litestar import Controller, get, Request
from litestar.response import Template, Redirect

from repositories.cart import get_cart
from internal.core.auth import login_required


class CartController(Controller):
    path = "/cart"

    @get(name="cart")
    @login_required
    async def cart(self, request: Request) -> Template | Redirect:
        if not request.user:
            return Redirect(request.app.route_reverse("login"))
        context = {
            "cart": await get_cart(request.user.id)
        }
        return Template("cart.html", context=context)

