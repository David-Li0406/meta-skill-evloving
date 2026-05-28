---
name: FastAPI Stack Development
description: Comprehensive guidance for FastAPI, Typer, and SQLModel development including patterns, best practices, API design, CLI development, database integration, testing, and common workflows. Use this skill when building applications with any of these frameworks.
---

# FastAPI Stack Development Skill

This skill provides guidance for the FastAPI ecosystem: **FastAPI** (web APIs), **Typer** (CLI tools), and **SQLModel** (database models). All three frameworks share common patterns and work seamlessly together.

## When to Use This Skill

Load this skill when you are:
- Building FastAPI applications and REST APIs
- Creating Typer CLI tools and utilities
- Designing SQLModel database schemas and queries
- Developing applications combining these technologies
- Refactoring or debugging FastAPI stack code
- Setting up new projects with this stack

Unload this skill when you're done with FastAPI/CLI/DB work to free up context.

## FastAPI Core Concepts

### Application Structure
- Organize routes into routers by domain or feature
- Use dependencies for shared logic (auth, DB sessions, config)
- Separate business logic from route handlers (service layer)
- Keep `main.py` minimal - import and include routers

### Pydantic Models & Validation
- Use Pydantic models for request/response bodies
- Leverage field validators for complex validation
- Separate request models from response models
- Use `Field()` for metadata (examples, constraints, descriptions)
- Consider using `BaseModel` vs `SQLModel` appropriately

### Dependency Injection
- Use `Depends()` for injectable components
- Create reusable dependencies (auth, caching, rate limiting)
- Use `yield` for resource cleanup (DB sessions, files)
- Cache dependencies with `use_cache=True` (default) or `use_cache=False`

### Async/Await & Performance
- Use `async def` for I/O-bound operations (DB queries, HTTP requests)
- Use `def` for CPU-bound operations or when not async-ready
- Database: Use `AsyncSession` for async drivers (asyncpg, aiomysql)
- Background tasks with `BackgroundTasks` for fire-and-forget operations

### Middleware & Security
- Add middleware for CORS, logging, compression
- Implement security: OAuth2 scopes, API keys, JWT
- Use `fastapi.security` utilities for auth schemes
- Validate origins in production for CORS

## Typer CLI Development

### Command Structure
- Use `typer.Typer()` for the main app instance
- Create subcommands with `@app.command()` or separate apps with `app.add_typer()`
- Use `app.callback()` for global options and setup
- Group related commands logically

### Arguments & Options
- Use arguments for required positional inputs
- Use options for optional parameters with defaults
- Leverage rich types (Path, File, enums) for automatic validation
- Use `rich` integration for formatted output (tables, panels, progress)

### Testing CLI
- Use `CliRunner` from `typer.testing` for unit tests
- Test happy paths, error cases, and validation
- Mock external dependencies (API calls, DB operations)

### Integration with FastAPI
- Share Pydantic models between API and CLI
- Use CLI for admin tasks (seed DB, migrations, diagnostics)
- Reuse service layer logic between endpoints and commands

## SQLModel Database Patterns

### Model Design
- Use `SQLModel` for tables that map to database
- Use `Field()` for DB constraints (primary_key, index, unique)
- Define relationships with back_populates
- Use `Field(default=None)` for nullable columns
- Separate read/write models with `Field(exclude=True)` or separate classes

### Session Management
- Use `sessionmaker` for DB session factory
- Async: Use `async_sessionmaker` with `AsyncSession`
- Use `yield` in dependencies for automatic cleanup
- Always commit or rollback explicitly

### Query Patterns
- Use `select(Model).where(Model.field == value)` for filtering
- Chain `.where()` conditions with `&` and `|`
- Use `.limit()` and `.offset()` for pagination
- Eager load relationships with `.selectinload()` or `.joinedload()`
- Use `.exec()` for queries, `.scalar_one_or_none()` for single results

### Migrations
- Use Alembic for schema migrations
- Generate migration with `alembic revision --autogenerate`
- Review generated migrations before applying
- Test migrations on a staging database first

## Integration Patterns

### FastAPI + SQLModel
- Create DB dependency that yields a session
- Pass session to service layer, not route handlers
- Use `response_model=` to document output types
- Return Pydantic models directly from endpoints

### Typer + FastAPI
- Share models between `models/` directory
- CLI commands can import FastAPI services
- Use CLI for health checks, data imports, admin tasks

