from sqlalchemy import Column, String, Text, CheckConstraint

from .base_model import BaseModel


class CharityProject(BaseModel):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    # __table_args__ = (
    #     CheckConstraint("LENGTH(description) >= 1"),
    # )