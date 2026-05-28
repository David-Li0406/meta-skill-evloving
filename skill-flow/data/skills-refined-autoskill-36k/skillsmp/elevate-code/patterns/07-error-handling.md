# Pattern 7: Error Handling

**Problem**: Errors are cryptic ("Error: ENOENT"), don't explain what went wrong, and provide no guidance on how to fix them.

**Solution**: Implement structured error handling with clear messages, retry logic for transient failures, and graceful degradation.

---

## Concept

Error Handling answers: **"What went wrong, and how do I fix it?"**

Good error handling provides:
1. **Clarity** — What failed and why
2. **Actionability** — How to fix it
3. **Resilience** — Automatic recovery from transient failures
4. **Graceful Degradation** — Partial results when possible

---

## The Error Message Template

Every user-facing error should include:

```
ERROR: <What failed>
REASON: <Why it failed>
FIX: <How to fix it>
DOCS: <Link if applicable>
```

### Examples

```
# BAD
Error: ENOENT: no such file or directory

# GOOD
ERROR: Cannot read configuration file
REASON: File not found: /home/user/.config/my-tool/config.json
FIX: Run 'my-tool init' to create the default configuration
DOCS: https://docs.my-tool.dev/configuration
```

```
# BAD
Error: 401 Unauthorized

# GOOD
ERROR: Authentication failed
REASON: The API key is invalid or expired
FIX: Check your API_KEY environment variable
     Current value: sk-proj-...abc (truncated)
     Get a new key: https://platform.openai.com/api-keys
```

---

## Implementation

### Python: Custom Exception Hierarchy

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class ErrorContext:
    """Structured error information."""
    what: str
    why: str
    fix: str
    docs: Optional[str] = None

    def __str__(self) -> str:
        lines = [
            f"ERROR: {self.what}",
            f"REASON: {self.why}",
            f"FIX: {self.fix}"
        ]
        if self.docs:
            lines.append(f"DOCS: {self.docs}")
        return "\n".join(lines)

class ToolError(Exception):
    """Base exception for all tool errors."""
    def __init__(self, context: ErrorContext):
        self.context = context
        super().__init__(str(context))

class ConfigurationError(ToolError):
    """Configuration-related errors."""
    pass

class AuthenticationError(ToolError):
    """Authentication-related errors."""
    pass

class NetworkError(ToolError):
    """Network-related errors."""
    pass

# Usage
def load_config(path: str) -> dict:
    import json
    from pathlib import Path

    config_path = Path(path)
    if not config_path.exists():
        raise ConfigurationError(ErrorContext(
            what="Cannot read configuration file",
            why=f"File not found: {config_path}",
            fix="Run 'my-tool init' to create the default configuration",
            docs="https://docs.my-tool.dev/configuration"
        ))

    try:
        return json.loads(config_path.read_text())
    except json.JSONDecodeError as e:
        raise ConfigurationError(ErrorContext(
            what="Invalid configuration file",
            why=f"JSON parse error at line {e.lineno}: {e.msg}",
            fix=f"Check the syntax of {config_path}",
            docs="https://docs.my-tool.dev/configuration#format"
        )) from e
```

### Python: Retry with Backoff

```python
import time
import random
from functools import wraps
from typing import Tuple, Type, Callable, TypeVar

T = TypeVar('T')

class RetryableError(Exception):
    """Marker for errors that should be retried."""
    pass

class PermanentError(Exception):
    """Marker for errors that should NOT be retried."""
    pass

