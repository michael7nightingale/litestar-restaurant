from litestar import Controller, get
from litestar.exceptions import HTTPException

from schemas.menu import CategorySchema, ProductSchema, CategoryListSchema
from db.services import (
    get_all_categories,
    get_category_by_slug,
    get_products_by_category_slug,
    get_product_with_ingredients_full_by_slug,

)


class MenuController(Controller):
    path = "/menu"

    @get()
    async def get_menu(self) -> list[CategoryListSchema]:
        return [
            CategoryListSchema(**category)
            for category in await get_all_categories()
        ]

    @get("/{category_slug:str}")
    async def get_category(self, category_slug: str) -> CategorySchema:
        category = await get_category_by_slug(category_slug)
        if not category:
            raise HTTPException(
                detail=f"Category {category_slug} does not exist.",
                status_code=404
            )
        return CategorySchema(
            **category,
            products=await get_products_by_category_slug(category_slug)
        )

    @get("/{category_slug:str}/{product_slug:str}")
    async def get_product(self, category_slug: str, product_slug: str) -> ProductSchema:
        product = await get_product_with_ingredients_full_by_slug(category_slug, product_slug)
        return ProductSchema(**product)
