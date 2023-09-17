from litestar import Controller, get, delete, Request, patch
from litestar.di import Provide
from litestar.enums import RequestEncodingType
from litestar.params import Body

from typing import Annotated

from internal.core.auth import login_required
from schemas.cart import CartProductUpdateScheme
from db.services import (
    get_cart_product as get_cart_product_db,
    delete_cart_product as delete_cart_product_db,
    update_cart_product as update_cart_product_db,
    get_cart,

)


async def get_cart_product_user_dependency(request: Request, product_id: int):
    if request.user is None:
        return None
    return await get_cart_product_db(product_id, request.user.id)


@get("/is-in-cart/{product_id:int}", dependencies={"product": Provide(get_cart_product_user_dependency)})
async def is_in_user_cart(request: Request, product: dict) -> dict:
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

    @get("/{product_id:str}")
    @login_required
    async def get_cart_product(self, request: Request, product: dict) -> dict:
        return product

    @delete("/{product_id:str}", status_code=203, dependencies={"product": Provide(get_cart_product_user_dependency)})
    @login_required
    async def delete_cart_product(self, request: Request, product: dict) -> dict:
        await delete_cart_product_db(product['id'])
        return {"detail": "Cart product deleted."}

    @patch("/{product_id:str}", dependencies={"product": Provide(get_cart_product_user_dependency)})
    @login_required
    async def update_cart_product(
            self,
            request: Request,
            product: dict,
            data: Annotated[CartProductUpdateScheme, Body(media_type=RequestEncodingType.JSON)]
    ) -> dict:
        await update_cart_product_db(product['id'], **data.dict())
        return {"detail": "Cart product updated."}
