from __future__ import annotations

import uuid
from typing import Optional

from src.common.dtos.base import DTO
from src.common.dtos.role import Role


class PublicUser(DTO):
    uuid: uuid.UUID
    login: str


class PrivateUser(PublicUser):
    password: str
    active: bool

    # Permission data
    refresh_token: str | None = None
    access_token: str | None = None

    # relations
    role: Role | None = None


class CreateUser(DTO):
    login: str
    password: str


class UpdateUserQuery(DTO):
    user_uuid: uuid.UUID
    login: Optional[str] = None
    password: Optional[str] = None


class UpdateUser(DTO):
    login: Optional[str] = None
    password: Optional[str] = None


class DeleteUser(DTO):
    user_uuid: Optional[uuid.UUID] = None
    login: Optional[str] = None


class SelectUser(DeleteUser):
    pass


class Fingerprint(DTO):
    fingerprint: str


class UserLogin(Fingerprint):
    login: str
    password: str
