import uuid
from typing import NotRequired, Required, TypedDict


class CreateUserType(TypedDict):
    login: Required[str]
    password: Required[str]
    role_uuid: uuid.UUID


class UpdateUserType(TypedDict):
    login: NotRequired[str | None]
    password: NotRequired[str | None]
    role_uuid: NotRequired[uuid.UUID | None]
