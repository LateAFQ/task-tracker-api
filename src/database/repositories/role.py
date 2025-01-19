import uuid
from typing import Optional, Unpack

from sqlalchemy import ColumnExpressionArgument

import src.database.models as models
from src.database.exceptions import InvalidParamsError
from src.database.models import types
from src.database.models.types import PermissionType
from src.database.repositories.base import BaseRepository
from src.database.repositories.types import CreateRoleType
from src.database.tools import select_with_relationships


class RoleRepository(BaseRepository[models.Role]):
    __slots__ = ()

    @property
    def model(self) -> type[models.Role]:
        return models.Role

    async def create(self, **data: Unpack[CreateRoleType]) -> Optional[models.Role]:
        return await self._crud.insert(**data)

    async def select(
        self,
        *loads: types._RoleLoadsType,
        role_uuid: Optional[uuid.UUID] = None,
        name: Optional[PermissionType] = None,
    ) -> Optional[models.Role]:
        if not any([role_uuid, name]):
            raise InvalidParamsError("at least one identifier must be provided")

        where_clauses: list[ColumnExpressionArgument[bool]] = []

        if role_uuid:
            where_clauses.append(self.model.uuid == role_uuid)
        if name:
            where_clauses.append(self.model.name == name)

        stmt = select_with_relationships(*loads, model=self.model).where(*where_clauses)
        return (await self._session.execute(stmt)).scalars().first()
