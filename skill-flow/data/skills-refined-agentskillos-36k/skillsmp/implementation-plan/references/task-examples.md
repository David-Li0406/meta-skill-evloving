# Task Examples by Language

This reference provides common task patterns for implementation plans across different programming languages and project types.

## Python Projects

### Web Application (Django/FastAPI)
```markdown
## Tasks
- [ ] Task 1: Create database models for User and Post
- [ ] Task 2: Implement API endpoints for CRUD operations
- [ ] Task 3: Add authentication middleware
- [ ] Task 4: Write unit tests for API endpoints
- [ ] Task 5: Set up database migrations
```

### CLI Tool
```markdown
## Tasks
- [ ] Task 1: Implement argument parsing with click/typer
- [ ] Task 2: Create main command handler
- [ ] Task 3: Add configuration file support
- [ ] Task 4: Implement logging functionality
- [ ] Task 5: Write integration tests
```

## JavaScript/TypeScript Projects

### React Application
```markdown
## Tasks
- [ ] Task 1: Set up project structure with Vite
- [ ] Task 2: Create main App component with routing
- [ ] Task 3: Implement state management (Zustand/Redux)
- [ ] Task 4: Build reusable UI components
- [ ] Task 5: Add API integration layer
- [ ] Task 6: Write component tests with Vitest
```

### Node.js API
```markdown
## Tasks
- [ ] Task 1: Set up Express server with middleware
- [ ] Task 2: Define API routes and handlers
- [ ] Task 3: Implement database layer with Prisma
- [ ] Task 4: Add input validation with Zod
- [ ] Task 5: Write API tests with Supertest
```

## Go Projects

### Microservice
```markdown
## Tasks
- [ ] Task 1: Define service interfaces and structs
- [ ] Task 2: Implement HTTP handlers
- [ ] Task 3: Add database repository layer
- [ ] Task 4: Implement service business logic
- [ ] Task 5: Add middleware for logging/auth
- [ ] Task 6: Write table-driven tests
```

### CLI Tool
```markdown
## Tasks
- [ ] Task 1: Set up Cobra command structure
- [ ] Task 2: Implement root command
- [ ] Task 3: Add subcommands with flags
- [ ] Task 4: Implement configuration loading
- [ ] Task 5: Add error handling and logging
```

## Rust Projects

### CLI Tool
```markdown
## Tasks
- [ ] Task 1: Set up project with Clap for argument parsing
- [ ] Task 2: Implement main command logic
- [ ] Task 3: Add error handling with thiserror
- [ ] Task 4: Implement configuration file parsing
- [ ] Task 5: Write unit tests with built-in test framework
```

## DevOps/Infrastructure

### Docker Setup
```markdown
## Tasks
- [ ] Task 1: Create Dockerfile for application
- [ ] Task 2: Write docker-compose configuration
- [ ] Task 3: Add environment variable management
- [ ] Task 4: Set up volume mounts for development
- [ ] Task 5: Configure health checks
```

### CI/CD Pipeline
```markdown
## Tasks
- [ ] Task 1: Create GitHub Actions workflow file
- [ ] Task 2: Configure build step for application
- [ ] Task 3: Add automated testing stage
- [ ] Task 4: Set up deployment to staging
- [ ] Task 5: Add production deployment with approval
```

## Database Tasks

### Schema Changes
```markdown
## Tasks
- [ ] Task 1: Design new table schema
- [ ] Task 2: Create migration file
- [ ] Task 3: Write rollback migration
- [ ] Task 4: Test migration on dev database
- [ ] Task 5: Update ORM models
```

## General Task Patterns

### Feature Implementation
```markdown
## Tasks
- [ ] Task 1: Design API interface
- [ ] Task 2: Implement core logic
- [ ] Task 3: Add error handling
- [ ] Task 4: Write unit tests
- [ ] Task 5: Write integration tests
- [ ] Task 6: Update documentation
```

### Bug Fix
```markdown
## Tasks
- [ ] Task 1: Reproduce and diagnose issue
- [ ] Task 2: Identify root cause
- [ ] Task 3: Implement fix
- [ ] Task 4: Add regression test
- [ ] Task 5: Verify fix resolves issue
- [ ] Task 6: Update related documentation
```

### Refactoring
```markdown
## Tasks
- [ ] Task 1: Identify code to refactor
- [ ] Task 2: Write tests for existing behavior
- [ ] Task 3: Implement refactored code
- [ ] Task 4: Verify tests still pass
- [ ] Task 5: Update any dependent code
- [ ] Task 6: Update documentation
```

## Task Writing Guidelines

### Be Specific
- **Good**: "Add user authentication with JWT tokens"
- **Bad**: "Work on auth"

### Keep Tasks Independent
- Each task should be completable without blocking others
- If tasks depend on each other, note the dependency

### Make Tasks Verifiable
- Include clear acceptance criteria
- Task is complete when verification passes

### Reasonable Scope
- Tasks should take 30 minutes to 2 hours
- Break larger work into multiple tasks
