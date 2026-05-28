**Skill**: [Implement Plan Engineering Standards](../SKILL.md)

# Constants Management

Core principle: **Abstract magic numbers into semantic, version-agnostic dynamic constants**

---

## The Rule

Replace hardcoded values with:

1. **Named constants** with semantic meaning
2. **Configuration** loaded from files/environment
3. **Dynamic values** computed at runtime when appropriate

---

## Magic Numbers to Avoid

| Category       | Bad                    | Good                                  |
| -------------- | ---------------------- | ------------------------------------- |
| **Timeouts**   | `timeout=30`           | `timeout=DEFAULT_API_TIMEOUT_SECONDS` |
| **Limits**     | `if len(items) > 100:` | `if len(items) > MAX_BATCH_SIZE:`     |
| **Ports**      | `port=8080`            | `port=config.server_port`             |
| **Thresholds** | `if ratio < 0.7:`      | `if ratio < MIN_SUCCESS_RATIO:`       |
| **Sizes**      | `chunk_size=1024`      | `chunk_size=BUFFER_SIZE_BYTES`        |

---

## Correct Patterns

### Named Constants

```python
# ✅ Semantic names at module level
DEFAULT_API_TIMEOUT_SECONDS = 30
MAX_RETRY_ATTEMPTS = 3
MIN_PASSWORD_LENGTH = 12
BUFFER_SIZE_BYTES = 4096

def fetch_data(url: str) -> dict:
    return requests.get(url, timeout=DEFAULT_API_TIMEOUT_SECONDS).json()
```

### Configuration Objects

```python
# ✅ Configuration from environment/files
@dataclass
class AppConfig:
    api_timeout: int = field(default_factory=lambda: int(os.getenv("API_TIMEOUT", "30")))
    max_batch_size: int = field(default_factory=lambda: int(os.getenv("MAX_BATCH_SIZE", "100")))
    server_port: int = field(default_factory=lambda: int(os.getenv("PORT", "8080")))

config = AppConfig()
```

### Dynamic Constants

```python
# ✅ Computed at runtime
from importlib.metadata import version

PACKAGE_VERSION = version("mypackage")  # Not hardcoded "1.2.3"

# ✅ Platform-specific
import multiprocessing
DEFAULT_WORKERS = multiprocessing.cpu_count()
```

---

## Version Strings

**Never hardcode version strings.** Use runtime discovery:

```python
# ❌ Bad - hardcoded
VERSION = "1.2.3"

# ✅ Good - dynamic
from importlib.metadata import version
__version__ = version("mypackage")
```

See [`semantic-release` skill](../../semantic-release/SKILL.md) for version management.

---

## Hardcode Detection

Before release, audit for hardcoded values:

```bash
# Requires CLAUDE_PLUGIN_ROOT to be set (available in plugin context)
# For manual runs, set to your plugin installation directory
uv run --script "$CLAUDE_PLUGIN_ROOT/skills/code-hardcode-audit/scripts/audit_hardcodes.py" -- src/
```

See [`code-hardcode-audit` skill](../../code-hardcode-audit/SKILL.md) for details.

---

## Exceptions

Some hardcoded values are acceptable:

- **Mathematical constants** - `PI = 3.14159`, `E = 2.71828`
- **Protocol constants** - HTTP status codes, well-known ports for standard services
- **Array indices** - When semantically clear (e.g., `row[0]` for first element)

The test: **Would this value ever need to change?** If yes, make it configurable.

---

## Organization

Group constants by domain:

```python
# constants.py

# Timing
DEFAULT_API_TIMEOUT_SECONDS = 30
DEFAULT_CACHE_TTL_SECONDS = 3600
HEALTH_CHECK_INTERVAL_SECONDS = 60

# Limits
MAX_BATCH_SIZE = 100
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10MB
MAX_CONCURRENT_REQUESTS = 10

# Feature flags (load from config in production)
ENABLE_DEBUG_LOGGING = os.getenv("DEBUG", "").lower() == "true"
```
