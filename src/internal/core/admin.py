from litestar import asgi

from piccolo_admin.endpoints import create_admin

from db.tables import table_list


admin = create_admin(table_list, allowed_hosts=["*"])
admin_app = asgi("/admin", is_mount=True)(admin)