def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    jitter: bool = True,
    retryable: Tuple[Type[Exception], ...] = (RetryableError, ConnectionError, TimeoutError)
) -> Callable:
    """Decorator for retry with exponential backoff."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except retryable as e:
                    last_exception = e

                    if attempt == max_retries:
                        break

                    delay = min(base_delay * (exponential_base ** attempt), max_delay)
                    if jitter:
                        delay *= 0.5 + random.random()

                    print(f"Attempt {attempt + 1}/{max_retries + 1} failed: {e}")
                    print(f"Retrying in {delay:.1f}s...")
                    time.sleep(delay)
                except Exception:
                    raise  # Non-retryable, propagate immediately

            raise last_exception
        return wrapper
    return decorator

# Usage
@retry_with_backoff(max_retries=3)
def fetch_api_data(url: str) -> dict:
    import requests
    response = requests.get(url, timeout=10)

    if response.status_code == 429:  # Rate limited
        raise RetryableError("Rate limited")
    if response.status_code >= 500:  # Server error
        raise RetryableError(f"Server error: {response.status_code}")
    if response.status_code == 401:
        raise PermanentError("Authentication failed")  # Don't retry

    response.raise_for_status()
    return response.json()
```

### Node.js: Error Classes

```javascript
class ToolError extends Error {
  constructor(what, why, fix, docs = null) {
    const message = [
      `ERROR: ${what}`,
      `REASON: ${why}`,
      `FIX: ${fix}`,
      docs ? `DOCS: ${docs}` : null
    ].filter(Boolean).join('\n');

    super(message);
    this.name = 'ToolError';
    this.what = what;
    this.why = why;
    this.fix = fix;
    this.docs = docs;
  }
}

class ConfigurationError extends ToolError {
  constructor(what, why, fix, docs) {
    super(what, why, fix, docs);
    this.name = 'ConfigurationError';
  }
}

class AuthenticationError extends ToolError {
  constructor(what, why, fix, docs) {
    super(what, why, fix, docs);
    this.name = 'AuthenticationError';
  }
}

// Usage
function loadConfig(filePath) {
  const fs = require('fs');

  if (!fs.existsSync(filePath)) {
    throw new ConfigurationError(
      'Cannot read configuration file',
      `File not found: ${filePath}`,
      "Run 'my-tool init' to create the default configuration",
      'https://docs.my-tool.dev/configuration'
    );
  }

  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch (e) {
    throw new ConfigurationError(
      'Invalid configuration file',
      `JSON parse error: ${e.message}`,
      `Check the syntax of ${filePath}`
    );
  }
}
```

### Node.js: Retry with Backoff

```javascript
async function withRetry(fn, options = {}) {
  const {
    maxRetries = 3,
    baseDelay = 1000,
    maxDelay = 60000,
    exponentialBase = 2,
    isRetryable = () => true
  } = options;

  let lastError;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;

      if (!isRetryable(error) || attempt === maxRetries) {
        throw error;
      }

      const delay = Math.min(baseDelay * Math.pow(exponentialBase, attempt), maxDelay);
      const jitteredDelay = delay * (0.5 + Math.random());

      console.log(`Attempt ${attempt + 1}/${maxRetries + 1} failed: ${error.message}`);
      console.log(`Retrying in ${Math.round(jitteredDelay)}ms...`);

      await new Promise(r => setTimeout(r, jitteredDelay));
    }
  }

  throw lastError;
}

// Usage
const data = await withRetry(
  () => fetchFromApi(url),
  {
    maxRetries: 3,
    isRetryable: (err) => {
      // Retry on network errors and 5xx, not on 4xx
      if (err.code === 'ENOTFOUND' || err.code === 'ETIMEDOUT') return true;
      if (err.status >= 500) return true;
      if (err.status === 429) return true;  // Rate limited
      return false;
    }
  }
);
```

### Graceful Degradation

```python
from dataclasses import dataclass
from typing import List, TypeVar, Generic

T = TypeVar('T')

@dataclass
class PartialResult(Generic[T]):
    """Result that may contain partial success."""
    successful: List[T]
    failed: List[tuple[T, Exception]]

    @property
    def all_succeeded(self) -> bool:
        return len(self.failed) == 0

    @property
    def any_succeeded(self) -> bool:
        return len(self.successful) > 0

def process_items_gracefully(items: List[T], processor) -> PartialResult[T]:
    """Process items, collecting successes and failures separately."""
    result = PartialResult(successful=[], failed=[])

    for item in items:
        try:
            processor(item)
            result.successful.append(item)
        except Exception as e:
            result.failed.append((item, e))

    return result

# Usage
result = process_items_gracefully(items, process_single_item)

if result.all_succeeded:
    print(f"All {len(result.successful)} items processed successfully")
elif result.any_succeeded:
    print(f"Processed {len(result.successful)}/{len(items)} items")
    print(f"Failed items:")
    for item, error in result.failed:
        print(f"  - {item}: {error}")
else:
    print("All items failed")
```

---

## Error Categories

| Category | Retry? | Example |
|----------|--------|---------|
| Configuration | No | Missing file, invalid JSON |
| Authentication | No | Invalid API key |
| Validation | No | Invalid user input |
| Network (transient) | Yes | Timeout, DNS failure |
| Rate Limit | Yes (with backoff) | 429 Too Many Requests |
| Server Error | Yes | 500, 502, 503 |
| Resource Not Found | No | 404 |

---

## Checklist

- [ ] Custom exception classes with structured context
- [ ] Error messages include what, why, and fix
- [ ] Retry logic for transient failures
- [ ] Exponential backoff with jitter
- [ ] Graceful degradation returns partial results
- [ ] Non-retryable errors fail fast
- [ ] Errors are logged with full context

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| `except Exception: pass` | Swallows all errors silently | Handle specific exceptions |
| Retry everything | Wastes time on permanent failures | Categorize retryable errors |
| No retry at all | Single failure = complete failure | Retry transient errors |
| Generic "Error occurred" | User can't fix it | Include context and fix |
