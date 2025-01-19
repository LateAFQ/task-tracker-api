from typing import TypedDict

from src.database.models.types import PermissionType


class CreateRoleType(TypedDict):
    name: PermissionType
