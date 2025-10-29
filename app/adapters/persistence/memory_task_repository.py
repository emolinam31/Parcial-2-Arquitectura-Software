from typing import List, Optional
from app.domain import Task
from app.application.ports import TaskRepository


class MemoryTaskRepository(TaskRepository):
    """Adapter: In-memory implementation of TaskRepository"""

    def __init__(self):
        self._tasks: dict[str, Task] = {}

    def save(self, task: Task) -> Task:
        """Save a task in memory"""
        self._tasks[task.id] = task
        return task

    def get_all(self) -> List[Task]:
        """Retrieve all tasks"""
        return list(self._tasks.values())

    def get_by_id(self, task_id: str) -> Optional[Task]:
        """Retrieve a task by id"""
        return self._tasks.get(task_id)

    def delete(self, task_id: str) -> bool:
        """Delete a task by id"""
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def update(self, task: Task) -> Optional[Task]:
        """Update a task"""
        if task.id in self._tasks:
            self._tasks[task.id] = task
            return task
        return None
