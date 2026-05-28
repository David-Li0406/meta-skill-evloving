---
name: fastapi
description: Comprehensive FastAPI development skill for building APIs from hello world to production-ready applications. Use when building REST APIs, microservices, ML/AI APIs, or full-stack applications with FastAPI. Covers project scaffolding, database integration (PostgreSQL, MySQL, MongoDB, SQLite), testing, Docker deployment, background tasks, file uploads, and production best practices.
---

# FastAPI Development

Build production-ready APIs with FastAPI, from simple hello world to complex microservices.

## Overview

This skill provides everything needed to build FastAPI applications:

- **Project scaffolding** - Generate project structures automatically
- **Database integration** - PostgreSQL, MySQL, MongoDB, SQLite patterns
- **Testing** - Pytest patterns and fixtures
- **Deployment** - Docker, docker-compose, production optimization
- **Advanced features** - Background tasks, file uploads, async operations
- **Templates** - Ready-to-use boilerplate code

## Quick Start Decision Tree

Choose your starting point based on what you're building:

**First time with FastAPI?**
→ Use `assets/hello-world/main.py` template (5 minutes)
→ Run `fastapi dev main.py` and explore http://localhost:8000/docs

**Building a simple CRUD API?**
→ Use `assets/crud-api-template/` (15 minutes)
→ Modify schemas in `schemas.py` for your data model

**Starting a new project from scratch?**
→ Use `scripts/scaffold_project.py` to generate full project structure
→ Choose project type: simple-api, microservice, fullstack, or ml-api

**Adding specific features to existing project?**
→ Database: See `references/databases.md`
→ Testing: See `references/testing.md`
→ Docker: See `references/docker.md`
→ Background tasks: See `references/background_tasks.md`
→ File uploads: See `references/file_uploads.md`

## Building Your First API

### Option 1: Hello World (Fastest)

Copy `assets/hello-world/main.py` to your project:

```bash
cp assets/hello-world/main.py .
pip install -r assets/hello-world/requirements.txt
fastapi dev main.py
```

### Option 2: CRUD API Template

Copy the CRUD template for a complete REST API:

```bash
cp -r assets/crud-api-template/* .
pip install -r requirements.txt
fastapi dev main.py
```

This gives you:
- Complete CRUD operations
- Pydantic validation
- API documentation
- Error handling

### Option 3: Scaffold a New Project

Generate a complete project structure:

```bash
python scripts/scaffold_project.py my-api --type simple-api --database postgresql
```

Project types:
- `simple-api` - Basic REST API with CRUD
- `microservice` - Microservice with health checks
- `fullstack` - Full-stack with frontend integration
- `ml-api` - ML/AI API with model serving

Options:
- `--database` - postgresql, mysql, sqlite, mongodb
- `--docker` - Include Docker configuration
- `--testing` - Include pytest setup

## Adding Database Integration

### Quick Database Setup

For **PostgreSQL, MySQL, or SQLite** (SQL databases):

1. Read `references/databases.md` for your database type
2. Copy the database configuration code
3. Define models with SQLAlchemy
4. Set up migrations with Alembic

For **MongoDB** (NoSQL):

1. Read `references/databases.md` MongoDB section
2. Install Beanie: `pip install motor beanie`
3. Define document models
4. Initialize database on startup

### Common Pattern

```python
# 1. Configure database (references/databases.md)
# 2. Define models
# 3. Create CRUD service functions
# 4. Use in endpoints with Depends(get_db)
```

The scaffolding script (`scripts/scaffold_project.py`) automatically generates this structure when you specify `--database`.

## Adding Features

### Testing

To add comprehensive testing to your project:

1. **Read** `references/testing.md`
2. **Install**: `pip install pytest pytest-asyncio httpx`
3. **Create** `tests/conftest.py` with test client fixture
4. **Write** test files in `tests/` directory
5. **Run**: `pytest --cov=app tests/`

Key patterns from testing.md:
- Test client setup
- Database fixtures
- Async testing
- Mocking external services

### Docker Deployment

To containerize your application:

1. **Read** `references/docker.md`
2. **Create** Dockerfile (see multi-stage build example)
3. **Create** docker-compose.yml
4. **Build**: `docker-compose up --build`

For production:
- Use multi-stage builds
- Run as non-root user
- Add health checks
- Use gunicorn with uvicorn workers

### Background Tasks

For async job processing:

**Simple tasks** (same process):
- Use FastAPI's built-in `BackgroundTasks`
- See `references/background_tasks.md` → FastAPI Background Tasks

**Production tasks** (distributed):
- Use Celery + Redis
- See `references/background_tasks.md` → Celery section
- Includes task monitoring with Flower

**Modern async tasks**:
- Use ARQ (async task queue)
- See `references/background_tasks.md` → ARQ section

### File Uploads

To handle file uploads:

