from typing import Optional
from pydantic import BaseModel

class TokenPayload(BaseModel):
    """Schema for Payload in JWT"""
    id: Optional['str']
    email: Optional['str']
