from database import Base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
class User(Base):
    __tablename__="user"
    id=Column(Integer,primary_key=True,index=True,autoincrement=True)
    username=Column(String,unique=True)
    email=Column(String,unique=True)
    firstname=Column(String)
    lastname=Column(String)
    hashedpassword=Column(String)
    isactive=Column(Boolean,default=True)
    role=Column(String)
class Todo(Base):
    __tablename__ = "todos"
    id=Column(Integer,primary_key=True,index=True,autoincrement=True)
    title=Column(String)
    description=Column(String)
    priority=Column(Integer)
    completed=Column(Boolean,default=False)
    ownerid=Column(Integer,ForeignKey("user.id"))