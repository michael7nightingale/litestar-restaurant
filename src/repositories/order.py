from db.tables import Order, CartToProduct


async def create_order(
        cart_id: str,
        home: str,
        street: str,
        comment: str | None = None,
        status: str | None = None,
) -> dict | None:
    return (await (
        Order.insert(
            Order(
                cart=cart_id,
                home=home,
                status=status,
                street=street,
                comment=comment
            )
        )
    ))[0]


async def get_order(user_id: str) -> dict | None:
    return await (
        Order.select(Order.all_columns())
        .where(Order.cart.user.id == user_id)
        .first()
    )


async def order_set_delivered(user_id: str) -> dict:
    return (await (
        Order.update({Order.is_delivered: True})
        .where(Order.cart.user.id == user_id)
    ))[0]


async def delete_cart_product_after_order(user_id: str) -> None:
    return await (
        CartToProduct.delete()
        .where(CartToProduct.cart.user.id == user_id)
    )
