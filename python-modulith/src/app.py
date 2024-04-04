from collections.abc import Callable
from datetime import datetime
from typing import Any

from analytics.dtos import TodosCounter
from analytics import AnalyticsModule as analytics
from notifications import NotificationsModule as notifications
from todos import TodoModule as todos
from todos.domain.repository import TodoRepository

from lato import Application, TransactionContext


def create_app() -> Application:
    # create an application with dependencies used across the handlers
    app = Application(
        "Tutorial",
        todo_repository=TodoRepository,  # used by todos module
        notification_service=notifications.NotificationService(),  # used by notifications module
        todos_counter=TodosCounter(),  # used ny analytics module
    )
    # add modules to the app
    app.include_submodule(todos)
    app.include_submodule(notifications)
    app.include_submodule(analytics)

    # add transaction context middlewares
    @app.on_enter_transaction_context
    def on_enter_transaction_context(ctx: TransactionContext):
        print("Begin transaction")
        ctx.set_dependencies(
            now=datetime.now(),
        )

    @app.on_exit_transaction_context
    def on_exit_transaction_context(ctx: TransactionContext, exception=None):
        print("End transaction")

    @app.transaction_middleware
    def logging_middleware(ctx: TransactionContext, call_next: Callable) -> Any:
        handler = ctx.current_handler
        message_name = ctx.get_dependency("message").__class__.__name__
        handler_name = f"{handler.source}.{handler.fn.__name__}"
        print(f"Executing {handler_name}({message_name})")
        result = call_next()
        print(f"Result from {handler_name}: {result}")
        return result

    @app.transaction_middleware
    def analytics_middleware(ctx: TransactionContext, call_next: Callable) -> Any:
        result = call_next()
        todos_counter = ctx.get_dependency(TodosCounter)
        print(
            f" todos stats: {todos_counter.completed_todos}/{todos_counter.created_todos}"
        )
        return result

    return app