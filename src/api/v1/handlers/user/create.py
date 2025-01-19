from typing import Any

from src.api.v1.handlers.base import BaseHandler
from src.common import dtos
from src.common.interfaces.hasher import AbstractHasher
from src.services import InternalServiceGateway


class CreateUserHandler(BaseHandler[dtos.CreateUser, dtos.PublicUser]):
    __slots__ = ("_internal_gateway",)

    def __init__(
        self, internal_gateway: InternalServiceGateway, hasher: AbstractHasher
    ) -> None:
        self._internal_gateway = internal_gateway
        self.user = internal_gateway.user()
        self.role = internal_gateway.role()
        self.hasher = hasher

    async def handle(self, query: dtos.CreateUser, **kwargs: Any) -> dtos.PublicUser:
        async with self._internal_gateway:
            role = await self.role.select(name="User")
            user = await self.user.create(
                login=query.login,
                password=query.password,
                role_uuid=role.uuid,
                hasher=self.hasher,
                **kwargs,
            )
            return dtos.PublicUser(**user.model_dump())
