from enum import IntEnum
from pydantic import BaseModel


class LikeCmdSchema(IntEnum):
    """
    Pydantic schema for the "command" given in the like request.
    This value can either be 0 or 1, which results in deletion or creation, respectively.
    """

    delete = 0
    create = 1


class LikeSchema(BaseModel):
    """
    Pydantic schema for likes.
    This value will be counted as an aggregate to count towards the user's reputation.
    cmd acts as certain command for the request to act out, provided the conditions are met.
    """

    reply_id: int
    cmd: LikeCmdSchema
