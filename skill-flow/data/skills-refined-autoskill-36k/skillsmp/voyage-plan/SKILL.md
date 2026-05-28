---
name: voyage-plan
description: Generate a structured voyage plan for ocaptain multi-ship execution
argument-hint: "<feature-description>"
allowed-tools: ["Read", "Glob", "Grep", "Bash", "Write", "Task"]
---

# Voyage Plan Generator

Generate a complete voyage plan with pre-created tasks for ocaptain ships.

## Output Structure

You will create four artifacts in `.claude/plans/{feature-slug}/`:

```
.claude/plans/{feature-slug}/
├── spec.md              # Design document - what to build and why
├── verify.sh            # Exit criteria - deterministic pass/fail script
├── voyage.json          # Configuration with recommended ship count
└── tasks/
    ├── 1.json           # Pre-created task files
    ├── 2.json
    └── ...
```

## Process

### Step 1: Gather Inputs

Ask the user for:
- Feature description (what to build)
- Repository in `owner/repo` format
- Voyage name (or generate one like `voyage-{feature-slug}`)

### Step 2: Explore the Codebase

Use exploration tools to understand:
1. **Project structure** - Source directories, test directories, config files
2. **Existing patterns** - How similar features are implemented
3. **Test infrastructure** - pytest, jest, go test, etc.
4. **Build/lint tools** - Commands in package.json, pyproject.toml, Makefile, CI config
5. **Code conventions** - Style, naming, architecture patterns

### Step 3: Identify Exit Criteria

Search for verification commands in:
- `package.json` scripts (npm test, npm run lint, npm run typecheck)
- `pyproject.toml` (pytest, ruff, mypy)
- `Makefile` targets
- CI configuration (.github/workflows/)

Exit criteria MUST be concrete commands that return 0 on success.

### Step 4: Write spec.md

Create `.claude/plans/{feature-slug}/spec.md` with:

```markdown
# {Feature Name} Specification

## Objective

{2-3 sentence description of what to build and why}

## Architecture

{Key design decisions, abstractions, data flow}

## Components

{Major components/modules to create or modify}

## Error Handling

{How errors should be handled}

## Testing Strategy

{What tests to write, coverage expectations}

## Exit Criteria

The following commands must pass:
- `{command1}`
- `{command2}`
- `{command3}`
```

### Step 5: Write verify.sh

Create `.claude/plans/{feature-slug}/verify.sh`:

```bash
#!/bin/bash
set -e
cd ~/voyage/workspace

echo "Running: {command1}"
{command1}
echo "  PASSED"

echo "Running: {command2}"
{command2}
echo "  PASSED"

echo ""
echo "All exit criteria passed!"
```

### Step 6: Create tasks/

Create 10-30 tasks as individual JSON files in `.claude/plans/{feature-slug}/tasks/`.

**Task file format (e.g., `1.json`):**

```json
{
  "id": "1",
  "subject": "Task title in imperative form",
  "description": "Detailed description of what to do.\n\nFiles: path/to/file.py, path/to/other.py\n\nAcceptance: Specific testable outcome",
  "activeForm": "Working on task title",
  "status": "pending",
  "blockedBy": [],
  "blocks": ["2", "3"],
  "metadata": {
    "voyage": "{voyage-name}",
    "repo": "{owner/repo}"
  }
}
```

**Task rules:**
- Each task completable in <30 minutes
- Use `blockedBy` for dependencies (task IDs as strings)
- Use `blocks` to indicate what this task unblocks
- Do NOT pre-assign tasks to ships - ships dynamically claim tasks at runtime
- All statuses start as "pending"
- IDs are string numbers: "1", "2", "3", etc.

**Task granularity:**
- Too coarse: "Implement authentication" (break down further)
- Too fine: "Add import statement" (merge into larger task)
- Just right: "Implement JWT token generation in auth/tokens.py"

### Step 7: Run DAG Analyzer

Run the DAG analyzer to compute recommended ships:

```bash
python3 ~/.claude/skills/voyage-plan/dag_analyzer.py .claude/plans/{feature-slug}/tasks/
```

This outputs JSON with `recommended_ships` based on max parallel width.

### Step 8: Write voyage.json

Create `.claude/plans/{feature-slug}/voyage.json` using analyzer output:

```json
{
  "name": "{voyage-name}",
  "repo": "{owner/repo}",
  "recommended_ships": {from analyzer},
  "max_parallel_width": {from analyzer},
  "total_tasks": {from analyzer},
  "created": "{ISO timestamp}"
}
```

### Step 9: Validate

Before finishing, verify:
- [ ] spec.md exists with objective and exit criteria
- [ ] verify.sh exists and is valid bash
- [ ] All task files are valid JSON
- [ ] All dependencies form a valid DAG (no cycles)
- [ ] Tasks are numbered sequentially starting from 1
- [ ] Each task has title, description, and metadata
- [ ] voyage.json has recommended_ships
- [ ] Final task depends on all others (integration/verification task)

### Step 10: Report

Output summary:
```
Voyage plan created: .claude/plans/{feature-slug}/

Files:
  - spec.md (design document)
  - verify.sh (exit criteria)
  - voyage.json (configuration)
  - tasks/ ({N} tasks)

Recommended ships: {N}
Max parallel width: {N}

Ready to launch:
  ocaptain sail .claude/plans/{feature-slug}/
```

## Example

For input: "Add user authentication with JWT to owner/myapp"

Output structure:
```
.claude/plans/user-auth/
├── spec.md
├── verify.sh
├── voyage.json
└── tasks/
    ├── 1.json   # Analyze codebase
    ├── 2.json   # Add JWT dependency
    ├── 3.json   # Create User model (blocked by 1)
    ├── 4.json   # Implement token generation (blocked by 2,3)
    ├── 5.json   # Create login endpoint (blocked by 4)
    ├── 6.json   # Create registration endpoint (blocked by 3)
    ├── 7.json   # Add auth middleware (blocked by 4)
    ├── 8.json   # Protect routes (blocked by 7)
    ├── 9.json   # Write auth tests (blocked by 5,6,7)
    ├── 10.json  # Update API docs (blocked by 5,6)
    └── 11.json  # Verify exit criteria (blocked by all)
```

voyage.json:
```json
{
  "name": "voyage-user-auth",
  "repo": "owner/myapp",
  "recommended_ships": 3,
  "max_parallel_width": 3,
  "total_tasks": 11,
  "created": "2026-01-25T12:00:00Z"
}
```
