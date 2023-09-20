from litestar.exceptions import HTTPException

from db.services import get_product_with_ingredients_by_slug, get_category_by_slug


async def get_category(category_slug: str) -> dict:
    category = await get_category_by_slug(category_slug)
    if not category:
        raise HTTPException(
            detail=f"Category {category_slug} does not exist.",
            status_code=404
        )
    return category


async def get_product(category_slug: str, product_slug: str) -> dict:
    product = await get_product_with_ingredients_by_slug(category_slug, product_slug)
    if not product:
        raise HTTPException("product not found", status_code=404)
    return product
