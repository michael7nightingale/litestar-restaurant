from litestar.contrib.piccolo import PiccoloDTO

from db.tables import User


UserDTO = PiccoloDTO[User]
