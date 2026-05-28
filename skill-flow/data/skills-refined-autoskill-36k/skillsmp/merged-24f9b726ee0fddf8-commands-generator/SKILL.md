---
name: commands-generator
description: Use this skill to generate project-specific Claude Code commands and templates based on the project structure and tech stack.
---

# Commands Generator

**Type:** L2 Domain Coordinator  
**Category:** 7XX Project Bootstrap  
**Parent:** None  

Generates `.claude/commands/` with project-specific Claude Code commands from templates.

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | Project structure, tech stack, template name, variable values |
| **Output** | .claude/commands/*.md files |
| **Worker** | Command templates generation |

---

## Workflow

1. **Analyze** project structure and detect tech stack.
2. **Extract** variables (paths, ports, frameworks).
3. **Delegate** to command templates generation with template name and variables.
4. **Verify** generated commands exist.

---

## Generated Commands

| Command | Purpose | Condition |
|---------|---------|-----------|
| refresh_context.md | Restore project context | Always |
| refresh_infrastructure.md | Restart services | Always |
| build-and-test.md | Full verification | Always |
| ui-testing.md | UI tests with Playwright | If Playwright detected |
| deploy.md | Deployment workflow | If CI/CD config exists |
| database-ops.md | Database operations | If database detected |

---

## Available Templates

| Template | Output File | Required |
|----------|-------------|----------|
| `refresh_context_template.md` | refresh_context.md | Always |
| `refresh_infrastructure_template.md` | refresh_infrastructure.md | Always |
| `build_and_test_template.md` | build-and-test.md | Always |
| `ui_testing_template.md` | ui-testing.md | If Playwright |
| `deploy_template.md` | deploy.md | If CI/CD |
| `database_ops_template.md` | database-ops.md | If Database |

---

## Variables Extracted

| Variable | Source | Example |
|----------|--------|---------|
| `{{PROJECT_NAME}}` | package.json / .csproj | "kehai-os" |
| `{{TECH_STACK}}` | Auto-detected | "React + .NET + PostgreSQL" |
| `{{FRONTEND_ROOT}}` | Directory scan | "src/frontend" |
| `{{BACKEND_ROOT}}` | Directory scan | "src/Kehai.Api" |
| `{{FRONTEND_PORT}}` | vite.config / package.json | "3000" |
| `{{BACKEND_PORT}}` | launchSettings.json | "5000" |

---

## Variable Syntax

All templates use Handlebars-style syntax: `{{VARIABLE_NAME}}`

Common variables include:
- `{{PROJECT_NAME}}` — Project name
- `{{FRONTEND_ROOT}}` — Frontend source path
- `{{BACKEND_ROOT}}` — Backend source path
- `{{FRONTEND_PORT}}` — Frontend dev server port
- `{{BACKEND_PORT}}` — Backend API port
- `{{TECH_STACK}}` — Technology stack summary

---

## Detection Logic

**Frontend:** vite.config.ts, package.json (react/vue/angular)  
**Backend:** *.csproj with Web SDK, or express/fastapi in dependencies  
**Database:** docker-compose.yml postgres/mysql, or connection strings  
**Playwright:** playwright.config.ts or @playwright/test in dependencies  
**CI/CD:** .github/workflows/, azure-pipelines.yml, Dockerfile  

---

**Version:** 2.0.0  
**Last Updated:** 2026-01-10