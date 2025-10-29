from dataclasses import dataclass, field
from typing import Literal
from uuid import uuid4


@dataclass
class Task:
    """Entity: Task in the domain model"""
    title: str
    status: Literal["pending", "done"]
    id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self):
        """Validate Task invariants"""
        if not self.title or not self.title.strip():
            raise ValueError("title is required and cannot be empty")

        if self.status not in ("pending", "done"):
            raise ValueError("status must be 'pending' or 'done'")

        self.title = self.title.strip()

    def mark_done(self) -> None:
        """Business operation: mark task as done"""
        self.status = "done"

    def mark_pending(self) -> None:
        """Business operation: mark task as pending"""
        self.status = "pending"
