from datetime import datetime
from pydantic import BaseModel


class PostBaseSchema(BaseModel):
    """Pydantic schema for post input. Acts as base class for other post schemas."""

    title: str
    content: str


class PostResSchema(PostBaseSchema):
    """Pydantic schema for post response."""

    created_at: datetime
    author_id: int

    class Config:
        """Allows schema to be compatible with SQLAlchemy"""
        orm_mode = True
