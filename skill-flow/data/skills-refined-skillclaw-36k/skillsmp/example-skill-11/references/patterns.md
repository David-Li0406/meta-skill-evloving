# Usage Patterns

> Common patterns and examples for the example-skill

---

## Pattern 1: Basic Script Invocation

```bash
# Direct execution
python scripts/greet.py --name "Alice"

# Agent orchestration
# 1. Agent reads SKILL.md
# 2. Identifies appropriate script
# 3. Constructs command with arguments
# 4. Parses JSON response
```

---

## Pattern 2: Chaining Scripts

```bash
# Generate data, then format it
python scripts/calculate.py --operation add --a 10 --b 20 | \
  python scripts/format_data.py --format table
```

---

## Pattern 3: Error Handling

```python
# In agent orchestration:
import subprocess
import json

result = subprocess.run(
    ["python", "scripts/calculate.py", "--operation", "divide", "--a", "10", "--b", "0"],
    capture_output=True,
    text=True
)

if result.returncode != 0:
    error = json.loads(result.stderr)
    print(f"Error {error['code']}: {error['message']}")
else:
    success = json.loads(result.stdout)
    print(f"Result: {success['result']}")
```

---

## Pattern 4: Configuration Templates

Use `assets/config.template.json` for reusable configurations:

```json
{
  "default_style": "casual",
  "output_format": "json",
  "verbose": false
}
```

---

## Anti-Patterns to Avoid

| ❌ Don't                  | ✅ Do Instead              |
| ------------------------- | -------------------------- |
| Print unstructured text   | Return JSON objects        |
| Use global state          | Accept all config via args |
| Require interactive input | Use stdin for data         |
| Hardcode paths            | Accept paths as arguments  |
