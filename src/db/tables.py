from piccolo.apps.user.tables import BaseUser
from piccolo_admin.example import Sessions
from piccolo.table import Table
from piccolo.columns import Varchar, Text, ForeignKey, Integer

from .config import DB


class User(Table, db=DB):
    name = Varchar(required=True)
    phone = Varchar(index=True, required=True)

    def __str__(self):
        return self.name


class Category(Table, db=DB):
    name = Varchar(index=True)
    slug = Varchar(index=True)

    def __str__(self):
        return self.name


class Product(Table, db=DB):
    name = Varchar(index=True)
    description = Text()
    category = ForeignKey(references=Category)
    slug = Varchar(index=True)
    price = Integer()
    discount = Integer(null=True)
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


class Review(Table, db=DB):
    user = ForeignKey(references=User)
    text = Text()
    stars = Integer()


table_list = [User, Product, Category, Review, BaseUser, Sessions]
