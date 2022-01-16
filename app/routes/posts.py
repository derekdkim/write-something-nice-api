from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

from ..db.models import Post, Reply
from ..db.connection import connect_db
from ..schemas.post import PostBaseSchema, PostResSchema
from ..auth.token import get_current_user

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/current-user", response_model=List[PostResSchema])
def get_my_posts(
    db: Session = Depends(connect_db), current_user: dict = Depends(get_current_user)
):
    """Retrieves the user's own posts in reverse chronological order."""

    try:
        posts = (
            db.query(Post)
            .filter(Post.author_id == current_user.id)
            .order_by(desc(Post.created_at))
            .all()
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve posts",
        )

    return posts


@router.get("/active", response_model=List[PostResSchema])
def get_other_posts(
    db: Session = Depends(connect_db), current_user: dict = Depends(get_current_user)
):
    """Retrieves all unanswered posts written by other users in reverse chronological order."""
    try:
        posts = (
            db.query(Post)
            .outerjoin(Reply, Reply.post_id == Post.id)
            .filter(Post.author_id != current_user.id)
            .filter(
                Reply.post_id == None
            )  # Cannot use is None or it won't query properly
            .order_by(desc(Post.created_at))
            .all()
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve posts",
        )

    return posts

@router.get("/random", response_model=PostResSchema)
def get_random_post(
    db: Session = Depends(connect_db), current_user: dict = Depends(get_current_user)
):
    """Retrieves a random unanswered post."""
    try:
        post = (
            db.query(Post)
            .outerjoin(Reply, Reply.post_id == Post.id)
            .filter(Post.author_id != current_user.id)
            .filter(
                Reply.post_id == None
            )  # Cannot use is None or it won't query properly
            .order_by(func.random())
            .first()
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve posts",
        )

    return post


@router.post("/new", status_code=status.HTTP_201_CREATED, response_model=PostResSchema)
def create_post(
    post: PostBaseSchema,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(connect_db),
):
    """Creates new post. Returns the contents of new post as a response"""
    try:
        new_post = Post(author_id=current_user.id, **post.dict())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error: Failed to create new post.",
        )
    return new_post
