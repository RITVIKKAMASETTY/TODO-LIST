from fastapi import FastAPI,APIRouter,Depends,status
from pydantic import BaseModel
from models import User
from passlib.context import CryptContext
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
router=APIRouter()
bcryot_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_depends=Annotated[Session,Depends(get_db)]
class Createuser(BaseModel):
    username:str
    email:str
    firstname:str
    lastname:str
    password:str
    role:str
@router.post("/auth",status_code=status.HTTP_201_CREATED)
async def create_user(db:db_depends,user:Createuser):
    new_user=User(
        username=user.username,
        email=user.email,
        firstname=user.firstname,
        lastname=user.lastname,
        hashedpassword=bcryot_context.hash(user.password),
        role=user.role,
        isactive=True
    )
    db.add(new_user)
    db.commit()
    return(new_user)
@router.get("/showusers",status_code=status.HTTP_200_OK)
async def get_users(db:db_depends):
    return db.query(User).all()