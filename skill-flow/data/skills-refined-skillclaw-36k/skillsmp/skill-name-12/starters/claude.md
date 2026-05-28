---
name: claude
description: Claude Code project configuration template
argument-hint: N/A
---

# CLAUDE.md

This file provides comprehensive guidance to Claude Code when working with **[PROJECT_NAME]** using **[PRIMARY_LANGUAGE]** and **[FRAMEWORK/STACK]**.

## Core Development Philosophy

### KISS (Keep It Simple, Stupid)

Simplicity should be a key goal in design. Choose straightforward solutions over complex ones whenever possible. Simple solutions are easier to understand, maintain, and debug.

### YAGNI (You Aren't Gonna Need It)

Avoid building functionality on speculation. Implement features only when they are needed, not when you anticipate they might be useful in the future.

### DRY (Don't Repeat Yourself)

Every piece of knowledge must have a single, unambiguous, authoritative representation within a system.

### Domain-Driven Design (DDD)

Structure code around business domains. Each domain should be self-contained with clear boundaries, its own models, and business logic.

### Clean Code Principles

Write code that is readable, testable, and maintainable. Functions should do one thing, names should be meaningful, and code should express intent clearly.

### Additional Design Patterns

**[ADDITIONAL_PATTERNS]**

<!-- Examples to add based on project needs:
- Repository Pattern: For data access abstraction
- Factory Pattern: For complex object creation
- Observer Pattern: For event-driven architecture
- Strategy Pattern: For interchangeable algorithms
- Adapter Pattern: For third-party integrations
-->

## 🤖 AI Assistant Guidelines

### Context Awareness

- When implementing features, always check existing patterns first
- Follow DDD principles: respect domain boundaries
- Use existing utilities before creating new ones
- Check for similar functionality in other domains/features

### Common Pitfalls to Avoid

- Creating duplicate functionality
- Overwriting existing tests
- Modifying core frameworks without explicit instruction
- Adding dependencies without checking existing alternatives
- Mixing domain logic with infrastructure concerns
- Creating anemic domain models
- **[PROJECT_SPECIFIC_PITFALLS]**

### Workflow Patterns

- **Test-First Approach**: Write tests before implementation when possible
- Use "think hard" for architecture decisions
- Break complex tasks into smaller, testable units
- Validate understanding before implementation
- Follow existing code patterns and conventions

## 🚀 Technology Stack

### Core Technologies

| Technology            | Version   | Purpose          | Setup Command | Test Command |
| --------------------- | --------- | ---------------- | ------------- | ------------ |
| **[LANGUAGE]**        | [VERSION] | Primary language | [INSTALL_CMD] | [TEST_CMD]   |
| **[FRAMEWORK]**       | [VERSION] | Main framework   | [INSTALL_CMD] | [TEST_CMD]   |
| **[DATABASE]**        | [VERSION] | Data persistence | [INSTALL_CMD] | [TEST_CMD]   |
| **[ADDITIONAL_TECH]** | [VERSION] | [PURPOSE]        | [INSTALL_CMD] | [TEST_CMD]   |

### Development Tools

| Tool               | Version   | Purpose         | Setup           | Verify               |
| ------------------ | --------- | --------------- | --------------- | -------------------- |
| **[LINTER]**       | [VERSION] | Code quality    | `[INSTALL_CMD]` | `[LINT_CMD]`         |
| **[FORMATTER]**    | [VERSION] | Code formatting | `[INSTALL_CMD]` | `[FORMAT_CHECK_CMD]` |
| **[TYPE_CHECKER]** | [VERSION] | Type safety     | `[INSTALL_CMD]` | `[TYPE_CHECK_CMD]`   |
| **[TEST_RUNNER]**  | [VERSION] | Testing         | `[INSTALL_CMD]` | `[TEST_RUN_CMD]`     |

## 🏗️ Project Structure (Domain-Driven Design)

