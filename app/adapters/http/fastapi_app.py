from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
from app.application.services import TaskService
from app.adapters.persistence import MemoryTaskRepository


# Pydantic schemas for HTTP
class TaskCreateRequest(BaseModel):
    """Request schema for task creation"""
    title: str = Field(..., min_length=1, description="Task title")
    status: Optional[str] = Field("pending", description="Task status: pending or done")


class TaskUpdateRequest(BaseModel):
    """Request schema for task update"""
    title: Optional[str] = Field(None, min_length=1, description="Task title")
    status: Optional[str] = Field(None, description="Task status: pending or done")


class TaskResponse(BaseModel):
    """Response schema for a task"""
    id: str
    title: str
    status: str

    class Config:
        from_attributes = True


class HealthResponse(BaseModel):
    """Response schema for health check"""
    status: str


# Initialize repository and service
repository = MemoryTaskRepository()
task_service = TaskService(repository=repository)

# Create FastAPI app
app = FastAPI(
    title="Task Management API",
    description="Simple REST API for task management with SOLID principles",
    version="1.0.0"
)


# Health check endpoint
@app.get("/health", response_model=HealthResponse)
def health_check():
    """Check service health status"""
    return HealthResponse(status="ok")


# GET /tasks - List all tasks
@app.get("/tasks", response_model=List[TaskResponse])
def list_tasks():
    """
    List all tasks.

    Returns:
        List of all tasks
    """
    tasks = task_service.get_all_tasks()
    return [TaskResponse(id=t.id, title=t.title, status=t.status) for t in tasks]


# POST /tasks - Create a new task
@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(request: TaskCreateRequest):
    """
    Create a new task.

    Args:
        request: Task creation data (title and optional status)

    Returns:
        Created task

    Raises:
        HTTPException 400: If validation fails
    """
    try:
        task = task_service.create_task(
            title=request.title,
            status=request.status or "pending"
        )
        return TaskResponse(id=task.id, title=task.title, status=task.status)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# GET /tasks/{task_id} - Get a specific task
@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: str):
    """
    Get a task by id.

    Args:
        task_id: Task id

    Returns:
        Task details

    Raises:
        HTTPException 404: If task not found
    """
    task = task_service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return TaskResponse(id=task.id, title=task.title, status=task.status)


# PUT /tasks/{task_id} - Update a task
@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: str, request: TaskUpdateRequest):
    """
    Update a task.

    Args:
        task_id: Task id
        request: Task update data (title and/or status)

    Returns:
        Updated task

    Raises:
        HTTPException 400: If validation fails
        HTTPException 404: If task not found
    """
    try:
        task = task_service.update_task(
            task_id=task_id,
            title=request.title,
            status=request.status
        )
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        return TaskResponse(id=task.id, title=task.title, status=task.status)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# DELETE /tasks/{task_id} - Delete a task
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str):
    """
    Delete a task.

    Args:
        task_id: Task id

    Raises:
        HTTPException 404: If task not found
    """
    deleted = task_service.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return None
