from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch, MagicMock
from models import Todos
import pytest

client = TestClient(app)

#Mocking the Database session
@pytest.fixture
def mock_db_session():
    with patch('main.SessionLocal') as mock:
        mock.return_value = MagicMock()
        yield mock


#Test for Post /todo
def test_create_todo(mock_db_session):
    test_todo = {
        "title": "Test Todo",
        "description": "This is testing a post in todo",
        "prioty": 3,
        "completed": True,
    }
    response = client.post("/todo", json=test_todo)
    assert response.status_code == 201
    assert response.json() == test_todo


#Test for Get /todos
def test_read_all_todos(mock_db_session):
    mock_db_session.return_value.query.return_value.all.return_value = [
        Todos(id=1, title = "Test Todo" )
    ]
    response = client.get("/todos")
    assert len(response.json()) == 1


#Test for Get /todos/{todos_id}
def test_read_one_todo(mock_db_session):
    mock_db_session.return_value.query.return_value.first.return_value = Todos(id=1, title = "Test Todo" )
    response = client.get("/todos/1")
    assert response.status_code == 200



#Test for Put /todo/{todo_id}
def test_update_one_todo(mock_db_session):
    mock_db_session.return_value.query.return_value.first.return_value = Todos(id=1, title = "Test Todo", description = "You fine too", prioty = 2, completed = True)
    test_todo = {
        "title": "Test Put Todo",
        "description": "This is testing a put in todo",
        "prioty": 3,
        "completed": False,
    }
    response = client.put("/todo/1", json=test_todo)
    assert response.status_code == 201
    assert response.json() == test_todo


#Test for Delete /todo/{todo_id}
def test_delete_one_todo(mock_db_session):
    #mock_db_session.return_value.query.return_value.first.return_value = Todos(id=1, title = "Test Todo", description = "You fine too", prioty = 2, completed = True)
    response = client.delete("/todo/1")
    assert response.status_code == 204