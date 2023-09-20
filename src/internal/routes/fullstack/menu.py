from litestar import Controller, get, post, Request
from litestar.di import Provide
from litestar.response import Template, Redirect

from repositories.menu import get_all_categories, get_products_by_category_slug
from repositories.cart import add_product_to_cart
from internal.dependencies.menu import get_product, get_category


class MenuController(Controller):

    path = "/menu"

    @get(name="menu")
    async def menu(self) -> Template:
        context = {
            "categories": await get_all_categories()
        }
        return Template("menu.html", context=context)

    @get(
        "/{category_slug:str}",
        name="category",
        dependencies={"category": Provide(get_category)}
    )
    async def category(self, request: Request, category: dict) -> Template:
        context = {
            "category": category,
            "products": await get_products_by_category_slug(category["slug"])
        }
        return Template("category.html", context=context)

    @get(
        "/{category_slug:str}/{product_slug:str}",
        name="product",
        dependencies={'product': Provide(get_product)}
    )
    async def product(self, product: dict) -> Template:
        context = {
            "product": product
        }
        return Template("product.html", context=context)

    @post(
        "/{category_slug:str}/{product_slug:str}",
        name="product_post",
        dependencies={'product': Provide(get_product)},
        status_code=303
    )
    async def product_add_to_cart(self, request: Request, product: dict) -> Redirect:
        if not request.user:
            return Redirect(request.app.route_reverse("login"))
        await add_product_to_cart(product['id'], request.user.id)
        return Redirect(request.app.route_reverse(
            "product",
            category_slug=product['category.slug'],
            product_slug=product['slug'],
        ))
