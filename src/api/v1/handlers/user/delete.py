import uuid
from typing import Any

from src.api.v1.handlers.base import BaseHandler
from src.common import dtos
from src.common.dtos.base import DTO
from src.services import InternalServiceGateway


class DeleteUserQuery(DTO):
    user_uuid: uuid.UUID | None = None
    login: str | None = None


class DeleteUserHandler(BaseHandler[DeleteUserQuery, dtos.PublicUser]):
    __slots__ = ("_internal_gateway",)

    def __init__(self, internal_gateway: InternalServiceGateway) -> None:
        self._internal_gateway = internal_gateway
        self.user = internal_gateway.user()

    async def handle(self, query: DeleteUserQuery, **kwargs: Any) -> dtos.PublicUser:
        async with self._internal_gateway:
            result = await self.user.delete(
                **query.model_dump(exclude_none=True), **kwargs
            )
            return dtos.PublicUser(**result.model_dump())
