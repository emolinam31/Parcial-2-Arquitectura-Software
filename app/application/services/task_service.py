from typing import List, Optional
from app.domain import Task
from app.application.ports import TaskRepository


class TaskService:
    """Application Service: Orchestrates task operations"""

    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def create_task(self, title: str, status: str = "pending") -> Task:
        """
        Create a new task.

        Args:
            title: Task title (required, non-empty)
            status: Task status (pending or done, default: pending)

        Returns:
            The created Task

        Raises:
            ValueError: If title is empty or status is invalid
        """
        task = Task(title=title, status=status)
        return self.repository.save(task)

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks from repository"""
        return self.repository.get_all()

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by id"""
        return self.repository.get_by_id(task_id)

    def update_task(self, task_id: str, title: str = None, status: str = None) -> Optional[Task]:
        """
        Update a task.

        Args:
            task_id: Task id to update
            title: New title (optional)
            status: New status (optional)

        Returns:
            Updated Task or None if not found
        """
        task = self.repository.get_by_id(task_id)
        if not task:
            return None

        if title is not None:
            task.title = title.strip()

        if status is not None:
            if status not in ("pending", "done"):
                raise ValueError("status must be 'pending' or 'done'")
            task.status = status

        return self.repository.update(task)

    def delete_task(self, task_id: str) -> bool:
        """Delete a task by id"""
        return self.repository.delete(task_id)