1. **Read** `references/file_uploads.md`
2. Choose your pattern:
   - Single file: Basic pattern
   - Multiple files: Batch upload
   - Large files: Streaming with progress
   - Images: Processing with Pillow
   - CSV/Excel: pandas integration

Key patterns:
- File validation (type, size)
- Unique filenames
- Organized storage
- Cloud storage (S3)

## Production Deployment

### Checklist

Before deploying to production:

1. **Database**
   - Use production database (not SQLite)
   - Set up connection pooling
   - Configure backups
   - Run migrations

2. **Security**
   - Use environment variables for secrets
   - Enable CORS properly
   - Add authentication (JWT, OAuth2)
   - Validate all inputs

3. **Performance**
   - Use gunicorn with uvicorn workers
   - Configure worker count based on CPU cores
   - Add caching (Redis)
   - Optimize database queries

4. **Monitoring**
   - Add health check endpoint
   - Configure logging
   - Set up error tracking
   - Monitor background tasks

5. **Docker**
   - Use production Dockerfile (see `references/docker.md`)
   - Set resource limits
   - Configure restart policies
   - Use docker-compose for multi-service setup

### Production Dockerfile Pattern

See `references/docker.md` → Production Optimization for:
- Multi-stage builds
- Non-root user
- Gunicorn configuration
- Health checks

### Environment Configuration

```python
# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
```

## Resources

### Scripts

**scaffold_project.py** - Generate complete project structures
- Supports 4 project types
- Configurable database backend
- Optional Docker and testing setup
- Run: `python scripts/scaffold_project.py --help`

### References

**databases.md** - Complete database integration guide
- PostgreSQL (sync & async)
- MySQL
- SQLite
- MongoDB with Beanie
- SQLAlchemy patterns
- Migrations with Alembic

**testing.md** - Comprehensive testing patterns
- Test client setup
- Database fixtures
- Async testing
- Mocking patterns
- Authentication testing
- File upload testing
- Coverage reporting

**docker.md** - Docker deployment guide
- Basic Dockerfile
- Multi-stage builds
- docker-compose configurations
- Production optimization
- Health checks
- Logging

**background_tasks.md** - Async job processing
- FastAPI BackgroundTasks
- Celery + Redis setup
- ARQ (async task queue)
- Scheduled tasks
- Task monitoring

**file_uploads.md** - File handling patterns
- Single & multiple uploads
- File validation
- Large file streaming
- Image processing
- CSV/Excel handling
- Cloud storage (S3)

### Assets

**hello-world/** - Minimal FastAPI application
- Single file setup
- Perfect for learning
- 3 example endpoints

**crud-api-template/** - Complete CRUD API
- Full REST API implementation
- Pydantic schemas
- Error handling
- Pagination
- Easy to customize

## Common Workflows

### Building a Simple API

1. Copy CRUD template: `cp -r assets/crud-api-template/* .`
2. Modify `schemas.py` with your data model
3. Update `main.py` with your business logic
4. Run: `fastapi dev main.py`
5. Test at http://localhost:8000/docs

### Building with Database

1. Scaffold project: `python scripts/scaffold_project.py myapi --database postgresql`
2. Configure `.env` with database credentials
3. Define models in `app/models/`
4. Create schemas in `app/schemas/`
5. Implement CRUD in `app/services/`
6. Add endpoints in `app/api/endpoints/`
7. Run migrations: `alembic upgrade head`

### Adding to Existing Project

**Add Database:**
1. Read `references/databases.md` for your DB type
2. Install dependencies
3. Create `app/core/database.py` with configuration
4. Define models
5. Add `get_db` dependency to endpoints

**Add Testing:**
1. Read `references/testing.md`
2. Install pytest dependencies
3. Create `tests/conftest.py`
4. Write tests in `tests/`
5. Run with `pytest`

**Add Docker:**
1. Read `references/docker.md`
2. Create Dockerfile
3. Create docker-compose.yml
4. Build and run: `docker-compose up`

### Deploying to Production

1. Review production checklist above
2. Create production Dockerfile (see `references/docker.md`)
3. Set up docker-compose with all services
4. Configure environment variables
5. Run database migrations
6. Start with: `docker-compose -f docker-compose.prod.yml up -d`
7. Monitor with health checks and logging

## Best Practices

1. **Always use type hints** - FastAPI uses them for validation
2. **Separate concerns** - Keep models, schemas, and services separate
3. **Use dependency injection** - For database sessions, auth, etc.
4. **Validate inputs** - Let Pydantic handle it with schemas
5. **Handle errors properly** - Use HTTPException with clear messages
6. **Test thoroughly** - Aim for high coverage on critical paths
7. **Use async** when needed - For I/O-bound operations
8. **Keep it simple** - Don't over-engineer early
9. **Read the docs** - Use references for detailed patterns
10. **Use the scaffolding** - Don't start from scratch every time
