# Script Bundling

Execute scripts without loading contents into context (zero-token execution).

## How It Works

- Scripts in skill directory executed via Bash
- Only stdout consumes tokens
- Script contents never loaded into context

## Directory Structure

```
my-skill/
├── SKILL.md
├── scripts/
│   ├── validate.py      # Executed, not loaded
│   └── process.sh       # Executed, not loaded
└── reference.md         # Loaded on demand
```

## Examples

**Validation script:**

SKILL.md:

```yaml
---
name: form-validator
description: Validates form data against schema
---

# Form Validator

To validate input, run:

python scripts/validate.py input.json

The script outputs JSON with validation results.
```

scripts/validate.py:

```python
#!/usr/bin/env python3
import json, sys

data = json.load(open(sys.argv[1]))
errors = []

if not data.get("email"):
    errors.append("Missing email")
if not data.get("name"):
    errors.append("Missing name")

print(json.dumps({"valid": len(errors) == 0, "errors": errors}))
```

**Data transformation script:**

SKILL.md:

```yaml
---
name: csv-processor
description: Processes CSV files for analysis
---

# CSV Processor

Transform CSV to JSON:

python scripts/csv_to_json.py input.csv > output.json
```

## Links

- Docs: https://code.claude.com/docs/en/skills.md (Script bundling section)
- Issues:
  - [#15757](https://github.com/anthropics/claude-code/issues/15757) - Skills can't read bundled files without permission
