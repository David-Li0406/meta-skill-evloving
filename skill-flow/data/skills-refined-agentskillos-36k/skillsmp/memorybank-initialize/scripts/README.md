# Memory Bank Scripts

Python helper scripts for validating, maintaining, and updating Memory Bank documentation.

## Requirements

- Python 3.8+
- No external dependencies (uses only standard library)
- Git (optional, for staleness detection and change analysis)

## Scripts Overview

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `validate_memorybank.py` | Validates Memory Bank structure and content | After initialization, before commits |
| `detect_stale.py` | Detects outdated Memory Bank files | Weekly or when codebase changes significantly |
| `extract_todos.py` | Extracts action items from Memory Bank | Daily planning, sprint planning |
| `sync_active.py` | Fast updates to active work context | After completing tasks, multiple times per day |

## Installation

No installation required. Scripts use Python standard library only.

```bash
# Make scripts executable (optional)
chmod +x scripts/*.py

# Verify Python version
python3 --version  # Should be 3.8+
```

## Scripts Documentation

### 1. validate_memorybank.py

Validates Memory Bank structure, checking for required files and sections.

**Usage:**
```bash
# Basic validation
python scripts/validate_memorybank.py /path/to/project

# Only check file existence (skip content validation)
python scripts/validate_memorybank.py /path/to/project --no-content-check

# Output as JSON
python scripts/validate_memorybank.py /path/to/project --json
```

**What it checks:**
- All 6 required files exist (`projectbrief.md`, `productContext.md`, etc.)
- Files are not empty (>50 bytes)
- Required sections are present in each file
- Proper markdown structure

**Exit codes:**
- `0` - Valid Memory Bank
- `1` - Validation failed

**Example output:**
```
============================================================
Memory Bank Validation: /path/to/project/memory-bank
============================================================

✅ Found: projectbrief.md (1234 bytes)
✅ Found: productContext.md (2345 bytes)
✅ Found: techContext.md (1890 bytes)
✅ Found: systemPatterns.md (2100 bytes)
✅ Found: activeContext.md (1567 bytes)
✅ Found: progress.md (1234 bytes)

✅ projectbrief.md has all required sections
✅ productContext.md has all required sections
⚠️  techContext.md missing sections: Constraints

============================================================
❌ Memory Bank validation failed
============================================================
```

---

### 2. detect_stale.py

Detects stale Memory Bank files by comparing modification times with git activity.

**Usage:**
```bash
# Check for staleness
python scripts/detect_stale.py /path/to/project

# Custom staleness threshold (default: 7 days)
python scripts/detect_stale.py /path/to/project --threshold 14

# Output as JSON
python scripts/detect_stale.py /path/to/project --json
```

**What it checks:**
- File modification dates
- Recent git commits (last 7 days)
- Code changes vs documentation updates
- Special attention to active files (activeContext.md, progress.md)

**Staleness levels:**
- **Fresh** - Updated recently
- **Stale** - Not updated in 7+ days (or custom threshold)
- **Very Stale** - Not updated in 30+ days

**Exit codes:**
- `0` - No staleness issues
- `1` - Staleness warnings or recommendations

**Example output:**
```
============================================================
Memory Bank Staleness Check: /path/to/project/memory-bank
============================================================

File Status:
  ✅ projectbrief.md: 2 days old (fresh)
  ✅ productContext.md: 5 days old (fresh)
  ✅ techContext.md: 3 days old (fresh)
  ✅ systemPatterns.md: 6 days old (fresh)
  🟡 activeContext.md: 9 days old (stale)
  🟡 progress.md: 8 days old (stale)

Recent Git Activity:
  5 code commits in last 7 days
  • abc1234: Add new feature (2025-01-20)
  • def5678: Fix bug in auth (2025-01-19)
  • ghi9012: Update dependencies (2025-01-18)

Recommendations:
  📝 Recent code changes detected (5 commits). Consider updating: activeContext.md, progress.md
  📝 activeContext.md should be updated more frequently (currently 9 days old)

============================================================
```

---

### 3. extract_todos.py

Extracts TODO items and action items from Memory Bank files.

**Usage:**
```bash
# Extract all TODOs
python scripts/extract_todos.py /path/to/project

# Show only pending items (exclude completed)
python scripts/extract_todos.py /path/to/project --pending-only

# Show only high-priority items
python scripts/extract_todos.py /path/to/project --high-priority

# Output as JSON
python scripts/extract_todos.py /path/to/project --json
```

**What it extracts:**
- Markdown checkboxes: `- [ ] Task` and `- [x] Done`
- TODO prefixes: `- TODO: Something`
- Bullet points under "Next Steps" sections
- Items under "Blockers", "Known Issues", "What's Left to Build"

**Priority detection:**
Automatically marks items as high-priority if they contain:
- "urgent", "critical", "important", "asap", "blocker", "blocked"

**Status detection:**
- `pending` - Not completed
- `in_progress` - Contains "in progress", "started", "working on"
- `completed` - Checked checkbox `[x]`

**Exit codes:**
- `0` - Always (informational tool)

**Example output:**
```
============================================================
Memory Bank TODOs: /path/to/project/memory-bank
============================================================

Summary:
  Total: 12
  Pending: 8
  In Progress: 2
  Completed: 2
  High Priority: 3

TODO Items:

🔄 In Progress:
     Fix authentication bug
     (activeContext.md::Next Steps)

     Update API documentation
     (progress.md::What's Left to Build)

📋 Pending:
  🔴 Critical: Database migration needs review
     (activeContext.md::Blockers)

     Add unit tests for new feature
     (progress.md::What's Left to Build)

     Optimize query performance
     (progress.md::Known Issues)

✅ Completed:
     Set up CI/CD pipeline
     (progress.md::What's Left to Build)

============================================================
```

