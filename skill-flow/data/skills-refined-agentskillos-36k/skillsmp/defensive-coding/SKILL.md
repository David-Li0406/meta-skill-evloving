---
name: defensive-coding
description: Use when writing code that handles external input, crosses system boundaries, or performs destructive operations. Covers multi-layer validation and observability.
---

# Defensive Coding

## Overview

Defensive coding makes bugs structurally impossible rather than temporarily fixed. The core principle: validate at every layer data passes through, and instrument for observability so failures are diagnosable. A bug isn't fixed until it's impossible.

## When to Use

- Invalid data caused a bug deep in the call stack
- Data crosses system boundaries (API → service → storage)
- Multiple code paths reach vulnerable code
- Tests mock intermediate layers
- Debugging production issues is difficult

## Core Pattern

### Layer 1: Entry Point Validation

**Purpose**: Reject invalid input at API/system boundary — your first defense line.

```python
def process_config(config_path: str) -> Config:
    if not config_path:
        raise ValueError("config_path is required")

    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    if path.suffix != ".yaml":
        raise ValueError(f"Expected .yaml file, got: {path.suffix}")

    return _load_config(path)
```

### Layer 2: Business Logic Validation

**Purpose**: Ensure data makes sense for this specific operation.

```python
def calculate_discount(price: float, discount_percent: float) -> float:
    if price < 0:
        raise ValueError(f"Price cannot be negative: {price=}")

    if not 0 <= discount_percent <= 100:
        raise ValueError(f"Discount must be 0-100: {discount_percent=}")

    return price * (1 - discount_percent / 100)
```

### Layer 3: Environment Guards

**Purpose**: Prevent dangerous operations in specific contexts.

```python
def initialize_repository(target_dir: str) -> None:
    path = Path(target_dir).resolve()

    # Guard: prevent git init outside temp dir in tests
    if os.getenv("ENV") == "test":
        if not path.is_relative_to(Path(tempfile.gettempdir())):
            raise RuntimeError(f"Refusing init outside temp dir in test: {path}")

    # Guard: never init in home directory root
    if path == Path.home():
        raise RuntimeError(f"Refusing init in home directory root: {path}")

    _do_git_init(path)
```

### Layer 4: Observability

**Purpose**: Capture context for forensics when other layers fail.

```python
logger = structlog.get_logger()

def process_order(order_id: str, items: list[dict]) -> OrderResult:
    logger.info("order_started", order_id=order_id, item_count=len(items))

    try:
        result = _do_process(order_id, items)
        logger.info("order_completed", order_id=order_id, total=result.total)
        return result
    except Exception:
        logger.exception("order_failed", order_id=order_id)
        raise
```

## Exception Handling Patterns

### Chain to Preserve Context

```python
try:
    config = load_config(path)
except FileNotFoundError as e:
    raise ConfigurationError(f"Failed to load config: {path}") from e
```

### Handle at the Right Layer

```python
# Bad — catching too early, losing context
def get_user(user_id: str) -> User:
    try:
        return db.fetch_user(user_id)
    except DatabaseError:
        return None  # Caller has no idea why

# Good — let it propagate, handle at boundary
@router.get("/users/{user_id}")
def get_user_endpoint(user_id: str) -> Response:
    try:
        return user_service.get(user_id)
    except UserNotFoundError:
        return Response(status=404)
```

## Observability Checklist

- [ ] Structured JSON logging (not string concatenation)
- [ ] Correlation IDs for request tracing
- [ ] Log at boundaries: entry, exit, errors
- [ ] Include context: IDs, counts, durations
- [ ] `logger.exception()` for stack traces on errors
- [ ] Sensitive data excluded (passwords, tokens, PII)

## Decision Heuristic

| Situation | Layers Needed |
|-----------|---------------|
| Public API, simple validation | 1 only |
| Data crosses multiple services | 1 + 2 + 4 |
| Destructive operations (delete, init, write) | 1 + 2 + 3 + 4 |
| Chasing hard-to-reproduce bug | 1 + 2 + 3 + 4 |
| Tests mock intermediate layers | At minimum: 1 + 3 |

## Quick Reference

| Layer | Question | Typical Check |
|-------|----------|---------------|
| Entry | Is input valid? | Non-empty, exists, correct type |
| Business | Does it make sense here? | Required for operation, within bounds |
| Environment | Safe in this context? | Not in prod, inside temp dir, bulk guard |
| Observability | Can we diagnose failures? | Structured logs, correlation IDs, context |

## Common Mistakes

| Mistake | Why It Fails | Correct Approach |
|---------|--------------|------------------|
| One validation point | Other code paths bypass it | Add entry + business layers minimum |
| Bare `except:` | Catches KeyboardInterrupt, hides bugs | Catch specific exceptions |
| `except Exception: pass` | Silent failure, impossible to debug | Log and re-raise, or handle specifically |
| String logs | Can't query log aggregators | Use structured logging with fields |
| Logging sensitive data | Security/compliance violation | Exclude passwords, tokens, PII |
| No correlation ID | Can't trace across services | Add at entry point |
| Guards only in prod | Test pollution, accidental side effects | Add guards in test too |

## Anti-Rationalizations

- "Validation at the entry point is enough" — Other code paths bypass it. Add business layer validation.
- "I'll add logging when there's a bug" — You won't have the context you need. Add it now.
- "Structured logging is overkill" — Until you're grepping gigabytes of logs at 3am.
- "Environment guards slow development" — Less than recovering from `rm -rf` in the wrong directory.

## Connection to Other Skills

- **[howto-code-in-python](../howto-code-in-python/SKILL.md)**: Exception handling style
- **[howto-program-functionally-ish](../howto-program-functionally-ish/SKILL.md)**: Pure logic (Layer 2) vs side effects (Layers 1, 3, 4)
