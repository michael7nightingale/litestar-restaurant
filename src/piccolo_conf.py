from piccolo.conf.apps import AppRegistry
from db.config import DB


APP_REGISTRY = AppRegistry(
    apps=["db.piccolo_app"]
)


