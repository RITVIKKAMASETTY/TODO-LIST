from fastapi import FastAPI, APIRouter, Depends, status, HTTPException,Request
from pydantic import BaseModel,Field
from models import User
from passlib.context import CryptContext
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os
from fastapi.templating import Jinja2Templates
load_dotenv(".env")
print(os.getenv("SECRET_KEY"))
print(os.getenv("ALGORITHM"))
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
router = APIRouter(prefix="/auth", tags=["auth"])
bcryot_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2bearer = OAuth2PasswordBearer(tokenUrl="auth/login")


async def getcurrentuser(token: Annotated[str, Depends(oauth2bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        role: str = payload.get("role")
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        return {"username": username, "id": user_id, "role": role}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


def create_access_token(
    username: str, user_id: int, role: str, expires_delta: timedelta
):
    encode = {"sub": username, "id": user_id, "role": role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_depends = Annotated[Session, Depends(get_db)]

templates=Jinja2Templates(directory="templates")

#######pages#########
@router.get("/login-page")
def render_login_page(request:Request):
    return templates.TemplateResponse("login.html",{"request":request})
@router.get("/register-page")
def render_register_page(request:Request):
    return templates.TemplateResponse("register.html",{"request":request})







def authenticateuser(db, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcryot_context.verify(password, user.hashed_password):
        return False
    return user


class Createuser(BaseModel):
    username: str
    email: str
    firstname: str
    lastname: str
    password: str
    role: str
    phone_number: str=Field(min_length=10)


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_depends, user: Createuser):
    new_user = User(
        username=user.username,
        email=user.email,
        first_name=user.firstname,
        last_name=user.lastname,
        hashed_password=bcryot_context.hash(user.password),
        role=user.role,
        is_active=True,
        phone_number=user.phone_number,
    )
    db.add(new_user)
    db.commit()
    return new_user


@router.get("/showusers", status_code=status.HTTP_200_OK)
async def get_users(db: db_depends):
    return db.query(User).all()


@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def register_user(
    db: db_depends, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticateuser(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        user.username, user.id, user.role, access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/updateuser", status_code=status.HTTP_200_OK)
async def update_user(db: db_depends, user: Createuser):
    updated_user = db.query(User).filter(User.username == user.username).first()
    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    updated_user.email = user.email
    updated_user.first_name = user.firstname
    updated_user.last_name = user.lastname
    updated_user.hashed_password = bcryot_context.hash(user.password)
    updated_user.role = user.role
    updated_user.phone_number = user.phone_number
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating user",
        )
    return updated_user
