# ETHIC Principles

## Overview

ETHIC enforces AI ethics principles to ensure responsible agent behavior.

## Core Principles

| Principle | Category | Priority |
|-----------|----------|----------|
| Human First | human_dignity | 10 |
| No Harm | safety | 10 |
| Sandbox Default | safety | 10 |
| User Override | autonomy | 9 |
| Data Privacy | privacy | 9 |
| Transparency | transparency | 9 |

## Categories

- `human_dignity` - Human rights and dignity
- `safety` - Harm prevention
- `autonomy` - User control
- `privacy` - Data protection
- `transparency` - Explainability

## Usage

### Quick Check

```python
from mcp_b import check_ethical

# Check if action is ethical
if check_ethical("collect_data", personal_data=True, consent=True):
    print("Action allowed")
else:
    print("Action blocked - ethical violation")
```

### Full API

```python
from mcp_b import ETHIC, EthicCategory

ethic = ETHIC()

# Get principles by category
for principle in ethic.get_by_category(EthicCategory.SAFETY):
    print(f"[{principle.priority}] {principle.name}")

# Check action with details
result = ethic.check_action(
    action="store_user_data",
    context={
        "personal_data": True,
        "consent": True,
        "encryption": True
    }
)

if result.allowed:
    print("Action permitted")
else:
    print(f"Violation: {result.violation.reason}")
```

## Ethics Model

MCP-B includes advanced ethics analysis tools:

```python
from mcp_b import get_ethics_prompt, MoralFramework

# Get analysis prompt for different frameworks
prompt = get_ethics_prompt(MoralFramework.DEONTOLOGICAL, "Is this action ethical?")
```
