---
name: project-setup-guidelines
description: Use this skill when managing project-specific settings, guidelines, and templates for a TypeScript project.
---

# Project Setup Guidelines

## Project Context

### Basic Settings

- **Project Type**: TypeScript project template for Claude Code
- **Scope**: Configurable based on project requirements
- **Implementation Policy**: LLM-driven implementation, quality-focused, adherence to YAGNI principle

### Technology Stack
- **Core Technologies**: TypeScript, Node.js
- **Testing Framework**: Vitest
- **Quality Management**: Biome, TypeScript strict mode

## Implementation Principles

### Key Features of Implementation Policy
- **LLM-driven Implementation**: Claude Code acts as the primary implementer
- **Quality Focus**: Prioritize quality over speed
- **YAGNI Principle**: Implement only when necessary
- **Systematic Design**: Design process guided by ADR/Design Docs/Work Plans

## Project Configuration File

### .claude/dev-core.local.md

Manage project-specific settings:

```markdown
---
package-manager: pnpm
test-command: pnpm test
lint-command: pnpm lint
build-command: pnpm build
typecheck-command: pnpm typecheck
---

# Project-Specific Settings

## Technology Stack

- Framework: Next.js 14 (App Router)
- UI: shadcn/ui + Tailwind CSS
- State Management: Zustand
- Form Handling: react-hook-form + zod
- Database: PostgreSQL + Prisma
- Authentication: Auth.js

## Directory Structure

Adopt FSD (Feature-Sliced Design):

```
src/
├── app/       # Next.js App Router
├── widgets/   # Page components
├── features/  # User-facing features
├── entities/  # Business entities
└── shared/    # Common components
```

## Coding Standards

- No hardcoding
- Limit use of useEffect
- TypeScript strict mode
```

## Project Template

### Next.js + FSD

```
project/
├── .claude/
│   └── dev-core.local.md
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── widgets/
│   ├── features/
│   │   └── auth/
│   │       ├── api/
│   │       ├── model/
│   │       ├── ui/
│   │       └── index.ts
│   ├── entities/
│   │   └── user/
│   │       ├── model/
│   │       ├── ui/
│   │       └── index.ts
│   └── shared/
│       ├── ui/
│       ├── lib/
│       └── config/
├── prisma/
│   └── schema.prisma
└── package.json
```

## Environment Variable Template

### .env.example

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/db

# Auth
AUTH_SECRET=your_auth_secret

# API
NEXT_PUBLIC_API_URL=http://localhost:3000/api
```

## CI/CD Configuration

### GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "pnpm"
      - run: pnpm install
      - run: pnpm typecheck
      - run: pnpm lint
      - run: pnpm test
```

## Recommended Packages

### Required
- `typescript`: Type safety
- `eslint`: Code quality
- `prettier`: Formatting
- `vitest` / `jest`: Testing

### Recommended
- `zod`: Schema validation
- `react-hook-form`: Form management
- `zustand`: State management
- `prisma`: ORM

## Documentation Structure

```
docs/
├── plans/           # Implementation plans
│   └── issue-123.md
├── api/             # API documentation
│   └── users.md
└── architecture/    # Architectural decisions
    └── adr-001.md
```

## Customization Guide

When using this template for a new project:

1. **Add Project-Specific Information**
   - Target user characteristics
   - Business requirements and constraints
   - Technical constraints

2. **Select Architecture**
   - Choose appropriate patterns from architecture skills

3. **Environment Setup**
   - Implement suitable environment variable management for the project
   - Add project-specific configuration files