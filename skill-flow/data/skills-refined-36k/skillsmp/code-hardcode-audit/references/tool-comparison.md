**Skill**: [Code Hardcode Audit](../SKILL.md)

# Tool Comparison

## Overview

| Tool             | Detection Focus                          | Language Support | Speed  | Install                 |
| ---------------- | ---------------------------------------- | ---------------- | ------ | ----------------------- |
| **Ruff PLR2004** | Magic value comparisons                  | Python only      | Fast   | `uv tool install ruff`  |
| **Semgrep**      | Pattern-based (URLs, ports, credentials) | Multi-language   | Medium | `brew install semgrep`  |
| **jscpd**        | Duplicate code blocks                    | Multi-language   | Slow   | `npx jscpd` (on-demand) |

## Detection Capabilities

### Ruff PLR2004

**Detects**: Magic numbers in comparisons

```python
# DETECTED
if timeout > 30:  # PLR2004: Magic value 30
if port == 8123:  # PLR2004: Magic value 8123

# NOT DETECTED (by design)
DEFAULT_TIMEOUT = 30  # Assignment, not comparison
```

**Limitations**:

- Python only
- Only comparisons, not assignments
- Doesn't detect string literals

### Semgrep (Custom Rules)

**Detects**: 7 pattern categories

| Rule ID                  | Detects                     | Severity |
| ------------------------ | --------------------------- | -------- |
| `hardcoded-url`          | HTTP/HTTPS URLs             | WARNING  |
| `hardcoded-port`         | Port numbers                | WARNING  |
| `hardcoded-timeframe`    | "1h", "4h", "1d" strings    | INFO     |
| `hardcoded-path`         | /tmp, /var, /home paths     | WARNING  |
| `hardcoded-credential`   | password=, api_key=, token= | ERROR    |
| `hardcoded-retry-config` | max_retries=, timeout=      | INFO     |
| `hardcoded-api-limit`    | limit=, batch_size=         | INFO     |

**Limitations**:

- Requires rule tuning to reduce false positives
- Pattern matching may miss obfuscated values

### jscpd

**Detects**: Copy-paste code blocks (DRY violations)

```python
# DETECTED: Identical blocks across files
def process_a():
    data = fetch()
    validate(data)
    transform(data)
    return data

def process_b():  # Clone of process_a
    data = fetch()
    validate(data)
    transform(data)
    return data
```

**Limitations**:

- Slower than other tools (full AST parsing)
- Requires Node.js (available via mise)
- High threshold to avoid false positives

## Complementary Coverage

```
┌─────────────────────────────────────────────────────────────┐
│                     Hardcode Detection                       │
├─────────────────┬─────────────────┬─────────────────────────┤
│   Ruff PLR2004  │    Semgrep      │        jscpd            │
│                 │                 │                         │
│  Magic numbers  │  URLs, ports    │  Duplicate blocks       │
│  in comparisons │  paths, creds   │  (any language)         │
│                 │  timeframes     │                         │
│  Python only    │  Multi-language │  Multi-language         │
└─────────────────┴─────────────────┴─────────────────────────┘
```

## When to Use Each Tool

| Scenario                           | Recommended Tool         |
| ---------------------------------- | ------------------------ |
| Quick Python magic number check    | Ruff alone               |
| Security audit (credentials, URLs) | Semgrep alone            |
| DRY violation detection            | jscpd alone              |
| Comprehensive audit                | All three (orchestrator) |
| CI/CD integration                  | Ruff + Semgrep (faster)  |
