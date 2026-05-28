# Defense-in-Depth Validation

When you fix a bug caused by invalid data, adding validation at one place feels sufficient. But that single check can be bypassed by different code paths, refactoring, or mocks.

**Core principle:** Validate at EVERY layer data passes through. Make the bug structurally impossible.

## Why Multiple Layers

Single validation: "We fixed the bug"
Multiple layers: "We made the bug impossible"

Different layers catch different cases:
- Entry validation catches most bugs
- Business logic catches edge cases
- Environment guards prevent context-specific dangers
- Debug logging helps when other layers fail

## The Four Layers

### Layer 1: Entry Point Validation
Reject obviously invalid input at API boundary.

```python
def create_project(name: str, working_directory: Path) -> Project:
    if not working_directory:
        raise ValueError("working_directory cannot be empty")
    if not working_directory.exists():
        raise ValueError(f"working_directory does not exist: {working_directory}")
    if not working_directory.is_dir():
        raise ValueError(f"working_directory is not a directory: {working_directory}")
    # ... proceed
```

### Layer 2: Business Logic Validation
Ensure data makes sense for this operation.

```python
def initialize_workspace(project_dir: Path, session_id: str) -> Workspace:
    if not project_dir:
        raise ValueError("project_dir required for workspace initialization")
    # ... proceed
```

### Layer 3: Environment Guards
Prevent dangerous operations in specific contexts.

```python
def git_init(directory: Path) -> None:
    # In tests, refuse git init outside temp directories
    if os.environ.get("TESTING"):
        temp_dir = Path(tempfile.gettempdir()).resolve()
        if not directory.resolve().is_relative_to(temp_dir):
            raise RuntimeError(
                f"Refusing git init outside temp dir during tests: {directory}"
            )
    # ... proceed
```

### Layer 4: Debug Instrumentation
Capture context for forensics.

```python
import traceback
import logging

logger = logging.getLogger(__name__)

def git_init(directory: Path) -> None:
    logger.debug(
        "About to git init",
        extra={
            "directory": str(directory),
            "cwd": os.getcwd(),
            "stack": "".join(traceback.format_stack()),
        },
    )
    # ... proceed
```

## Applying the Pattern

When you find a bug:

1. **Trace the data flow** - Where does bad value originate? Where used?
2. **Map all checkpoints** - List every point data passes through
3. **Add validation at each layer** - Entry, business, environment, debug
4. **Test each layer** - Try to bypass layer 1, verify layer 2 catches it

## Key Insight

All four layers are necessary. During testing, each layer catches bugs the others miss:
- Different code paths bypass entry validation
- Mocks bypass business logic checks
- Edge cases on different platforms need environment guards
- Debug logging identifies structural misuse

**Don't stop at one validation point.** Add checks at every layer.
