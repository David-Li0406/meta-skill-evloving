---
name: writing-code
description: ALWAYS use when writing or refactoring code. Loads foundational sub-skills and enforces engineering principles for correctness, maintainability, and clarity.
---

# Writing Code

## Overview

Writing code succeeds when we ensure correctness, readability, and maintainability. This skill enforces foundational engineering principles and coordinates sub-skills for specific contexts. The goal: code that is correct by construction, not by accident.

## Required Sub-Skills

Always load these when writing or refactoring code:

| Skill | Purpose |
|-------|---------|
| [defensive-coding](../defensive-coding/SKILL.md) | Multi-layer validation, observability, exception handling |
| [designing-software](../designing-software/SKILL.md) | Property discovery, architecture decisions, SOLID principles |
| [howto-program-functionally-ish](../howto-program-functionally-ish/SKILL.md) | Separate pure logic from side effects (Gather → Process → Persist) |

## Conditional Sub-Skills

Load these when the context applies:

| Skill | When to Load |
|-------|--------------|
| [howto-code-in-python](../howto-code-in-python/SKILL.md) | Writing or reviewing Python code |
| [writing-useful-tests](../writing-useful-tests/SKILL.md) | Writing tests, reviewing test code, discussing testing strategy |

## Core Engineering Principles

### Correctness Over Convenience

**Model the complete problem space.** Shortcuts create bugs. Edge cases ignored during development become incidents in production.

- Plan for all states, including error states
- Handle all edge cases explicitly
- Use type systems to make invalid states unrepresentable
- Catch issues as early as possible — compile time beats runtime, runtime beats production

```python
# Good — type system prevents invalid states
@dataclass
class OrderStatus:
    pass

@dataclass
class Pending(OrderStatus):
    created_at: datetime

@dataclass
class Shipped(OrderStatus):
    shipped_at: datetime
    tracking_number: str  # Required for shipped orders

@dataclass
class Cancelled(OrderStatus):
    cancelled_at: datetime
    reason: str  # Required for cancellations
```

```python
# Bad — stringly-typed, invalid states possible
@dataclass
class Order:
    status: str  # "pending", "shipped", "cancelled"
    tracking_number: str | None  # Can be None even when shipped
    cancellation_reason: str | None  # Can be None even when cancelled
```

### Never Assume

**Verify, don't guess.** When uncertain about requirements, existing code, or system behavior:

- Ask clarifying questions rather than making assumptions
- Explore the codebase to understand existing patterns
- Iterate with feedback rather than building in isolation
- Document assumptions explicitly when they must be made

### Never Simplify Error Handling

**Errors are information.** Obscuring or glossing over errors makes debugging impossible.

- Preserve error context through exception chaining
- Use specific exception types, not generic ones
- Never swallow exceptions silently
- Log errors with sufficient context for diagnosis

```python
# Good — preserves context, specific exception
try:
    config = load_config(path)
except FileNotFoundError as e:
    raise ConfigurationError(f"Config file missing: {path}") from e

# Bad — loses context, generic handling
try:
    config = load_config(path)
except Exception:
    config = {}  # Silently use defaults, hide the real problem
```

### Never Use `Any` to Escape Type Checking

**Type systems exist to catch bugs.** Using `Any` (Python), `any` (TypeScript), or equivalent types to bypass difficult type-checking decisions defeats the purpose.

- If a type is genuinely dynamic, model it explicitly (unions, generics, protocols)
- If the type system is fighting you, the design may need reconsideration
- `Any` is acceptable only at true system boundaries (e.g., parsing arbitrary JSON from external APIs)

```python
# Good — explicit union for dynamic content
def parse_response(data: dict[str, str | int | list[str]]) -> Response: ...

# Good — generic for reusable containers
def first[T](items: list[T]) -> T | None: ...

# Bad — Any to avoid thinking about types
def process(data: Any) -> Any: ...
```

### Build Incrementally

**Small, composable pieces.** Large monolithic implementations are hard to test, hard to debug, and hard to change.

- Build and verify in small increments
- Each piece should be independently testable
- Compose complex behavior from simple, well-tested parts
- Prefer explicit composition over implicit coupling

### Never Abstract Early

**Wait for patterns to emerge.** Premature abstraction creates complexity without benefit.

- Prefer some duplication over the wrong abstraction
- Abstract after three similar implementations, not before
- If an abstraction doesn't simplify, remove it
- The right time to abstract is when duplication causes maintenance pain

