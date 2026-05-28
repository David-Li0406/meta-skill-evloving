---
name: python-standards
description: Python 3.12+ coding standards and conventions (source of truth). Use when working on Python projects, implementing features, or reviewing code for standards compliance.
---

# Python Backend & MCP Team Guide

## What Is This Guide?

This is the **source of truth** for coding standards in Python backend and MCP server projects.

### Purpose

- Define **priority-ordered rules** that all code must follow
- Provide a **single reference** for both developers and reviewers
- Ensure **consistent quality** across the team

### How It Works

Rules are organized by priority:

| Priority | Category | Blocks Merge? | When to Fix |
|----------|----------|---------------|-------------|
| **1** | Security | Yes | MUST fix before merge |
| **2** | Style & Readability | Yes | MUST adhere to standards |
| **3** | Performance | No | SUGGESTED optimizations |

### Who Uses This Guide

- **Developers**: Reference when writing code to follow standards
- **Reviewers**: Use as checklist when reviewing PRs
- **AI Agents**: Both `python-developer` and `python-reviewer` skills reference this guide

### Related Files

```text
This guide (source of truth)
    ^                    ^
python-developer       python-reviewer
(coding patterns)      (review checklist)
```

---

## Priority 1: Security (MUST FIX)

Issues in this category **block merge**. They represent security vulnerabilities, data loss risks, or critical bugs.

| Rule | Principle | Developer Action |
|------|-----------|------------------|
| 1.1 | **Input Validation** | All user input must be sanitized and validated. Never trust external data. |
| 1.2 | **Secrets Management** | No hardcoded credentials, API keys, or tokens. Use environment variables or secret managers. Never log secrets. |
| 1.3 | **Dangerous Functions** | FORBIDDEN in production: dynamic code execution, `os.system()`, unsafe deserialization, `yaml.load()` (use `safe_load`), `assert` for validation. |
| 1.4 | **SQL Injection** | Only parameterized queries. Never use f-strings or string concatenation for SQL. |
| 1.5 | **Error Exposure** | Error messages must not expose sensitive system details, stack traces, or internal paths to users. |
| 1.6 | **Multi-tenancy** | All database queries must be scoped by `owner_id`. No cross-tenant data access. |
| 1.7 | **Path Traversal** | Validate file paths from user input. Use `pathlib` and reject paths containing `..`. |

### Security Examples

```python
# 1.4 SQL Injection
# NEVER
cursor.run(f"SELECT * FROM users WHERE id = {user_id}")

# ALWAYS
cursor.run("SELECT * FROM users WHERE id = %s", (user_id,))

# 1.6 Multi-tenancy
# NEVER
stmt = select(User).where(User.id == user_id)

# ALWAYS
stmt = select(User).where(User.id == user_id, User.owner_id == owner_id)
```

---

## Priority 2: Style & Readability (MUST ADHERE)

Issues in this category **should be fixed** before merge. They ensure code consistency and maintainability.

| Rule | Principle | Developer Action |
|------|-----------|------------------|
| 2.1 | **Formatting** | Use Ruff/Black formatting with 88 character line length. Run `make format` before commit. |
| 2.2 | **Naming** | `snake_case` for variables/functions, `CamelCase` for classes, `ALL_CAPS` for constants. |
| 2.3 | **Docstrings** | All public functions, methods, and classes must have docstrings describing purpose, args, returns, and raises. |
| 2.4 | **Imports** | Group imports: 1) Standard library, 2) Third-party, 3) Local. Use absolute imports. |
| 2.5 | **Type Hints** | All functions must have type hints. Use modern syntax: `X \| None` not `Optional[X]`, `dict[str, Any]` not `Dict[str, Any]`. |
| 2.6 | **Error Handling** | Catch specific exceptions only. No bare `except:` or `except Exception:` without re-raise. Use exception chaining (`raise X from e`). |
| 2.7 | **Function Size** | Functions should be under 50 lines. If longer, split into smaller functions. |
| 2.8 | **Parameters** | Maximum 4 parameters per function. Use dataclass or Pydantic model for more. |
| 2.9 | **Nesting** | Maximum 3 levels of nesting. Use early returns to reduce depth. |
| 2.10 | **TaskGroup** | Use `asyncio.TaskGroup` for structured concurrency (Python 3.11+). |
| 2.11 | **ExceptionGroups** | Use `except*` for handling ExceptionGroups from TaskGroup (Python 3.11+). |
| 2.12 | **Exception Notes** | Use `e.add_note()` to add context to exceptions (Python 3.11+). |
| 2.13 | **@override** | Use `@override` decorator when overriding parent methods (Python 3.12+). |
| 2.14 | **Generic Syntax** | Prefer `class Foo[T]:` syntax for generics (Python 3.12+). |
| 2.15 | **Type Aliases** | Use `type` keyword for type aliases (Python 3.12+). |
| 2.16 | **Typed kwargs** | Use `Unpack[TypedDict]` for typed `**kwargs` (Python 3.12+). |
| 2.17 | **Constants** | Extract repeated strings/magic numbers (appearing 2+ times) to a `constants.py` file. Exception: logging messages. |

