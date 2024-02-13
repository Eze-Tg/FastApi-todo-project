from fastapi import FastAPI
from routers.auth import router
from routers.todo import todo_router

app = FastAPI()

#Include the router
app.include_router(router)
app.include_router(todo_router)

