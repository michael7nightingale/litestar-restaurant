from db.tables import CartToProduct, Cart


async def get_cart(cart_id: str) -> list[dict]:
    return await (
        CartToProduct.select(
            CartToProduct.product.all_columns(),
            CartToProduct.amount,
            CartToProduct.cart.id,
            CartToProduct.product.category.all_columns()
        )
        .where(CartToProduct.cart.id == cart_id)
    )


async def get_cart_product(product_id: int, cart_id: int) -> dict | None:
    return await (
        CartToProduct.select(CartToProduct.all_columns(), CartToProduct.product.all_columns())
        .where(CartToProduct.product.id == product_id, CartToProduct.cart.id == cart_id)
        .first()
    )


async def add_product_to_cart(product_id: int, cart_id: str) -> dict | None:
    cart = await Cart.select().where(Cart.id == cart_id).first()
    return await (
        CartToProduct.insert(
            CartToProduct(product=product_id, cart=cart['id'], amount=1)
        )
    )


async def update_cart_product(product_id: int, **values) -> None:
    update_causes = {getattr(CartToProduct, k): v for k, v in values.items()}
    await (
        CartToProduct.update(update_causes)
        .where(CartToProduct.id == product_id)
    )


async def delete_cart_product(product_id: int) -> None:
    await (
        CartToProduct.delete()
        .where(CartToProduct.id == product_id)
    )