### Style Examples

```python
# 2.5 Type Hints (Python 3.10+ style)
# Avoid
from typing import Optional, Dict, List
def process(data: Optional[Dict[str, Any]]) -> Optional[List[str]]:
    ...

# Prefer
def process(data: dict[str, Any] | None) -> list[str] | None:
    ...

# 2.6 Error Handling
# Avoid
try:
    do_stuff()
except Exception:
    pass

# Prefer
try:
    do_stuff()
except SpecificError as e:
    logger.error("Operation failed: %s", e)
    raise ServiceError("Failed to process") from e
```

---

## Priority 3: Performance (SUGGESTED)

Issues in this category are **recommendations**. They improve performance but don't block merge.

| Rule | Principle | Developer Action |
|------|-----------|------------------|
| 3.1 | **Complexity** | Avoid O(n^2) or worse when O(n) or O(n log n) solutions exist. Flag nested loops over large datasets. |
| 3.2 | **Comprehensions** | Prefer list/dict/set comprehensions over explicit loops where they improve readability. |
| 3.3 | **Resources** | Use `with` statements (context managers) for files, connections, locks, and other resources. |
| 3.4 | **N+1 Queries** | Never make database calls inside loops. Batch queries instead. |
| 3.5 | **Async Blocking** | No blocking calls (`time.sleep`, `requests`, sync file I/O) inside async functions. Use async alternatives. |
| 3.6 | **Generators** | Use generators/iterators for large sequences instead of loading everything into memory. |
| 3.7 | **Caching** | Consider caching for expensive computations or repeated external calls. |

### Performance Examples

```python
# 3.4 N+1 Queries
# Avoid
for user_id in user_ids:
    user = await db.get_user(user_id)  # N database calls

# Prefer
users = await db.get_users(user_ids)  # 1 database call

# 3.5 Async Blocking
# Avoid
async def fetch():
    time.sleep(1)  # Blocks event loop!
    response = requests.get(url)  # Sync HTTP

# Prefer
async def fetch():
    await asyncio.sleep(1)
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
```

---

## Python 3.11+ Features

### Exception Groups and `except*` (PEP 654)

```python
# Raise multiple exceptions together
raise ExceptionGroup("multiple errors", [
    ValueError("invalid value"),
    TypeError("wrong type"),
])

# Handle specific exception types from a group
try:
    async with asyncio.TaskGroup() as tg:
        tg.create_task(might_fail_1())
        tg.create_task(might_fail_2())
except* ValueError as e:
    print(f"Value errors: {e.exceptions}")
except* TypeError as e:
    print(f"Type errors: {e.exceptions}")

# Add notes to exceptions for context
try:
    process_data(data)
except ProcessingError as e:
    e.add_note(f"Processing failed for user_id={user_id}")
    raise
```

### asyncio.TaskGroup (Structured Concurrency)

