---
name: agent-ops-create-python-project
description: Use this skill when you need to create a plan and issues for implementing a production-ready Python project with proper structure, tooling, and best practices.
---

# Skill body

## Triggers

- User asks to create a new Python project
- User provides project requirements/discussion to convert into implementation
- User wants to scaffold a CLI tool, library, or application in Python

## Procedure

### Phase 1: Requirements Gathering

1. **If input provided**: Analyze the discussion/requirements.
2. **If no input**: Interview user about:
   - Project name and purpose
   - Core features/commands
   - External services/APIs needed
   - Data processed (files, APIs, databases)
   - CLI, library, or both?
   - Specific dependencies?

### Phase 2: Architecture Design

Extract from requirements:
- **Features**: List all behaviors/capabilities.
- **Data Models**: Entities and relationships.
- **Dependencies**: Map features to PyPI packages.
- **Modules**: Cohesive, loosely-coupled units.
- **Interfaces**: Public APIs per module.

### Phase 3: Issue Creation

Create issues for:
1. **Project scaffold** (pyproject.toml, README, .gitignore, AGENTS.md)
2. **Build pipeline** (scripts/build.py)
3. **Configuration** (src/package/config.py)
4. **CLI layer** (src/package/cli.py)
5. **Core modules** (one issue per module)
6. **Test infrastructure** (tests/conftest.py)
7. **Unit tests** (tests/unit/*)

### Phase 4: Plan Generation

Create plan with:
- Dependency order (scaffold → config → core → CLI → tests)
- Estimated effort per issue
- Quality gates between phases

## Project Structure

```
project-name/
├── pyproject.toml          # Config, dependencies, tools
├── README.md               # Overview, install, usage
├── AGENTS.md               # AI agent guidelines
├── .gitignore
├── scripts/
│   └── build.py            # Build pipeline
├── src/<package>/
│   ├── __init__.py
│   ├── cli.py              # Thin CLI (typer)
│   ├── config.py           # Configuration
│   └── <modules>.py        # Core logic
└── tests/
    ├── conftest.py
    ├── unit/
```