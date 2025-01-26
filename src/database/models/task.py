import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base.core import Base
from src.database.models.base.mixins import ModelWithUUIDMixin
from src.database.models.task_category import TaskCategory
from src.database.models.task_category_association import task_category_association
from src.database.models.types import TaskPriority

if TYPE_CHECKING:
    from src.database.models import TaskCategory, User


class Task(ModelWithUUIDMixin, Base):
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    priority: Mapped[TaskPriority] = mapped_column(
        Enum(TaskPriority), nullable=False, default=TaskPriority.LOW
    )
    categories: Mapped["TaskCategory | None"] = relationship(
        "TaskCategory",
        secondary=task_category_association,
        back_populates="tasks",
    )
    user_uuid: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.uuid", ondelete="CASCADE", name="fk_task_user"),
        nullable=False,
    )

    users: Mapped["User"] = relationship("User", back_populates="tasks")
