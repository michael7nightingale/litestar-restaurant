import datetime

from .tables import Ingredient, Product, Category, TableReservation, User


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
        return await (
            User.insert(
                User(
                    name=name,
                    phone=phone
                )
            )
        )
    except:
        return None
