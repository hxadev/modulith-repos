from uuid import UUID
from lato import Event

class TodoWasCompleted(Event):
    todo_id:UUID