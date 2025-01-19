import uuid
from typing import Any

from src.api.v1.handlers.base import BaseHandler
from src.common import dtos
from src.common.dtos.base import DTO
from src.services import InternalServiceGateway


class SelectUserQuery(DTO):
    user_uuid: uuid.UUID | None = None
    login: str | None = None


class SelectUserHandler(BaseHandler[SelectUserQuery, dtos.PublicUser]):
    __slots__ = ("_internal_gateway",)

    def __init__(self, internal_gateway: InternalServiceGateway) -> None:
        self._internal_gateway = internal_gateway
        self.user = internal_gateway.user()

    async def handle(self, query: SelectUserQuery, **kwargs: Any) -> dtos.PublicUser:
        async with self._internal_gateway.database.manager.session:
            result = await self.user.select(
                **query.model_dump(exclude_none=True), **kwargs
            )
            return dtos.PublicUser(**result.model_dump())
