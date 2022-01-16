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

class UserProfileSchema(BaseModel):
    """
    Pydantic schema for a complete user profile.
    Currently returns UserResSchema and an aggregate likes acount.
    """
    User: UserResSchema
    likes: int
    class Config:
        """Adds compatibility with SQLAlchemy"""
        orm_mode = True
