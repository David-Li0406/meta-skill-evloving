# faion-software-developer

Full-stack software development skill covering Python, JavaScript/TypeScript, backend languages, testing, API design, and browser automation. Contains 111 methodologies and 14,690+ lines of technical reference.

## Overview

This skill orchestrates all software development activities. It provides patterns, best practices, and code examples for modern development across multiple languages and frameworks. Used by code and test agents for consistent, production-quality output.

## Structure

| Path | Purpose |
|------|---------|
| `SKILL.md` | Main skill definition, quick reference, methodology index |
| `ref-*.md` | Technical reference documents (28 files, ~14,000 lines) |
| `django-*.md` | Django-specific patterns and conventions (7 files) |
| `*.md` | Methodologies (112 files) |

## Agents

| Agent | Purpose |
|-------|---------|
| faion-code-agent | Code generation and review |
| faion-test-agent | Test generation and execution |
| faion-frontend-brainstormer-agent | Generate 3-5 design variants |
| faion-storybook-agent | Setup/maintain Storybook |
| faion-frontend-component-agent | Develop components with stories |

## Key References

| File | Content | Lines |
|------|---------|-------|
| ref-python.md | Python, Django, FastAPI, pytest, typing | ~1760 |
| ref-javascript.md | TypeScript, React, Node.js, Bun, testing | ~1350 |
| ref-go-backend.md | Go backend, Gin, Echo, concurrency | ~500 |
| ref-testing.md | pytest, Jest, Vitest, E2E testing | ~1810 |
| ref-browser-automation.md | Puppeteer, Playwright, scraping | ~1490 |
| ref-methodologies.md | 68 development methodologies | ~1573 |
| ref-best-practices-2026.md | AI-assisted development, modern patterns | ~600 |

## Methodologies

Organized by domain with semantic naming:

- **Python**: python.md, testing.md, django/ (7 files)
- **JavaScript/TypeScript**: javascript.md, testing.md, frontend-design.md
- **Backend**: go-backend.md, ruby-rails.md, php-laravel.md, java-spring.md, csharp-dotnet.md, rust-backend.md
- **API Design**: rest-api-design.md, graphql-api.md, openapi-specification.md, api-versioning.md, api-authentication.md

## Quick Commands

```bash
# Python
black src/ && isort src/           # Format
pytest --cov=src                   # Test

# JavaScript/TypeScript
prettier --write .                 # Format
eslint . --fix                     # Lint
vitest run --coverage              # Test
```

## Language Selection

| Language | Use Case |
|----------|----------|
| Python | Backend APIs, data processing, ML, scripting |
| TypeScript | Frontend, Node.js backend, full-stack |
| Go | High-performance services, CLI tools |
| Rust | Systems programming, WASM |

## Framework Selection

| Framework | Use Case |
|-----------|----------|
| Django | Full-featured web apps, admin panels |
| FastAPI | Modern async APIs, microservices |
| React | Complex UIs, SPAs |
| Next.js | Full-stack React, SSR/SSG |

## Related Skills

| Skill | Relationship |
|-------|--------------|
| faion-devops | Deployment, CI/CD, infrastructure |
| faion-ml | AI/ML integrations |
| faion-sdd | Specification-driven development |
