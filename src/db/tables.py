from piccolo.apps.user.tables import BaseUser
from piccolo_admin.example import Sessions
from piccolo.table import Table
from piccolo.columns import Varchar, Text, ForeignKey, Integer, M2M, LazyTableReference, Date, Boolean

from .config import DB


class User(Table, db=DB):
    name = Varchar(required=True)
    phone = Varchar(index=True, required=True)

    def __str__(self):
        return self.name


class Category(Table, db=DB):
    name = Varchar(index=True)
    slug = Varchar(index=True)

    image_path = Varchar()

    def __str__(self):
        return self.name


class Ingredient(Table, db=DB):
    name = Varchar(length=50, index=True, unique=True)
    products = M2M(LazyTableReference("IngredientToProduct", app_name="db"))


class Product(Table, db=DB):
    name = Varchar(index=True)
    description = Text()
    category = ForeignKey(Category)
    slug = Varchar(index=True)
    price = Integer()
    discount = Integer(null=True)
    has_ingredients = Boolean(default=True)
    ingredients = M2M(LazyTableReference("IngredientToProduct", app_name="db"))
    caloricity = Integer(null=True)    # в КДж
    weight = Integer(null=True)        # в граммах
    volume = Integer(null=True)        # в мл
    image_path = Varchar()

    @property
    def total_price(self) -> int:
        if self.discount:
            return int(self.price * (1 - (self.discount / 100)))
        return self.price

    @property
    def show_price(self) -> str:
        return f"{self.total_price} ₽"

    def __str__(self):
        return self.name


class IngredientToProduct(Table, db=DB):
    ingredient = ForeignKey(Ingredient)
    product = ForeignKey(Product)


class Review(Table, db=DB):
    user = ForeignKey(User)
    text = Text()
    stars = Integer()


class TableReservation(Table, db=DB):
    name = Varchar(length=100)
    phone = Varchar(length=20)
    number_of_guests = Integer()
    date = Date()
    message = Text()


table_list = [
    User, Product, Category, Review,
    BaseUser, Sessions,
    IngredientToProduct, Ingredient,
    TableReservation,

]
