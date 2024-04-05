from datetime import datetime
from typing import Annotated, Optional
from uuid import UUID, uuid4
from fastapi import Depends, FastAPI, Request
from pydantic import BaseModel
import uvicorn

from app import create_app,Application
from modules.todo.application.commands import CompleteTodo, CreateTodo
from modules.todo.application.queries import GetAllTodos, GetTodoDetails

api = FastAPI()
api.lato_application = create_app()


class TodoRequest(BaseModel):
    title: str
    description: str
    due_at: Optional[datetime]=None

async def get_application(request: Request) -> Application:
    app = request.app.lato_application
    return app

@api.get("/todos", status_code=200)
def get_todos(app: Annotated[Application, Depends(get_application)]):
    result = app.execute(GetAllTodos())
    return {"data": result}

@api.get("/todos/{todo_id}", status_code=200)
def get_todos(todo_id: UUID, app: Annotated[Application, Depends(get_application)]):
    result = app.execute(GetTodoDetails(todo_id=todo_id))
    return {"data": result}

@api.post("/todos", status_code=201)
def store_todo(request:TodoRequest, app: Annotated[Application, Depends(get_application)]):
    app.execute(CreateTodo(todo_id=uuid4(), title=request.title, description=request.description, due_at=request.due_at))
    
@api.put("/todos/{todo_id}", status_code=200)
def complete_todo(todo_id: UUID, app: Annotated[Application, Depends(get_application)]):
    print(todo_id)
    app.execute(CompleteTodo(todo_id=todo_id))
    
    
if __name__ == "__main__":
    uvicorn.run(api, host="0.0.0.0", port=5001)