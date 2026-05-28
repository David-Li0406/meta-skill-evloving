---
name: project-scaffolding
description: Use this skill when you need to initialize new projects with the proper structure, configuration, and setup from a BaseProject template.
---

# Project Scaffolding Skill

## When to Activate

Activate this skill when:
- Creating new projects from scratch
- Setting up project directory structures
- Initializing configuration files
- Starting from a BaseProject template
- Setting up technology-specific projects

## Quick Setup Methods

| Method            | Best For            | Time     |
|-------------------|---------------------|----------|
| Automated Script   | Standard projects    | 2-3 min  |
| Manual Setup       | Custom configurations | 10-15 min|

## Directory Naming Conventions

```
Directories:     CamelCase (VideoProcessor, AudioTools)
Date-based:      kebab-case with YYYY-MM-DD (logs-2025-01-15)
NO spaces or underscores in directory names
```

## Manual Setup Workflow

### Step 1: Copy Template
```bash
cp -r /path/to/BaseProject ~/Projects/YourProjectName/
cd ~/Projects/YourProjectName/
```

### Step 2: Clean Git History
```bash
rm -rf .git
```

### Step 3: Customize AGENT.md
Fill in project-specific sections:
```markdown
## Project Purpose
A REST API for managing inventory with real-time updates.

## Tech Stack
- Language: Python 3.11+
- Framework: FastAPI
- Key Libraries: SQLAlchemy, Pydantic
- Package Manager: UV

## Architecture Notes
- Microservices with event-driven updates
- Redis for caching
- PostgreSQL for persistence
```

### Step 4: Initialize Git
```bash
git init
git add .
git commit -m "chore: initialize repository from BaseProject"
```

## Technology-Specific Setup

### Python with UV
```bash
uv init
cp AgentUsage/templates/pyproject.toml.example pyproject.toml
uv add fastapi uvicorn sqlalchemy
uv add --dev pytest black ruff mypy

mkdir -p src/YourProject/{core,utils,config}
mkdir -p tests/{unit,integration}
touch src/YourProject/__init__.py
```

### JavaScript/TypeScript
```bash
pnpm init
pnpm add express dotenv
pnpm add -D typescript @types/node jest eslint prettier

mkdir -p src/{routes,controllers,middleware,utils}
touch src/index.ts
```

### Go
```bash
go mod init github.com/user/project
mkdir -p cmd/api internal/{handlers,models,database} pkg
touch cmd/api/main.go
```

### Rust
```bash
cargo init
mkdir -p src/{routes,models,db}
cargo build
```

## Standard Project Structure

### Python
```
project/
├── src/
│   └── projectname/
│       ├── __init__.py
│       ├── main.py
│       ├── core/
```