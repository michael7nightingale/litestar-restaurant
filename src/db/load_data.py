import csv
from slugify import slugify
from .tables import Category, Product
from schemas.menu import CategoryListSchema, ProductListSchema


async def load_categories():
    with open("db/data/categories.csv") as csv_file:
        lines = list(csv.DictReader(csv_file))

    for line in lines:
        try:
            line = {k: v if v else None for k, v in line.items()}
            await Category.insert(Category(**CategoryListSchema(**line).dict()))
        except Exception as e:
            pass


async def load_products():
    with open("db/data/products.csv") as csv_file:
        lines = list(csv.DictReader(csv_file))

    for line in lines:
        try:
            line = {k: v if v else None for k, v in line.items()}
            line["slug"] = slugify(line['name'])
            await Product.insert(Product(**ProductListSchema(**line).dict()))
        except Exception as e:
            pass


async def load_data():
    await load_categories()
    await load_products()
