from collections.abc import Callable
from datetime import datetime
from typing import Any
from lato import Application, TransactionContext
from modules.analytic.application.analytics_module import TodosCounter,analytics
from modules.notification.application.notifications_module import NotificationService,notifications
from modules.todo.application.todo_module import TodoRepository,todos

def create_app() -> Application:
    
    app = Application(
        "Todo App",
        todo_repository=TodoRepository(),  # used by todos module
        notification_service=NotificationService(),  # used by notifications module
        todos_counter=TodosCounter(),  # used ny analytics module
    )
    
    app.include_submodule(todos)
    app.include_submodule(notifications)
    app.include_submodule(analytics)
    
    @app.on_enter_transaction_context
    def on_enter_transaction_context(ctx: TransactionContext):
        print("[LOG] Begin transaction")
        ctx.set_dependencies(
            now=datetime.now(),
        )

    @app.on_exit_transaction_context
    def on_exit_transaction_context(ctx: TransactionContext, exception=None):
        """
        on_exit_transaction_context - A function that handles the exit of a transaction context.

        Parameters:
            ctx (TransactionContext): The transaction context.
            exception (optional): Any exception that occurred.

        Returns:
            None
        """
        print("[LOG] End transaction")

    @app.transaction_middleware
    def logging_middleware(ctx: TransactionContext, call_next: Callable) -> Any:
        """
        A transaction middleware that handles logging for each function call.
        
        Parameters:
            - ctx (TransactionContext): The transaction context object.
            - call_next (Callable): The next function to be called in the middleware chain.
        
        Returns:
            - Any: The result of the next function call.
        """
        handler = ctx.current_handler
        message_name = ctx.get_dependency("message").__class__.__name__
        handler_name = f"{handler.source}.{handler.fn.__name__}"
        print(f"[LOG] Executing {handler_name}({message_name})")
        result = call_next()
        print(f"[LOG] Result from {handler_name}: {result}")
        return result

    @app.transaction_middleware
    def analytics_middleware(ctx: TransactionContext, call_next: Callable) -> Any:
        """
        A middleware function that takes in a TransactionContext and a Callable, and returns Any. 
        It calls the next function, retrieves a dependency TodosCounter from the context, 
        and prints the statistics of completed and created todos. 
        """
        result = call_next()
        todos_counter = ctx.get_dependency(TodosCounter)
        print(
            f"[ANALYTICS MIDDLEWARE] todos stats: {todos_counter.completed_todos}/{todos_counter.created_todos}"
        )
        return result


    return app