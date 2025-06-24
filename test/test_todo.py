from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from main import app
from routers.auth import get_db, getcurrentuser
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from models import Todo
from database import Base
import database
SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
database.SessionLocal = TestingSessionLocal
database.engine=engine
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    print("override_get_current_user")
    return {"username": "khushbu", "id": 1, "role": "admin"}


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[getcurrentuser] = override_get_current_user
client = TestClient(app)
@pytest.fixture
def test_todo():
    todo = Todo(
        title="test todo",
        description="test description",
        priority=1,
        completed=False,
        ownerid=1,
    )
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    db.refresh(todo)

    yield todo
    # with engine.connect() as Connection:
    #     Connection.execute(text("DELETE FROM todos;"))
    #     Connection.commit()
def test_read_all_authenticated(test_todo):
    response=client.get("/")
    assert response.status_code==status.HTTP_200_OK
    assert response.json()==[
        {
           "completed":False,
            "title":"test todo",
           "description":"test description",
           "id":1,
           "priority":1,
           "ownerid":1
        }
    ]

# @pytest.fixture
# def test_todo():
#     todo = Todo(
#         title="test todo",
#         description="test description",
#         priority=1,
#         completed=False,
#         ownerid=1,
#     )
#     db = TestingSessionLocal()
#     db.add(todo)
#     db.commit()
#     yield todo
#     with engine.connect() as Connection:
#         Connection.execute(text("DELETE FROM todo;"))
#         Connection.commit()
#     return todo


# def test_get_all_todos(test_todo):
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == [
#         {
#             "id": 1,
#             "title": "test todo",
#             "description": "test description",
#             "priority": 1,
#             "completed": False,
#             "ownerid": 1,
#         }
#     ]
