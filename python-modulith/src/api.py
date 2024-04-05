from datetime import datetime
from typing import Annotated, Optional
from uuid import uuid4
from fastapi import Depends, FastAPI, Request
from pydantic import BaseModel
from app import Application, create_app
from commands import CreateTodo
from queries import GetAllTodos

api = FastAPI()
api.lato_application = create_app()

class TodoRequest(BaseModel):
    title: str
    description: str
    due_at: Optional[datetime]=None

async def get_application(request: Request) -> Application:
    app = request.app.lato_application
    return app

@api.get("/todos")
def get_todos(app: Annotated[Application, Depends(get_application)]):
    result = app.execute(GetAllTodos())
    return {"todos": result}

@api.post("/todos")
def store_todo(request:TodoRequest, app: Annotated[Application, Depends(get_application)]):
    app.execute(CreateTodo(todo_id=uuid4(), title=request.title, description=request.description, due_at=request.due_at))