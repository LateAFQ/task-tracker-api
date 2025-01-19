from typing import Any

from src.api.common.cache.redis import RedisCache
from src.api.common.security.jwt import JWT
from src.api.v1.handlers.base import BaseHandler
from src.common import dtos
from src.common.dtos.base import DTO
from src.common.exceptions import (
    ForbiddenError,
    ServiceNotImplementedError,
    UnAuthorizedError,
)
from src.database.models.types import PermissionType
from src.services import InternalServiceGateway


class PermissionQuery(DTO):
    permissions: tuple[PermissionType | None, ...]
    access_token: str | None
    refresh_token: str


class PermissionHandler(BaseHandler[PermissionQuery, dtos.PrivateUser]):
    def __init__(
        self,
        internal_gateway: InternalServiceGateway,
        jwt: JWT,
        redis: RedisCache,
    ) -> None:
        self._internal_gateway = internal_gateway
        self.user = internal_gateway.user()
        self.auth = internal_gateway.auth(jwt, redis)

    async def handle(self, query: PermissionQuery, **kwargs: Any) -> dtos.PrivateUser:
        if query.access_token:
            user_uuid = await self.auth.verify_token(query.access_token, "access")
        else:
            user_uuid = await self.auth.verify_token(query.refresh_token, "refresh")

        async with self._internal_gateway.database.manager.session:
            user = await self.user.select("role", user_uuid=user_uuid, **kwargs)

        if not user.active:
            raise ForbiddenError("You have been blocked")
        if not user.role:
            raise ServiceNotImplementedError("Role not found")
        if allowed_roles := query.permissions:
            if user.role.name not in allowed_roles:
                raise UnAuthorizedError("Not Allowed")

        user.access_token = query.access_token
        user.refresh_token = query.refresh_token
        return user
