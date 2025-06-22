from fastapi import FastAPI,APIRouter,Path,status,HTTPException,Depends
import models
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from models import Todo
from pydantic import BaseModel,Field
from routers.auth import getcurrentuser
router=APIRouter()
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
user_depends=Annotated[dict,Depends(getcurrentuser)]
db_depends=Annotated[Session,Depends(get_db)]
class Todorequest(BaseModel):
 title:str=Field(min_length=3)
 description:str=Field(min_length=3)
 priority:int=Field(gt=0)
 completed:bool
@router.get("/",status_code=status.HTTP_200_OK)
async def read_all(db:db_depends,users:user_depends):
    if(users is None):
        raise HTTPException(status_code=401,detail="Unauthorized")
    return db.query(Todo).filter(Todo.ownerid==users["id"]).all()
@router.get("/todo/{todo_id}",status_code=status.HTTP_200_OK)
async def read_todo(users:user_depends,db:db_depends,todo_id:int=Path(gt=0)):
    if(users is None):
      raise HTTPException(status_code=401,detail="Unauthorized")
    todo_mode=db.query(Todo).filter(Todo.id==todo_id).filter(Todo.ownerid==users["id"]).first()
    if todo_mode is None:
        raise HTTPException(status_code=404,detail="Todo not found")
    return todo_mode
@router.post("/add",status_code=status.HTTP_201_CREATED)
async def add_todo(user:user_depends,db:db_depends,todo:Todorequest):
    print("user",user)
    if user is None:
        raise HTTPException(status_code=401,detail="Unauthorized")
    new_todo=Todo(**todo.dict(),ownerid=user["id"])
    db.add(new_todo)
    db.commit()
@router.put("/udate/{todo_id}",status_code=status.HTTP_200_OK)
async def update_todo(user:user_depends,db:db_depends,todo:Todorequest,todo_id:int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401,detail="Unauthorized")
    updated_todo=db.query(Todo).filter(Todo.id==todo_id).filter(Todo.ownerid==user["id"]).first()
    if updated_todo is None:
        raise HTTPException(status_code=404,detail="Todo not found")
    updated_todo.title=todo.title
    updated_todo.description=todo.description
    updated_todo.priority=todo.priority
    updated_todo.completed=todo.completed
    db.commit()
    return updated_todo
@router.delete("/delete/{todo_id}",status_code=status.HTTP_200_OK)
async def delete_todo(user:user_depends,db:db_depends,todo_id:int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401,detail="Unauthorized")
    deleted_todo=db.query(Todo).filter(Todo.id==todo_id).filter(Todo.ownerid==user["id"]).first()
    if deleted_todo is None:
        raise HTTPException(status_code=404,detail="Todo not found")
    db.delete(deleted_todo)
    db.commit()
    return deleted_todo