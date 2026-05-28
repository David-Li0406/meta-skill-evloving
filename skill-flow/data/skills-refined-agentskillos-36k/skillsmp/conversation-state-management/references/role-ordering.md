# Role Ordering

Message role validation logic and edge cases for LLM conversation management.

---

## Role Ordering Rules

### Valid Roles

| Role | Purpose | Position |
|------|---------|----------|
| `system` | Set AI behavior, personality, constraints | First message only |
| `user` | Human input | After system or assistant |
| `assistant` | AI response | After user |

### Sequence Rules

```
┌─────────────────────────────────────────────────────────┐
│ Optional: system (position 0 only, max 1)               │
├─────────────────────────────────────────────────────────┤
│ user                                                     │
│ assistant                                                │
│ user                                                     │
│ assistant                                                │
│ ... (strict alternation)                                │
└─────────────────────────────────────────────────────────┘
```

### Constraints

1. **System message**: Only at start (index 0), maximum one
2. **After system**: Must be `user`
3. **After user**: Must be `assistant`
4. **After assistant**: Must be `user`
5. **No consecutive same-role**: Two users or two assistants in a row is invalid

---

## Validation Implementation

### Core Validator

```python
from typing import Literal

Role = Literal["system", "user", "assistant"]


def validate_role_sequence(
    existing_roles: list[str],
    new_role: Role
) -> bool:
    """
    Check if new_role can be added after existing_roles.

    Args:
        existing_roles: List of roles in order (can be empty)
        new_role: Role to add

    Returns:
        True if valid, False otherwise
    """
    # Empty conversation: system or user allowed
    if not existing_roles:
        return new_role in ("system", "user")

    last_role = existing_roles[-1]

    # System only allowed at start
    if new_role == "system":
        return False

    # After system, must be user
    if last_role == "system":
        return new_role == "user"

    # Strict alternation after that
    if last_role == "user":
        return new_role == "assistant"

    if last_role == "assistant":
        return new_role == "user"

    return False
```

### With Custom Error Messages

```python
class RoleOrderingError(Exception):
    """Raised when message role violates ordering rules."""

    def __init__(self, message: str, last_role: str, attempted_role: str):
        super().__init__(message)
        self.last_role = last_role
        self.attempted_role = attempted_role


def validate_and_raise(
    existing_roles: list[str],
    new_role: str
) -> None:
    """Validate role sequence, raise descriptive error if invalid."""

    if not existing_roles:
        if new_role not in ("system", "user"):
            raise RoleOrderingError(
                f"First message must be 'system' or 'user', got '{new_role}'",
                last_role="none",
                attempted_role=new_role
            )
        return

    last_role = existing_roles[-1]

    if new_role == "system":
        raise RoleOrderingError(
            "System message can only appear at the start of conversation",
            last_role=last_role,
            attempted_role=new_role
        )

    if last_role == "system" and new_role != "user":
        raise RoleOrderingError(
            f"After system message, next must be 'user', got '{new_role}'",
            last_role=last_role,
            attempted_role=new_role
        )

    if last_role == "user" and new_role != "assistant":
        raise RoleOrderingError(
            f"After user message, next must be 'assistant', got '{new_role}'",
            last_role=last_role,
            attempted_role=new_role
        )

    if last_role == "assistant" and new_role != "user":
        raise RoleOrderingError(
            f"After assistant message, next must be 'user', got '{new_role}'",
            last_role=last_role,
            attempted_role=new_role
        )
```

---

## Edge Cases

### Case 1: Empty Conversation

```python
# Valid
validate_role_sequence([], "system")  # True - system at start
validate_role_sequence([], "user")    # True - can start with user

# Invalid
validate_role_sequence([], "assistant")  # False - can't start with assistant
```

### Case 2: Multiple System Messages

```python
# Invalid - only one system message allowed
validate_role_sequence(["system", "user", "assistant"], "system")  # False
```

### Case 3: System After Other Messages

```python
# Invalid - system only at position 0
validate_role_sequence(["user"], "system")  # False
validate_role_sequence(["user", "assistant"], "system")  # False
```

### Case 4: Consecutive Same Role

```python
# Invalid - no consecutive same roles
validate_role_sequence(["user"], "user")  # False
validate_role_sequence(["system", "user", "assistant"], "assistant")  # False
```

### Case 5: Valid Sequences

