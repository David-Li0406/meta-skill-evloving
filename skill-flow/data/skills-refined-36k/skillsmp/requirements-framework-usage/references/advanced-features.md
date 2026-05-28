# Advanced Features

Deep dive into advanced Requirements Framework features.

## Auto-Satisfaction via Skills

Requirements can be automatically satisfied when specific skills complete.

### How It Works

```
1. User tries action (e.g., git commit) → Blocked by pre_commit_review
2. User runs skill (e.g., /requirements-framework:pre-commit)
3. Skill completes → PostToolUse hook auto-satisfies pre_commit_review
4. User retries action → Success!
5. PostToolUse hook → Clears single_use requirement (if applicable)
```

### Built-in Mappings

Located in `~/.claude/hooks/auto-satisfy-skills.py`:

```python
DEFAULT_SKILL_MAPPINGS = {
    'requirements-framework:pre-commit': 'pre_commit_review',
    'requirements-framework:quality-check': 'pre_pr_review',
    'requirements-framework:codex-review': 'codex_reviewer',
}
```

### Adding Custom Mappings

Edit `~/.claude/hooks/auto-satisfy-skills.py`:

```python
DEFAULT_SKILL_MAPPINGS = {
    'requirements-framework:pre-commit': 'pre_commit_review',
    'requirements-framework:quality-check': 'pre_pr_review',
    'my-plugin:my-skill': 'my_requirement',  # Add here
}
```

Or use `satisfied_by_skill` in configuration:

```yaml
requirements:
  architecture_review:
    enabled: true
    scope: single_use
    satisfied_by_skill: 'architecture-guardian'  # Custom mapping
```

---

## Single-Use Requirements

Requirements that automatically clear after the triggering action completes.

### Use Case

Enforce code review before EVERY commit (not just once per session):

```yaml
requirements:
  pre_commit_review:
    enabled: true
    scope: single_use   # Key: auto-clears after action
    trigger_tools:
      - tool: Bash
        command_pattern: "git\\s+commit"
```

### Workflow

```
1. git commit → Blocked (pre_commit_review not satisfied)
2. /requirements-framework:pre-commit → Auto-satisfies
3. git commit → Success!
4. PostToolUse hook → Clears single_use requirement
5. git commit (again) → Blocked (must review again)
```

### Difference from Session Scope

| Scope | Behavior |
|-------|----------|
| `session` | Satisfy once, valid until session ends |
| `single_use` | Must satisfy before EACH triggering action |

---

## Message Deduplication

Prevents spam by deduplicating identical messages.

### How It Works

- 5-minute TTL cache per unique message
- First occurrence: Message shown to user
- Subsequent occurrences (within 5 min): Silently suppressed
- 90% reduction in repeated prompts

### Benefits

- No configuration needed
- Works for all requirements
- Handles parallel tool calls gracefully
- Prevents "wall of identical errors"

---

## Stop Hook Verification

Prevents Claude from stopping with unsatisfied requirements.

### Default Behavior

1. Claude tries to stop (end of task)
2. Stop hook checks session-scoped requirements
3. If unsatisfied → Blocks stop, reminds user
4. Once satisfied → Allows stop

### Configuration

```yaml
hooks:
  stop:
    verify_requirements: true       # Enable/disable
    verify_scopes: [session]        # Which scopes to check
```

### Emergency Override

Disable for current session only:

```bash
req config --set hooks.stop.verify_requirements=false --local
```

---

## Protected Branch Guards

Prevent direct edits on main/master/production branches.

### Configuration

```yaml
requirements:
  protected_branch:
    enabled: true
    type: guard           # New strategy type
    branches:
      - main
      - master
      - production
      - release/*         # Glob patterns supported
    message: |
      🚫 **Cannot edit files on protected branch**

      Please create a feature branch first.
```

### Guard vs Blocking Strategy

| Strategy | Satisfaction | Use Case |
|----------|--------------|----------|
| Blocking | Manual (`req satisfy`) | Planning, review tasks |
| Guard | Automatic (condition check) | Branch protection, env guards |
| Dynamic | Automatic (calculated) | Size limits, metrics |

### Emergency Hotfix Override

```bash
req approve protected_branch
```

---

## Dynamic Requirements (Branch Size)

Requirements that calculate conditions at runtime.

### Branch Size Limit

```yaml
requirements:
  branch_size_limit:
    enabled: true
    type: dynamic
    scope: session
    threshold: 400                   # Max changes before warning
    calculation_cache_ttl: 30        # Cache results (seconds)
    message: |
      📊 **Branch has {size} changes (threshold: {threshold})**

      Consider splitting into smaller branches.
```

### How It Works

1. Tool triggered (Edit/Write)
2. Dynamic calculator runs: `branch_size_calculator.py`
3. Calculates: `git diff main...HEAD --numstat | wc -l`
4. If size > threshold → Blocks with message
5. Result cached for TTL seconds (performance)

---

## TTL (Time-To-Live)

Expire requirements automatically after a time period.

### Usage

```bash
# Satisfy for 1 hour
req satisfy commit_plan --ttl 3600

# Satisfy for 24 hours (full day)
req satisfy commit_plan --ttl 86400

# Satisfy for 8 hours (work day)
req satisfy commit_plan --ttl 28800
```

---

## Metadata Storage

Attach additional data to satisfied requirements.

### Usage

```bash
req satisfy github_ticket --metadata '{"ticket":"#123","reviewer":"alice"}'
req satisfy code_review --metadata '{"approved_by":"bob","timestamp":"2025-01-15"}'
```

### Accessing Metadata

Metadata is stored in `.git/requirements/[branch].json`:

```json
{
  "requirements": {
    "github_ticket": {
      "sessions": {
        "abc12345": {
          "satisfied": true,
          "metadata": {
            "ticket": "#123",
            "reviewer": "alice"
          }
        }
      }
    }
  }
}
```

---

## Plan Mode Triggers

Requirements can trigger on planning mode transitions.

### Configuration

```yaml
requirements:
  adr_plan_validation:
    enabled: true
    type: blocking
    scope: single_use
    trigger_tools:
      - ExitPlanMode    # Triggers when Claude exits planning
    satisfied_by_skill: 'adr-guardian'
    message: |
      📋 **Plan validation required**

      Run ADR guardian before implementing.
```

### Use Cases

- Pre-planning ADR review (EnterPlanMode)
- Plan validation against ADRs (ExitPlanMode)
- Architectural compliance at planning stage

---

## State Files

Requirements state is stored in `.git/requirements/[branch].json`:

```json
{
  "version": "1.0",
  "branch": "feature/auth",
  "requirements": {
    "commit_plan": {
      "scope": "session",
      "sessions": {
        "abc12345": {
          "satisfied": true,
          "satisfied_at": 1702345678,
          "ttl": null,
          "metadata": {}
        }
      }
    }
  }
}
```

### State Locations

- `.git/requirements/` - Per-branch state (gitignored)
- `~/.claude/sessions.json` - Session registry
- `/tmp/claude-msg-dedup-*.json` - Deduplication cache