```python
# Old style - error handling issues, tasks may leak
tasks = [asyncio.create_task(fetch(url)) for url in urls]
results = await asyncio.gather(*tasks, return_exceptions=True)

# Python 3.11+ style - proper cancellation and error handling
async with asyncio.TaskGroup() as tg:
    tasks = [tg.create_task(fetch(url)) for url in urls]
# All tasks complete when exiting
# If one fails, others are cancelled
# Errors raised as ExceptionGroup
```

### tomllib - Built-in TOML Parser

```python
import tomllib

# Read pyproject.toml
with open("pyproject.toml", "rb") as f:
    config = tomllib.load(f)

# Note: tomllib is read-only; use tomli-w for writing
```

---

## Python 3.12+ Features

### Type Parameter Syntax (PEP 695)

```python
# Old style (still valid)
from typing import TypeVar, Generic
T = TypeVar('T')
class Box(Generic[T]):
    def __init__(self, item: T) -> None:
        self.item = item

# Python 3.12+ style (preferred)
class Box[T]:
    def __init__(self, item: T) -> None:
        self.item = item

# Generic functions
def first[T](items: list[T]) -> T:
    return items[0]

# Type aliases with lazy evaluation
type Vector[T] = list[tuple[T, T]]
```

### @override Decorator (PEP 698)

```python
from typing import override

class Parent:
    def process(self) -> str:
        return "parent"

class Child(Parent):
    @override  # Type checker verifies this actually overrides
    def process(self) -> str:
        return "child"

    @override  # Error! 'handle' doesn't exist in Parent
    def handle(self) -> None:
        pass
```

### Improved F-Strings

```python
# Quote reuse now allowed
items = ["a", "b", "c"]
result = f"Items: {', '.join(items)}"  # Quotes inside f-string OK

# Multi-line expressions with comments
data = f"""Result: {
    compute_value()  # This comment is now allowed
}"""
```

### TypedDict for **kwargs (PEP 692)

```python
from typing import TypedDict, Unpack

class RequestOptions(TypedDict, total=False):
    timeout: float
    retries: int
    headers: dict[str, str]

def make_request(url: str, **kwargs: Unpack[RequestOptions]) -> Response:
    # kwargs is now typed with specific keys
    timeout = kwargs.get("timeout", 30.0)
    ...
```

---

## Modern Python Preferences

These are preferred patterns over legacy alternatives. Using modern idioms improves readability and safety.

### Path Operations: `pathlib` over `os.path`

```python
# Avoid - legacy os.path
import os
path = os.path.join(base_dir, "subdir", "file.txt")
if os.path.exists(path):
    with open(path) as f:
        content = f.read()
name = os.path.basename(path)
ext = os.path.splitext(path)[1]

# Prefer - pathlib.Path
from pathlib import Path
path = Path(base_dir) / "subdir" / "file.txt"
if path.exists():
    content = path.read_text()
name = path.name
ext = path.suffix
```

### String Formatting: f-strings over `.format()` and `%`

```python
# Avoid - legacy formatting
msg = "User %s has %d items" % (name, count)
msg = "User {} has {} items".format(name, count)

# Prefer - f-strings
msg = f"User {name} has {count} items"

# For logging, use lazy formatting (don't format until needed)
logger.info("User %s has %d items", name, count)  # OK for logging
```

### Type Hints: Modern syntax over typing module

```python
# Avoid - legacy typing imports
from typing import Optional, List, Dict, Union, Tuple

def process(
    items: List[str],
    config: Optional[Dict[str, Any]] = None
) -> Tuple[str, int]:
    ...

# Prefer - built-in generics (Python 3.9+) and union syntax (3.10+)
def process(
    items: list[str],
    config: dict[str, Any] | None = None
) -> tuple[str, int]:
    ...
```

### Collections: `collections.abc` for abstract types

```python
# Avoid - concrete types in signatures when not needed
def process(items: list[str]) -> dict[str, int]: ...

# Prefer - abstract types for input, concrete for output
from collections.abc import Iterable, Mapping, Sequence

def process(items: Iterable[str]) -> dict[str, int]: ...
def lookup(data: Mapping[str, Any]) -> str: ...
def get_slice(items: Sequence[T]) -> T: ...
```

### Context Managers: `with` for resource management