```python
# All valid
validate_role_sequence([], "user")  # True
validate_role_sequence(["user"], "assistant")  # True
validate_role_sequence(["user", "assistant"], "user")  # True
validate_role_sequence(["system"], "user")  # True
validate_role_sequence(["system", "user"], "assistant")  # True
```

---

## State Machine Representation

```
                    ┌─────────────┐
                    │    START    │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │ system     │ user       │
              ▼            │            │
        ┌─────────┐        │            │
        │ SYSTEM  │        │            │
        └────┬────┘        │            │
             │ user        │            │
             ▼             ▼            │
        ┌─────────────────────┐        │
        │        USER         │◄───────┘
        └──────────┬──────────┘
                   │ assistant
                   ▼
        ┌─────────────────────┐
        │     ASSISTANT       │
        └──────────┬──────────┘
                   │ user
                   └──────────────┐
                                  │
              ┌───────────────────┘
              ▼
        ┌─────────────────────┐
        │        USER         │ (loops back)
        └─────────────────────┘
```

---

## Database Constraint (Optional)

For additional integrity, add a database trigger:

```sql
-- PostgreSQL trigger to validate role ordering
CREATE OR REPLACE FUNCTION validate_message_role()
RETURNS TRIGGER AS $$
DECLARE
    last_role VARCHAR(20);
BEGIN
    -- Get the last message role for this conversation
    SELECT role INTO last_role
    FROM message
    WHERE conversation_id = NEW.conversation_id
    ORDER BY created_at DESC
    LIMIT 1;

    -- Empty conversation
    IF last_role IS NULL THEN
        IF NEW.role NOT IN ('system', 'user') THEN
            RAISE EXCEPTION 'First message must be system or user';
        END IF;
        RETURN NEW;
    END IF;

    -- System only at start
    IF NEW.role = 'system' THEN
        RAISE EXCEPTION 'System message can only be first';
    END IF;

    -- After system, must be user
    IF last_role = 'system' AND NEW.role != 'user' THEN
        RAISE EXCEPTION 'After system, next must be user';
    END IF;

    -- Alternation check
    IF last_role = 'user' AND NEW.role != 'assistant' THEN
        RAISE EXCEPTION 'After user, next must be assistant';
    END IF;

    IF last_role = 'assistant' AND NEW.role != 'user' THEN
        RAISE EXCEPTION 'After assistant, next must be user';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_message_role
    BEFORE INSERT ON message
    FOR EACH ROW
    EXECUTE FUNCTION validate_message_role();
```

**Note**: Application-level validation is preferred for better error messages. Use database trigger as a safety net only.

---

## Testing Role Validation

```python
import pytest
from app.crud.message import validate_role_sequence, RoleOrderingError


class TestRoleOrdering:
    """Test suite for role ordering validation."""

    def test_empty_conversation_allows_system(self):
        assert validate_role_sequence([], "system") is True

    def test_empty_conversation_allows_user(self):
        assert validate_role_sequence([], "user") is True

    def test_empty_conversation_rejects_assistant(self):
        assert validate_role_sequence([], "assistant") is False

    def test_system_only_at_start(self):
        assert validate_role_sequence(["user"], "system") is False
        assert validate_role_sequence(["user", "assistant"], "system") is False

    def test_after_system_must_be_user(self):
        assert validate_role_sequence(["system"], "user") is True
        assert validate_role_sequence(["system"], "assistant") is False

    def test_alternation_user_to_assistant(self):
        assert validate_role_sequence(["user"], "assistant") is True
        assert validate_role_sequence(["user"], "user") is False

    def test_alternation_assistant_to_user(self):
        assert validate_role_sequence(["user", "assistant"], "user") is True
        assert validate_role_sequence(["user", "assistant"], "assistant") is False

    def test_long_valid_sequence(self):
        roles = ["system", "user", "assistant", "user", "assistant"]
        assert validate_role_sequence(roles, "user") is True

    def test_long_invalid_sequence(self):
        roles = ["system", "user", "assistant", "user", "assistant"]
        assert validate_role_sequence(roles, "assistant") is False
```

---

## API Error Response

When role validation fails, return 400 Bad Request:

```python
from fastapi import HTTPException
from app.crud.message import RoleOrderingError

@router.post("/{conversation_id}/messages")
async def create_message(conversation_id: str, data: MessageCreate, ...):
    try:
        message = add_message(...)
        return message
    except RoleOrderingError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "role_ordering_violation",
                "message": str(e),
                "last_role": e.last_role,
                "attempted_role": e.attempted_role
            }
        )
```
