import uuid
from typing import Optional

from src.common import dtos
from src.common.exceptions import ConflictError, NotFoundError
from src.database.converter import from_model_to_dto
from src.database.models.types import PermissionType, _RoleLoadsType
from src.database.repositories import RoleRepository
from src.database.tools import on_integrity


class RoleService:
    __slots__ = ("_repository",)

    def __init__(self, repository: RoleRepository) -> None:
        self._repository = repository

    async def select(
        self,
        *loads: _RoleLoadsType,
        role_uuid: Optional[uuid.UUID] = None,
        name: Optional[PermissionType] = None,
    ) -> dtos.Role:
        result = await self._repository.select(*loads, role_uuid=role_uuid, name=name)
        if not result:
            raise NotFoundError("Role not found")

        return from_model_to_dto(result, dtos.Role)

    @on_integrity("name")
    async def create(self, name: PermissionType) -> dtos.Role:
        result = await self._repository.create(name=name)

        if not result:
            raise ConflictError("This role already exists")

        return from_model_to_dto(result, dtos.Role)
