---
id: claude-md-creation
name: "CLAUDE.md Creation"
domain: DEV
skill: faion-software-developer
category: "development"
---

# CLAUDE.md Creation

## Overview

CLAUDE.md is a project-specific instruction file that provides Claude Code with context about the codebase, conventions, and workflows. A well-crafted CLAUDE.md enables Claude to work more effectively within your project's constraints.

## When to Use

- Setting up a new project for Claude Code
- Onboarding Claude to an existing codebase
- Documenting project-specific conventions
- Providing quick reference for common operations
- Maintaining consistency across AI-assisted development

## Key Principles

- **Be concise**: Claude has limited context window
- **Be specific**: Exact commands, paths, conventions
- **Be current**: Update when project changes
- **Be structured**: Easy to scan and reference
- **Be practical**: Focus on what Claude needs to know

## Best Practices

### Basic CLAUDE.md Structure

```markdown
# CLAUDE.md

## Project Overview
One paragraph describing the project, its purpose, and architecture.

## Tech Stack
- **Language**: Python 3.11
- **Framework**: FastAPI
- **Database**: PostgreSQL 15
- **Cache**: Redis
- **Queue**: Celery

## Quick Commands

```bash
# Development
make dev          # Start development server
make test         # Run all tests
make lint         # Run linters

# Database
make migrate      # Apply migrations
make seed         # Seed test data
```

## Project Structure

```
src/
├── api/          # FastAPI routes
├── core/         # Business logic
├── models/       # SQLAlchemy models
├── schemas/      # Pydantic schemas
└── services/     # External integrations
```

## Conventions

### Code Style
- Follow PEP 8
- Use type hints everywhere
- Docstrings for public functions

### Naming
- Files: snake_case
- Classes: PascalCase
- Functions: snake_case
- Constants: UPPER_SNAKE_CASE

### Git
- Branch: `feature/TICKET-description`
- Commit: `type: description`

## Key Files
- `config/settings.py` - Configuration
- `src/core/` - Business logic
- `tests/` - Test files mirror src structure
```

### Full CLAUDE.md Template

```markdown
# CLAUDE.md - [Project Name]

## Overview
[Brief description of the project and its purpose]

## Architecture

### System Diagram
```
[Simple ASCII diagram if helpful]
User → API Gateway → Backend → Database
                  ↓
              Redis Cache
```

### Key Components
| Component | Purpose | Location |
|-----------|---------|----------|
| API | REST endpoints | `src/api/` |
| Services | Business logic | `src/services/` |
| Models | Database entities | `src/models/` |

## Development Setup

### Prerequisites
- Python 3.11+
- Docker and Docker Compose
- Node.js 18+ (for frontend)

### Quick Start
```bash
# Clone and setup
git clone <repo>
cd project
cp .env.example .env

# Start services
docker-compose up -d

# Install dependencies
pip install -e ".[dev]"

# Run migrations
alembic upgrade head

# Start server
uvicorn src.main:app --reload
```

### Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection | Required |
| `REDIS_URL` | Redis connection | `redis://localhost` |
| `SECRET_KEY` | JWT signing key | Required |
| `DEBUG` | Enable debug mode | `false` |

## Commands Reference

### Development
```bash
# Run development server
make dev
# or: uvicorn src.main:app --reload --port 8000

# Run with debugger
python -m debugpy --listen 5678 -m uvicorn src.main:app --reload
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/test_users.py::test_create_user -v

# Run only fast tests
pytest -m "not slow"
```

### Database
```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Reset database (dev only)
make db-reset
```

### Code Quality
```bash
# Format code
black src tests
isort src tests

# Lint
ruff check src tests
mypy src

# All checks
make lint
```

## Code Conventions

### File Organization
```
src/
├── api/
│   ├── __init__.py
│   ├── deps.py         # Dependencies (auth, db)
│   └── v1/
│       ├── __init__.py
│       └── users.py    # User endpoints
├── core/
│   ├── config.py       # Settings
│   └── security.py     # Auth helpers
├── models/
│   ├── __init__.py
│   └── user.py         # SQLAlchemy models
├── schemas/
│   ├── __init__.py
│   └── user.py         # Pydantic schemas
└── services/
    ├── __init__.py
    └── email.py        # External services
```

### Naming Conventions
- **Files**: `snake_case.py`
- **Classes**: `PascalCase`
- **Functions**: `snake_case`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private**: `_leading_underscore`

### Import Order
```python
# Standard library
import os
from datetime import datetime

# Third-party
from fastapi import FastAPI
from sqlalchemy import Column

# Local
from src.core.config import settings
from src.models.user import User
```

### Type Hints
Always use type hints for function signatures:
```python
def get_user(user_id: int) -> User | None:
    ...

async def list_users(
    skip: int = 0,
    limit: int = 100,
) -> list[User]:
    ...
```

