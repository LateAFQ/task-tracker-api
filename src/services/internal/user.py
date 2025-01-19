import uuid
from typing import Optional

from src.common import dtos
from src.common.exceptions import ConflictError, NotFoundError
from src.common.interfaces.hasher import AbstractHasher
from src.database.converter import from_model_to_dto
from src.database.models.types import _UserLoadsType
from src.database.repositories import UserRepository
from src.database.tools import on_integrity


class UserService:
    __slots__ = ("_repository",)

    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def select(
        self,
        *loads: _UserLoadsType,
        user_uuid: Optional[uuid.UUID] = None,
        login: Optional[str] = None,
    ) -> dtos.PrivateUser:
        result = await self._repository.select(*loads, user_uuid=user_uuid, login=login)
        if not result:
            raise NotFoundError("User not found")

        return from_model_to_dto(result, dtos.PrivateUser)

    @on_integrity("login")
    async def create(
        self, login: str, password: str, role_uuid: uuid.UUID, hasher: AbstractHasher
    ) -> dtos.PrivateUser:
        hashed_password = hasher.hash_password(password)
        result = await self._repository.create(
            login=login, password=hashed_password, role_uuid=role_uuid
        )

        if not result:
            raise ConflictError("This user already exists")

        return from_model_to_dto(result, dtos.PrivateUser)

    async def update(
        self,
        hasher: AbstractHasher,
        user_uuid: uuid.UUID,
        role_uuid: Optional[uuid.UUID],
        login: Optional[str],
        password: Optional[str],
    ) -> dtos.PrivateUser:
        if password:
            hashed_password = hasher.hash_password(plain=password)

        result = await self._repository.update(
            user_uuid, role_uuid=role_uuid, login=login, password=hashed_password
        )

        if not result:
            raise ConflictError("Cannot update user")

        return from_model_to_dto(result, dtos.PrivateUser)

    async def delete(
        self, login: Optional[str] = None, user_uuid: Optional[uuid.UUID] = None
    ) -> dtos.PrivateUser:
        result = await self._repository.delete(login=login, user_uuid=user_uuid)

        if not result:
            raise ConflictError("Cannot delete user")

        return from_model_to_dto(result, dtos.PrivateUser)
