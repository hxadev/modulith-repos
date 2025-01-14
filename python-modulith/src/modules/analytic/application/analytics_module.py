from modules.todo.application.commands import CreateTodo
from modules.todo.application.events import TodoWasCompleted

from lato import ApplicationModule

class TodosCounter:
    def __init__(self):
        self.created_todos = 0
        self.completed_todos = 0

analytics = ApplicationModule("analytics")

@analytics.handler(CreateTodo)
def handle_create_todo(command: CreateTodo, counter: TodosCounter):
    """
    Handle the creation of a new todo item.

    Args:
        command (CreateTodo): The command object containing the details of the todo to be created.
        counter (TodosCounter): The counter object to track the number of created todos.

    Returns:
        None
    """
    counter.created_todos += 1

@analytics.handler(TodoWasCompleted)
def on_todo_was_completed(event: TodoWasCompleted, counter: TodosCounter) -> None:
    """
    A function that handles the completion of a todo item.

    Parameters:
    - event: TodoWasCompleted, the event representing the completed todo.
    - counter: TodosCounter, the counter object to track completed todos.

    Returns:
    - None
    """
    counter.completed_todos += 1