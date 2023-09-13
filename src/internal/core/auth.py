from datetime import datetime, timedelta

from litestar.connection import ASGIConnection
from litestar.types import Send, Scope, Receive, ASGIApp
from litestar import Request, Response
from litestar.response import Redirect
from litestar.middleware import MiddlewareProtocol
from litestar.exceptions import HTTPException

from pydantic import BaseModel

from settings import get_settings
from db.services import get_user
from jose import jwt, JWTError


class Token(BaseModel):
    user_id: str | int
    exp: datetime


class User(BaseModel):
    name: str


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
    async def inner(request: Request, *args, **kwargs):
        res = await func(request, *args, **kwargs)
        return res
    return inner


def login_user(request: Request, user_id: str) -> None:
    token = encode_jwt_token(user_id)
    request.cookies["authorization"] = token


def logout_user(request: Request) -> None:
    if "authorization" in request.cookies:
        del request.cookies['authorization']


class AuthenticationMiddleware(MiddlewareProtocol):
    def __init__(self, app: "ASGIApp") -> None:
        self.app = app

    def get_token(self, connection: ASGIConnection) -> str | None:
        token = connection.cookies.get('authorization')
        if token is None:
            return
        return token

    async def __call__(self, scope: "Scope", receive: "Receive", send: "Send") -> None:
        token = self.get_token(ASGIConnection(scope, receive, send))
        if token is not None:
            token_model = decode_jwt_token(token)
            if token_model is not None:
                user_data = await get_user(token_model.user_id)
                user = User(**user_data)
                scope['user'] = user
        await self.app(scope, receive, send)