```
[PROJECT_ROOT]/
├── src/
│   ├── domains/              # Business domains (DDD)
│   │   └── [domain-name]/
│   │       ├── __tests__/    # Domain unit tests
│   │       ├── entities/     # Domain entities
│   │       ├── value-objects/ # Value objects
│   │       ├── services/     # Domain services
│   │       ├── repositories/ # Repository interfaces
│   │       ├── events/       # Domain events
│   │       └── index.[ext]   # Domain public API
│   ├── application/          # Application services
│   │   ├── use-cases/        # Business use cases
│   │   └── dto/              # Data transfer objects
│   ├── infrastructure/       # Technical implementations
│   │   ├── persistence/      # Repository implementations
│   │   ├── http/             # HTTP/REST layer
│   │   ├── config/           # Configuration
│   │   └── [external-services]/
│   └── shared/               # Shared kernel
│       ├── errors/           # Common errors
│       ├── types/            # Shared types
│       └── utils/            # Utility functions
├── tests/
│   └── integration/          # Integration tests
├── scripts/                  # Build/deploy scripts
├── [CONFIG_FILES]            # .env.example, etc.
├── [PACKAGE_FILE]            # package.json, pyproject.toml, etc.
├── compose.yml               # Docker Compose configuration
└── CLAUDE.md
```

## 📦 Dependencies

### Core Dependencies

```bash
# Essential production dependencies
[CORE_DEPENDENCY_1] - [PURPOSE]
[CORE_DEPENDENCY_2] - [PURPOSE]
[CORE_DEPENDENCY_3] - [PURPOSE]

# Installation
[INSTALL_ALL_COMMAND]
```

### Development Dependencies

```bash
# Essential development dependencies
[DEV_DEPENDENCY_1] - [PURPOSE]
[DEV_DEPENDENCY_2] - [PURPOSE]
[DEV_DEPENDENCY_3] - [PURPOSE]

# Installation
[INSTALL_DEV_COMMAND]
```

### Dependency Guidelines

- Justify every new dependency
- Check bundle size impact
- Prefer well-maintained packages
- Review security advisories
- **[PROJECT_SPECIFIC_GUIDELINES]**

## 🛡️ Data Validation

### Validation Library: **[VALIDATION_LIB]** (e.g., Zod, Joi, Yup)

```[LANGUAGE]
// Example schema definition
[VALIDATION_SCHEMA_EXAMPLE]

// Example usage
[VALIDATION_USAGE_EXAMPLE]
```

## 🧪 Testing Strategy

### Test Framework: **[TEST_FRAMEWORK]**

```[LANGUAGE]
// Test structure example
[TEST_EXAMPLE]
```

### Test Commands

```bash
# Run all tests
[TEST_COMMAND]

# Run unit tests only
[TEST_UNIT_COMMAND]

# Run integration tests only
[TEST_INTEGRATION_COMMAND]

# Run in watch mode
[TEST_WATCH_COMMAND]
```

## 🔐 Security & Environment

### Environment Variables

```[LANGUAGE]
// Required environment variables
[REQUIRED_ENV_VARS]

// Environment validation
[ENV_VALIDATION_EXAMPLE]
```

### Security Checklist

- [ ] All inputs validated with schemas
- [ ] Environment variables validated at startup
- [ ] Sensitive data never logged
- [ ] Dependencies regularly updated
- [ ] SQL injection prevention (if applicable)
- [ ] XSS prevention (if web app)
- [ ] CORS properly configured (if API)
- [ ] **[PROJECT_SPECIFIC_SECURITY]**

## 📊 Logging

### Logger Configuration: **[LOGGER_NAME]**

```[LANGUAGE]
// Logger setup
[LOGGER_SETUP_EXAMPLE]

// Usage example
[LOGGER_USAGE_EXAMPLE]
```

### Log Levels

- **ERROR**: Application errors requiring attention
- **WARN**: Potentially harmful situations
- **INFO**: General informational messages
- **DEBUG**: Detailed debug information (dev only)

## 🔄 Error Handling

### Error Types

```[LANGUAGE]
// Base error class
[BASE_ERROR_EXAMPLE]

// Domain errors
[DOMAIN_ERROR_EXAMPLE]

// Application errors
[APPLICATION_ERROR_EXAMPLE]
```

## 🐳 Docker Configuration

