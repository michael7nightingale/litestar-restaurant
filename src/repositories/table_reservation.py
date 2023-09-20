import datetime

from db.tables import TableReservation


async def create_table_reservation(
    name: str,
    phone: str,
    number_of_guests: int,
    date: datetime.date,
    message: str
) -> TableReservation:
    return await TableReservation.insert(
        TableReservation(
            name=name,
            phone=phone,
            number_of_guests=number_of_guests,
            date=date,
            message=message
        )
    )