---

### 4. sync_active.py

Fast update tool for `activeContext.md` and `progress.md`. Allows quick updates without full Memory Bank review.

**Usage:**
```bash
# Update Current Focus in activeContext.md
python scripts/sync_active.py /path/to/project \
  --active '{"Current Focus": "Working on authentication module"}'

# Append to Next Steps (preserves existing content)
python scripts/sync_active.py /path/to/project \
  --active '{"Next Steps": "- Add integration tests\n- Deploy to staging"}' \
  --append

# Update progress.md
python scripts/sync_active.py /path/to/project \
  --progress '{"Current Status": "Sprint 3 Day 5 - On track"}'

# Update both files at once
python scripts/sync_active.py /path/to/project \
  --active '{"Current Focus": "Bug fixes", "Blockers": "- Waiting on API keys"}' \
  --progress '{"Known Issues": "- Slow database queries"}'

# Read updates from JSON file
python scripts/sync_active.py /path/to/project --active @updates.json

# Output as JSON
python scripts/sync_active.py /path/to/project --active '...' --json
```

**Valid sections for activeContext.md:**
- Current Focus
- Recent Changes
- Next Steps
- Blockers
- Learnings

**Valid sections for progress.md:**
- What's Working
- What's Left to Build
- Current Status
- Known Issues

**Update modes:**
- **Replace** (default) - Replaces section content
- **Append** (`--append`) - Adds to existing content

**Exit codes:**
- `0` - Update successful
- `1` - Update failed

**Example with JSON file:**

Create `updates.json`:
```json
{
  "Current Focus": "Implementing user authentication with OAuth2",
  "Next Steps": "- Set up OAuth provider\n- Add JWT middleware\n- Write integration tests",
  "Blockers": "None currently"
}
```

Run:
```bash
python scripts/sync_active.py . --active @updates.json
```

**Example output:**
```
============================================================
Memory Bank Sync: /path/to/project/memory-bank
============================================================

activeContext.md updated:
  ✅ Current Focus
  ✅ Next Steps
  ✅ Blockers

============================================================
✅ Sync completed successfully
============================================================
```

---

## Common Workflows

### Daily Workflow

```bash
# Morning: Check what needs to be done
python scripts/extract_todos.py . --pending-only

# During work: Quick context updates as you progress
python scripts/sync_active.py . \
  --active '{"Current Focus": "Working on feature X"}' \
  --progress '{"Current Status": "Day 2 of sprint"}'

# End of day: Update what was accomplished
python scripts/sync_active.py . \
  --active '{"Recent Changes": "- Completed feature X\n- Fixed bugs in Y"}' \
  --append
```

### Weekly Workflow

```bash
# Check for stale documentation
python scripts/detect_stale.py .

# Review all TODOs for planning
python scripts/extract_todos.py .

# Validate structure before committing
python scripts/validate_memorybank.py .
```

### Pre-Commit Workflow

```bash
# Validate Memory Bank before committing
python scripts/validate_memorybank.py . || exit 1

# Optionally check staleness
python scripts/detect_stale.py . --threshold 14
```

### CI/CD Integration

```yaml
# .github/workflows/validate-docs.yml
name: Validate Memory Bank

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.8'

      - name: Validate Memory Bank
        run: python scripts/validate_memorybank.py .

      - name: Check for stale docs
        run: python scripts/detect_stale.py . --threshold 30
```

---

## Best Practices

### Script Usage

1. **Run validation frequently** - Before commits, after major changes
2. **Check staleness weekly** - Keep documentation fresh
3. **Use sync_active.py liberally** - Quick updates are better than no updates
4. **Extract TODOs daily** - For task planning and prioritization

### Integration with Memory Bank Skills

These scripts are designed to work with Memory Bank skills:

- `/memory-bank-initialize` - Uses `validate_memorybank.py` after creation
- `/memory-bank-read` - Uses `detect_stale.py` and `validate_memorybank.py` for health checks
- `/memory-bank-sync` - Uses `sync_active.py` and `extract_todos.py` for quick updates
- `/memory-bank-update` - Uses all scripts for comprehensive reviews

### Automation

Consider setting up:

1. **Git hooks** - Pre-commit validation
2. **Cron jobs** - Daily staleness checks
3. **CI/CD** - Automated validation on PRs
4. **Editor integration** - Quick TODO extraction

---

## Troubleshooting

### "Memory Bank not found"

Ensure the `memory-bank/` directory exists in your project root:
```bash
ls -la memory-bank/
```

### "Cannot read file" errors

Check file permissions:
```bash
chmod 644 memory-bank/*.md
```

### Git-related errors in detect_stale.py

Ensure you're in a git repository:
```bash
git status
```

Script will work without git but with reduced functionality.

### Python version issues

Verify Python 3.8+:
```bash
python3 --version
```

---

## Contributing

When adding new scripts:

1. Use Python 3.8+ standard library only
2. Include comprehensive help text (`--help`)
3. Support JSON output (`--json`)
4. Use consistent exit codes (0=success, 1=failure/warnings)
5. Add documentation to this README
6. Follow existing code style and patterns

---

## License

Part of Claude Code Memory Bank system.
