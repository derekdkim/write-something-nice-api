from datetime import datetime
from pydantic import BaseModel


class UserSchema(BaseModel):
    """Schema for user."""

    username: str
    password: str


class UserResSchema(BaseModel):
    """Response Schema for user. Excludes password but returns other information."""

    username: str
    created_at: datetime
    id: int
    # TODO: Get aggregate of likes count

    class Config:
        """Adds compatibility with SQLAlchemy"""

        orm_mode = True
