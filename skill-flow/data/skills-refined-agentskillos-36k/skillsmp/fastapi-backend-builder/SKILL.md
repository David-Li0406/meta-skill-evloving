---
name: fastapi-backend-builder
description: Comprehensive FastAPI backend development with full codebase documentation, architecture planning, router design, endpoint specification, and automated error resolution. Use when building FastAPI applications from detailed documentation, planning backend APIs, creating routers and endpoints, or developing complete FastAPI backend systems with error-free execution.
---

# FastAPI Backend Builder

This skill provides a systematic, end-to-end approach to building production-ready FastAPI backend applications with comprehensive planning, documentation, and automated error resolution.

## Core Workflow

This skill follows a strict 6-phase workflow to ensure robust, error-free FastAPI applications:

### Phase 1: Codebase Documentation Review

**Objective**: Understand the full backend logic and existing architecture.

1. **Locate Documentation**
   - Search for `codebase_docs/` or equivalent documentation directories
   - Look for architecture diagrams, API specifications, database schemas
   - Review any existing FastAPI code or backend implementations

2. **Extract Key Information**
   - Business logic requirements
   - Data models and database schemas
   - Authentication/authorization requirements
   - External service integrations
   - Performance requirements
   - Security considerations

3. **Document Current State**
   - Existing folder structure
   - Current modules and their responsibilities
   - Dependencies and tech stack
   - Configuration requirements

### Phase 2: Architecture Planning

**Objective**: Design the complete backend architecture before writing code.

1. **Define Folder Structure**
   ```
   backend/
   ├── app/
   │   ├── __init__.py
   │   ├── main.py              # FastAPI application entry
   │   ├── config.py            # Configuration and settings
   │   ├── dependencies.py      # Dependency injection
   │   ├── models/              # Pydantic models & SQLAlchemy ORM
   │   │   ├── __init__.py
   │   │   ├── database.py      # Database models
   │   │   └── schemas.py       # Request/Response schemas
   │   ├── routers/             # API route handlers
   │   │   ├── __init__.py
   │   │   └── [domain]_router.py
   │   ├── services/            # Business logic layer
   │   │   ├── __init__.py
   │   │   └── [domain]_service.py
   │   ├── repositories/        # Data access layer
   │   │   ├── __init__.py
   │   │   └── [domain]_repository.py
   │   ├── utils/               # Utility functions
   │   │   ├── __init__.py
   │   │   └── helpers.py
   │   └── middleware/          # Custom middleware
   │       └── __init__.py
   ├── tests/                   # Test suite
   ├── requirements.txt         # Dependencies
   ├── .env.example            # Environment variables template
   └── README.md               # Documentation
   ```

2. **Plan Router Structure**
   - List all routers needed (e.g., auth, users, products, orders)
   - Define router responsibilities and boundaries
   - Plan router dependencies and interactions
   - Document router prefix and tags

3. **Plan Services & Repositories**
   - Map business logic to service modules
   - Define repository patterns for data access
   - Plan dependency injection strategy
   - Design error handling patterns

4. **Create Implementation Plan**
   - Document in `IMPLEMENTATION_PLAN.md`:
     * Routers to create
     * Endpoints per router
     * Models needed
     * Services needed
     * Dependencies to install
     * Configuration requirements
     * Testing strategy

### Phase 3: Endpoint Specification

**Objective**: Define all API endpoints with complete specifications.

For each router, document:

1. **Endpoint Details**
   - HTTP method (GET, POST, PUT, PATCH, DELETE)
   - Path with parameters
   - Summary and description
   - Request body schema (if applicable)
   - Response schema
   - Status codes (200, 201, 400, 401, 403, 404, 500)
   - Authentication requirements
   - Authorization requirements

2. **Create Endpoint Specification Document**
   ```markdown
   # API Endpoints Specification
   
   ## Router: Users
   
   ### POST /users/register
   - **Summary**: Register a new user
   - **Request Body**: UserCreate schema
   - **Response**: UserResponse schema (201)
   - **Errors**: 400 (validation), 409 (already exists)
   - **Auth**: None
   
   ### GET /users/me
   - **Summary**: Get current user profile
   - **Response**: UserResponse schema (200)
   - **Errors**: 401 (unauthorized)
   - **Auth**: Required (Bearer token)
   ```

