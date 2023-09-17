from litestar import Controller, get, post, Request
from litestar.di import Provide
from litestar.exceptions import HTTPException
from litestar.response import Template, Redirect

from db.services import (
    get_all_categories,
    get_category_by_slug,
    get_products_by_category_slug,
    get_product_with_ingredients_by_slug, add_product_to_cart,

)


async def get_product(category_slug: str, product_slug: str):
    product = await get_product_with_ingredients_by_slug(category_slug, product_slug)
    if not product:
        raise HTTPException("product not found", status_code=404)
    return product


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

    @get("/{category_slug:str}/{product_slug:str}", name="product", dependencies={'product': Provide(get_product)})
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
