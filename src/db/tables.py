from piccolo.table import Table
from piccolo.columns import Varchar

from .config import DB


class User(Table, db=DB):
    name = Varchar(required=True)
    phone = Varchar(index=True, required=True)
