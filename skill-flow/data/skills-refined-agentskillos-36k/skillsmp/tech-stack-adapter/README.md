---
type: directory-documentation
directory: .claude/skills/tech-stack-adapter
title: Tech Stack Adapter
sibling_claude: CLAUDE.md
parent: null
children:
  - ARCHIVED/README.md
---

# Tech Stack Adapter

> **Automatic project detection for Python/uv projects - enabling workflow adaptation to any tech stack**

The Tech Stack Adapter provides automatic project configuration detection by analyzing `pyproject.toml`, installed dependencies, and project structure. It generates appropriate commands for testing, building, coverage, database migrations, and containerization, enabling the workflow to adapt to different project configurations without hardcoded assumptions.

## Features

- ✅ **Automatic detection** - Reads pyproject.toml to detect dependencies and tools
- ✅ **Command generation** - Generates correct commands based on detected tools
- ✅ **JSON output** - Structured, parseable configuration for other skills
- ✅ **Fallback commands** - Graceful degradation if tools not configured
- ✅ **Tech-stack agnostic** - Adapts to any Python/uv project structure
- ✅ **Cached configuration** - Run once per session, reuse throughout workflow
- ✅ **Comprehensive detection** - Tests, coverage, database, ORM, migrations, containers, linting, type checking

## Quick Start

### Run Project Detection

```bash
# From repository root
python .claude/skills/tech-stack-adapter/scripts/detect_stack.py

# Output (JSON):
# {
#   "stack": "python",
#   "package_manager": "uv",
#   "project_name": "german",
#   "repo_root": "/Users/stharrold/Documents/GitHub/german",
#
#   "install_cmd": "uv sync",
#   "test_cmd": "uv run pytest",
#   "build_cmd": "uv build",
#
#   "coverage_cmd": "uv run pytest --cov=src --cov-report=term",
#   "coverage_check": "uv run pytest --cov=src --cov-fail-under=80",
#
#   "database": "sqlite",
#   "orm": "none",
#   "migrate_cmd": "echo \"No migrations\"",
#
#   "container": "podman",
#   "has_containerfile": false,
#   "has_compose": false,
#
#   "lint_cmd": "uv run ruff check",
#   "lint_fix_cmd": "uv run ruff check --fix",
#   "format_cmd": "uv run ruff format",
#   "type_check_cmd": "uv run mypy src/"
# }
```

## Detection Logic

### What Gets Detected

| Component | Detection Method | Example Output |
|-----------|-----------------|----------------|
| Project type | pyproject.toml presence | `"stack": "python"` |
| Package manager | pyproject.toml format | `"package_manager": "uv"` |
| Testing framework | pytest in dependencies | `"test_cmd": "uv run pytest"` |
| Coverage tool | pytest-cov in dependencies | `"coverage_cmd": "uv run pytest --cov=src"` |
| Database | Default or sqlalchemy detected | `"database": "sqlite"` or `"postgresql"` |
| ORM | sqlalchemy in dependencies | `"orm": "sqlalchemy"` |
| Migrations | alembic in dependencies | `"migrate_cmd": "uv run alembic upgrade head"` |
| Container | Containerfile, podman-compose.yml | `"container": "podman", "has_containerfile": true` |
| Linting | ruff in dev dependencies | `"lint_cmd": "uv run ruff check"` |
| Type checking | mypy in dev dependencies | `"type_check_cmd": "uv run mypy src/"` |

### Detection Examples

**Minimal Python project:**
```toml
# pyproject.toml
[project]
name = "myproject"
dependencies = []

[tool.pytest.ini_options]
testpaths = ["tests"]
```

**Detected configuration:**
```json
{
  "test_cmd": "echo \"No pytest configured\"",
  "coverage_cmd": "echo \"No coverage tool\"",
  "database": "sqlite",
  "orm": "none",
  "migrate_cmd": "echo \"No migrations\""
}
```

**Full-featured project:**
```toml
# pyproject.toml
[project]
name = "german"
dependencies = [
    "pydantic>=2.12.3",
    "sqlalchemy>=2.0.0",
]

[dependency-groups]
dev = [
    "pytest>=8.4.2",
    "pytest-cov>=7.0.0",
    "ruff>=0.14.1",
    "mypy>=1.18.2",
    "alembic>=1.13.0",
]
```

**Detected configuration:**
```json
{
  "test_cmd": "uv run pytest",
  "coverage_cmd": "uv run pytest --cov=src --cov-report=term",
  "coverage_check": "uv run pytest --cov=src --cov-fail-under=80",
  "database": "postgresql",
  "orm": "sqlalchemy",
  "migrate_cmd": "uv run alembic upgrade head",
  "lint_cmd": "uv run ruff check",
  "type_check_cmd": "uv run mypy src/"
}
```

## Workflow Integration

### Phase 0: Session Start

```bash
# Workflow orchestrator calls detection at session start
python .claude/skills/tech-stack-adapter/scripts/detect_stack.py

# Output cached in SESSION_CONFIG for entire session
```

### Adaptive Command Usage

**Instead of hardcoded commands:**
```python
# ❌ Bad: Assumes pytest available
subprocess.run(['pytest'], check=True)
```

**Use detected commands:**
```python
# ✅ Good: Adapts to project
import json
import subprocess

# Run detection
result = subprocess.run([
    'python',
    '.claude/skills/tech-stack-adapter/scripts/detect_stack.py'
], capture_output=True, text=True, check=True)

# Parse JSON
config = json.loads(result.stdout)

# Use detected commands
subprocess.run(config['test_cmd'], shell=True, check=True)
subprocess.run(config['coverage_cmd'], shell=True, check=True)
```

