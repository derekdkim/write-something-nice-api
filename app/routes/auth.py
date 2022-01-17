from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..db.connection import connect_db
from ..db.models import User
from ..auth.helper import verify_pw
from ..auth.token import create_access_token

router = APIRouter(tags=["Authentication"])

@router.get("/")
def welcome():
    """Returns welcome message to check if API is working"""
    return "Write Somthing Nice API is running"

@router.post("/login")
def login(
    user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(connect_db)
):
    """Handles user login and returns a JWT"""
    ref_user = db.query(User).filter(User.username == user.username).first()

    if (not ref_user) or (not verify_pw(user.password, ref_user.password)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid username or password.",
        )

    token = create_access_token({"id": ref_user.id, "username": ref_user.username})
    response = JSONResponse(content={"message": "logged in", "token": token})
    response.set_cookie(key="wsn-session", value=token)
    return response


@router.post("/logout")
def logout():
    """Logs out user by clearing their access cookie"""
    try:
        response = JSONResponse(content={"message": "User logged out"})
        response.delete_cookie(key="wsn-session")
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error: Something went wrong while logging out",
        )
    return response
