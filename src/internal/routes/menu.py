from litestar import Controller, get
from litestar.response import Template

from db.tables import Category, Product


class MenuController(Controller):

    path = "/menu"

    @get(name="menu")
    async def menu(self) -> Template:
        context = {
            "categories": await Category.select()
        }
        return Template("menu.html", context=context)

    @get("/{category_slug:str}", name="category")
    async def category(self, category_slug: str) -> Template:
        context = {
            "products": await Product.select().where(Product.category.slug == category_slug)
        }
        return Template("category.html", context=context)

