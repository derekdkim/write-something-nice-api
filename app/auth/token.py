from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import status, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer

from ..settings import env
from ..schemas.token import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def create_access_token(data: dict):
    """Creates new JWT."""
    to_encode = data.copy()

    expire_time = datetime.utcnow() + timedelta(minutes=env.jwt_exp_minutes)
    to_encode.update({"exp": expire_time})

    token = jwt.encode(to_encode, env.jwt_secret_key, algorithm=env.jwt_algo)

    return token


def verify_access_token(token: str, auth_exception):
    """Verify the validity of JWT"""
    try:
        payload = jwt.decode(token, env.jwt_secret_key, algorithms=[env.jwt_algo])
        user_id: str = payload.get("id")
        username: str = payload.get("username")

        if user_id is None:
            raise auth_exception
        token_data = TokenPayload(id=user_id, username=username)
    except JWTError:
        raise auth_exception

    return token_data


def get_current_user(request: Request):
    """Middleware to verify JWT and return information about the current user for HTTP requests."""
    auth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Failed to validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # Extract JWT from cookie
    token = request.cookies.get("wsn-session")

    return verify_access_token(token, auth_exception)
