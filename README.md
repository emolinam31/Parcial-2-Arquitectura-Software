# Task Management API

A simple REST API for task management built with FastAPI, following SOLID principles and clean architecture patterns.

## Architecture

This project demonstrates:

- **Domain Layer** (`app/domain/`): Core business entities (Task)
- **Application Layer** (`app/application/`): Business logic and use cases (TaskService)
- **Adapter Layer** (`app/adapters/`): HTTP endpoints (FastAPI) and persistence (in-memory repository)

### Design Patterns Used

- **Repository Pattern**: Abstraction for data access (TaskRepository interface)
- **Dependency Injection**: Service receives repository through constructor
- **Factory Pattern**: Task validation and creation in the domain entity

### SOLID Principles Applied

- **SRP (Single Responsibility)**: Each class has one reason to change
  - Task: domain logic
  - TaskService: business orchestration
  - MemoryTaskRepository: persistence
  - FastAPI endpoints: HTTP transport

- **OCP (Open/Closed)**: Open for extension (implement TaskRepository), closed for modification
  - Can switch to database persistence without changing TaskService

- **DIP (Dependency Inversion)**: TaskService depends on TaskRepository abstraction, not concrete implementation

## Features

- **GET /health**: Health check endpoint
- **GET /tasks**: List all tasks
- **POST /tasks**: Create a new task
- **GET /tasks/{id}**: Get a specific task
- **PUT /tasks/{id}**: Update a task
- **DELETE /tasks/{id}**: Delete a task

## Requirements

- Python 3.10+
- FastAPI
- Uvicorn
- Pydantic

## Installation (Local Development)

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the API

```bash
python -m uvicorn app.adapters.http.fastapi_app:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## Docker Execution

### Build the Docker image

```bash
docker build -t task-api:latest .
```

### Run the container

```bash
docker run -p 8000:8000 task-api:latest
```

The API will be available at `http://localhost:8000`

## API Usage

### 1. Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "ok"
}
```

### 2. List Tasks

```bash
curl http://localhost:8000/tasks
```

Response:
```json
[]
```

### 3. Create a Task

```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn Docker",
    "status": "pending"
  }'
```

Response:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Learn Docker",
  "status": "pending"
}
```

### 4. Get a Specific Task

```bash
curl http://localhost:8000/tasks/550e8400-e29b-41d4-a716-446655440000
```

### 5. Update a Task

```bash
curl -X PUT http://localhost:8000/tasks/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "done"
  }'
```

### 6. Delete a Task

```bash
curl -X DELETE http://localhost:8000/tasks/550e8400-e29b-41d4-a716-446655440000
```

## Validation Rules

- **title**: Required, non-empty string
- **status**: Must be `pending` or `done`

Invalid requests return HTTP 400 with error details.

## Interactive API Documentation

When running locally, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Project Structure

```
.
├── app/
│   ├── domain/
│   │   └── task.py                      # Task entity
│   ├── application/
│   │   ├── services/
│   │   │   └── task_service.py          # Business logic
│   │   └── ports/
│   │       └── task_repository.py       # Repository interface
│   └── adapters/
│       ├── http/
│       │   └── fastapi_app.py           # HTTP endpoints
│       └── persistence/
│           └── memory_task_repository.py # In-memory implementation
├── Dockerfile                           # Docker configuration
├── requirements.txt                     # Python dependencies
└── README.md                            # This file
```

## Testing

To test the API, you can use:

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test with HTTPie
http GET http://localhost:8000/health
http POST http://localhost:8000/tasks title="Test" status="pending"

# Use the interactive Swagger UI at http://localhost:8000/docs
```

## Notes

- Tasks are stored in memory and will be lost when the container stops
- For production use, replace MemoryTaskRepository with a database implementation
- The service generates unique IDs for each task using UUID4

## Future Improvements

- Add database persistence (PostgreSQL, SQLite)
- Add authentication and authorization
- Add task filtering and pagination
- Add unit and integration tests
- Add logging and monitoring
