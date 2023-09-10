from piccolo.conf.apps import AppRegistry
from piccolo.engine import SQLiteEngine

APP_REGISTRY = AppRegistry(
    apps=["db.piccolo_app"]
)

DB = SQLiteEngine(path="db.sqlite3")
