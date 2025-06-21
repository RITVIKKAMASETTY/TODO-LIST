from fastapi import FastAPI,Depends,Path,status,Query
import models
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from models import Todo
from fastapi import HTTPException
from pydantic import BaseModel,Field
from routers import auth
from routers import todo
app=FastAPI()
models.Base.metadata.create_all(bind=engine)


app.include_router(auth.router)
app.include_router(todo.router)
