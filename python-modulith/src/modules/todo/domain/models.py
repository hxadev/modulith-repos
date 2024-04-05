from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class TodoModel:
    """Model representing a todo"""

    id: UUID
    title: str
    description: str = ""
    due_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    @property
    def is_completed(self) -> bool:
        return self.completed_at is not None

    def is_due(self, now: datetime) -> bool:
        if self.due_at is None or self.is_completed is False:
            return False
        return self.due_at < now

    def mark_as_completed(self, when: datetime) -> None:
        self.completed_at = when
        

@dataclass
class TodoReadModel:
    """Read model exposed to the external world"""

    id: UUID
    title: str
    description: str
    is_due: bool
    is_completed: bool