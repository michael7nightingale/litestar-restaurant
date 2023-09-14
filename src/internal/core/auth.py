from litestar.connection import ASGIConnection
from litestar.types import Send, Scope, Receive, ASGIApp
from litestar import Request, Response
from litestar.response import Redirect
from litestar.middleware import AbstractAuthenticationMiddleware, AuthenticationResult
from litestar.exceptions import HTTPException

from datetime import datetime, timedelta
from jose import jwt, JWTError

from settings import get_settings
from db.services import get_user
from schemas.token import Token, ScopeUser


def encode_jwt_token(user_id) -> str | None:
    settings = get_settings()
    token = Token(
        user_id=user_id,
        exp=datetime.now() + timedelta(minutes=settings.EXPIRE_MINUTES)
    )
    return jwt.encode(
        token.dict(),
        key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def decode_jwt_token(encoded_token: str) -> Token | None:
    settings = get_settings()
    try:
        payload = jwt.decode(
            token=encoded_token,
            key=settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return Token(**payload)
    except JWTError:
        return


def auth_exception_handler(request: Request, exc: HTTPException) -> Response:
    return Redirect(request.app.route_reverse("login"))


def login_required(func):
    async def inner(request: Request, *args, **kwargs) -> Response:
        res = await func(request, *args, **kwargs)
        return res
    return inner


def login_user(request: Request, user_id: str) -> None:
    token = encode_jwt_token(user_id)
    request.cookies["authorization"] = token


def logout_user(request: Request) -> None:
    if "authorization" in request.cookies:
        del request.cookies['authorization']


class AuthenticationMiddleware(AbstractAuthenticationMiddleware):

    def __init__(self, app: "ASGIApp") -> None:
        self.app = app

    def get_token(self, connection: ASGIConnection) -> str | None:
        token = connection.headers.get("authorization") or connection.cookies.get('authorization')
        if token is None:
            return
        return token

    async def authenticate_request(self, connection: ASGIConnection) -> AuthenticationResult:
        token = self.get_token(connection)
        if token is not None:
            token_model = decode_jwt_token(token)
            if token_model is not None:
                user_data = await get_user(token_model.user_id)
                user = ScopeUser(**user_data)
                return AuthenticationResult(
                    user=user,
                    auth=token
                )
        return AuthenticationResult(None, None)

    async def __call__(self, scope: "Scope", receive: "Receive", send: "Send") -> None:
        auth_result = await self.authenticate_request(ASGIConnection(scope, receive, send))
        scope['user'] = auth_result.user
        scope['auth'] = auth_result.auth
        await self.app(scope, receive, send)
