# Architecture Overview

Design patterns, strategies, and architectural decisions in the Requirements Framework.

## Core Architecture

### Two-Location System

The framework exists in two places that must stay synchronized:

```
Repository                          Deployed
~/Tools/claude-requirements-framework/    ~/.claude/hooks/
├── hooks/                          ├── *.py (hooks)
│   ├── *.py (hooks)        ←sync→  └── lib/*.py (libraries)
│   └── lib/*.py
└── plugin/                         ~/.claude/plugins/requirements-framework/
    └── (agents, commands, skills)  (symlink to repo)
```

- **Repository**: Git-controlled source of truth
- **Deployed Hooks**: Copied to `~/.claude/hooks/` (active runtime)
- **Plugin**: Symlinked (live updates without reinstall)

---

## Session Lifecycle

### Hook Execution Order

```
1. SessionStart (handle-session-start.py)
   → Clean stale sessions
   → Update registry with current session
   → Inject full status into context

2. PreToolUse (check-requirements.py) - on Edit/Write/Bash/EnterPlanMode/ExitPlanMode
   → Load config (global → project → local cascade)
   → Check requirements against session/branch state
   → Allow or block with message

3. PostToolUse (multiple hooks)
   → auto-satisfy-skills.py: Auto-satisfy when skills complete
   → clear-single-use.py: Clear single_use after Bash triggers
   → handle-plan-exit.py: Show status after ExitPlanMode

4. Stop (handle-stop.py)
   → Check stop_hook_active flag (prevent loops!)
   → Verify session-scoped requirements
   → Block stop if unsatisfied

5. SessionEnd (handle-session-end.py)
   → Remove session from registry
   → Clean session state
```

---

## Configuration Cascade

Configurations merge in order, with later files overriding earlier ones:

```
1. Global (~/.claude/requirements.yaml)
   │
   ↓ (merge if inherit=true)
   │
2. Project (.claude/requirements.yaml)
   │  - Version controlled
   │  - Team shared settings
   │
   ↓ (always merge)
   │
3. Local (.claude/requirements.local.yaml)
      - Gitignored
      - Personal overrides
```

### Merge Behavior

```yaml
# Global
requirements:
  commit_plan:
    enabled: true
    scope: session
    message: "Global message"

# Project (inherit: true)
requirements:
  commit_plan:
    checklist:         # Added (new field)
      - "Item 1"
  adr_reviewed:        # Added (new requirement)
    enabled: true

# Effective result:
requirements:
  commit_plan:
    enabled: true      # From global
    scope: session     # From global
    message: "Global"  # From global
    checklist:         # From project
      - "Item 1"
  adr_reviewed:        # From project
    enabled: true
```

---

## Strategy Pattern

Requirements use a strategy pattern for extensibility:

### Strategy Registry

```python
# strategy_registry.py
STRATEGIES = {
    'blocking': BlockingStrategy,
    'dynamic': DynamicStrategy,
    'guard': GuardStrategy,
}

def get_strategy(requirement_type: str) -> BaseStrategy:
    return STRATEGIES[requirement_type]()
```

### Strategy Types

| Type | Satisfaction | Condition | Use Case |
|------|--------------|-----------|----------|
| **Blocking** | Manual (`req satisfy`) | User action | Planning, review tasks |
| **Dynamic** | Automatic (calculated) | Runtime check | Branch size limits |
| **Guard** | Automatic (condition) | Boolean check | Protected branches |

### Strategy Interface

```python
class BaseStrategy(ABC):
    @abstractmethod
    def is_satisfied(self, requirement, state, session_id) -> bool:
        """Check if requirement is satisfied."""
        pass

    @abstractmethod
    def satisfy(self, requirement, state, session_id, **kwargs):
        """Mark requirement as satisfied."""
        pass

    @abstractmethod
    def get_message(self, requirement, context) -> str:
        """Get user-facing message."""
        pass
```

---

## State Management

### State Storage Location

```
.git/requirements/
├── feature-auth.json    # Branch: feature/auth
├── feature-api.json     # Branch: feature/api
└── main.json            # Branch: main
```

### State Schema

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

### Session Registry

