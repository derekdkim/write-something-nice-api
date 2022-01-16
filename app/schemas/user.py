from pydantic import BaseModel
from datetime import datetime

class UserSchema(BaseModel):
    """Schema for User"""
    username: str
    password: str

class UserResSchema(BaseModel):
    username: str
    created_at: datetime
    id: int
    # TODO: Get aggregate of likes count

    class Config:
        """Adds compatibility with SQLAlchemy"""
        orm_mode = True