### Phase 4: FastAPI Implementation

**Objective**: Build the FastAPI application according to the plan.

1. **Setup Project Structure**
   - Create all directories from the plan
   - Initialize `__init__.py` files
   - Create base configuration files

2. **Install Dependencies**
   ```bash
   pip install fastapi uvicorn pydantic pydantic-settings sqlalchemy alembic python-dotenv python-jose passlib bcrypt
   ```
   
   Create `requirements.txt`:
   ```
   fastapi==0.104.1
   uvicorn[standard]==0.24.0
   pydantic==2.5.0
   pydantic-settings==2.1.0
   sqlalchemy==2.0.23
   alembic==1.13.0
   python-dotenv==1.0.0
   python-jose[cryptography]==3.3.0
   passlib[bcrypt]==1.7.4
   python-multipart==0.0.6
   ```

3. **Implement Core Components (In Order)**
   
   a. **Configuration** (`app/config.py`)
      - Environment variables
      - Database connection strings
      - JWT settings
      - CORS settings
   
   b. **Database Models** (`app/models/database.py`)
      - SQLAlchemy ORM models
      - Database relationships
      - Table definitions
   
   c. **Pydantic Schemas** (`app/models/schemas.py`)
      - Request schemas
      - Response schemas
      - Validation rules
   
   d. **Database Connection** (`app/models/__init__.py`)
      - Database engine setup
      - Session management
      - Base class configuration
   
   e. **Repositories** (`app/repositories/`)
      - CRUD operations
      - Database queries
      - Data access abstraction
   
   f. **Services** (`app/services/`)
      - Business logic implementation
      - Service layer orchestration
      - Error handling
   
   g. **Dependencies** (`app/dependencies.py`)
      - Database session dependency
      - Authentication dependency
      - Common dependencies
   
   h. **Routers** (`app/routers/`)
      - Route handlers
      - Input validation
      - Response formatting
      - Error responses
   
   i. **Main Application** (`app/main.py`)
      - FastAPI app initialization
      - Router registration
      - Middleware configuration
      - CORS setup
      - Global error handlers

4. **Implementation Best Practices**
   
   - **Type Hints**: Use type hints everywhere for better IDE support
   - **Dependency Injection**: Use FastAPI's dependency injection system
   - **Error Handling**: Create custom exception classes and handlers
   - **Logging**: Add structured logging throughout
   - **Validation**: Use Pydantic models for all input/output
   - **Security**: Implement proper authentication and authorization
   - **Documentation**: FastAPI auto-generates OpenAPI docs
   - **Testing**: Write tests as you build (optional but recommended)

### Phase 5: Error Resolution

**Objective**: Identify and fix all errors using systematic debugging.

1. **Initial Error Detection**
   - Try to import the FastAPI app
   - Check for syntax errors
   - Verify all imports are correct
   - Validate configuration

2. **Apply Error Root Analyzer Skill**
   
   When errors are encountered, use the `@error-root-analyzer` skill:
   
   ```
   @error-root-analyzer
   
   The FastAPI app has the following error:
   [paste error traceback]
   
   Please analyze the root cause and provide comprehensive fixes.
   ```
   
   The error-root-analyzer will:
   - Identify root causes (not just symptoms)
   - Review the entire module for related issues
   - Implement holistic fixes
   - Prevent similar errors
   
   See `@SKILLS/error-root-analyzer/SKILL.md` for details.

3. **Iterative Error Resolution**
   
   Repeat until all errors are resolved:
   
   a. **Run the app**
      ```bash
      uvicorn app.main:app --reload
      ```
   
   b. **Capture errors**
      - Full stack trace
      - Error type and message
      - Line numbers
      - Context
   
   c. **Apply error-root-analyzer**
      - Analyze root cause
      - Review affected modules
      - Implement comprehensive fixes
   
   d. **Verify fix**
      - Test the specific error case
      - Check for regressions
      - Ensure no new errors introduced
   
   e. **Document the fix**
      - What was the error
      - What was the root cause
      - What was fixed
      - How to prevent in future