### compose.yml

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: [development|production]
    ports:
      - "[HOST_PORT]:[CONTAINER_PORT]"
    environment:
      - NODE_ENV=[development|production]
      - [OTHER_ENV_VARS]
    volumes:
      - ./src:/app/src  # For development hot reload
    depends_on:
      - [database]
      - [cache]
    networks:
      - app-network

  [database]:
    image: [DB_IMAGE]:[VERSION]
    ports:
      - "[DB_PORT]:[DB_PORT]"
    environment:
      - [DB_ENV_VARS]
    volumes:
      - db-data:/var/lib/[database]/data
    networks:
      - app-network

  [additional-services]:
    # Redis, ElasticSearch, etc.

volumes:
  db-data:
  [other-volumes]:

networks:
  app-network:
    driver: bridge
```

### Dockerfile

```dockerfile
# Multi-stage build
FROM [BASE_IMAGE]:[VERSION] AS base

# Install system dependencies
[SYSTEM_DEPS_INSTALL]

WORKDIR /app

# Copy dependency files
COPY [PACKAGE_FILES] ./

# Development stage
FROM base AS development
[DEV_SETUP]

# Production build stage
FROM base AS build
[BUILD_COMMANDS]

# Production runtime
FROM [RUNTIME_IMAGE]:[VERSION] AS production
[PRODUCTION_SETUP]

# Non-root user for security
USER [NON_ROOT_USER]

EXPOSE [PORT]

[ENTRYPOINT_COMMAND]
```

## ⚠️ Development Workflow (Critical Guidelines)

Follow this **exact sequence** for every feature/change:

### 1. **Ensure Domain-Driven Design**

- Identify the domain boundary
- Keep domain logic pure (no infrastructure dependencies)
- Define entities, value objects, and domain services

### 2. **Write Tests First (When Possible)**

- Write unit tests for domain logic
- Write integration tests for workflows (NO MOCKS)
- Tests should fail initially

### 3. **Implement the Feature**

- Follow existing patterns in the codebase
- Keep functions small and focused
- Use meaningful names

### 4. **Run Type Checking**

```bash
[TYPE_CHECK_COMMAND]
```

- Fix all type errors before proceeding

### 5. **Run All Tests**

```bash
[TEST_COMMAND]
```

- Ensure all tests pass (especially integration tests)
- No mocking in integration tests

### 6. **Validate Data Schemas**

- Update validation schemas for new endpoints/features
- Ensure all inputs are validated
- Test edge cases and error scenarios

### 7. **Handle Error Scenarios**

- Add proper error handling
- Ensure errors are logged appropriately
- User-friendly error messages

### 8. **Code Quality Check**

```bash
[LINT_COMMAND]
[FORMAT_COMMAND]
```

- Assert plan has been implemented correctly
- Ensure consistent formatting

### 9. **Update Documentation**

- Update relevant docs
- Add/update code comments where needed
- Update API documentation if applicable

### 10. **Final Verification**

- Run the application locally
- Test the feature manually
- Verify no regressions

**IMPORTANT**: Never skip steps. Each step catches different categories of issues.

## 🔧 Commands Reference

```bash
# Development
[DEV_START_COMMAND]        # Start development server
[DEV_WATCH_COMMAND]        # Start with file watching

# Testing
[TEST_COMMAND]             # Run all tests
[TEST_UNIT_COMMAND]        # Run unit tests only
[TEST_INTEGRATION_COMMAND] # Run integration tests only
[TEST_WATCH_COMMAND]       # Run tests in watch mode

# Code Quality
[LINT_COMMAND]             # Run linter
[FORMAT_COMMAND]           # Format code
[TYPE_CHECK_COMMAND]       # Run type checker

# Docker
docker compose up          # Start all services
docker compose up -d       # Start in background
docker compose down        # Stop all services
docker compose logs -f app # Follow app logs

# Database (if applicable)
[DB_MIGRATE_COMMAND]       # Run migrations
[DB_SEED_COMMAND]          # Seed database
[DB_RESET_COMMAND]         # Reset database

# Build & Deploy
[BUILD_COMMAND]            # Build for production
[DEPLOY_COMMAND]           # Deploy to environment
```
