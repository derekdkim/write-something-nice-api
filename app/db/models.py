from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from ..db.connection import Base

class Post(Base):
    """SQLAlchemy Table Declaration for Posts"""
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    author_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    author = relationship("User")

class Reply(Base):
    """SQLAlchemy Table Declaration for Replies"""
    __tablename__ = "replies"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    author_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    author = relationship("User")

    post_id = Column(
        Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False
    )
    post = relationship("Post")

class Like(Base):
    """SQLAlchemy Table Declaration for records of users liking replies"""
    __tablename__ = "likes"

    # Composite keys
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, primary_key=True
    )
    reply_id = Column(
        Integer, ForeignKey("replies.id", ondelete="CASCADE"), nullable=False, primary_key=True
    )

class User(Base):
    """SQLAlchemy Table Declaration for Users"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
