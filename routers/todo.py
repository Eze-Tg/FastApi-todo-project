from fastapi import Depends, HTTPException, Path, APIRouter
from typing import Annotated
from pydantic import BaseModel, Field
import models
from starlette import status
from models import Todos
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from .auth import get_current_user

todo_router = APIRouter()

models.Base.metadata.create_all(bind = engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

user_dependency = Annotated[models.User, Depends(get_current_user)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    prioty: int = Field(gt=0, lt=6)
    completed: bool

#Read all todo for this user
@todo_router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db:db_dependency):

    all_todos = db.query(Todos).filter(Todos.owner_id == user.get('id')).all()
    return all_todos

#Read one todo
@todo_router.get("/todos/{todos_id}", status_code=status.HTTP_200_OK)
async def read_one(user: user_dependency, db: db_dependency, 
                   todos_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    
    todo_model = db.query(Todos).filter(Todos.id == todos_id)\
        .filter(Todos.owner_id == user.get('id')).first()
    
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="user Not Found")

#Create a new Todo
@todo_router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, 
                      db:db_dependency, 
                      todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")

    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get('id'))

    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)

    return todo_model


#Update a Todo
@todo_router.put("/todo/{todo_id}", status_code=status.HTTP_201_CREATED)
async def update_todo(user: user_dependency,
                      db:db_dependency, 
                      todo_request: TodoRequest,
                      todo_id: int = Path(gt=0)):
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")

    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('id')).first()
    
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo Not Found")
    
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.prioty = todo_request.prioty
    todo_model.completed = todo_request.completed

    db.add(todo_model)
    db.commit()

    return todo_model

#Delete a Todo
@todo_router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency,
                      db:db_dependency, 
                      todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")

    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('id')).first()
    
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo Not Found")

    db.delete(todo_model)
    db.commit()

    return todo_model