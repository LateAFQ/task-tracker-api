from typing import Any, Final

from fastapi.concurrency import run_in_threadpool

from src.api.common.cache.redis import RedisCache
from src.api.common.security.jwt import JWT
from src.api.v1.handlers.base import BaseHandler
from src.common import dtos
from src.common.dtos.base import DTO
from src.common.exceptions import (
    ForbiddenError,
    UnAuthorizedError,
)
from src.common.interfaces.hasher import AbstractHasher
from src.services import InternalServiceGateway

DEFAULT_TOKENS_COUNT: Final[int] = 5


class LoginQuery(DTO):
    login: str
    password: str
    fingerprint: str


class LoginHandler(BaseHandler[LoginQuery, dtos.TokensExpire]):
    def __init__(
        self,
        internal_gateway: InternalServiceGateway,
        hasher: AbstractHasher,
        jwt: JWT,
        redis: RedisCache,
    ) -> None:
        self._internal_gateway = internal_gateway
        self.user = internal_gateway.user()
        self.cache = redis
        self.jwt = jwt
        self.hasher = hasher

    async def handle(self, query: LoginQuery, **kwargs: Any) -> dtos.TokensExpire:
        async with self._internal_gateway.database.manager.session:
            user = await self.user.select(login=query.login)

        if not user.active:
            raise ForbiddenError("You have been blocked")
        if not self.hasher.verify_password(user.password, query.password):
            raise UnAuthorizedError("Incorrect password")

        _, access = await run_in_threadpool(
            self.jwt.create, typ="access", sub=str(user.uuid)
        )
        expire, refresh = await run_in_threadpool(
            self.jwt.create, typ="refresh", sub=str(user.uuid)
        )
        tokens = await self.cache.get_list(str(user.uuid))

        if len(tokens) > DEFAULT_TOKENS_COUNT:
            await self.cache.delete(str(user.uuid))

        await self.cache.set_list(
            str(user.uuid), f"{query.fingerprint}::{refresh.token}"
        )

        return dtos.TokensExpire(
            refresh_expire=expire,
            tokens=dtos.Tokens(access=access.token, refresh=refresh.token),
        )
