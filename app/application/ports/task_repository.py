from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain import Task


class TaskRepository(ABC):
    """Port: Abstract interface for Task persistence"""

    @abstractmethod
    def save(self, task: Task) -> Task:
        """Save a task and return it"""
        pass

    @abstractmethod
    def get_all(self) -> List[Task]:
        """Retrieve all tasks"""
        pass

    @abstractmethod
    def get_by_id(self, task_id: str) -> Optional[Task]:
        """Retrieve a task by id, None if not found"""
        pass

    @abstractmethod
    def delete(self, task_id: str) -> bool:
        """Delete a task by id, return True if deleted"""
        pass

    @abstractmethod
    def update(self, task: Task) -> Optional[Task]:
        """Update a task, return updated task or None if not found"""
        pass
