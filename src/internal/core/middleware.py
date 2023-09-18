from litestar.connection import ASGIConnection
from litestar.middleware import MiddlewareProtocol
from litestar.types import Scope, Receive, Send, ASGIApp


class PaginationMiddleware(MiddlewareProtocol):
    """Saves current and PREVIOUS url to cookies."""

    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        conn = ASGIConnection(scope, receive, send)
        http_request_method = scope.get('method')
        if http_request_method == "GET":
            current_url = conn.cookies.get("current-url")
            if current_url is None:
                previous_url = conn.app.route_reverse("homepage")
            else:
                previous_url = current_url
            current_url = conn.url.path
            conn.cookies["current-url"] = current_url
            conn.cookies['previous-url'] = previous_url
        await self.app(scope, receive, send)