### Docstrings
Google style for public functions:
```python
def process_order(order_id: str, user: User) -> OrderResult:
    """Process an order for the given user.

    Args:
        order_id: Unique order identifier.
        user: The user placing the order.

    Returns:
        OrderResult with status and details.

    Raises:
        OrderNotFoundError: If order doesn't exist.
    """
```

## Git Workflow

### Branch Naming
```
feature/PROJ-123-add-user-auth
bugfix/PROJ-456-fix-login-error
hotfix/PROJ-789-security-patch
```

### Commit Format
```
type: short description

Longer description if needed.

Refs: PROJ-123
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### PR Process
1. Create branch from `develop`
2. Make changes with tests
3. Run `make lint test`
4. Push and create PR
5. Get code review
6. Squash merge to `develop`

## Testing

### Test Structure
```
tests/
├── conftest.py          # Shared fixtures
├── unit/
│   └── test_services.py
├── integration/
│   └── test_api.py
└── e2e/
    └── test_flows.py
```

### Test Naming
```python
def test_create_user_with_valid_data_succeeds():
    ...

def test_create_user_with_duplicate_email_raises_error():
    ...
```

### Fixtures Location
- `conftest.py` in tests root for shared fixtures
- Local `conftest.py` for module-specific fixtures

## API Patterns

### Endpoint Structure
```python
@router.post(
    "/",
    response_model=UserResponse,
    status_code=201,
)
async def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
) -> User:
    """Create a new user."""
    return await user_service.create(db, user_in)
```

### Error Handling
```python
from fastapi import HTTPException

raise HTTPException(
    status_code=404,
    detail="User not found"
)
```

## Common Tasks

### Add New Endpoint
1. Create schema in `src/schemas/`
2. Add route in `src/api/v1/`
3. Implement service logic
4. Add tests
5. Update OpenAPI docs if needed

### Add New Model
1. Create model in `src/models/`
2. Create migration: `alembic revision --autogenerate`
3. Apply migration: `alembic upgrade head`
4. Add repository methods
5. Add tests

### Debug Issues
1. Check logs: `docker-compose logs -f api`
2. Enable SQL logging in `.env`: `SQLALCHEMY_ECHO=true`
3. Use debugger: See development commands above

## External Services

### Database
- Host: `localhost:5432` (dev)
- Name: `project_db`
- Migrations: Alembic

### Redis
- Host: `localhost:6379` (dev)
- Used for: Caching, sessions, rate limiting

### Email (SendGrid)
- Test mode in development
- Templates in `templates/email/`

## Troubleshooting

### Common Issues

**Database connection refused**
```bash
docker-compose up -d postgres
```

**Migration errors**
```bash
alembic downgrade -1
alembic upgrade head
```

**Import errors**
```bash
pip install -e ".[dev]"
```

## Links

- [API Docs](http://localhost:8000/docs)
- [Project Board](https://github.com/org/repo/projects)
- [Wiki](https://github.com/org/repo/wiki)
```

### CLAUDE.md for Monorepos

```markdown
# CLAUDE.md - Monorepo

## Structure
```
/
├── apps/
│   ├── web/           # Next.js frontend
│   ├── api/           # FastAPI backend
│   └── worker/        # Background jobs
├── packages/
│   ├── ui/            # Shared React components
│   ├── config/        # Shared configuration
│   └── types/         # Shared TypeScript types
└── infrastructure/    # Terraform, K8s configs
```

## Per-App Instructions

### Web (apps/web)
See [apps/web/CLAUDE.md](apps/web/CLAUDE.md)

### API (apps/api)
See [apps/api/CLAUDE.md](apps/api/CLAUDE.md)

### Worker (apps/worker)
See [apps/worker/CLAUDE.md](apps/worker/CLAUDE.md)

## Cross-Cutting Concerns

### Shared Types
All shared types are in `packages/types/`
Import as: `import { User } from '@repo/types'`

### Running All Services
```bash
# Start everything
turbo dev

# Build all
turbo build

# Test all
turbo test
```
```

### Minimal CLAUDE.md

```markdown
# CLAUDE.md

## Commands
```bash
npm run dev    # Development
npm test       # Tests
npm run build  # Production build
```

## Structure
- `src/` - Source code
- `tests/` - Tests
- `docs/` - Documentation

## Conventions
- TypeScript strict mode
- ESLint + Prettier
- Conventional commits
```

## Anti-patterns

- **Too much information**: Overwhelming context
- **Stale content**: Instructions that don't work
- **Duplicate docs**: Same info in README and CLAUDE.md
- **Missing commands**: Not including how to run/test
- **No structure**: Wall of text without sections
- **Wrong audience**: Written for humans, not AI

## References

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Memory and Context](https://docs.anthropic.com/en/docs/claude-code/memory)
- [Project Setup Best Practices](https://docs.anthropic.com/en/docs/claude-code/project-setup)
