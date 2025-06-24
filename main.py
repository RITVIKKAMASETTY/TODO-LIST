from fastapi import FastAPI,Depends,Path,status,Query,Request
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
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
app=FastAPI()
models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")
app.mount("/static",StaticFiles(directory="static"),name="static")
@app.get("/")
def test(request:Request):
    return RedirectResponse("/todo/todo-page",status_code=status.HTTP_302_FOUND)
@app.get("/healthy")
def healthcheck():
    return {"healthy":True}
app.include_router(auth.router)
app.include_router(todo.router)
app.include_router(admin.router)
app.include_router(users.router)