from fastapi import APIRouter, status, HTTPException, Depends,Path
import models
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, Field
from routers.auth import getcurrentuser
from routers.auth import bcryot_context
class Userverification(BaseModel):
    password: str
    newpassword: str = Field(min_length=4)

class phonenumber(BaseModel):
    phonenumber:str
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(prefix="/user", tags=["user"])
user_depends = Annotated[dict, Depends(getcurrentuser)]
db_depends = Annotated[Session, Depends(get_db)]


@router.get("/getuser", status_code=status.HTTP_200_OK)
async def get_user(db: db_depends, user: user_depends):
    user = db.query(models.User).filter(models.User.id == user["id"]).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    return user


@router.put("/changepassword", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_depends, db: db_depends, userverification: Userverification
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    user = db.query(models.User).filter(models.User.id == user["id"]).first()
    user.hashedpassword = bcryot_context.hash(userverification.newpassword)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating user",
        )
    return user
@router.put("/updatephonenumber/{phonenumber}",status_code=status.HTTP_204_NO_CONTENT)
async def updatephonenumber(user:user_depends,db:db_depends,phonenumber:str=Path(min_length=10)):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    user=db.query(models.User).filter(models.User.id==user["id"]).first()
    user.phone_number=phonenumber
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating user"
        )