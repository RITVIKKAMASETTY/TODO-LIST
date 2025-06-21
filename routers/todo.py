from fastapi import FastAPI,APIRouter,Path,status,HTTPException,Depends
import models
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from models import Todo
from pydantic import BaseModel,Field
router=APIRouter()
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_depends=Annotated[Session,Depends(get_db)]
class Todorequest(BaseModel):
 title:str=Field(min_length=3)
 description:str=Field(min_length=3)
 priority:int=Field(gt=0)
 completed:bool
@router.get("/",status_code=status.HTTP_200_OK)
async def read_all(db:db_depends):
    return db.query(Todo).all()
@router.get("/",status_code=status.HTTP_200_OK)
async def read_all(db:db_depends):
    return db.query(Todo).all()
@router.get("/todo/{todo_id}",status_code=status.HTTP_200_OK)
async def read_todo(db:db_depends,todo_id:int=Path(gt=0)):
    todo_mode=db.query(Todo).filter(Todo.id==todo_id).first()
    if todo_mode is None:
        raise HTTPException(status_code=404,detail="Todo not found")
    return todo_mode
@router.post("/add",status_code=status.HTTP_201_CREATED)
async def add_todo(db:db_depends,todo:Todorequest):
    new_todo=Todo(**todo.dict())
    db.add(new_todo)
    db.commit()
@router.put("/udate/{todo_id}",status_code=status.HTTP_200_OK)
async def update_todo(db:db_depends,todo:Todorequest,todo_id:int=Path(gt=0)):
    updated_todo=db.query(Todo).filter(Todo.id==todo_id).first()
    if updated_todo is None:
        raise HTTPException(status_code=404,detail="Todo not found")
    updated_todo.title=todo.title
    updated_todo.description=todo.description
    updated_todo.priority=todo.priority
    updated_todo.completed=todo.completed
    db.commit()
    return updated_todo
@router.delete("/delete/{todo_id}",status_code=status.HTTP_200_OK)
async def delete_todo(db:db_depends,todo_id:int=Path(gt=0)):
    deleted_todo=db.query(Todo).filter(Todo.id==todo_id).first()
    if deleted_todo is None:
        raise HTTPException(status_code=404,detail="Todo not found")
    db.delete(deleted_todo)
    db.commit()
    return deleted_todo