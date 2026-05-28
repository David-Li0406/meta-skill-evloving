# Examples

**Example: Implement Centralized Error Handler**
Request: "Create a reusable error handling module for our Node.js API"
Result: Created lib/sentry.ts with captureError function, scope management, and breadcrumb utilities

**Example: Add Transaction Tracing**
Request: "Track performance of our checkout flow"
Result: Implemented transaction with child spans for cart, payment, and confirmation steps

### Python Patterns
```python
import sentry_sdk
from contextlib import contextmanager

@contextmanager
def sentry_scope(tags: dict = None, extra: dict = None):
    with sentry_sdk.push_scope() as scope:
        if tags:
            for key, value in tags.items():
                scope.set_tag(key, value)
        if extra:
            for key, value in extra.items():
                scope.set_extra(key, value)
        yield scope

# Usage
with sentry_scope(tags={'operation': 'sync'}, extra={'count': 100}):
    perform_sync_operation()
```