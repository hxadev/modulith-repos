import datetime
from lato import ApplicationModule, TransactionContext
from Commands import CreateTodo
from dtos import TodosCounter
from Events import TodoWasCompleted

analytics = ApplicationModule('analytics')

@analytics.handler(CreateTodo)
def handle_create_todo(command: CreateTodo, counter: TodosCounter):
    counter.created_todos += 1


@analytics.handler(TodoWasCompleted)
def on_todo_was_completed(event: TodoWasCompleted, counter: TodosCounter) -> None:
    counter.completed_todos += 1