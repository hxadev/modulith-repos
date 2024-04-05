

from lato import ApplicationModule, TransactionContext

from modules.todo.application.events import TodoWasCompleted
from modules.todo.application.queries import GetTodoDetails
from modules.todo.application.todo_module import TodoReadModel


class NotificationService:
    def push(self, message):
        print(message)

notifications = ApplicationModule("notifications")

@notifications.handler(TodoWasCompleted)
def on_todo_was_completed(
    event: TodoWasCompleted, service: NotificationService, ctx: TransactionContext
):
    details: TodoReadModel = ctx.execute(GetTodoDetails(todo_id=event.todo_id))
    print(details)
    message = f"**** [NOTIFICATION] **** A todo {details.title} was completed"
    service.push(message)