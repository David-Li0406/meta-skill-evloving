---
type: claude-context
directory: .claude/skills/tech-stack-adapter
purpose: Tech Stack Adapter provides **automatic project detection** for Python/uv projects. It reads `pyproject.toml`, detects installed dependencies and tools, and generates appropriate commands for testing, building, coverage, database migrations, and containerization. Enables workflow to adapt to different project configurations without hardcoded assumptions.
parent: null
sibling_readme: README.md
children:
  - ARCHIVED/CLAUDE.md
  - scripts/CLAUDE.md
related_skills:
  - **workflow-orchestrator** - Uses detect_stack.py at session start
  - **quality-enforcer** - Uses detected test/coverage commands
  - **git-workflow-manager** - Uses project_name and repo_root
  - **bmad-planner** - Adapts Q&A based on detected stack
  - **speckit-author** - Includes detected stack in specifications
---

# Claude Code Context: tech-stack-adapter

## Purpose

Tech Stack Adapter provides **automatic project detection** for Python/uv projects. It reads `pyproject.toml`, detects installed dependencies and tools, and generates appropriate commands for testing, building, coverage, database migrations, and containerization. Enables workflow to adapt to different project configurations without hardcoded assumptions.

## Directory Structure

```
.claude/skills/tech-stack-adapter/
├── scripts/                      # Project detection automation
│   ├── detect_stack.py           # Main detection script (Phase 0)
│   └── __init__.py               # Package initialization
├── templates/                    # (none - no template files)
├── SKILL.md                      # Complete skill documentation
├── CLAUDE.md                     # This file
├── README.md                     # Human-readable overview
├── CHANGELOG.md                  # Version history
└── ARCHIVED/                     # Deprecated files
    ├── CLAUDE.md
    └── README.md
```

## Key Scripts

### detect_stack.py

**Purpose:** Detect Python project configuration and generate workflow commands

**When to use:**
- Beginning of workflow session (Phase 0)
- After dependency changes
- When user asks "what commands should I use?"

**Invocation:**
```bash
python .claude/skills/tech-stack-adapter/scripts/detect_stack.py
```

**Output (JSON):**
```json
{
  "stack": "python",
  "package_manager": "uv",
  "project_name": "german",
  "repo_root": "/Users/stharrold/Documents/GitHub/german",

  "install_cmd": "uv sync",
  "test_cmd": "uv run pytest",
  "build_cmd": "uv build",

  "coverage_cmd": "uv run pytest --cov=src --cov-report=term",
  "coverage_check": "uv run pytest --cov=src --cov-report=term --cov-fail-under=80",

  "database": "sqlite",
  "orm": "none",
  "migrate_cmd": "echo \"No migrations\"",

  "container": "podman",
  "has_containerfile": false,
  "has_compose": false,

  "lint_cmd": "uv run ruff check",
  "lint_fix_cmd": "uv run ruff check --fix",
  "format_cmd": "uv run ruff format",
  "type_check_cmd": "uv run mypy src/"
}
```

**What it detects:**

1. **Project type:** Python with uv (from pyproject.toml)
2. **Package manager:** uv (modern Python package manager)
3. **Testing framework:** pytest (if pytest in dependencies)
4. **Coverage tool:** pytest-cov (if pytest-cov in dependencies)
5. **Database:** SQLite (default) or PostgreSQL (if sqlalchemy detected)
6. **ORM:** None or SQLAlchemy (if sqlalchemy in dependencies)
7. **Migrations:** Alembic (if alembic in dependencies)
8. **Container:** Podman (checks for Containerfile, podman-compose.yml)
9. **Linting:** Ruff (checks for ruff in dev dependencies)
10. **Type checking:** mypy (checks for mypy in dev dependencies)

**Key features:**
- Reads pyproject.toml to detect dependencies
- Generates correct commands based on detected tools
- Returns JSON for easy parsing
- Exits with error if not a Python project
- Fallback commands if tools not configured

**Detection logic:**

```python
# Example: Coverage detection
has_coverage = 'pytest-cov' in all_deps_str or 'coverage' in all_deps_str

if has_coverage:
    coverage_cmd = 'uv run pytest --cov=src --cov-report=term'
    coverage_check = 'uv run pytest --cov=src --cov-fail-under=80'
else:
    coverage_cmd = 'uv run pytest'
    coverage_check = 'echo "No coverage tool"'
```

**Error handling:**

```bash
# Not a git repo
Error: Not a git repository

# No pyproject.toml
Error: pyproject.toml not found - not a Python/uv project

# Missing tomllib
Error: tomllib/tomli not available. Install tomli: pip install tomli
```

---

## Usage by Claude Code

### Phase 0: Session Start

**Context:** User starts new session, Claude needs to understand project

**User says:**
- "Next step?" (implicitly triggers detection)
- "What commands should I use?"
- "How do I run tests?"

**Claude Code should:**
```python
import json
import subprocess

# Run detection
result = subprocess.run([
    'python',
    '.claude/skills/tech-stack-adapter/scripts/detect_stack.py'
], capture_output=True, text=True, check=True)

# Parse JSON output
config = json.loads(result.stdout)

# Use detected commands
TEST_CMD = config['test_cmd']  # 'uv run pytest'
COVERAGE_CMD = config['coverage_cmd']  # 'uv run pytest --cov=src --cov-report=term'
BUILD_CMD = config['build_cmd']  # 'uv build'

# Now use these commands throughout the session
```

