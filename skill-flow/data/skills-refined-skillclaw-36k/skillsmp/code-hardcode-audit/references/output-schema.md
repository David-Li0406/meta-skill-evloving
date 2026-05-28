**Skill**: [Code Hardcode Audit](../SKILL.md)

# Output Schema

## JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "summary": {
      "type": "object",
      "properties": {
        "total_findings": { "type": "integer" },
        "by_tool": {
          "type": "object",
          "additionalProperties": { "type": "integer" }
        },
        "by_severity": {
          "type": "object",
          "additionalProperties": { "type": "integer" }
        }
      }
    },
    "findings": {
      "type": "array",
      "items": { "$ref": "#/definitions/Finding" }
    },
    "errors": {
      "type": "array",
      "items": { "type": "string" }
    }
  },
  "definitions": {
    "Finding": {
      "type": "object",
      "required": ["id", "tool", "rule", "file", "line"],
      "properties": {
        "id": { "type": "string", "pattern": "^(RUFF|SGRP|JSCPD)-[0-9]{3}$" },
        "tool": { "enum": ["ruff", "semgrep", "jscpd"] },
        "rule": { "type": "string" },
        "file": { "type": "string" },
        "line": { "type": "integer" },
        "column": { "type": "integer" },
        "end_line": { "type": ["integer", "null"] },
        "message": { "type": "string" },
        "severity": { "enum": ["high", "medium", "low"] },
        "suggested_fix": { "type": "string" }
      }
    }
  }
}
```

## Example Output

### Full Audit (JSON)

```json
{
  "summary": {
    "total_findings": 5,
    "by_tool": {
      "ruff": 2,
      "semgrep": 2,
      "jscpd": 1
    },
    "by_severity": {
      "high": 1,
      "medium": 3,
      "low": 1
    }
  },
  "findings": [
    {
      "id": "RUFF-001",
      "tool": "ruff",
      "rule": "PLR2004",
      "file": "src/config.py",
      "line": 42,
      "column": 8,
      "message": "Magic value used in comparison: 8123",
      "severity": "medium",
      "suggested_fix": "Extract to named constant"
    },
    {
      "id": "SGRP-001",
      "tool": "semgrep",
      "rule": "hardcoded-credential",
      "file": "src/client.py",
      "line": 15,
      "column": 1,
      "message": "Potential hardcoded credential. Use environment variables.",
      "severity": "high",
      "suggested_fix": "Use os.environ, Doppler, or secrets manager"
    },
    {
      "id": "JSCPD-001",
      "tool": "jscpd",
      "rule": "duplicate-code",
      "file": "src/handlers/a.py",
      "line": 20,
      "end_line": 45,
      "message": "Clone detected with src/handlers/b.py (25 lines)",
      "severity": "low",
      "suggested_fix": "Extract to shared function or module"
    }
  ],
  "errors": []
}
```

### Text Output

```
src/config.py:42:8: PLR2004 Magic value used in comparison: 8123 [ruff]
src/client.py:15:1: hardcoded-credential Potential hardcoded credential [semgrep]
src/handlers/a.py:20-45: duplicate-code Clone detected (25 lines) [jscpd]

Summary: 5 findings (ruff: 2, semgrep: 2, jscpd: 1)
```

## Finding ID Format

| Prefix   | Tool         | Example     |
| -------- | ------------ | ----------- |
| `RUFF-`  | Ruff PLR2004 | `RUFF-001`  |
| `SGRP-`  | Semgrep      | `SGRP-001`  |
| `JSCPD-` | jscpd        | `JSCPD-001` |

## Severity Levels

| Level    | Meaning                         | Action                |
| -------- | ------------------------------- | --------------------- |
| `high`   | Security risk or critical issue | Fix immediately       |
| `medium` | Code quality issue              | Fix in current sprint |
| `low`    | Minor improvement               | Track for later       |

## Tool-Specific Severity Mapping

| Tool    | Default Severity | Notes                                 |
| ------- | ---------------- | ------------------------------------- |
| Ruff    | medium           | Magic numbers are quality issues      |
| Semgrep | Varies by rule   | Credentials = high, timeframes = low  |
| jscpd   | low              | Duplicates are refactoring candidates |
