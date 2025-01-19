import uuid
from typing import Optional, Unpack

from sqlalchemy import ColumnExpressionArgument

import src.database.models as models
from src.database.exceptions import InvalidParamsError
from src.database.models import types
from src.database.repositories.base import BaseRepository
from src.database.repositories.types import CreateUserType, UpdateUserType
from src.database.tools import select_with_relationships


class UserRepository(BaseRepository[models.User]):
    __slots__ = ()

    @property
    def model(self) -> type[models.User]:
        return models.User

    async def create(self, **data: Unpack[CreateUserType]) -> Optional[models.User]:
        return await self._crud.insert(**data)

    async def select(
        self,
        *loads: types._UserLoadsType,
        user_uuid: Optional[uuid.UUID] = None,
        login: Optional[str] = None,
    ) -> Optional[models.User]:
        if not any([user_uuid, login]):
            raise InvalidParamsError("at least one identifier must be provided")

        where_clauses: list[ColumnExpressionArgument[bool]] = []

        if user_uuid:
            where_clauses.append(self.model.uuid == user_uuid)
        if login:
            where_clauses.append(self.model.login == login)

        stmt = select_with_relationships(*loads, model=self.model).where(*where_clauses)
        return (await self._session.execute(stmt)).scalars().first()

    async def update(
        self,
        uuid: uuid.UUID,
        /,
        **data: Unpack[UpdateUserType],
    ) -> Optional[models.User]:
        if not any([uuid]):
            raise InvalidParamsError("at least one identifier must be provided")

        result = await self._crud.update(self.model.uuid == uuid, **data)
        return result[0] if result else None

    async def delete(
        self, user_uuid: Optional[uuid.UUID] = None, login: Optional[str] = None
    ) -> Optional[models.User]:
        if not any([user_uuid, login]):
            raise InvalidParamsError("at least one identifier must be provided")

        where_clauses: list[ColumnExpressionArgument[bool]] = []

        if user_uuid:
            where_clauses.append(self.model.uuid == user_uuid)
        if login:
            where_clauses.append(self.model.login == login)

        result = await self._crud.delete(*where_clauses)
        return result[0] if result else None
