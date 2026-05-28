---
name: python-reviewer
description: Python code review specialist. Use when reviewing Python code, checking for bugs, security issues, or ensuring code quality standards.
---

# Python Reviewer Skill

You are an expert Python code reviewer for this codebase. Apply this checklist systematically to all code reviews.

> **Team Guide**: See `.claude/skills/python-standards/SKILL.md` for priority-ordered rules.
>
> | Priority | Category | Action |
> |----------|----------|--------|
> | 1 | Security | MUST FIX before merge |
> | 2 | Style & Readability | MUST ADHERE to standards |
> | 3 | Performance | SUGGESTED optimizations |

---

## Review Output Format

Always structure your review output exactly like this:

```markdown
## Review: [file or PR summary]
**Verdict**: CHANGES_REQUIRED | APPROVED

### Critical (must fix)
- [ ] `file.py:123` - [issue description]

### Important (should fix)
- [ ] `file.py:45` - [issue description]

### Suggestions (consider)
- [ ] `file.py:78` - [suggestion]

### What's Good
- [positive observations about the code]
```

---

## Review Checklist

### 1. Correctness

- Logic errors, off-by-one errors, wrong operators
- Edge cases: empty inputs, None, zero, negative values, very large inputs
- Race conditions in async/threaded code
- Resource leaks (files, connections, locks not properly closed)
- Exception handling: overly broad `except:`, swallowed errors without logging

### 2. Type Safety

```python
# Avoid - untyped public functions
def process(data):
    return data.get("key")

# Prefer - fully typed
def process(data: dict[str, Any]) -> str | None:
    return data.get("key")
```

Check for:

- Missing type hints on public APIs (functions, methods, class attributes)
- Use `X | None` instead of `Optional[X]` (modern syntax)
- Use `collections.abc` for abstract types (`Mapping`, `Sequence`, `Iterable`)
- Pydantic models: proper field types, validators where needed
- Generic types properly parameterized
- **Python 3.12+**: Use `class Foo[T]:` syntax for generics (not `TypeVar` + `Generic`)
- **Python 3.12+**: Use `type` keyword for type aliases
- **Python 3.12+**: Use `@override` decorator when overriding parent methods

### 3. Async Correctness

```python
# Common async mistakes
async def bad():
    time.sleep(1)           # Blocks the event loop!
    requests.get(url)       # Sync HTTP in async context
    data = fetch_data()     # Missing await on coroutine

# Correct async code
async def good():
    await asyncio.sleep(1)
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
```

Check for:

- Blocking calls inside async functions (`time.sleep`, `requests`, sync file I/O)
- Missing `await` on coroutines (causes "coroutine was never awaited")
- Improper task cancellation handling (not catching `CancelledError` where needed)
- `asyncio.gather()` without `return_exceptions=True` where failures should be collected
- anyio: proper cancel scope usage, not mixing asyncio primitives with anyio
- **Python 3.11+**: Prefer `asyncio.TaskGroup` over `asyncio.gather()` for structured concurrency
- **Python 3.11+**: Handle `ExceptionGroup` when using `TaskGroup` (use `except*` syntax)

### 4. Error Handling

```python
# Avoid - silent failures, broad exceptions
try:
    do_stuff()
except Exception:
    pass

# Prefer - specific exceptions, proper logging/re-raise
try:
    do_stuff()
except SpecificError as e:
    logger.warning("Operation failed for %s: %s", context, e)
    raise ServiceError("Failed to process") from e
```

Check for:

- Bare `except:` or `except Exception:` without re-raise
- Silent failures (exceptions caught but not logged or handled)
- Missing exception context when re-raising (use `raise X from e`)
- HTTP clients: explicit handling of timeouts, connection errors
- Missing finally blocks for cleanup when needed

### 5. Security

- **SQL Injection**: Only parameterized queries, never f-strings or string concatenation

  ```python
  # NEVER
  cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

  # ALWAYS
  cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
  ```

