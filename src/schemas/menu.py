from pydantic import BaseModel


class ProductListSchema(BaseModel):
    id: str | int
    name: str
    slug: str
    category: str | int
    price: int
    discount: int | None = None
    has_ingredients: bool
    weight: int | None = None
    caloricity: int | None = None
    volume: int | None = None
    image_path: str | None = None


class CategoryListSchema(BaseModel):
    id: str | int
    name: str
    slug: str
    image_path: str | None = None


class CategorySchema(CategoryListSchema):
    products: list["ProductListSchema"]


class IngredientSchema(BaseModel):
    id: str
    name: str


class ProductSchema(ProductListSchema):
    ingredients: list["IngredientSchema"]
