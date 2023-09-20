from db.tables import Product, Ingredient, Category


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
