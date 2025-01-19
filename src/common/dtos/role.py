from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from src.common.dtos.base import DTO
from src.database.models.types import RoleType

if TYPE_CHECKING:
    from src.common.dtos.user import PrivateUser


class Role(DTO):
    uuid: UUID
    name: RoleType

    # relations
    users: list[PrivateUser] | None = None
