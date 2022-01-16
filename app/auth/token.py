from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import status, HTTPException, Depends
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
        id: str = payload.get("user_id")

        if id is None:
            raise auth_exception
        token_data = TokenPayload(id=id)
    except JWTError:
        raise auth_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    """Middleware to verify JWT and return information about the current user for HTTP requests."""
    auth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Failed to validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return verify_access_token(token, auth_exception)