```python
# Avoid - manual resource management
f = open("file.txt")
try:
    content = f.read()
finally:
    f.close()

# Prefer - context manager
with open("file.txt") as f:
    content = f.read()

# For multiple resources
with (
    open("input.txt") as infile,
    open("output.txt", "w") as outfile,
):
    outfile.write(infile.read())
```

### Iteration: Use built-in helpers

```python
# Avoid - index-based iteration
for i in range(len(items)):
    print(i, items[i])

# Prefer - enumerate
for i, item in enumerate(items):
    print(i, item)

# Avoid - manual counter
count = 0
for item in items:
    if item.is_valid():
        count += 1

# Prefer - sum with generator
count = sum(1 for item in items if item.is_valid())

# Avoid - manual zipping
for i in range(len(list1)):
    process(list1[i], list2[i])

# Prefer - zip
for a, b in zip(list1, list2, strict=True):  # strict=True catches length mismatch
    process(a, b)
```

### Dict Operations: Modern syntax

```python
# Avoid - dict() constructor
config = dict(timeout=30, retries=3)

# Prefer - literal syntax
config = {"timeout": 30, "retries": 3}

# Avoid - .update() for merging
merged = base_config.copy()
merged.update(override_config)

# Prefer - union operator (Python 3.9+)
merged = base_config | override_config

# Avoid - manual get with default
value = d[key] if key in d else default

# Prefer - .get() or walrus
value = d.get(key, default)
```

### Structural Pattern Matching (Python 3.10+)

```python
# Avoid - nested if/elif chains
if isinstance(response, SuccessResponse):
    return response.data
elif isinstance(response, ErrorResponse):
    if response.code == 404:
        return None
    else:
        raise APIError(response.message)

# Prefer - match statement
match response:
    case SuccessResponse(data=data):
        return data
    case ErrorResponse(code=404):
        return None
    case ErrorResponse(message=msg):
        raise APIError(msg)
```

### Walrus Operator for Assignment Expressions

```python
# Avoid - separate assignment and check
match_result = re.search(pattern, text)
if match_result:
    process(match_result.group(1))

# Prefer - walrus operator
if match_result := re.search(pattern, text):
    process(match_result.group(1))

# Useful in while loops
while chunk := file.read(8192):
    process(chunk)
```

---

## Tech Stack Specific Rules

### Pydantic v2

- Use `model_config` instead of inner `Config` class
- Use `field_validator` decorator (not `validator`)
- Prefer `model_validate()` over `parse_obj()`

### FastAPI

- Always use dependency injection (`Depends()`) for shared resources
- Return proper HTTP status codes (201 for created, 404 for not found, etc.)
- Use response models to control output shape

### SQLAlchemy/SQLModel

- Always use async sessions with `asyncpg`
- Use `select()` statements, not legacy Query API
- Handle `scalar_one_or_none()` vs `scalars().all()` correctly

### LangGraph

**Message Content Extraction**:

When extracting text content from LangGraph/LangChain messages, **always use `.text`** with a fallback pattern. The `.content` attribute may return a list or dict, not a string.

```python
# CORRECT: Use .text with fallback for backwards compatibility
text = msg.text if hasattr(msg, "text") else str(msg.content)

# Or using getattr (preferred for conciseness)
content = getattr(result, "text", None) or str(result.content)

# AVOID: Direct .content access (may return list, not string)
text = msg.content  # ❌ Can be list[dict] or dict, not str
```

**Why this matters**: LangChain messages can have multimodal content (images, tool calls) stored as a list in `.content`. The `.text` property safely extracts only the text portion.

**State Management**:

