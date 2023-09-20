from db.tables import User, Cart


async def get_user(user_id: str | int) -> dict:
    return await (
        User.select()
        .where(User.id == user_id)
        .first()
    )


async def login_user(phone: str) -> dict | None:
    user = await (
        User.select()
        .where(User.phone == phone)
        .first()
    )
    return user if user else None


async def create_user(name: str, phone: str) -> dict | None:
    try:
        users_insert = await (
            User.insert(
                User(
                    name=name,
                    phone=phone
                )
            )
        )
        new_user = users_insert[0]
        await Cart.insert(
            Cart(user=new_user['id'])
        )
        return new_user
    except Exception:
        return None
