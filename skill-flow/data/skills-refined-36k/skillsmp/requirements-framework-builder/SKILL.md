---
name: requirements-framework-builder
description: This skill should be used when the user asks to "extend requirements framework", "add new requirement type", "create custom strategy", "add custom calculator", "modify framework architecture", "create requirement plugin", or wants to build new requirement strategies. Also triggers on questions about strategy registration, calculator implementation, or auto-satisfaction mappings.
git_hash: 7953a43
---

# Requirements Framework - Extension Guide

Guide for extending and customizing the **Claude Code Requirements Framework**. Use this skill when you need to add new requirement types, create custom strategies, or deeply customize the framework.

**Current Status**: ✅ PRODUCTION READY (v2.0.4)
**Repository**: https://github.com/HarmAalbers/claude-requirements-framework

## When to Use This Skill

Invoke this skill when you need to:

| Task | This Skill? | Alternative |
|------|-------------|-------------|
| Add a new requirement type (strategy) | ✅ Yes | - |
| Create custom calculator for dynamic reqs | ✅ Yes | - |
| Modify framework architecture | ✅ Yes | - |
| Understand framework internals | ✅ Yes | - |
| Configure existing requirements | ❌ No | `requirements-framework-usage` |
| Check current status | ❌ No | `requirements-framework-status` |
| Fix bugs / sync changes | ❌ No | `requirements-framework-development` |

**→ For current status metrics**: See `requirements-framework-status` skill

---

## How to Extend the Framework

### Adding a New Requirement Type

To add a custom requirement (e.g., `code_review`, `security_scan`):

#### Step 1: Define in Configuration

```yaml
# .claude/requirements.yaml
requirements:
  code_review:
    enabled: true
    type: blocking      # blocking | dynamic | guard | custom
    scope: session      # session | branch | permanent | single_use
    trigger_tools:
      - Edit
      - Write
      - MultiEdit
    message: |
      📝 **Code Review Required**

      Please review your changes before proceeding.

      **To satisfy**: `req satisfy code_review`
    checklist:
      - "Self-reviewed changes"
      - "No console.log statements"
      - "Error handling present"
```

#### Step 2: For Custom Strategies

If built-in strategies (blocking, dynamic, guard) don't fit, create a custom strategy:

```python
# hooks/lib/my_strategy.py
from base_strategy import BaseStrategy

class MyCustomStrategy(BaseStrategy):
    def is_satisfied(self, requirement, state, session_id) -> bool:
        """Check if requirement is satisfied."""
        # Custom logic here
        return custom_condition_check()

    def satisfy(self, requirement, state, session_id, **kwargs):
        """Mark requirement as satisfied."""
        # Store satisfaction state
        pass

    def get_message(self, requirement, context) -> str:
        """Get user-facing message."""
        return requirement.get('message', 'Custom requirement')

    def clear(self, requirement, state, session_id):
        """Clear satisfaction."""
        pass
```

#### Step 3: Register the Strategy

```python
# hooks/lib/strategy_registry.py
from my_strategy import MyCustomStrategy

STRATEGIES = {
    'blocking': BlockingStrategy,
    'dynamic': DynamicStrategy,
    'guard': GuardStrategy,
    'my_custom': MyCustomStrategy,  # Add here
}
```

#### Step 4: Test

```bash
cd ~/Tools/claude-requirements-framework
python3 hooks/test_requirements.py
./sync.sh deploy
```

**→ Example**: See `examples/custom-requirement-strategy.py`

### Creating a Dynamic Calculator

For requirements that auto-calculate conditions:

```python
# hooks/lib/my_calculator.py
from calculator_interface import CalculatorInterface

class CodeComplexityCalculator(CalculatorInterface):
    """Calculate code complexity for dynamic requirements."""

    def calculate(self, project_dir: str, branch: str) -> dict:
        """
        Calculate complexity metrics.

        Returns:
            dict with 'value' and 'threshold_exceeded' keys
        """
        # Example: Count TODO comments
        import subprocess
        result = subprocess.run(
            ['grep', '-r', 'TODO', project_dir, '-c'],
            capture_output=True,
            text=True
        )
        todo_count = int(result.stdout.strip() or 0)

        threshold = 10  # Configurable
        return {
            'value': todo_count,
            'threshold_exceeded': todo_count > threshold
        }
```

