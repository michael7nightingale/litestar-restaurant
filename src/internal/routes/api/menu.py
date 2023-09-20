from litestar import Controller, get
from litestar.di import Provide

from internal.dependencies.menu import get_product, get_category
from schemas.menu import CategorySchema, ProductSchema, CategoryListSchema
from repositories.menu import (
    get_all_categories,
    get_products_by_category_slug,

)


class MenuController(Controller):
    path = "/menu"

    @get()
    async def get_menu(self) -> list[CategoryListSchema]:
        return [
            CategoryListSchema(**category)
            for category in await get_all_categories()
        ]

    @get("/{category_slug:str}", dependencies={"category": Provide(get_category)})
    async def get_category(self, category: dict) -> CategorySchema:
        return CategorySchema(
            **category,
            products=await get_products_by_category_slug(category["slug"])
        )

    @get("/{category_slug:str}/{product_slug:str}", dependencies={'product': Provide(get_product)})
    async def get_product(self, product: dict) -> ProductSchema:
        return ProductSchema(**product)
