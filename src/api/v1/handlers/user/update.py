import uuid
from typing import Any, Optional

from src.api.v1.handlers.base import BaseHandler
from src.common import dtos
from src.common.dtos.base import DTO
from src.common.interfaces.hasher import AbstractHasher
from src.database.models.types import PermissionType
from src.services import InternalServiceGateway


class UpdateUserQuery(DTO):
    user_uuid: uuid.UUID
    role: Optional[PermissionType] = None
    role_uuid: Optional[uuid.UUID] = None
    login: Optional[str] = None
    password: Optional[str] = None


class UpdateUserHandler(BaseHandler[UpdateUserQuery, dtos.PublicUser]):
    __slots__ = ("_internal_gateway",)

    def __init__(
        self, internal_gateway: InternalServiceGateway, hasher: AbstractHasher
    ) -> None:
        self._internal_gateway = internal_gateway
        self.user = internal_gateway.user()
        self.role = internal_gateway.role()
        self.hasher = hasher

    async def handle(self, query: UpdateUserQuery, **kwargs: Any) -> dtos.PublicUser:
        async with self._internal_gateway:
            if query.role:
                role = await self.role.select(name=query.role)
                query.role_uuid = role.uuid

            result = await self.user.update(
                **query.model_dump(exclude_none=True, exclude={"role"}),
                hasher=self.hasher,
                **kwargs,
            )
            return dtos.PublicUser(**result.model_dump())
