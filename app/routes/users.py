from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..db.models import User, Reply, Like
from ..db.connection import connect_db
from ..schemas.user import UserSchema, UserProfileSchema
from ..auth.token import get_current_user
from ..auth.helper import get_pw_hash

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/new", status_code=status.HTTP_201_CREATED)
def create_user(user: UserSchema, db: Session = Depends(connect_db)):
    """
    Create new user account

    Arguments:

    user -- contains username and password,

    db -- current database connection through SQLAlchemy
    """
    duplicate = db.query(User).filter(User.username == user.username).first()
    if duplicate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error: Username {user.username} is already taken.",
        )

    hashed_pw = get_pw_hash(user.password)
    user.password = hashed_pw
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": f"Created new user {user.username}", "id": new_user.id}


@router.get("/", response_model=UserProfileSchema)
def get_user(
    current_user: dict = Depends(get_current_user), db: Session = Depends(connect_db)
):
    """
    Retrieve user information. Meant to be used for displaying user's profile.
    """
    user = (
        db.query(User, func.count(Like.reply_id).label("likes"))
        .outerjoin(Reply, Reply.author_id == User.id)
        .outerjoin(Like, Like.reply_id == Reply.id)
        .group_by(User.id)
        .filter(User.id == current_user.id)
        .first()
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cannot find user with {current_user.id}",
        )
    return user


@router.delete("/close-account", status_code=status.HTTP_204_NO_CONTENT)
def close_account(
    current_user: dict = Depends(get_current_user), db: Session = Depends(connect_db)
):
    """Deletes the current user's account"""
    user_query = db.query(User).filter(User.id == current_user.id)
    user = user_query.first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cannot find user with id: {current_user.id}",
        )

    user_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
