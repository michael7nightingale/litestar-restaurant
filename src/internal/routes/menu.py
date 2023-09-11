from litestar import Controller, get
from litestar.response import Template

from db.services import (
    get_all_categories,
    get_category_by_slug,
    get_products_by_category_slug,
    get_product_with_ingredients_by_slug,

)


class MenuController(Controller):

    path = "/menu"

    @get(name="menu")
    async def menu(self) -> Template:
        context = {
            "categories": await get_all_categories()
        }
        return Template("menu.html", context=context)

    @get("/{category_slug:str}", name="category")
    async def category(self, category_slug: str) -> Template:
        context = {
            "category": await get_category_by_slug(category_slug),
            "products": await get_products_by_category_slug(category_slug)
        }
        return Template("category.html", context=context)

    @get("/{category_slug:str}/{product_slug:str}", name="product")
    async def product(self, category_slug: str, product_slug: str) -> Template:
        context = {
            "product": await get_product_with_ingredients_by_slug(category_slug, product_slug)
        }
        return Template("product.html", context=context)
