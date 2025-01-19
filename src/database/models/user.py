import uuid
from typing import TYPE_CHECKING

from sqlalchemy import BOOLEAN, UUID, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import Index

from src.database.models import Base
from src.database.models.base.mixins import ModelWithTimeMixin, ModelWithUUIDMixin

if TYPE_CHECKING:
    from src.database.models import Role


class User(ModelWithUUIDMixin, ModelWithTimeMixin, Base):
    login: Mapped[str] = mapped_column(String, index=True, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    active: Mapped[bool] = mapped_column(BOOLEAN, default=True, nullable=False)
    role_uuid: Mapped[uuid.UUID] = mapped_column(
        UUID(True), ForeignKey("role.uuid", ondelete="RESTRICT", name="fk_user_role")
    )

    role: Mapped["Role | None"] = relationship(
        "Role",
        back_populates="users",
        primaryjoin="foreign(User.role_uuid) == Role.uuid",
    )

    __table_args__ = (Index("idx_lower_login", func.lower(login), unique=True),)