```python
# Good — concrete implementations, duplication is fine for now
def process_user_created_event(event: UserCreatedEvent) -> None:
    logger.info("user_created", user_id=event.user_id)
    db.insert_user(event.user_id, event.email)
    email_service.send_welcome(event.email)

def process_order_placed_event(event: OrderPlacedEvent) -> None:
    logger.info("order_placed", order_id=event.order_id)
    db.insert_order(event.order_id, event.items)
    email_service.send_confirmation(event.customer_email)

# Bad — premature abstraction before patterns are clear
class EventProcessor(ABC):
    @abstractmethod
    def extract_id(self, event: Event) -> str: ...
    @abstractmethod
    def persist(self, event: Event) -> None: ...
    @abstractmethod
    def notify(self, event: Event) -> None: ...

    def process(self, event: Event) -> None:
        logger.info(self.event_type, id=self.extract_id(event))
        self.persist(event)
        self.notify(event)
```

### Document Non-Obvious Decisions

**Rationale matters.** When making difficult or non-obvious decisions, document:

- What decision was made
- Why it was made (alternatives considered, constraints)
- When it might need revisiting

```python
# Good — documents the non-obvious choice
# We use a list instead of a set here because:
# 1. Order of insertion matters for display
# 2. Items may contain unhashable nested structures
# 3. Typical size is <10 items, so O(n) lookup is acceptable
recent_items: list[Item] = []
```

## File Organization

### Descriptive Filenames Over Generic Utilities

**Name files by purpose, not category.** Generic utility files become dumping grounds.

| Avoid | Prefer |
|-------|--------|
| `utils.py` | `string_formatting.py` |
| `helpers.py` | `date_arithmetic.py` |
| `common.py` | `api_error_handling.py` |
| `misc.py` | `user_validation.py` |

**Why this matters:**
- Discoverability — find code by scanning filenames
- Cohesion — related code stays together
- Prevents bloat — no 2000-line utils files
- Clear imports — `from user_validation import validate_email`

### Organize Around Components

Modules should map to logical components, not technical layers.

```
# Good — organized by component
order_processing/
├── orders.py           # Order domain logic
├── pricing.py          # Price calculations
├── validation.py       # Order validation
└── notifications.py    # Order notifications

# Bad — organized by technical layer
order_processing/
├── models.py           # All models
├── utils.py            # All utilities
├── services.py         # All services
└── validators.py       # All validators
```

## Red Flags

Warning signs that code needs attention:

- [ ] `Any` or equivalent used to bypass type checking
- [ ] Bare `except:` or `except Exception: pass`
- [ ] `utils.py` or `helpers.py` exceeding 200 lines
- [ ] Business logic mixed with I/O operations
- [ ] Error messages that don't include relevant context
- [ ] Assumptions about input without validation
- [ ] Single-use abstractions or premature generalization
- [ ] Missing type annotations on public functions
- [ ] Platform-specific code mixed with cross-platform logic

## Common Mistakes

| Mistake | Why It Fails | Correct Approach |
|---------|--------------|------------------|
| Using `Any` to fix type errors | Hides bugs the type system would catch | Model the type explicitly |
| Catching generic exceptions | Masks unexpected errors, makes debugging impossible | Catch specific exceptions |
| "Utils" files | Become unmaintainable dumping grounds | Name files by purpose |
| Early abstraction | Wrong abstraction is worse than duplication | Wait for three use cases |
| Assumptions about input | Invalid data causes bugs deep in call stack | Validate at entry points |
| Swallowing errors | Silent failures are impossible to diagnose | Log and re-raise, or handle explicitly |
| Building in isolation | Misunderstanding requirements wastes effort | Iterate with feedback |
| Skipping type annotations | Lose compile-time bug detection | Annotate public interfaces |
| Technical-layer organization | Code for one feature spread across files | Organize by component |

## Anti-Rationalizations

- "I'll handle that edge case later" — You will not. Handle it now or document it as a known limitation.
- "The type system is too strict" — The type system is catching a bug. Fix the design.
- "It's just a small shortcut" — Shortcuts compound. The "small" ones cause production incidents.
- "I'll refactor when I have time" — You won't have time. Refactor now while context is fresh.
- "This abstraction will be useful later" — Build for current requirements. Abstract when patterns emerge.
- "Error handling clutters the code" — Error handling IS the code. The happy path is the easy part.
- "I know how this system works" — Verify anyway. Systems change, memory fades, edge cases hide.

## Summary

1. **Model the complete space.** Handle all edge cases; use types to make invalid states unrepresentable.
2. **Never assume.** Explore, ask questions, iterate — verify before building.
3. **Preserve error context.** Never swallow exceptions; errors are information.
4. **Avoid `Any`.** If the type system is fighting you, reconsider the design.
5. **Abstract after three.** Duplication is better than the wrong abstraction.
6. **Name files by purpose.** No `utils.py`; use `user_validation.py`.
