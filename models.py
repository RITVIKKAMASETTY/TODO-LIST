from database import Base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True,autoincrement=True)
    username=Column(String,unique=True)
    email=Column(String,unique=True)
    first_name=Column(String)
    last_name=Column(String)
    hashed_password=Column(String)
    is_active=Column(Boolean,default=True)
    role=Column(String)
    phone_number = Column(String,nullable=False)
class Todo(Base):
    __tablename__ = "todos"
    id=Column(Integer,primary_key=True,index=True,autoincrement=True)
    title=Column(String)
    description=Column(String)
    priority=Column(Integer)
    completed=Column(Boolean,default=False)
    ownerid=Column(Integer,ForeignKey("users.id"))