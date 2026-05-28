---
name: backend-development
description: Use this skill when building scalable backend systems, optimizing database queries, implementing business logic, and ensuring security across various technologies.
---

# Backend Development

This skill provides a comprehensive toolkit for building robust, scalable, and secure backend systems using various technologies including NodeJS, Express, Go, Python, FastAPI, Postgres, GraphQL, and REST APIs.

## Core Capabilities

### 1. API Design & Implementation
- **RESTful Design**: Resource-oriented URLs, proper HTTP methods, and status codes.
- **Best Practices**: Validation, dependency injection, and async handlers.
- **Documentation**: Automatic OpenAPI generation with clear descriptions and examples.

### 2. Database Management
- **Schema Design**: Normalized relationships, indexing strategies, and migration management.
- **ORM Usage**: Efficient session management and repository patterns.
- **Optimization**: Avoiding N+1 problems, query analysis, and connection pooling.

### 3. Security
- **Authentication**: Implementing JWT/OAuth2, password hashing.
- **Authorization**: Role-Based Access Control (RBAC) and scopes.
- **Data Protection**: Input sanitization and SQL injection prevention.

### 4. Performance Tuning
- **Caching**: Implementing caching strategies using Redis.
- **Async I/O**: Utilizing non-blocking calls for databases and APIs.
- **Background Tasks**: Offloading heavy processing tasks.

## Quick Start

### Main Capabilities

This skill provides automated scripts for key tasks:

```bash
# Script 1: API Scaffolder
python scripts/api_scaffolder.py <project-path> [options]

# Script 2: Database Migration Tool
python scripts/database_migration_tool.py <target-path> [--verbose]

# Script 3: API Load Tester
python scripts/api_load_tester.py [arguments] [options]
```

## Development Workflow

### 1. Setup and Configuration

```bash
# Install dependencies
npm install
# or
pip install -r requirements.txt

# Configure environment
cp .env.example .env
```

### 2. Run Quality Checks

```bash
# Use the analyzer script
python scripts/database_migration_tool.py .

# Review recommendations and apply fixes
```

### 3. Implement Best Practices

Follow documented patterns and practices for API design, database optimization, and security.

## Best Practices Summary

### Code Quality
- Follow established patterns and write comprehensive tests.
- Document decisions and review code regularly.

### Performance
- Measure before optimizing and use appropriate caching.
- Optimize critical paths and monitor in production.

### Security
- Validate all inputs and use parameterized queries.
- Implement proper authentication and keep dependencies updated.

### Maintainability
- Write clear code with consistent naming and helpful comments.

## Common Commands

```bash
# Development
npm run dev
npm run build
npm run test
npm run lint

# Analysis
python scripts/database_migration_tool.py .
python scripts/api_load_tester.py --analyze

# Deployment
docker build -t app:latest .
docker-compose up -d
kubectl apply -f k8s/
```

## Troubleshooting

### Common Issues

Refer to the troubleshooting section in the backend security practices documentation.

### Getting Help

- Review reference documentation and script output messages.
- Consult tech stack documentation and error logs.

## Resources

- API Design Patterns
- Database Optimization Guide
- Backend Security Practices
- Tool Scripts