```json
// ~/.claude/sessions.json
{
  "abc12345": {
    "project": "/Users/harm/Work/myproject",
    "branch": "feature/auth",
    "pid": 12345,
    "started_at": 1702340000
  }
}
```

---

## Fail-Open Design

The framework is designed to **never block Claude** due to internal errors:

```python
def check_requirements(tool_input):
    try:
        # Normal requirement checking
        return check_all_requirements(tool_input)
    except Exception as e:
        # Log error but allow operation
        logger.error(f"Hook error: {e}")
        return {"allow": True}  # Fail open
```

### Error Handling Principles

1. **Log all errors** - Structured JSON logging to `~/.claude/requirements.log`
2. **Never raise exceptions** - Catch and allow operation
3. **Degrade gracefully** - Missing files/configs use defaults
4. **Inform user** - Error messages when appropriate

---

## Caching Architecture

### Message Deduplication Cache

```python
# Prevents spam from parallel tool calls
CACHE_TTL = 300  # 5 minutes
CACHE_FILE = "/tmp/claude-msg-dedup-{pid}.json"

def is_duplicate(message_hash) -> bool:
    cache = load_cache()
    if message_hash in cache:
        if time.time() - cache[message_hash] < CACHE_TTL:
            return True  # Suppress duplicate
    cache[message_hash] = time.time()
    save_cache(cache)
    return False
```

### Calculation Cache

```python
# Caches expensive calculations (branch size)
CACHE_TTL = 30  # 30 seconds

def get_branch_size(branch):
    cached = calculation_cache.get(branch)
    if cached and cached.is_valid():
        return cached.value

    # Expensive calculation
    size = calculate_branch_diff_size(branch)
    calculation_cache.set(branch, size, ttl=30)
    return size
```

---

## Hook Configuration

### settings.json Structure

```json
{
  "hooks": {
    "PreToolUse": "~/.claude/hooks/check-requirements.py",
    "SessionStart": "~/.claude/hooks/handle-session-start.py",
    "Stop": "~/.claude/hooks/handle-stop.py",
    "SessionEnd": "~/.claude/hooks/handle-session-end.py",
    "PostToolUse": [
      "~/.claude/hooks/auto-satisfy-skills.py",
      "~/.claude/hooks/clear-single-use.py",
      "~/.claude/hooks/handle-plan-exit.py"
    ]
  }
}
```

### Hook Input/Output

```python
# Input (from Claude Code)
{
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "/path/to/file.py",
    "old_string": "...",
    "new_string": "..."
  },
  "session_id": "abc12345"
}

# Output (from hook)
{
  "allow": false,  # or true
  "message": "Requirement not satisfied..."  # optional
}
```

---

## Plugin Architecture

### Manifest (plugin.json)

```json
{
  "name": "requirements-framework",
  "version": "2.0.5",
  "description": "Claude Code Requirements Framework",
  "skills": "./skills/",
  "commands": "./commands/",
  "agents": [
    "./agents/code-reviewer.md",
    "./agents/adr-guardian.md"
  ]
}
```

### Component Discovery

```
plugin/
├── .claude-plugin/
│   └── plugin.json          # Manifest
├── skills/                   # Auto-discovered
│   └── */skill.md
├── commands/                 # Auto-discovered
│   └── *.md
└── agents/                   # Listed in manifest
    └── *.md
```

---

## Architecture Decision Records

| ADR | Decision | Impact |
|-----|----------|--------|
| ADR-001 | Remove main/master skip | All branches enforce requirements |
| ADR-002 | Use native session_id | Better session correlation |
| ADR-003 | Dynamic sync discovery | sync.sh auto-finds new files |
| ADR-004 | Guard strategy | Condition-based requirements |
| ADR-005 | Per-project init | `req init` wizard |
| ADR-006 | Plugin architecture | Unified plugin structure |
| ADR-007 | Deterministic commands | Reliable orchestration |
| ADR-008 | CLAUDE.md maintenance | Weekly review process |

---

## Performance Considerations

1. **Caching** - 30-sec calculation cache, 5-min message dedup
2. **Lazy loading** - Configs loaded on demand
3. **Minimal I/O** - State files only updated on changes
4. **Async-safe** - File locking for concurrent access
5. **Small payloads** - Concise hook responses
