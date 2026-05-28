**Skill**: [Skill Architecture](../SKILL.md)

# Workflow Patterns

Common patterns for skill creation with practical examples.

---

## Pattern A: Minimal Skill (Single File)

**Use when**: Simple, stateless operations

```yaml
---
name: code-formatter
description: Format Python code using black. Use when formatting Python files.
allowed-tools: Read, Edit, Bash
---

# Code Formatter

Run black formatter:
1. Check file: `file <filename.py>`
2. Format: `black <filename.py>`
3. Verify changes
```

**Directory**: Just `SKILL.md` (no subdirectories)
**Tokens**: ~30 metadata, ~150 when loaded

## Pattern B: Skill with Scripts

**Use when**: Deterministic operations, repeated code

```yaml
---
name: data-validator
description: Validate CSV files for data quality. Use with CSV or tabular data.
allowed-tools: Read, Bash
---

# Data Validator

Validate data:
1. Run: `scripts/validate.py --input data.csv`
2. Review validation report
3. Fix errors if found

## Scripts
- validate.py: Schema, nulls, duplicates check
```

**Directory**:

```
data-validator/
├── SKILL.md
└── scripts/
    └── validate.py
```

## Pattern C: Skill with References

**Use when**: Large documentation, schemas

```yaml
---
name: api-client
description: Call internal REST API following company standards. Use for API requests.
allowed-tools: Read, Bash
---

# API Client

API operations:
1. Consult [API Reference](references/api-spec.md) for endpoints
2. Build request per [Examples](references/examples.md)
3. Execute with curl

Use grep for specific endpoints:
`grep -i "POST /users" references/api-spec.md`
```

**Directory**:

```
api-client/
├── SKILL.md
└── references/
    ├── api-spec.md (10k words)
    └── examples.md
```

---

## Workflow Comparison

| Criteria             | Marketplace Process | Manual Process |
| -------------------- | ------------------- | -------------- |
| Complexity           | Medium-High         | Low            |
| Uses scripts         | Yes                 | Optional       |
| Structure guaranteed | Yes (init script)   | Manual         |
| Validation           | Automatic           | Manual         |
| Best for             | Complex skills      | Simple skills  |
| Setup time           | 5-10 min            | 2-3 min        |

**Recommendation**: Use marketplace process for skills with scripts/references/assets. Use manual for simple instruction-only skills.
