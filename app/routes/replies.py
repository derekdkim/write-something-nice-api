from typing import List
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

from ..db.models import Post, Reply
from ..db.connection import connect_db
from ..schemas.reply import ReplyBaseSchema, ReplyResSchema
from ..auth.token import get_current_user

router = APIRouter(prefix="/replies", tags=["Replies"])


@router.get("/{post_id}", response_model=List[ReplyResSchema])
def get_replies(
    post_id: int,
    db: Session = Depends(connect_db),
    current_user: dict = Depends(get_current_user),
):
    """Retrieves the post's replies."""

    try:
        post = db.query(Post).filter(Post.id == post_id).first()
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve parent post",
        )
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Error: No post exists with id {post_id}.",
        )
    if int(post.author_id) != int(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the author can access their post's replies.",
        )
    try:
        replies = db.query(Reply).filter(Reply.post_id == post_id).all()
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve replies",
        )

    return replies


@router.post(
    "/{post_id}", status_code=status.HTTP_201_CREATED, response_model=ReplyResSchema
)
def create_reply(
    post_id: int,
    reply: ReplyBaseSchema,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(connect_db),
):
    """Creates new reply. Returns the contents of new reply as a response"""
    try:
        parent_post = db.query(Post).filter(Post.id == post_id).first()
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred while searching for parent post.",
        )
    if parent_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Error: No post exists with id {post_id}.",
        )
    if int(parent_post.author_id) == int(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error: The author cannot reply to their post.",
        )
    try:
        new_reply = Reply(author_id=current_user.id, post_id=post_id, **reply.dict())
        db.add(new_reply)
        db.commit()
        db.refresh(new_reply)
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error: Failed to create new reply.",
        )
    return new_reply


@router.put("/{reply_id}", response_model=ReplyResSchema)
def update_reply(
    reply_id: int,
    reply: ReplyBaseSchema,
    db: Session = Depends(connect_db),
    current_user: dict = Depends(get_current_user),
):
    """Edit the user's own reply"""
    ref_reply_query = db.query(Reply).filter(Reply.id == reply_id)
    ref_reply = ref_reply_query.first()
    if ref_reply is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Error: No reply found with id {reply_id}",
        )
    if int(ref_reply.author_id) != int(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Error: User must be the author to update this reply.",
        )

    ref_reply_query.update(reply.dict(), synchronize_session=False)
    db.commit()
    db.refresh(ref_reply)
    return ref_reply


@router.delete("/{reply_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reply(
    reply_id: int,
    db: Session = Depends(connect_db),
    current_user: dict = Depends(get_current_user),
):
    """Delete the user's own reply"""
    ref_reply_query = db.query(Reply).filter(Reply.id == reply_id)
    ref_reply = ref_reply_query.first()
    if ref_reply is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Error: No reply found with id {reply_id}",
        )
    if int(ref_reply.author_id) != int(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Error: User must be the author to delete this post.",
        )

    ref_reply_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
