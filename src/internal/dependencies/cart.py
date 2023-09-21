from litestar import Request

from repositories.cart import get_cart_product


async def get_cart_product_user_dependency(request: Request, product_id: int) -> dict | None:
    if request.user is None:
        return None
    return await get_cart_product(product_id, request.user.id)
