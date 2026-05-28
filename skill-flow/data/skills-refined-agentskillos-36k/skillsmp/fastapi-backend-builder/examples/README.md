# Complete FastAPI Application Example

This directory contains a complete, working FastAPI application example that demonstrates all the concepts in this skill.

## Overview

This example implements a simple Task Management API with:
- User authentication (JWT)
- CRUD operations for tasks
- Clean architecture (routers → services → repositories)
- Pydantic validation
- SQLAlchemy ORM
- Proper error handling

## Project Structure

```
example_app/
├── main.py                  # Application entry point
├── config.py                # Configuration
├── dependencies.py          # DI functions
├── models/
│   ├── database.py         # SQLAlchemy models
│   └── schemas.py          # Pydantic schemas
├── routers/
│   ├── auth.py             # Authentication routes
│   └── tasks.py            # Task routes
├── services/
│   ├── auth_service.py     # Auth business logic
│   └── task_service.py     # Task business logic
└── repositories/
    ├── user_repository.py  # User data access
    └── task_repository.py  # Task data access
```

## Features Demonstrated

### 1. Authentication
- User registration
- Login with JWT tokens
- Protected routes
- Password hashing with bcrypt

### 2. Task Management
- Create tasks
- List tasks (with filtering)
- Update tasks
- Delete tasks
- Mark tasks as complete

### 3. Architecture Patterns
- Dependency injection
- Repository pattern
- Service layer
- Pydantic validation
- Error handling
- Type hints throughout

### 4. Best Practices
- Configuration via Pydantic Settings
- Environment variables
- Clean separation of concerns
- Proper error responses
- API documentation
- Input validation

## How to Run

1. **Install dependencies**:
```bash
pip install fastapi uvicorn sqlalchemy pydantic pydantic-settings python-jose passlib bcrypt python-multipart
```

2. **Set environment variables**:
Create `.env` file:
```
DATABASE_URL=sqlite:///./tasks.db
SECRET_KEY=your-secret-key-here
```

3. **Run the application**:
```bash
# From the examples directory
cd example_app
uvicorn main:app --reload
```

4. **Access the API**:
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/token` - Login and get access token

### Tasks
- `GET /tasks` - List all tasks (requires auth)
- `POST /tasks` - Create a task (requires auth)
- `GET /tasks/{task_id}` - Get specific task (requires auth)
- `PUT /tasks/{task_id}` - Update task (requires auth)
- `DELETE /tasks/{task_id}` - Delete task (requires auth)
- `PATCH /tasks/{task_id}/complete` - Mark as complete (requires auth)

## Testing the API

### 1. Register a user
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","username":"testuser","password":"testpass123"}'
```

### 2. Login
```bash
curl -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpass123"
```

This returns a token like:
```json
{"access_token":"eyJ0eXAi...","token_type":"bearer"}
```

### 3. Create a task (use token from login)
```bash
curl -X POST "http://localhost:8000/tasks" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"title":"My Task","description":"Task description"}'
```

### 4. List tasks
```bash
curl -X GET "http://localhost:8000/tasks" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 5. Mark task as complete
```bash
curl -X PATCH "http://localhost:8000/tasks/1/complete" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Code Walkthrough

### 1. Configuration (config.py)
- Uses Pydantic Settings for type-safe configuration
- Loads from environment variables
- Provides defaults for development

### 2. Database Models (models/database.py)
- SQLAlchemy ORM models
- Defines User and Task tables
- Establishes relationships

### 3. Pydantic Schemas (models/schemas.py)
- Request/response validation
- Separate schemas for create/update/response
- Type safety and automatic documentation

### 4. Repositories (repositories/)
- Data access layer
- CRUD operations
- Database queries
- No business logic

### 5. Services (services/)
- Business logic layer
- Orchestrates repositories
- Handles authentication
- Error handling

### 6. Routers (routers/)
- HTTP request/response handling
- Input validation
- Calls services
- Returns responses

### 7. Main Application (main.py)
- FastAPI app setup
- CORS configuration
- Router registration
- Database initialization

## Learning Points

1. **Clean Architecture**: Notice how concerns are separated - routers handle HTTP, services handle logic, repositories handle data.

2. **Dependency Injection**: Database sessions and current user are injected via FastAPI's dependency system.

3. **Type Safety**: Type hints everywhere make the code self-documenting and catch errors early.

4. **Validation**: Pydantic validates all input automatically.

5. **Security**: Passwords are hashed, JWT tokens protect routes.

6. **Error Handling**: Proper HTTP status codes and error messages.

## Extending This Example

To add a new feature (e.g., task comments):

1. **Add model** in `models/database.py`:
```python
class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    task_id = Column(Integer, ForeignKey("tasks.id"))
```

2. **Add schemas** in `models/schemas.py`:
```python
class CommentCreate(BaseModel):
    text: str

class CommentResponse(BaseModel):
    id: int
    text: str
    task_id: int
```

3. **Add repository** in `repositories/comment_repository.py`:
```python
class CommentRepository:
    def create(self, data):
        # Implementation
```

4. **Add service** in `services/comment_service.py`:
```python
class CommentService:
    def add_comment(self, task_id, comment_data):
        # Implementation
```

5. **Add router** in `routers/comments.py`:
```python
@router.post("/tasks/{task_id}/comments")
async def add_comment(task_id: int, comment: CommentCreate):
    # Implementation
```

6. **Register router** in `main.py`:
```python
app.include_router(comments.router)
```

This structure makes it easy to extend the application systematically.
