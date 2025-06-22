from fastapi import FastAPI,APIRouter,Path,status,HTTPException,Depends
from models import User
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from models import Todo
from pydantic import BaseModel,Field
from routers.auth import getcurrentuser
router=APIRouter(
    prefix="/admin",
    tags=["admin"]
)
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
user_depends=Annotated[dict,Depends(getcurrentuser)]
db_depends=Annotated[Session,Depends(get_db)]
@router.get("/showusers",status_code=status.HTTP_200_OK)
async def get_users(db:db_depends,user:user_depends):
    if(user is None or user["role"]!="admin"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized")
    return db.query(User).all()
@router.get("/showtodos",status_code=status.HTTP_200_OK)
async def get_todos(db:db_depends,user:user_depends):
    if(user is None or user["role"]!="admin"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized")
    return db.query(Todo).all()
@router.delete("/todo/delete/{todo_id}",status_code=status.HTTP_200_OK)
async def delete_todo(user:user_depends,db:db_depends,todo_id:int=Path(gt=0)):
    if user is None or user["role"]!="admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized")
    deleted_todo=db.query(Todo).filter(Todo.id==todo_id).first()
    if deleted_todo is None:
        raise HTTPException(status_code=404,detail="Todo not found")
    db.delete(deleted_todo)
    db.commit()
    return deleted_todo