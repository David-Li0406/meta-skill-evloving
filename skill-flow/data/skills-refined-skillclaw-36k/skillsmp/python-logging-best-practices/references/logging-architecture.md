# Python Logging Architecture Guide

## When to Use Which Approach

| Approach              | Use Case                         | Pros                                       | Cons                |
| --------------------- | -------------------------------- | ------------------------------------------ | ------------------- |
| `loguru`              | Modern scripts, CLI tools        | Zero-config, async-safe, built-in rotation | External dependency |
| `RotatingFileHandler` | LaunchAgent daemons, stdlib-only | No dependencies                            | More setup required |
| `logger_setup.py`     | Rich terminal apps               | Beautiful output                           | Complex setup       |

## Decision Tree

```
Need logging?
├── Stdlib-only required?
│   └── YES → RotatingFileHandler
│       └── See: launchagent-log-rotation skill
├── LaunchAgent/daemon?
│   └── YES → RotatingFileHandler
│       └── Prevents unbounded log growth
├── Rich terminal output needed?
│   └── YES → logger_setup.py pattern
│       └── See: ~/scripts/utils/logger_setup.py
└── Modern script/CLI tool?
    └── YES → loguru + platformdirs
        └── This skill's recommended pattern
```

## Approach Details

### 1. Loguru (Recommended for Scripts)

**Best for**: Modern Python scripts, CLI tools, automation

```python
from loguru import logger
import platformdirs

logger.add(
    platformdirs.user_log_dir("my-app", ensure_exists=True) + "/app.jsonl",
    rotation="10 MB",
    retention="7 days",
    compression="gz"
)
```

**Advantages**:

- Zero configuration to start
- Built-in rotation, retention, compression
- Async-safe by default
- Structured logging with `extra` kwargs
- Exception formatting included

### 2. RotatingFileHandler (Stdlib)

**Best for**: LaunchAgent services, stdlib-only requirements

```python
from logging.handlers import RotatingFileHandler
import logging

handler = RotatingFileHandler(
    "/path/to/app.log",
    maxBytes=100 * 1024 * 1024,  # 100MB
    backupCount=5
)
logging.getLogger().addHandler(handler)
```

**Advantages**:

- No external dependencies
- Predictable disk usage
- Well-understood behavior

**Reference**: `Skill(launchagent-log-rotation)`

### 3. Rich Integration (Complex Apps)

**Best for**: Applications with rich terminal UI

```python
from rich.logging import RichHandler
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)]
)
```

**Advantages**:

- Beautiful terminal output
- Syntax-highlighted tracebacks
- Progress bars integration

## Output Format Recommendations

| Output Type      | Format                                     | Extension |
| ---------------- | ------------------------------------------ | --------- |
| Machine analysis | JSONL                                      | `.jsonl`  |
| Human reading    | Plain text                                 | `.log`    |
| Both             | JSONL (parseable by jq AND human readable) | `.jsonl`  |

## Common Patterns

### Dual Output (Console + File)

```python
from loguru import logger
import sys

# Human-readable to console
logger.add(sys.stderr, level="INFO")

# Machine-readable to file
logger.add("app.jsonl", format=json_formatter, level="DEBUG")
```

### Environment-Based Configuration

```python
import os

log_level = os.getenv("LOG_LEVEL", "INFO")
logger.add(sys.stderr, level=log_level)
```

## Related Resources

- [loguru-patterns.md](./loguru-patterns.md) - Loguru configuration
- [platformdirs-xdg.md](./platformdirs-xdg.md) - Cross-platform paths
- [migration-guide.md](./migration-guide.md) - From print() to logging
