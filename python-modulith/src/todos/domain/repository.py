from uuid import UUID
from models import Todo

class TodoRepository:
    def __init__(self):
        self.items: list[Todo] = []

    def add(self, item: Todo) -> None:
        self.items.append(item)

    def get_by_id(self, todo_id: UUID) -> Todo:
        for item in self.items:
            if item.id == todo_id:
                return item
        raise ValueError(f"Todo with id {todo_id} does not exist")

    def get_all(self) -> list[Todo]:
        return self.items

    def get_all_completed(self):
        return [todo for todo in self.items if todo.is_completed]

    def get_all_not_completed(self):
        return [todo for todo in self.items if not todo.is_completed]