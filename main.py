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
from routers import admin
from routers import users
app=FastAPI()
models.Base.metadata.create_all(bind=engine)
@app.get("/healthy")
def healthcheck():
    return {"healthy":True}
app.include_router(auth.router)
app.include_router(todo.router)
app.include_router(admin.router)
app.include_router(users.router)