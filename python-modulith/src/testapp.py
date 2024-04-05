from uuid import UUID
import pytest
from app import create_app
from commands import CreateTodo, CompleteTodo
from queries import GetAllTodos

app = create_app()

app.execute(CreateTodo(todo_id=UUID(int=1), title="Publish the tutorial"))

all_todos = app.execute(GetAllTodos())
print(all_todos)

app.execute(CompleteTodo(todo_id=UUID(int=1)))

all_todos = app.execute(GetAllTodos())
print(all_todos)