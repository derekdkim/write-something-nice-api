from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

from ..db.models import Reply, Like
from ..db.connection import connect_db
from ..schemas.like import LikeSchema
from ..auth.token import get_current_user

router = APIRouter(prefix="/like", tags=["Likes"])


@router.post("/")
def like_reply(
    like: LikeSchema,
    db: Session = Depends(connect_db),
    current_user: dict = Depends(get_current_user),
):
    """Like or Revert Like on a Particular Reply"""
    try:
        reply = db.query(Reply).filter(Reply.id == like.reply_id).first()
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error: Something went wrong while fetching parent reply data,",
        )

    if int(reply.author_id) == int(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Authors of a reply cannot like their own work,",
        )
    try:
        like_query = db.query(Like).filter(
            Like.reply_id == like.reply_id, Like.user_id == current_user.id
        )
        like_result = like_query.first()
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error: Something went wrong while fetching like data,",
        )

    if like.cmd == 1:
        if like_result:
            # already exists
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {current_user.username} has already liked this reply,",
            )
        else:
            # Good to proceed
            try:
                new_like = Like(reply_id=like.reply_id, user_id=current_user.id)
                db.add(new_like)
                db.commit()
                return {"message": "successfully liked the reply."}
            except:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error: Something went wrong while liking the reply,",
                )
    else:
        if not like_result:
            # Trying to delete but it doesn't exist
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Like does not exist,",
            )
        else:
            like_query.delete(synchronize_session=False)
            db.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
