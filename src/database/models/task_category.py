import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base.core import Base
from src.database.models.base.mixins import ModelWithUUIDMixin
from src.database.models.task_category_association import task_category_association

if TYPE_CHECKING:
    from src.database.models import User
    from src.database.models.task import Task

class TaskCategory(ModelWithUUIDMixin, Base):
    name: Mapped[str]  = mapped_column(String, index=True)
    user_uuid: Mapped[uuid.UUID] = mapped_column(
        UUID(True),
        ForeignKey("user.uuid", ondelete="CASCADE", name="fk_taskcategory_user"),
        nullable=True,
    )

    tasks: Mapped["Task | None"] = relationship(
        "Task",
        secondary=task_category_association,
        back_populates="categories",
    )

    users: Mapped["User"] = relationship("User", back_populates="categories")
