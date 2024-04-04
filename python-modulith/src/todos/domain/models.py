from dataclasses import dataclass
import datetime
from typing import Optional
from uuid import UUID

@dataclass
class Todo:
    id: UUID
    title: str
    description: str=""
    due_at: datetime=None
    completed_at: datetime=None
    
    @property
    def is_completed(self):
        return self.completed_at is not None
    
    def is_due(self, now: datetime) -> bool:
        if self.due_at is None or self.is_completed is False:
            return False
        return self.due_at < now

    def mark_as_completed(self, when: datetime) -> None:
        self.completed_at = when