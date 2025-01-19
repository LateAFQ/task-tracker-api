from typing import TYPE_CHECKING

from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.common.tools.text import pascal_to_snake
from src.database.models import Base, types
from src.database.models.base.mixins import ModelWithTimeMixin, ModelWithUUIDMixin

if TYPE_CHECKING:
    from src.database.models import User


class Role(ModelWithUUIDMixin, ModelWithTimeMixin, Base):
    name: Mapped[types.RoleType] = mapped_column(
        Enum(
            types.RoleType,
            native_enum=False,
            values_callable=lambda x: [e.value for e in x],
            name=pascal_to_snake(types.RoleType),
        ),
        index=True,
    )

    users: Mapped[list["User"]] = relationship(
        "User",
        back_populates="role",
        primaryjoin="Role.uuid == foreign(User.role_uuid)",
    )
