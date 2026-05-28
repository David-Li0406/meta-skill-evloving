---
name: agent-ops-project-sections
description: Use this skill when you need to identify and map different sections of a software project for context scoping and architecture documentation.
---

# Project Section Identification Workflow

## Purpose

Analyze a software project to identify and categorize its logical sections (backend API, frontend, database layer, CLI, domain logic, etc.). This enables:

- **Context scoping**: Focus agent work on specific project areas.
- **Architecture documentation**: Generate structured overview.
- **Dependency analysis**: Understand how sections relate.
- **Instruction optimization**: Input for optimizing prompt/skill context.

## When to Use

- Starting work on an unfamiliar codebase.
- Need to scope work to a specific layer (e.g., "just the API").
- Generating architecture documentation.
- Preparing context for focused implementation.
- Input for `agent-ops-context-map` or instruction optimization.

## Section Types

| Section Type   | Description                                      | Common Indicators                                      |
|----------------|--------------------------------------------------|-------------------------------------------------------|
| `api`          | REST/GraphQL endpoints, route handlers           | `/api/`, `/routes/`, `controllers/`, OpenAPI specs   |
| `frontend`     | UI components, pages, client-side code           | `/components/`, `/pages/`, `.tsx`, `.vue`, `.svelte` |
| `backend`      | Server-side logic, services                       | `/services/`, `/handlers/`, server entry points      |
| `database`     | Data access, migrations, models                   | `/models/`, `/migrations/`, `/repositories/`, ORM files |
| `cli`          | Command-line interface                             | `/cli/`, `__main__.py`, `bin/`, Typer/Click/Commander |
| `domain`       | Business logic, core entities                     | `/domain/`, `/core/`, `/entities/`, pure logic       |
| `infrastructure`| Cloud, deployment, CI/CD                         | `/infra/`, `/deploy/`, `terraform/`, `docker/`      |
| `tests`        | Test suites                                      | `/tests/`, `*.test.*`, `*.spec.*`                    |
| `config`       | Configuration files                               | `/config/`, `.env*`, `*.config.*`, `settings.*`     |
| `docs`         | Documentation                                     | `/docs/`, `*.md`, OpenAPI, JSDoc                     |
| `scripts`      | Build/utility scripts                             | `/scripts/`, `Makefile`, `package.json` scripts      |
| `shared`       | Shared utilities, types, constants                | `/shared/`, `/common/`, `/utils/`, `/types/`        |

## Procedure

### Phase 1: Project Discovery

1. **Scan root directory** for high-level structure.
2. **Identify project type** from indicators:
   - `package.json` → Node.js project
   - Other indicators based on the section types listed above.