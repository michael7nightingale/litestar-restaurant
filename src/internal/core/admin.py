from litestar import asgi

from piccolo_admin.endpoints import create_admin, BaseUser

from settings import get_settings
from db.tables import table_list


admin = create_admin(table_list, allowed_hosts=["*"])
admin_app = asgi("/admin", is_mount=True)(admin)


async def create_superuser() -> None:
    settings = get_settings()
    try:
        await BaseUser.create_user(
            username=settings.SUPERUSER_USERNAME,
            password=settings.SUPERUSER_PASSWORD,
            admin=True,
            active=True,
            superuser=True
        )
    except Exception:
        pass
