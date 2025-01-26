from enum import Enum, StrEnum
from typing import Literal

_RoleLoadsType = Literal["user",]
_UserLoadsType = Literal["role"]


class RoleType(StrEnum):
    ADMIN = "Admin"
    USER = "User"

class TaskPriority(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

PermissionType = Literal["Admin", "User"]

