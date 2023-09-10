from litestar import Litestar

from internal.core.app import App


def create_app() -> Litestar:
    return App().app
