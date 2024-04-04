from dataclasses import dataclass
from uuid import UUID

@dataclass
class TodoRead:
    id: UUID
    title: str
    description: str
    is_due: bool
    is_completed: bool