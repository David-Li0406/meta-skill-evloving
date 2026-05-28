# My Tool - AI Collaboration Guide

## Project Overview

My Tool is a CLI tool that [describe what it does].

**Tech Stack**: Python 3.10+, Click/argparse, Rich

## Architecture

```
Input → [Processing Stage] → Output
```

## Key Files

| File | Purpose |
|------|---------|
| `src/my_tool/cli.py` | Entry point, argument parsing |
| `src/my_tool/models.py` | Data structures (dataclasses) |
| `src/my_tool/processor.py` | Core business logic |
| `tests/conftest.py` | Shared test fixtures |

## Patterns

### The Triad
- **Doctor**: `cli.py:doctor()` checks dependencies
- **Safety Net**: TODO - implement undo log
- **Statekeeper**: TODO - implement checkpoints

### Conventions
- Type hints required on all functions
- Dataclasses for all data structures
- No raw dicts in function signatures

## Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=src/my_tool
```

## Common Tasks

### Adding a new command

1. Add subparser in `cli.py`
2. Create handler function
3. Add tests in `tests/test_cli.py`

### Adding a dependency check

Add to `cli.py:doctor()`:
```python
("binary-name", check_binary("binary-name")),
```
