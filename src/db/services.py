import datetime

from .tables import Ingredient, Product, Category, TableReservation, User, Review, Cart, CartToProduct


async def get_all_categories() -> list[dict]:
    return await Category.select()


async def get_category_by_slug(category_slug: str) -> dict:
    return await (
        Category.select(Category.all_columns())
        .where(Category.slug == category_slug)
        .first()
    )


async def get_products_by_category_slug(category_slug: str) -> list[dict]:
    return await (
        Product.select(
                Product.all_columns(),
                Product.category.slug
            )
        .where(Product.category.slug == category_slug)
    )


async def get_product_with_ingredients_by_slug(category_slug, product_slug: str) -> dict:
    return await (
        Product.select(
                Product.all_columns(),
                Product.category.name, Product.category.slug,
                Product.ingredients(Ingredient.name, as_list=True)
            )
        .where(
                Product.slug == product_slug,
                Product.category.slug == category_slug
            )
        .first()
    )


async def get_product_with_ingredients_full_by_slug(category_slug, product_slug: str) -> dict:
    return await (
        Product.select(
                Product.all_columns(),
                Product.category.name, Product.category.slug,
                Product.ingredients()
            )
        .where(
                Product.slug == product_slug,
                Product.category.slug == category_slug
            )
        .first()
    )


async def create_table_reservation(
    name: str,
    phone: str,
    number_of_guests: int,
    date: datetime.date,
    message: str
) -> TableReservation:
    return await TableReservation.insert(
        TableReservation(
            name=name,
            phone=phone,
            number_of_guests=number_of_guests,
            date=date,
            message=message
        )
    )


async def get_user(user_id: str | int) -> dict:
    return await (
        User.select()
        .where(User.id == user_id)
        .first()
    )


async def login_user(phone: str) -> dict | None:
    user = await (
        User.select()
        .where(User.phone == phone)
        .first()
    )
    return user if user else None


async def create_user(name: str, phone: str) -> dict | None:
    try:
        users_insert = await (
            User.insert(
                User(
                    name=name,
                    phone=phone
                )
            )
        )
        new_user = users_insert[0]
        await Cart.insert(
            Cart(user=new_user['id'])
        )
        return new_user
    except Exception:
        raise
        return None


async def get_reviews() -> list[dict]:
    return await (
        Review.select(Review.all_columns(), Review.user.name)
    )


async def create_review(user_id: str, stars: int, message: str) -> dict:
    return await (
        Review.insert(
            Review(
                user=user_id,
                stars=stars,
                message=message
            )
        )
    )


async def get_cart(user_id: int) -> list[dict]:
    return await (
        CartToProduct.select(
            CartToProduct.product.all_columns(),
            CartToProduct.amount,
            CartToProduct.cart.id,
            CartToProduct.product.category.all_columns()
        )
        .where(CartToProduct.cart.user == user_id)
    )


async def get_cart_product(product_id: int, user_id: int) -> dict | None:
    return await (
        CartToProduct.select(CartToProduct.all_columns(), CartToProduct.product.all_columns())
        .where(CartToProduct.product.id == product_id, CartToProduct.cart.user.id == user_id)
        .first()
    )


async def add_product_to_cart(product_id: int, user_id: str) -> dict | None:
    cart = await Cart.select().where(Cart.user == user_id).first()
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
