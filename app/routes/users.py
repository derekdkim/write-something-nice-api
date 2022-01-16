from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from ..db.connection import connect_db
# import schemas

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/new", status_code=status.HTTP_201_CREATED, response_model='hello')
def create_user(user: UserInput, db: Session = Depends(connect_db)):
    return "hellow world"