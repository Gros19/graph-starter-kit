"""Thread ORM model."""
from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.persistence.database import BaseModel


class Thread(BaseModel):
    """Represents a conversation thread."""
    __tablename__ = "threads"

    title: Mapped[str | None] = mapped_column(String(500), nullable=True)
    metadata_: Mapped[dict] = mapped_column(JSON, default=dict, name="metadata")