4. **Common FastAPI Error Patterns**
   
   - **Import Errors**: Missing dependencies, circular imports
   - **Pydantic Validation**: Schema mismatches, type errors
   - **Database Errors**: Connection issues, migration problems
   - **Dependency Injection**: Incorrect dependency signatures
   - **Async/Await**: Missing await keywords, sync/async mixing
   - **CORS Issues**: Incorrect middleware configuration
   - **Authentication**: JWT token validation, password hashing

### Phase 6: Application Launch

**Objective**: Successfully run the FastAPI application.

1. **Pre-Launch Checks**
   - All dependencies installed
   - Environment variables configured
   - Database migrations applied (if applicable)
   - No import errors
   - No syntax errors

2. **Launch the Application**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Verify Successful Launch**
   - Server starts without errors
   - Check startup logs
   - Verify health endpoint (if implemented)
   - Access interactive API docs at `http://localhost:8000/docs`
   - Access alternative docs at `http://localhost:8000/redoc`

4. **Basic Smoke Tests**
   - Test a simple GET endpoint
   - Test authentication (if implemented)
   - Verify CORS headers (if needed)
   - Check error responses format

5. **Document Running Application**
   - Server URL and port
   - API documentation URL
   - How to stop/restart
   - Environment requirements
   - Next steps for development

## Key Principles

1. **Documentation First**: Always review documentation before coding
2. **Plan Before Build**: Create detailed specifications before implementation
3. **Systematic Implementation**: Follow the logical order of dependencies
4. **Zero Errors**: Use error-root-analyzer to achieve error-free execution
5. **Clean Architecture**: Separate concerns (routers, services, repositories)
6. **Type Safety**: Use Pydantic and type hints throughout
7. **Security First**: Implement authentication/authorization properly
8. **Auto-Documentation**: Leverage FastAPI's automatic OpenAPI generation

## FastAPI Best Practices

### Project Structure

Use layered architecture:
- **Routers**: Handle HTTP requests/responses
- **Services**: Implement business logic
- **Repositories**: Access data layer
- **Models**: Define data structures (Pydantic + SQLAlchemy)

### Configuration Management

Use Pydantic Settings:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### Dependency Injection

Create reusable dependencies:

```python
from fastapi import Depends
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/items/")
def read_items(db: Session = Depends(get_db)):
    return db.query(Item).all()
```

### Error Handling

Create custom exception handlers:

```python
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

class CustomException(Exception):
    def __init__(self, message: str):
        self.message = message

@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=400,
        content={"message": exc.message}
    )
```

### Authentication

Use OAuth2 with JWT:

```python
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username
```

## Integration with Error Root Analyzer

This skill integrates tightly with the `error-root-analyzer` skill:

1. **When to Use Error Root Analyzer**
   - Any error occurs during implementation
   - Import errors when starting the app
   - Runtime errors during testing
   - Database connection issues
   - Pydantic validation failures

2. **How to Invoke**
   ```
   @error-root-analyzer
   
   Error encountered in FastAPI app:
   [error details]
   ```

3. **What Error Root Analyzer Provides**
   - Root cause identification (not just symptoms)
   - Comprehensive module review
   - Holistic fixes for all related issues
   - Prevention mechanisms

## Success Criteria

A successful FastAPI backend implementation has:

✅ Complete architecture documentation
✅ All routers implemented according to spec
✅ All endpoints functioning correctly
✅ Zero errors when starting the application
✅ Proper error handling and validation
✅ Interactive API documentation accessible
✅ Type hints and Pydantic models throughout
✅ Clean separation of concerns (routers/services/repositories)
✅ Ready for development and testing

## Reference Materials

See the `references/` directory for:
- FastAPI patterns and examples
- Common error solutions
- Authentication implementations
- Database integration patterns
