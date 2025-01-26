from sqlalchemy import Column, ForeignKey, Table

from src.database.models.base.core import Base

task_category_association = Table(
    "task_category_association",
    Base.metadata,
    Column("task_uuid", ForeignKey("task.uuid"), primary_key=True),
    Column("category_uuid", ForeignKey("task_category.uuid"), primary_key=True),
)


