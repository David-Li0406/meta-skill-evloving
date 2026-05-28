---
name: faion-software-developer
description: "Developer role: Python, JavaScript/TypeScript, backend, APIs, testing, automation, UI design. Full-stack development with 111 methodologies."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite, Skill
---

# Developer Domain Skill

**Communication: User's language. Code: English.**

## Purpose

Orchestrates all software development activities. Covers programming languages, frameworks, testing, API design, and automation.

---

## Agents

| Agent | Purpose |
|-------|---------|
| faion-code-agent | Code generation and review |
| faion-test-agent | Test generation and execution |
| faion-frontend-brainstormer-agent | Generate 3-5 design variants |
| faion-storybook-agent | Setup/maintain Storybook |
| faion-frontend-component-agent | Develop components with stories |

---

## References

Detailed technical context for each area:

| Reference | Content | Lines |
|-----------|---------|-------|
| [ref-python.md](ref-python.md) | Python, Django, FastAPI, pytest, typing | ~1760 |
| [ref-javascript.md](ref-javascript.md) | TypeScript, React, Node.js, Bun, testing | ~1350 |
| [ref-go-backend.md](ref-go-backend.md) | Go backend, Gin, Echo, concurrency | ~500 |
| [ref-testing.md](ref-testing.md) | Unit, integration, E2E, TDD, coverage | ~1810 |
| [ref-browser-automation.md](ref-browser-automation.md) | Puppeteer, Playwright, scraping | ~1490 |
| [ref-methodologies.md](ref-methodologies.md) | 68 development methodologies (M-DEV-*) | ~1573 |
| [ref-documentation.md](ref-documentation.md) | CLAUDE.md creation templates | ~180 |
| [ref-frontend-design.md](ref-frontend-design.md) | UI brainstorming, Storybook workflow | ~90 |
| [ref-shadcn-ui.md](ref-shadcn-ui.md) | shadcn/ui architecture, CVA, composition | ~160 |
| [ref-tailwind.md](ref-tailwind.md) | Tailwind patterns, class ordering, tokens | ~250 |
| `django-*.md` | Django-specific patterns (7 files) | ~600 |

**Total:** ~14,690 lines of technical reference

---

## Quick Reference

### Language Selection

| Language | When to Use |
|----------|-------------|
| **Python** | Backend APIs, data processing, ML, scripting |
| **TypeScript** | Frontend, Node.js backend, full-stack |
| **Go** | High-performance services, CLI tools |
| **Rust** | Systems programming, WASM |

### Framework Selection

| Framework | Use Case |
|-----------|----------|
| **Django** | Full-featured web apps, admin panels |
| **FastAPI** | Modern async APIs, microservices |
| **React** | Complex UIs, SPAs |
| **Next.js** | Full-stack React, SSR/SSG |
| **Express** | Simple Node.js APIs |
| **Bun** | Fast TypeScript runtime |

### Testing Strategy

| Level | Coverage | Tools |
|-------|----------|-------|
| Unit | 70% | pytest, Vitest, Jest |
| Integration | 20% | pytest-django, Supertest |
| E2E | 10% | Playwright, Cypress |

---

## Methodologies (37)

### Python

| Name | Purpose |
|------|---------|
| python-poetry-setup | Dependency management |
| django-coding-standards | Models, views, services |
| python-fastapi | Routes, dependencies, Pydantic |
| django-pytest | Fixtures, mocking, parametrize |
| python-type-hints | Type safety, mypy |
| code-formatting (in tools) | Black, isort, flake8 |
| virtual-environments (in python.md) | venv, Poetry, pyenv |
| python-async-patterns | asyncio, concurrent execution |

### JavaScript/TypeScript

| Name | Purpose |
|------|---------|
| react-component-architecture | React feature-based structure |
| typescript-strict-mode | Type safety patterns |
| react-hooks | Custom hooks best practices |
| nodejs-service-layer | Controller-Service-Repository |
| error-handling | Custom errors, middleware |
| tdd-workflow | Testing pyramid, unit, integration, E2E balance |
| pnpm-package-management | pnpm, lockfiles, security |
| performance-testing | Memoization, virtualization |

### Backend

| Name | Purpose |
|------|---------|
| clean-architecture | Layers, dependencies |
| database-design | Normalization, indexes |
| caching-strategy | Redis, in-memory, CDN |
| api-authentication | JWT, sessions, OAuth |
| api-rate-limiting | Token bucket, sliding window |
| message-queues | Background jobs, Celery, BullMQ, cron |
| logging-patterns | Structured logs, metrics |
| error-handling | Retry, circuit breaker |

### API Design

| Name | Purpose |
|------|---------|
| api-rest-design | Resources, verbs, status codes |
| api-openapi-spec | Documentation, code generation |
| api-versioning | URL, header, query strategies |
| api-pagination (in rest-design) | Cursor, offset, keyset |
| api-error-handling | Consistent error format |
| api-graphql | Schema, resolvers, N+1 |
| websocket-design | Real-time communication |
| api-security (in rest-design) | CORS, rate limits, validation |

### Development Practices

| Name | Purpose |
|------|---------|
| xp-extreme-programming | XP values, 12 practices, planning game |
| pair-programming | Driver/navigator, ping-pong, strong-style |
| mob-programming | Whole team collaboration, rotation |
| trunk-based-development | Short-lived branches, feature flags |
| continuous-delivery | Pipeline automation, deployment strategies |

---

## Workflows

### New Feature Development

```
1. Understand requirements
2. Design API/data model
3. Write failing tests (TDD)
4. Implement code
5. Pass tests
6. Code review
7. Deploy
```

### Code Review Checklist

- [ ] Follows project conventions
- [ ] Has appropriate tests
- [ ] No security vulnerabilities
- [ ] Error handling complete
- [ ] Performance considered
- [ ] Documentation updated

### Debugging Process

```
1. Reproduce the issue
2. Check logs and stack trace
3. Isolate the problem
4. Write failing test
5. Fix the issue
6. Verify fix
7. Add regression test
```

---

## Code Quality Tools

### Python

```bash
# Format
black src/ && isort src/

# Lint
flake8 src/ && mypy src/

# Test
pytest --cov=src
```

### JavaScript/TypeScript

```bash
# Format
prettier --write .

# Lint
eslint . --fix

# Test
vitest run --coverage
```

### Pre-commit

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.1.0
    hooks: [{ id: black }]
  - repo: https://github.com/pycqa/isort
    rev: 5.13.0
    hooks: [{ id: isort }]
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks: [{ id: mypy }]
```

---

## Project Templates

### Python Backend

```
project/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── models/
│   ├── services/
│   ├── api/
│   └── utils/
├── tests/
├── pyproject.toml
└── Dockerfile
```

### TypeScript Full-Stack

```
project/
├── apps/
│   ├── web/          # Next.js frontend
│   └── api/          # Express/Fastify backend
├── packages/
│   ├── ui/           # Shared components
│   ├── config/       # Shared configs
│   └── types/        # Shared types
├── pnpm-workspace.yaml
└── turbo.json
```

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| faion-devops | Deployment, CI/CD |
| faion-ml | AI/ML integrations |
| faion-sdd | Specification-driven development |

---

## Error Handling

| Issue | Action |
|-------|--------|
| Unknown language | Ask user or infer from files |
| Missing context | Read ref-*.md files for patterns |
| Complex architecture | Use Task tool with Explore agent |

---

*Developer Domain Skill v3.1*
*12 Reference Areas | 70 Methodologies | 5 Agents*
*Consolidated from: faion-development, faion-dev-django, faion-dev-docs, faion-dev-frontend*
