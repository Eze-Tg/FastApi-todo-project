from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from pytest import Session
from database import SessionLocal
from models import User
from starlette import status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_passwords):
        return False
    return True

@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency,create_user_request: CreateUserRequest):
    create_user_model = User(
        username=create_user_request.username,
        email=create_user_request.email,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_passwords=bcrypt_context.hash(create_user_request.password),
        role=create_user_request.role,
        is_active=True,
    )
    db.add(create_user_model)
    db.commit()


@router.post("/token")
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    return "Successfully logged in"