### Integration with Other Skills

**quality-enforcer:**
```bash
# Quality gates use detected test/coverage commands
python .claude/skills/quality-enforcer/scripts/run_quality_gates.py
# (internally uses tech-stack-adapter config)
```

**git-workflow-manager:**
```bash
# Uses project_name for worktree naming
# Uses repo_root for path resolution
```

**bmad-planner:**
```bash
# Adapts Q&A based on detected tools
# Skips database questions if no ORM detected
```

**speckit-author:**
```bash
# Includes detected stack in specifications
# Adapts plan.md based on available tools
```

## Conditional Features

### Database Migrations (if Alembic detected)

```python
import json
import subprocess

config = json.loads(subprocess.check_output([
    'python',
    '.claude/skills/tech-stack-adapter/scripts/detect_stack.py'
], text=True))

if config['orm'] == 'sqlalchemy' and 'echo' not in config['migrate_cmd']:
    # Alembic is available
    print("Running database migrations...")
    subprocess.run(config['migrate_cmd'], shell=True, check=True)
else:
    print("No database migrations configured")
```

### Container Operations (if Containerfile detected)

```python
if config['has_containerfile']:
    print("Building container...")
    subprocess.run([
        'podman', 'build',
        '-t', f"{config['project_name']}:latest",
        '.'
    ], check=True)
else:
    print("No Containerfile found - skipping container build")
```

## Error Handling

### Not a git repository

```bash
✗ Error: Not a git repository

Fix: Initialize git or run from git repository
  git init
```

### No pyproject.toml

```bash
✗ Error: pyproject.toml not found - not a Python/uv project

Fix: Create pyproject.toml or run from Python project root
```

### Missing tomllib

```bash
✗ Error: tomllib/tomli not available. Install tomli: pip install tomli

Fix: Ensure Python 3.11+ or install tomli
  uv add tomli
```

## Constants and Rationale

| Constant | Value | Rationale |
|----------|-------|-----------|
| Default package manager | `uv` | Modern Python package manager, faster than pip |
| Default container engine | `podman` | Docker-compatible, daemonless, rootless, more secure |
| Default coverage threshold | 80% | Industry standard minimum |
| Default ORM | SQLAlchemy | Most popular Python ORM |

## Detection Rationale

**Why detect instead of hardcode?**

1. **Portability** - Workflow works with any Python project, not just one tech stack
2. **Flexibility** - Projects evolve (add/remove tools), detection adapts automatically
3. **Explicit** - JSON output shows exactly what will be used
4. **Debugging** - Easy to see why workflow chose certain commands

**Why JSON output?**

1. **Parseable** - Easy for workflows to parse and use
2. **Complete** - All commands in one place
3. **Cacheable** - Store once per session, reuse throughout
4. **Debuggable** - User can run script manually to see configuration

**Why fallback commands?**

1. **Graceful degradation** - If pytest not installed, workflow doesn't crash
2. **Clear messaging** - "No pytest configured" vs silent failure
3. **Actionable** - User knows what's missing and can install it

## Examples

### Python Project with Minimal Dependencies

```toml
# pyproject.toml
[project]
name = "simple-cli"
version = "0.1.0"
dependencies = []

[dependency-groups]
dev = ["pytest>=8.4.2"]
```

**Detection output:**
```json
{
  "test_cmd": "uv run pytest",
  "coverage_cmd": "uv run pytest",
  "build_cmd": "uv build",
  "database": "sqlite",
  "orm": "none",
  "lint_cmd": "echo \"No linting configured\"",
  "type_check_cmd": "echo \"No type checking configured\""
}
```

### FastAPI + PostgreSQL + Full Tooling

```toml
# pyproject.toml
[project]
name = "api-backend"
dependencies = [
    "fastapi>=0.100.0",
    "sqlalchemy>=2.0.0",
    "psycopg2-binary>=2.9.0",
]

[dependency-groups]
dev = [
    "pytest>=8.4.2",
    "pytest-cov>=7.0.0",
    "ruff>=0.14.1",
    "mypy>=1.18.2",
    "alembic>=1.13.0",
]
```

**Detection output:**
```json
{
  "test_cmd": "uv run pytest",
  "coverage_cmd": "uv run pytest --cov=src --cov-report=term",
  "coverage_check": "uv run pytest --cov=src --cov-fail-under=80",
  "build_cmd": "uv build",
  "database": "postgresql",
  "orm": "sqlalchemy",
  "migrate_cmd": "uv run alembic upgrade head",
  "lint_cmd": "uv run ruff check",
  "lint_fix_cmd": "uv run ruff check --fix",
  "format_cmd": "uv run ruff format",
  "type_check_cmd": "uv run mypy src/"
}
```

## Related Documentation

- **[SKILL.md](SKILL.md)** - Complete technical documentation
- **[CLAUDE.md](CLAUDE.md)** - Claude Code integration guide
- **[CHANGELOG.md](CHANGELOG.md)** - Version history

**See also:**
- [WORKFLOW.md](../../WORKFLOW.md) - Complete workflow guide
- [quality-enforcer](../quality-enforcer/) - Uses detected commands
- [workflow-orchestrator](../workflow-orchestrator/) - Calls detection at session start

## Contributing

This skill is part of the workflow system. To update:

1. Modify scripts in `scripts/`
2. Update version in `SKILL.md` frontmatter
3. Document changes in `CHANGELOG.md`
4. Run validation: `python .claude/skills/workflow-utilities/scripts/validate_versions.py`
5. Sync documentation: `python .claude/skills/workflow-utilities/scripts/sync_skill_docs.py tech-stack-adapter <version>`

## License

Part of the german repository workflow system.
