# Root Cause Tracing

Bugs often manifest deep in the call stack. Your instinct is to fix where the error appears, but that's treating a symptom.

**Core principle:** Trace backward through the call chain until you find the original trigger, then fix at the source.

## When to Use

**Use when:**
- Error happens deep in execution (not at entry point)
- Stack trace shows long call chain
- Unclear where invalid data originated
- Need to find which test/code triggers the problem

## The Tracing Process

### 1. Observe the Symptom
```
subprocess.CalledProcessError: git init failed in /project/packages/core
```

### 2. Find Immediate Cause
What code directly causes this?
```python
subprocess.run(["git", "init"], cwd=project_dir, check=True)
```

### 3. Ask: What Called This?
```python
WorktreeManager.create_session_worktree(project_dir, session_id)
  -> called by Session.initialize_workspace()
  -> called by Session.create()
  -> called by test at Project.create()
```

### 4. Keep Tracing Up
What value was passed?
- `project_dir = Path("")` (empty!)
- Empty Path as `cwd` resolves to `Path.cwd()`
- That's the source code directory!

### 5. Find Original Trigger
Where did empty path come from?
```python
context = setup_test()  # Returns {"temp_dir": Path("")}
Project.create("name", context["temp_dir"])  # Accessed before setup!
```

## Adding Stack Traces

When you can't trace manually, add instrumentation:

```python
import traceback
import sys

def git_init(directory: Path) -> None:
    stack = "".join(traceback.format_stack())
    print(
        f"DEBUG git init: directory={directory}, cwd={os.getcwd()}",
        file=sys.stderr,
    )
    print(f"Stack:\n{stack}", file=sys.stderr)
    # ... proceed
```

**Critical:** Use `sys.stderr` in tests (stdout may be captured/suppressed)

**Run and capture:**
```bash
pytest 2>&1 | grep 'DEBUG git init'
```

**Analyze stack traces:**
- Look for test file names
- Find the line number triggering the call
- Identify the pattern (same test? same parameter?)

## Key Principle

```
Found immediate cause
  -> Can trace one level up?
    -> YES: Trace backwards, repeat
    -> NO: Fix at deepest traceable point + add defense-in-depth
  -> Is this the source?
    -> YES: Fix at source
    -> NO: Keep tracing
```

**NEVER fix just where the error appears.** Trace back to find the original trigger.

## Stack Trace Tips

- **In tests:** Use `sys.stderr`, not logger (may be suppressed)
- **Before operation:** Log before the dangerous operation, not after it fails
- **Include context:** Directory, cwd, environment variables, timestamps
- **Capture stack:** `traceback.format_stack()` shows complete call chain

## Python-Specific Patterns

### Using breakpoint for interactive tracing
```python
def suspicious_function(data):
    breakpoint()  # Drops into pdb
    # Inspect locals, up/down stack frames
```

### Rich tracebacks with locals
```python
import traceback

try:
    risky_operation()
except Exception:
    traceback.print_exc()
    # Or for programmatic access:
    # traceback.format_exception(*sys.exc_info())
```

### Logging with structlog for context
```python
import structlog

logger = structlog.get_logger()

def git_init(directory: Path) -> None:
    logger.debug(
        "git_init",
        directory=str(directory),
        cwd=os.getcwd(),
    )
```
