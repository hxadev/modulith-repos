from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from flask import Flask, request, jsonify

from app import create_app, Application
from modules.todo.application.commands import CompleteTodo, CreateTodo
from modules.todo.application.queries import GetAllTodos, GetTodoDetails

app = Flask(__name__)
app.lato_application = create_app()

class TodoRequest:
    def __init__(self, title: str, description: str, due_at: Optional[datetime] = None):
        self.title = title
        self.description = description
        self.due_at = due_at

def get_application():
    return app.lato_application

@app.route("/todos", methods=["GET"])
def get_todos():
    app_instance = get_application()
    result = app_instance.execute(GetAllTodos())
    return jsonify({"data": result}), 200

@app.route("/todos/<todo_id>", methods=["GET"])
def get_todo_details(todo_id: UUID):
    app_instance = get_application()
    result = app_instance.execute(GetTodoDetails(todo_id=todo_id))
    return jsonify({"data": result}), 200

@app.route("/todos", methods=["POST"])
def store_todo():
    request_data = request.get_json()
    todo_request = TodoRequest(**request_data)
    app_instance = get_application()
    app_instance.execute(CreateTodo(todo_id=uuid4(), title=todo_request.title, description=todo_request.description, due_at=todo_request.due_at))
    return "", 201

@app.route("/todos/<todo_id>", methods=["PUT"])
def complete_todo(todo_id: UUID):
    app_instance = get_application()
    app_instance.execute(CompleteTodo(todo_id=todo_id))
    return "", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