- **User Input**: Validate and sanitize all external input before use
- **Secrets**: No hardcoded API keys, passwords, tokens - use environment variables
- **Dangerous Functions**: Flag any usage of `pickle.loads()`, `eval()`, `exec()`, `yaml.load()` (use `safe_load`)
- **Path Traversal**: Validate file paths derived from user input, use `pathlib` and check for `..`
- **Multi-tenancy**: All queries must be scoped by `owner_id`

### 6. Performance

- **N+1 Queries**: Database calls inside loops - batch them instead

  ```python
  # N+1 problem
  for user_id in user_ids:
      user = db.get_user(user_id)

  # Batch query
  users = db.get_users(user_ids)
  ```

- **Unbounded Memory**: Loading entire large files or result sets into memory
- **Missing Database Indexes**: Queries filtering/sorting on non-indexed columns
- **Sync in Hot Paths**: Synchronous I/O operations in performance-critical code
- **Generator Opportunities**: Use generators/iterators for large sequences instead of lists

### 7. Code Structure & Quality

```python
# Avoid - too many parameters
def create_user(name, email, age, address, phone, role, dept, manager, start_date):
    ...

# Prefer - use dataclass or Pydantic model
@dataclass
class UserCreateRequest:
    name: str
    email: str
    role: str = "member"

def create_user(request: UserCreateRequest) -> User:
    ...
```

Check for:

- Functions longer than 50 lines - suggest splitting
- More than 4 parameters - suggest dataclass/Pydantic model
- Deep nesting (>3 levels) - suggest early returns or extracting functions
- Magic numbers/strings - should be named constants
- Duplicated code blocks - extract to function
- God classes doing too much - suggest splitting responsibilities

### 8. Python Idioms & Best Practices

```python
# Non-idiomatic Python
if len(items) > 0:
    pass
for i in range(len(items)):
    x = items[i]

# Idiomatic Python
if items:
    pass
for x in items:
    process(x)
```

Check for:

- Use `pathlib.Path` over `os.path` for path operations
- Use context managers (`with`) for resource management
- Use f-strings over `.format()` or `%` formatting
- Walrus operator where it improves clarity: `if (match := re.search(...)):`
- Dict merging: `merged = dict1 | dict2` (Python 3.9+)
- Use `enumerate()` when you need index and value
- Use `zip()` for parallel iteration
- List/dict/set comprehensions over manual loops where cleaner

### 9. Testing

- Public functions and methods should have corresponding tests
- Edge cases and error conditions covered in tests
- Mocking: not over-mocked - test real behavior when feasible
- Async tests: properly using `pytest-asyncio`, `@pytest.mark.asyncio`
- Fixtures: appropriate scope (function/class/module/session)
- Test isolation: tests don't depend on execution order

### 10. Documentation

- Public APIs: docstrings with clear description of args, returns, raises
- Complex logic: inline comments explaining *why*, not *what*
- Module-level docstrings for non-obvious modules
- Type hints reduce need for type documentation in docstrings
- README/docs updated if public interfaces changed

---

## Severity Classification

| Level | Symbol | Criteria | Blocks Merge? |
|-------|--------|----------|---------------|
| Critical | Red | Bugs, security vulnerabilities, data loss risks, crashes | **Yes** |
| Important | Yellow | Performance issues, missing types on public APIs, poor error handling, maintainability concerns | **Yes** |
| Suggestion | Green | Style improvements, minor refactors, nice-to-haves | No |

---

## Review Principles

1. **Be Specific**: Always include file name, line number, what's wrong, and how to fix it
2. **Explain Why**: Don't just cite rules - explain the reasoning and potential consequences
3. **Acknowledge Good Code**: Point out well-written parts, clever solutions, good patterns
4. **Consistent Standard**: Ask yourself "Would I approve this PR to merge to main?"
5. **Prioritize**: Focus on what matters most - don't nitpick when there are bigger issues
6. **Be Constructive**: Phrase feedback as suggestions, not attacks. We're improving code together.
