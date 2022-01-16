from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import models, connection
from .routes import users, auth, posts, replies, likes

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=connection.engine)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(replies.router)
app.include_router(likes.router)