### Pydantic Model Reuse
- Create base models in `models/base.py`
- Use inheritance for request/response variants
- Keep models in `models/` separate from routes
- Consider using `TypeAdapter` for validation outside APIs

### Configuration Management
- Use `pydantic-settings` for environment-based config
- Share config instance across FastAPI and Typer
- Validate config at startup with Pydantic
- Document environment variables in README

## Project Structure

### Recommended Layout
```
project/
├── alembic/              # Database migrations
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app instance
│   ├── cli.py           # Typer CLI app
│   ├── config.py        # Pydantic settings
│   ├── models/          # SQLModel models
│   ├── schemas/         # Request/response models
│   ├── api/             # FastAPI routers
│   ├── services/        # Business logic
│   ├── db/              # Database utilities
│   └── utils/           # Shared utilities
├── tests/
└── requirements.txt     # or pyproject.toml
```

### Separation of Concerns
- Routes: HTTP request/response handling only
- Services: Business logic and orchestration
- Models: Data structures and database schemas
- Utils: Pure functions and helpers

### Test Organization
- Mirror source structure in `tests/`
- Unit tests for services and utilities
- Integration tests for API endpoints
- Use `pytest` and `httpx.AsyncClient` for FastAPI testing

## Common Workflows

### Setting Up a New Project
1. Create virtual environment and install dependencies
2. Initialize FastAPI app in `main.py`
3. Set up `pydantic-settings` in `config.py`
4. Create SQLModel models in `models/`
5. Configure Alembic for migrations
6. Create Typer CLI in `cli.py`
7. Set up test fixtures and tests

### Adding Authentication
1. Install `python-jose` and `passlib` for JWT
2. Create auth dependency with `Depends()`
3. Add login endpoint that returns JWT token
4. Protect routes with `Depends(get_current_user)`
5. Add optional OAuth2 scopes for fine-grained access

### Creating Admin CLI Commands
1. Add command in `cli.py` with `@app.command()`
2. Import models and services from `app/`
3. Add rich output for better UX
4. Add tests with `CliRunner`
5. Document in `--help` text

### Database Migrations
1. Create Alembic config with `alembic init`
2. Set `sqlalchemy.url` in `alembic.ini`
3. Generate migration with `autogenerate`
4. Review and edit migration script
5. Apply with `alembic upgrade head`
6. Add rollback with `alembic downgrade -1`

### Testing Strategies
- Unit tests: Mock DB and external services
- Integration tests: Use test database, real sessions
- FastAPI: Use `httpx.AsyncClient` with test app
- Typer: Use `CliRunner` with test runner
- Use pytest fixtures for common setup (DB, client, auth)

## Best Practices

### Type Hints Across Frameworks
- Always annotate function signatures
- Use `typing.Optional` for nullable fields
- Use `typing.List[Model]` or `list[Model]` for collections
- Leverage Pydantic for runtime type checking
- Run `mypy` or `pyright` for static type checking

### Validation & Error Handling
- Use Pydantic for request validation (automatic)
- Return `HTTPException` for expected errors
- Use custom exception handlers for consistent responses
- Log errors with context (request ID, user ID, params)
- Never expose stack traces in production

### Documentation
- API: OpenAPI/Swagger at `/docs` auto-generated
- Add `description=` to endpoints for better docs
- Add examples to Pydantic fields
- CLI: Use `help=` on arguments and options
- Keep README up-to-date with setup and usage

### Async vs Sync Patterns
- Database: Prefer `AsyncSession` with async drivers
- External APIs: Use `httpx.AsyncClient`
- File I/O: Use `aiofiles` for async operations
- CPU-bound: Use `run_in_executor()` if needed

### Performance Optimization
- Use response compression middleware
- Cache expensive operations with `functools.lru_cache` or Redis
- Use database indexes properly
- Eager load relationships to avoid N+1 queries
- Implement rate limiting on public endpoints

### Security Considerations
- Validate all inputs (Pydantic handles this)
- Sanitize user input for queries (SQLModel parameterized)
- Use HTTPS in production
- Implement rate limiting on auth endpoints
- Regularly update dependencies
- Use secrets management for API keys and passwords

## Progressive Disclosure

When working with this skill:
1. Start with SKILL.md - this gives you the core concepts and patterns
2. Only load additional reference docs when you hit a specific problem
3. Focus on the relevant section (FastAPI, Typer, or SQLModel) based on your current task
4. Refer back to project structure and best practices when refactoring

## Reference Resources

- [FastAPI Official Documentation](https://fastapi.tiangolo.com/)
- [Typer Documentation](https://typer.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
