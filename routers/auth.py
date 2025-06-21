from fastapi import FastAPI,APIRouter,Depends,status,HTTPException
from pydantic import BaseModel
from models import User
from passlib.context import CryptContext
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import JWTError,jwt
from datetime import datetime,timedelta,timezone
from dotenv import load_dotenv
import os
load_dotenv(".env")
print(os.getenv("SECRET_KEY"))
print(os.getenv("ALGORITHM"))
SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
router=APIRouter(
    prefix="/auth",
    tags=["auth"]
)
bcryot_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
oauth2bearer=OAuth2PasswordBearer(tokenUrl="auth/login")
async def getcurrentuser(token:Annotated[str,Depends(oauth2bearer)]):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str=payload.get("sub")
        user_id:int=payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
        return {"username":username,"id":user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
def create_access_token(username:str,user_id:int,expires_delta:timedelta):
    encode={"sub":username,"id":user_id}
    expires=datetime.now(timezone.utc)+expires_delta
    encode.update({"exp":expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_depends=Annotated[Session,Depends(get_db)]
def authenticateuser(db,username:str,password:str):
    user=db.query(User).filter(User.username==username).first()
    if not user:
        return False
    if not bcryot_context.verify(password,user.hashedpassword):
        return False
    return user
class Createuser(BaseModel):
    username:str
    email:str
    firstname:str
    lastname:str
    password:str
    role:str
class Token(BaseModel):
    access_token:str
    token_type:str
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
@router.post("/login",response_model=Token,status_code=status.HTTP_200_OK)
async def register_user(db:db_depends,form_data:Annotated[OAuth2PasswordRequestForm,Depends()]):
    user=authenticateuser(db,form_data.username,form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect username or password")
    access_token_expires=timedelta(minutes=30)
    access_token=create_access_token(user.username,user.id,access_token_expires)
    return {"access_token":access_token,"token_type":"bearer"}