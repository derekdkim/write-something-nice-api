from datetime import datetime
from pydantic import BaseModel


class ReplyBaseSchema(BaseModel):
    """Pydantic schema for reply input. Acts as base class for other reply schemas."""

    title: str
    content: str


class ReplyResSchema(ReplyBaseSchema):
    """Pydantic schema for reply response."""

    created_at: datetime
    author_id: int
    post_id: int
    id: int

    class Config:
        """Allows schema to be compatible with SQLAlchemy"""
        orm_mode = True
