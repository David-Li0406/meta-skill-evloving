**Skill**: [Implement Plan Engineering Standards](../SKILL.md)

# Error Handling Standards

Core principle: **Raise + propagate; no fallback/default/retry/silent**

---

## The Rule

When an error occurs, the code must:

1. **Raise** an exception with clear context
2. **Propagate** the error up the call stack
3. **Fail visibly** so the issue can be identified and fixed

---

## Forbidden Patterns

| Pattern                     | Why Forbidden                                 |
| --------------------------- | --------------------------------------------- |
| **Silent catch**            | Hides failures, causes debugging nightmares   |
| **Default values on error** | Masks real issues with fake data              |
| **Automatic retry**         | Hides intermittent failures, wastes resources |
| **Fallback to alternative** | Unclear which path executed, hard to debug    |

### Bad Examples

```python
# ❌ Silent catch
try:
    result = fetch_data()
except Exception:
    pass  # Error silently ignored

# ❌ Default on error
try:
    config = load_config()
except FileNotFoundError:
    config = {}  # Hides missing config

# ❌ Auto-retry
for _ in range(3):
    try:
        return api_call()
    except:
        time.sleep(1)
return None  # Silent failure after retries

# ❌ Fallback
try:
    return primary_service()
except:
    return backup_service()  # Which one ran? Unknown.
```

---

## Correct Patterns

```python
# ✅ Raise with context
def fetch_data(url: str) -> dict:
    response = requests.get(url)
    if response.status_code != 200:
        raise APIError(f"Failed to fetch {url}: {response.status_code}")
    return response.json()

# ✅ Propagate with additional context
def process_user(user_id: str) -> User:
    try:
        data = fetch_user_data(user_id)
    except APIError as e:
        raise ProcessingError(f"Cannot process user {user_id}") from e
    return User.from_dict(data)

# ✅ Let caller handle
def main():
    try:
        result = process_user("123")
    except ProcessingError as e:
        logger.error(f"User processing failed: {e}")
        sys.exit(1)  # Visible failure
```

---

## When Exceptions Are Appropriate

Errors should be raised for:

- **Invalid input** - Data that doesn't meet requirements
- **Missing resources** - Files, services, configs that must exist
- **API failures** - Network errors, unexpected responses
- **State violations** - Invariants that are broken

---

## Logging Before Raising

When raising, log the error with context:

```python
def connect_database(config: DBConfig) -> Connection:
    try:
        conn = create_connection(config.url)
    except ConnectionError as e:
        logger.error(f"Database connection failed: {config.url}", exc_info=True)
        raise DatabaseError(f"Cannot connect to database") from e
    return conn
```

---

## Rationale

This approach:

1. **Surfaces problems immediately** - No hidden failures
2. **Preserves error context** - Full stack trace available
3. **Simplifies debugging** - Error location is clear
4. **Forces explicit handling** - Callers must decide how to respond
