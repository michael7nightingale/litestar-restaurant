from litestar import Controller, get, delete, Request, patch
from litestar.di import Provide
from litestar.params import Body

from typing import Annotated

from internal.core.auth import login_required
from internal.dependencies.cart import get_cart_product_user_dependency
from schemas.cart import CartProductUpdateScheme
from repositories.cart import (
    delete_cart_product as delete_cart_product_db,
    update_cart_product as update_cart_product_db,
    get_cart,

)


@get("/is-in-cart/{product_id:int}", dependencies={"product": Provide(get_cart_product_user_dependency)})
async def is_in_user_cart(request: Request, product: dict | None) -> dict:
    if request.user is None:
        return {"is-in-cart": False}
    if product is None:
        return {"is-in-cart": False}
    return {"is-in-cart": True, "amount": product['amount']}


class CartController(Controller):
    path = "/cart"

    @get()
    @login_required
    async def get_cart(self, request: Request) -> list[dict]:
        return await get_cart(request.user.id)

    @delete(
        "/{product_id:str}",
        status_code=202,
        dependencies={"product": Provide(get_cart_product_user_dependency)}
    )
    @login_required
    async def delete_cart_product(self, request: Request, product: dict) -> dict:
        await delete_cart_product_db(product['id'])
        return {"detail": "Cart product deleted."}

    @patch(
        "/{product_id:str}",
        dependencies={"product": Provide(get_cart_product_user_dependency)}
    )
    @login_required
    async def update_cart_product(
            self,
            request: Request,
            product: dict,
            data: Annotated[CartProductUpdateScheme, Body()]
    ) -> dict:
        await update_cart_product_db(product['id'], **data.dict())
        return {"detail": "Cart product updated."}
