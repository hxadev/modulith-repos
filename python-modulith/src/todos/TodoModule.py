import datetime
from lato import ApplicationModule, TransactionContext
from Commands import CreateTodo, CompleteTodo
from Queries import GetAllTodos, GetSomeTodos, GetTodoDetails
from domain.repository import TodoRepository
from domain.models import Todo
from TodoRead import TodoRead
from Events import TodoWasCompleted

todos = ApplicationModule('todos')

@todos.handler(CreateTodo)
def handle_create_todo(command: CreateTodo, repo: TodoRepository):
    new_todo = Todo(
        id=command.todo_id,
        title=command.title,
        description=command.description,
        due_at=command.due_at,
    )
    repo.add(new_todo)


@todos.handler(CompleteTodo)
def handle_complete_todo(
    command: CompleteTodo, repo: TodoRepository, ctx: TransactionContext, now: datetime
):
    a_todo = repo.get_by_id(command.todo_id)
    a_todo.mark_as_completed(now)
    ctx.publish(TodoWasCompleted(todo_id=a_todo.id))


@todos.handler(GetTodoDetails)
def get_todo_details(query: GetTodoDetails, repo: TodoRepository, now: datetime):
    a_todo = repo.get_by_id(query.todo_id)
    return todo_model_to_read_model(a_todo, now)


@todos.handler(GetAllTodos)
def get_all_todos(
    query: GetAllTodos, repo: TodoRepository, now: datetime
) -> list[TodoRead]:
    result = repo.get_all()
    return [todo_model_to_read_model(todo, now) for todo in result]


@todos.handler(GetSomeTodos)
def get_some_todos(query: GetSomeTodos, repo: TodoRepository, now: datetime):
    if query.completed is None:
        result = repo.get_all()
    else:
        result = (
            repo.get_all_completed()
            if query.completed
            else repo.get_all_not_completed()
        )

    return [todo_model_to_read_model(todo, now) for todo in result]

def todo_model_to_read_model(todo: Todo, now: datetime) -> TodoRead:
    return TodoRead(
        id=todo.id,
        title=todo.title,
        description=todo.description,
        is_due=todo.is_due(now),
        is_completed=todo.is_completed,
    )