- Prefer Pydantic models for state (over dataclass or TypedDict)
- Return partial dict with only changed fields - LangGraph handles merging
- State objects should be immutable (return new state, don't mutate)

```python
# Return only changed fields - LangGraph merges automatically
async def classify_intent(state: AgentState) -> dict[str, Any]:
    """Node: Classify user intent."""
    intent = await classifier.classify(state.messages[-1])
    return {"intent": intent}  # Only return what changed
```

**Node Functions**:

- Use verb-based naming: `classify_intent`, `fetch_data`, `format_response`
- Always async: `async def node_name(state: AgentState) -> dict[str, Any]:`
- Single responsibility - one task per node
- Keep nodes focused and testable

**Conditional Edges**:

- Must be pure functions (no side effects)
- Use contextual naming that describes the routing decision
- Return string keys that match node names

```python
def route_by_intent(state: AgentState) -> str:
    """Route to appropriate agent based on classified intent."""
    match state.intent:
        case "data":
            return "genie_agent"
        case "platform":
            return "platform_agent"
        case _:
            return "default_response"
```

**Error Handling**:

- Retry if the failure is transient and retry makes sense
- Otherwise, raise exception - outer layer catches and handles
- Don't silently swallow errors in nodes

**AG-UI Events**:

- Emit "thinking text" at end of each step for internal steps
- This provides visibility into agent progress for the UI

### MCP Server

**Tool Naming**:

- Use CRUD-style naming: `<action>_<resource>`
- Actions: `get`, `list`, `create`, `update`, `delete`
- Singular for single item: `get_bridge` returns one bridge
- Plural for collections: `get_bridges` returns list of bridges

```python
# Good naming
async def get_bridge(bridge_id: str) -> Bridge: ...
async def get_bridges(owner_id: str) -> list[Bridge]: ...
async def create_bridge(request: BridgeCreate) -> Bridge: ...
```

**Authentication**:

- Fail fast on auth errors with dedicated exception
- This triggers token refresh flow in the client
- Don't retry auth failures - let the caller handle refresh

```python
if response.status_code == 401:
    raise AuthenticationError("Token expired or invalid")
```

**Error Handling**:

- Log errors internally for debugging
- Raise exceptions for internal error propagation
- Return standard error format to external callers

**Tool Documentation (NumPy Style)**:

All MCP tools must have NumPy-style docstrings with these sections:

```python
async def get_bridge(bridge_id: str, owner_id: str) -> Bridge:
    """Get a bridge by its unique identifier.

    Parameters
    ----------
    bridge_id : str
        The unique identifier of the bridge.
    owner_id : str
        The owner ID for multi-tenancy scoping.

    Returns
    -------
    Bridge
        The bridge object with all its properties.

    Raises
    ------
    NotFoundError
        If no bridge exists with the given ID.
    AuthenticationError
        If the token is expired or invalid.

    Limitations
    -----------
    - Only returns bridges visible to the authenticated user
    - Bridge status may be cached for up to 30 seconds

    Examples
    --------
    >>> bridge = await get_bridge("br-123", "owner-456")
    >>> print(bridge.name)
    'Main Office Bridge'
    """
```

Docstring requirements:

- **All sections required**: Parameters, Returns, Raises
- **Examples**: Only for complex tools (e.g., `dict[str, Any]` params)
- **Limitations**: Document known limitations if applicable
- **Raises**: Document all possible errors

### Testing (pytest)

**Test Types Required**:

| Type | Scope | What to Mock |
|------|-------|--------------|
| Unit | Single function/class | External APIs, LLM, database |
| Integration | Multiple components | Nothing - test real interactions |
| E2E | Full system | Nothing - test real flows |

**Coverage Goals**:

- Target: High coverage across all codebase
- No hard threshold currently enforced
- Focus on critical paths and edge cases

**Mocking Rules**:

```python
# Unit tests - mock external dependencies
@pytest.mark.asyncio
async def test_classify_intent(mock_llm):
    mock_llm.return_value = "data"
    result = await classify_intent("show me sales data")
    assert result == "data"

# Integration tests - no mocks
@pytest.mark.asyncio
async def test_full_agent_flow(db_session):
    # Uses real database, real LLM calls
    result = await process_message(db_session, "hello")
    assert result.intent is not None
```

**Best Practices**:

- Mark async tests with `@pytest.mark.asyncio`
- Use fixtures for setup/teardown
- Test error cases, not just happy paths
- Isolate tests - no dependency on order

### Database (PostgreSQL + Flyway)

**Migration Naming**:

- Use Flyway naming convention: `V{version}__{description}.sql`
- Example: `V001__create_users_table.sql`, `V002__add_owner_id_column.sql`

**Transactions**:

- Use SQLAlchemy's session-level transactions
- Messages: commit immediately after each write
- Events: batch at end of operation

```python
# Messages - commit immediately
async def save_message(db: AsyncSession, message: Message) -> Message:
    db.add(message)
    await db.commit()
    await db.refresh(message)
    return message

# Events - batch at end
async def process_events(db: AsyncSession, events: list[Event]) -> None:
    for event in events:
        db.add(event)
    await db.commit()  # Single commit at end
```

**Data Versioning (Not Soft Delete)**:

- Don't use soft delete with `is_deleted` flag
- Create new row for updates, deactivate previous version
- Maintains full history and audit trail

```python
# Versioning pattern
async def update_instruction(
    db: AsyncSession,
    instruction_id: str,
    new_content: str
) -> Instruction:
    # Deactivate current version
    current = await get_instruction(db, instruction_id)
    current.is_active = False

    # Create new version
    new_version = Instruction(
        owner_id=current.owner_id,
        content=new_content,
        version=current.version + 1,
        is_active=True,
    )
    db.add(new_version)
    await db.commit()
    return new_version
```

### Logging (loguru)

**Log Levels**:

| Level | Use Case |
|-------|----------|
| `error` | Exceptions that need attention |
| `warning` | Non-fatal issues, fallbacks used |
| `debug` | Internal debugging, verbose output |
| `info` | User-visible information (no PII) |
| `success` | Milestone completions |

**Structured Logging**:

Always use `bind()` to include context fields:

```python
from loguru import logger

# Bind context at start of request/operation
log = logger.bind(
    thread_id=thread_id,
    run_id=run_id,
    user_id=user_id,
    owner_id=owner_id,
)

# Use throughout the operation
log.info("Processing user request")
log.debug("Classified intent: %s", intent)
log.success("Request completed successfully")
```

**Required Fields**:

- `thread_id`: Conversation thread identifier
- `run_id`: Current execution run
- `user_id`: User making the request
- `owner_id`: Tenant identifier

### Configuration

**Secrets (dotenv)**:

- Store in `.env` files (never commit to git)
- Use for: API keys, database passwords, tokens

```bash
# .env
DB_PASSWORD=secret123
OPENAI_API_KEY=sk-...
AWS_SECRET_ACCESS_KEY=...
```

**Application Config (pydantic-settings)**:

- Use `BaseSettings` for typed configuration
- Validates at startup, fails fast on missing values

```python
from pydantic_settings import BaseSettings

class DatabaseSettings(BaseSettings):
    host: str
    port: int = 5432
    name: str
    user: str
    password: str

    model_config = {"env_prefix": "DB_"}

class Settings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()
    debug: bool = False
```

**Environment Variable Naming**:

- No prefix for top-level settings
- Split into logical parts: `DB_HOST`, `DB_PORT`, `DB_NAME`
- Use underscores, not dots: `AWS_REGION` not `AWS.REGION`

### Git Workflow

**Branch Naming**:

- Format: `TICKET-type-description` (e.g., `CLDS-12345-feature-add-auth`)
- **No slashes** - causes deployment issues and clutters branch lists
- **Jira ticket required** - if no ticket, create one first
- Types: `feature`, `fix`, `docs`, `refactor`, `test`, `chore`, `perf`

```bash
# Correct format
CLDS-12345-feature-add-auth
CLDS-12345-fix-login-timeout
CLDS-12345-refactor-api-client

# Wrong - has slash
feature/CLDS-12345-add-auth  ❌

# Wrong - no ticket
feature-add-auth  ❌
```

**If no Jira ticket exists**: Create one before starting the branch:
```bash
acli jira workitem create --project "CLDS" --type "Task" --summary "Add user authentication"
```

**Commit Messages (Conventional Commits)**:

| Prefix | Use Case |
|--------|----------|
| `feat:` | New feature |
| `fix:` | Bug fix |
| `refactor:` | Code restructure (no behavior change) |
| `docs:` | Documentation only |
| `test:` | Adding or fixing tests |
| `chore:` | Maintenance, deps, config |

```bash
# Examples
feat: add user authentication endpoint
fix: resolve timeout in bridge connection
refactor: extract validation logic to helper
docs: update API documentation
test: add edge cases for intent classifier
chore: upgrade pydantic to v2.5
```

### Type Checking (ty)

**Tool**: `ty` (Rust-based type checker from Ruff team)

**Adoption Strategy**:

1. **Audit**: Run `ty` on codebase, document all issues
2. **Fix**: Address type errors incrementally
3. **Enforce**: Add to CI pipeline once clean

**Common Issues to Fix**:

- Missing type hints on public functions
- Overly wide types (`Any` where specific type exists)
- Incorrect `None` handling
- Incompatible return types

```bash
# Run type check
ty check src/

# Check specific file
ty check src/core/agents/wilibot.py
```

---

## Common Review Issues

These are the most frequently flagged issues in code reviews. Address them proactively:

| Issue | Priority | How to Avoid |
|-------|----------|--------------|
| Missing type hints | P2 | Add types to all public functions |
| Overly wide types (`Any`) | P2 | Use specific types where possible |
| Outdated docstrings | P2 | Update docstrings when changing code |
| Async race conditions | P1 | Use locks, proper task management |
| Old Python style | P2 | Use modern syntax (3.10+ features) |
| Poor test edge cases | P2 | Test empty, None, error conditions |
| Missing @override | P2 | Add to all overridden methods (3.12+) |
| Legacy generic syntax | P2 | Use `class Foo[T]:` syntax (3.12+) |

---

## PR Review Comment Workflow

When fixing PR review comments, follow this exact order for **EACH comment**:

### Fix Order

1. **Fix** - Make the code change
2. **Lint** - Run `make lint`
3. **Format** - Run `make format`
4. **Commit** - Commit the fix
5. **Reply** - Reply to the PR comment

### Reply Command

```bash
# Get repo info
OWNER=$(gh repo view --json owner -q '.owner.login')
REPO=$(gh repo view --json name -q '.name')

# Reply to a specific comment (always include signature)
gh api "repos/${OWNER}/${REPO}/pulls/${PR_NUMBER}/comments/${COMMENT_ID}/replies" \
  -f body="Fixed: [explanation of what was changed and why]

(by Claude Code)"
```

### Resolve Thread (after replying)

```bash
# Get the thread ID from the comment
THREAD_ID="PRRT_kwDO..."  # From GraphQL query

# Resolve the thread
gh api graphql -f query='
  mutation($threadId: ID!) {
    resolveReviewThread(input: {threadId: $threadId}) {
      thread { id isResolved }
    }
  }
' -f threadId="$THREAD_ID"
```

### Finding Comment IDs

```bash
# List all comments on a PR with their IDs
gh api "repos/${OWNER}/${REPO}/pulls/${PR_NUMBER}/comments" \
  --jq '.[] | {id, path, line, body}'
```

### Reply Format

**All replies must end with `(by Claude Code)` signature.**

**When fixed:**

```text
Fixed: Added input validation for user_id parameter to prevent SQL injection.

(by Claude Code)
```

**When no change needed (after asking user):**

```text
No change needed: This validation is already handled by the Pydantic model at the API boundary (see UserRequest in models.py).

(by Claude Code)
```

### Handling Disagreements

If a review comment seems incorrect or not applicable:

1. **Ask the user first** - Don't assume, clarify with the developer
2. **If user agrees no fix needed** - Reply explaining why
3. **If user wants fix anyway** - Implement the fix

---

## Quick Reference

| Priority | Category | Blocks Merge | Action |
|----------|----------|--------------|--------|
| 1 | Security | Yes | MUST FIX |
| 2 | Style | Yes | MUST ADHERE |
| 3 | Performance | No | SUGGESTED |

When reviewing, check Priority 1 issues first. If any exist, stop and request fixes before continuing.

### Fix Order (for each PR comment)

```text
Fix -> make lint -> make format -> git commit -> gh api reply
```
