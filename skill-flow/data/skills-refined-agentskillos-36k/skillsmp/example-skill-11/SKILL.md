---
name: example-skill
description: Template skill demonstrating the complete Skillsets framework structure. Use as a reference when creating new skills for AI agents.
---

# Example Skill

> **Template skill demonstrating the Skillsets framework structure**

---

## Overview

This is a **template skill** showing how to create skills for AI agents. Use this as a reference when building your own skills.

---

## When to Trigger

Activate this skill when the user:

- Asks about creating skills
- Wants to see skill structure examples
- Needs a template for new skill development

**Example prompts:**

- "Show me how skills work"
- "Create a skill template"
- "Use the example-skill to demonstrate the framework"

---

## Capabilities

| Feature       | Description                       |
| ------------- | --------------------------------- |
| **Greet**     | Generate personalized greetings   |
| **Calculate** | Perform simple calculations       |
| **Format**    | Convert data to different formats |

---

## Quick Start

### 1. Basic Usage

```bash
# Run the greeting script
python skills/example-skill/scripts/greet.py --name "World"
# Output: {"status": "success", "message": "Hello, World!"}

# Perform a calculation
python skills/example-skill/scripts/calculate.py --operation add --a 5 --b 3
# Output: {"status": "success", "result": 8}
```

### 2. Using References

Check reference documentation in `references/` for detailed patterns and examples.

---

## Scripts

| Script           | Purpose            | Arguments                   |
| ---------------- | ------------------ | --------------------------- |
| `greet.py`       | Generate greetings | `--name` (required)         |
| `calculate.py`   | Math operations    | `--operation`, `--a`, `--b` |
| `format_data.py` | Data formatting    | `--input`, `--format`       |

---

## Directory Structure

```
example-skill/
├── SKILL.md              # This file (required)
├── scripts/              # Executable tools
│   ├── greet.py          # Greeting generator
│   ├── calculate.py      # Calculator
│   └── format_data.py    # Data formatter
├── references/           # On-demand documentation
│   └── patterns.md       # Common usage patterns
└── assets/               # Templates, configs, etc.
    └── config.template.json
```

---

## Best Practices

### 1. Script Design

- ✅ Accept CLI arguments with `argparse`
- ✅ Return JSON output for easy parsing
- ✅ Use exit codes (0=success, 1+=error)
- ✅ Include docstrings with usage examples

### 2. Documentation

- ✅ Clear "When to Trigger" section
- ✅ Quick Start with working examples
- ✅ Script reference table
- ✅ Error handling notes

### 3. Integration

- ✅ Self-contained (minimal external deps)
- ✅ Idempotent operations where possible
- ✅ Structured error responses

---

## Error Handling

| Exit Code | Meaning           |
| --------- | ----------------- |
| 0         | Success           |
| 1         | Invalid arguments |
| 2         | Input not found   |
| 3         | Processing error  |

**Error Response Format:**

```json
{
  "status": "error",
  "code": 1,
  "message": "Descriptive error message"
}
```

---

## See Also

- [SKILLS_CATALOG.md](../SKILLS_CATALOG.md) — Full skills listing
- [skill-creator](../../skill-creator/SKILL_skillcreator.md) — Create new skills
- [AGENTS.md](../../AGENTS.md) — 3-Layer Architecture guide