Register in `requirement_strategies.py`:

```python
CALCULATORS = {
    'branch_size': BranchSizeCalculator,
    'code_complexity': CodeComplexityCalculator,  # Add here
}
```

Configure:

```yaml
requirements:
  code_complexity:
    enabled: true
    type: dynamic
    calculator: code_complexity
    threshold: 10
    message: "Too many TODOs ({value} found, max {threshold})"
```

### Adding Auto-Satisfaction

Link skills to requirements:

```python
# hooks/auto-satisfy-skills.py
DEFAULT_SKILL_MAPPINGS = {
    'requirements-framework:pre-commit': 'pre_commit_review',
    'requirements-framework:quality-check': 'pre_pr_review',
    'my-plugin:my-skill': 'my_requirement',  # Add mapping
}
```

Or configure per-requirement:

```yaml
requirements:
  architecture_review:
    enabled: true
    satisfied_by_skill: 'architecture-guardian'
```

## Existing Requirement Strategies

### Blocking Strategy

Manual satisfaction required. User must run `req satisfy`.

**Use for**: Planning, review checkpoints, approval gates

```yaml
commit_plan:
  type: blocking
  scope: session
```

### Dynamic Strategy

Auto-calculates conditions at runtime. Uses calculators.

**Use for**: Metrics, size limits, automated checks

```yaml
branch_size_limit:
  type: dynamic
  threshold: 400
  calculation_cache_ttl: 30
```

### Guard Strategy

Condition must pass. No manual satisfaction possible.

**Use for**: Branch protection, environment checks

```yaml
protected_branch:
  type: guard
  branches: [main, master]
```

## Architecture Overview

### Key Components

```
hooks/
├── check-requirements.py      # PreToolUse hook entry
├── lib/
│   ├── requirements.py        # Core BranchRequirements API
│   ├── config.py              # Configuration cascade
│   ├── strategy_registry.py   # Strategy dispatch
│   ├── blocking_strategy.py   # Blocking implementation
│   ├── dynamic_strategy.py    # Dynamic implementation
│   ├── guard_strategy.py      # Guard implementation
│   ├── state_storage.py       # JSON state persistence
│   └── session.py             # Session tracking
```

### Configuration Cascade

```
Global (~/.claude/requirements.yaml)
    ↓ merge if inherit=true
Project (.claude/requirements.yaml)
    ↓ always merge
Local (.claude/requirements.local.yaml)
```

### State Storage

State persists in `.git/requirements/[branch].json`:

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
          "satisfied_at": 1702345678
        }
      }
    }
  }
}
```

**→ For CLI commands**: See `requirements-framework-usage` skill
**→ For development workflow**: See `requirements-framework-development` skill
**→ For ADRs and status**: See `requirements-framework-status` skill

---

## Troubleshooting

### New Requirement Not Working

1. Check config syntax: `req config my_requirement`
2. Verify enabled: `enabled: true`
3. Check trigger_tools matches your use case
4. Run `req doctor` for diagnostics

### Custom Strategy Not Loading

1. Check file in `hooks/lib/`
2. Verify registered in `strategy_registry.py`
3. Deploy: `./sync.sh deploy`
4. Check for import errors in logs

### Tests Failing

```bash
# Run verbose
python3 ~/.claude/hooks/test_requirements.py -v

# Run specific test
python3 ~/.claude/hooks/test_requirements.py -k "test_name"
```

## Resources

- **README**: `~/Tools/claude-requirements-framework/README.md`
- **Development Guide**: `DEVELOPMENT.md`
- **ADRs**: `docs/adr/`
- **Sync Tool**: `./sync.sh`
- **Tests**: `hooks/test_requirements.py`

## Example Files

- `examples/custom-requirement-strategy.py` - Custom strategy implementation examples
