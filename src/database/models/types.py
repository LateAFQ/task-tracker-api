from enum import StrEnum
from typing import Literal

_RoleLoadsType = Literal["user",]
_UserLoadsType = Literal["role"]


class RoleType(StrEnum):
    ADMIN = "Admin"
    USER = "User"


PermissionType = Literal["Admin", "User"]
