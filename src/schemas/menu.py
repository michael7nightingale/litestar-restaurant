from pydantic import BaseModel, Field


class ProductListSchema(BaseModel):
    id: int
    name: str
    slug: str
    category: int = Field(alias="category_id")
    price: int
    discount: int | None = None
    has_ingredients: bool
    weight: int | None = None
    caloricity: int | None = None
    volume: int | None = None
    image_path: str | None = None


class CategoryListSchema(BaseModel):
    id: int
    name: str
    slug: str
    image_path: str | None = None


class CategorySchema(CategoryListSchema):
    products: list["ProductListSchema"]


class IngredientSchema(BaseModel):
    id: int
    name: str


class ProductSchema(ProductListSchema):
    ingredients: list["IngredientSchema"]
