from pydantic import BaseModel
import datetime


class Reservation(BaseModel):
    name: str
    phone: str
    number_of_guests: int
    date: datetime.date
    message: str