**Store config for session:**
```python
# Cache in session memory
SESSION_CONFIG = config

# Later in Phase 3 (Quality Gates):
subprocess.run(SESSION_CONFIG['test_cmd'], shell=True, check=True)
subprocess.run(SESSION_CONFIG['coverage_cmd'], shell=True, check=True)
```

---

### Adaptive Command Usage

**Instead of hardcoded commands:**
```python
# ❌ Bad: Hardcoded assumption
subprocess.run(['pytest'], check=True)
```

**Use detected commands:**
```python
# ✅ Good: Adapt to project
config = detect_stack()
subprocess.run(config['test_cmd'], shell=True, check=True)
```

---

### Conditional Features

**Database migrations (if Alembic detected):**
```python
config = detect_stack()

if config['orm'] == 'sqlalchemy' and 'echo' not in config['migrate_cmd']:
    # Alembic is available
    print("Running database migrations...")
    subprocess.run(config['migrate_cmd'], shell=True, check=True)
else:
    print("No database migrations configured")
```

**Container operations (if Containerfile detected):**
```python
config = detect_stack()

if config['has_containerfile']:
    print("Building container...")
    subprocess.run(['podman', 'build', '-t', f"{config['project_name']}:latest", '.'], check=True)
else:
    print("No Containerfile found - skipping container build")
```

---

## Integration with Other Skills

**workflow-orchestrator:**
- Orchestrator calls detect_stack.py at session start
- Stores config in session state
- Uses config throughout workflow phases

**quality-enforcer:**
- Uses test_cmd, coverage_cmd, lint_cmd from detection
- Adapts quality gates to available tools

**git-workflow-manager:**
- Uses project_name for worktree naming
- Uses repo_root for path resolution

**bmad-planner:**
- Uses detected stack in architecture questions
- Adapts Q&A based on detected tools (e.g., skip database questions if no ORM)

**speckit-author:**
- Uses detected stack in specification generation
- Includes detected tools in tech stack documentation

---

## Detected Configurations

### Minimal Python Project

**pyproject.toml:**
```toml
[project]
name = "myproject"
dependencies = []

[tool.pytest.ini_options]
testpaths = ["tests"]
```

**Detected commands:**
```json
{
  "test_cmd": "echo \"No pytest configured\"",
  "coverage_cmd": "echo \"No coverage tool\"",
  "database": "sqlite",
  "orm": "none",
  "migrate_cmd": "echo \"No migrations\""
}
```

---

### Full-Featured Project

**pyproject.toml:**
```toml
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

**Detected commands:**
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

---

## Detection Rationale

**Why detect instead of hardcode?**

1. **Portability:** Workflow works with any Python project, not just this one
2. **Flexibility:** Projects evolve (add/remove tools), detection adapts automatically
3. **Explicit:** JSON output shows exactly what will be used
4. **Debugging:** Easy to see why workflow chose certain commands

**Why JSON output?**

1. **Parseable:** Easy for Claude Code to parse and use
2. **Complete:** All commands in one place
3. **Cacheable:** Store once per session, reuse throughout
4. **Debuggable:** User can run script manually to see configuration

**Why fallback commands?**

1. **Graceful degradation:** If pytest not installed, workflow doesn't crash
2. **Clear messaging:** "No pytest configured" vs silent failure
3. **Actionable:** User knows what's missing and can install it

---

## Constants and Rationale

**Default package manager:** `uv`
- **Rationale:** Modern Python package manager, faster than pip, handles virtual environments automatically

**Default container engine:** `podman`
- **Rationale:** Docker-compatible, daemonless, rootless, more secure than Docker

**Default coverage threshold:** 80%
- **Rationale:** Industry standard minimum for test coverage

**Default ORM:** SQLAlchemy (if detected)
- **Rationale:** Most popular Python ORM, well-supported

---

## Workflow Pattern

**Session initialization:**
```bash
# 1. User starts session
User: "next step?"

# 2. Orchestrator detects stack
python .claude/skills/tech-stack-adapter/scripts/detect_stack.py

# 3. Orchestrator caches config
SESSION_CONFIG = {...}

# 4. Throughout session, use cached commands
# Phase 3:
uv run pytest  # from SESSION_CONFIG['test_cmd']

# Phase 5:
uv build  # from SESSION_CONFIG['build_cmd']
```

---

## Related Documentation

- **[SKILL.md](SKILL.md)** - Complete skill documentation
- **[README.md](README.md)** - Human-readable overview
- **[CHANGELOG.md](CHANGELOG.md)** - Version history

**Child Directories:**
- **[ARCHIVED/CLAUDE.md](ARCHIVED/CLAUDE.md)** - Archived files

## Related Skills

- **workflow-orchestrator** - Uses detect_stack.py at session start
- **quality-enforcer** - Uses detected test/coverage commands
- **git-workflow-manager** - Uses project_name and repo_root
- **bmad-planner** - Adapts Q&A based on detected stack
- **speckit-author** - Includes detected stack in specifications
