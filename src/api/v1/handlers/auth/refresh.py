from typing import Any

from src.api.common.cache.redis import RedisCache
from src.api.common.security.jwt import JWT
from src.api.v1.handlers.base import BaseHandler
from src.common import dtos
from src.common.dtos.base import DTO
from src.common.exceptions import UnAuthorizedError
from src.services import InternalServiceGateway


class RefresTokenQuery(DTO):
    data: dtos.Fingerprint
    user: dtos.PrivateUser


class RefreshTokenHandler(BaseHandler[RefresTokenQuery, dtos.TokensExpire]):
    def __init__(
        self,
        internal_gateway: InternalServiceGateway,
        jwt: JWT,
        redis: RedisCache,
    ) -> None:
        self._internal_gateway = internal_gateway
        self.user = internal_gateway.user()
        self.auth = internal_gateway.auth(jwt, redis)

    async def handle(self, query: RefresTokenQuery, **kwargs: Any) -> dtos.TokensExpire:
        if not (refresh_token := query.user.refresh_token):
            raise UnAuthorizedError("Not allowed")

        return await self.auth.verify_refresh(query.data, refresh_token, query.user)
