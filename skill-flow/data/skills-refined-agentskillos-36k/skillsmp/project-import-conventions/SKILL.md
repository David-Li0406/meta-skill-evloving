---
name: project-import-conventions
description: Import paths and test conventions for GUTTERS codebase. Critical for avoiding common errors with module resolution and test mocking.
---

# Project Import Conventions

This codebase has specific import patterns. Following them prevents debugging time waste.

## Import Path Rules

### From Project Root (tests, scripts, commands)
```python
# ALWAYS use src.app prefix
from src.app.models.user import User
from src.app.modules.registry import ModuleRegistry
from src.app.core.ai.llm_factory import get_llm
from src.app.api.v1.intelligence import router

# ⚠️ WARNING: Standardize to one format.
# If PYTHONPATH includes 'src', use 'from app...'
# Otherwise, use 'from src.app...'.
# GUTTERS preference: ALWAYS use 'src.app' for tests to avoid ambiguity.
```
```

### Within src/app (relative imports OK)
```

---

## Circular Dependencies

Circular dependencies occur when Module A imports B, and B imports A. This causes `AttributeError` during collection.

### 🚩 Detection
If you see `AttributeError: module 'x' has no attribute 'Y'` but you KNOW it exists, it's likely a circular import.

### ✅ Resolution: Deferred Imports
Move the import UNTIL it is needed (inside the method/function).

```python
# src/app/modules/intelligence/synthesis/synthesizer.py
class ProfileSynthesizer:
    async def synthesize_profile(self, user_id, db):
        # ❌ WRONG: Top-level import
        # results in circular dependency if ModuleRegistry imports synthesizer
        
        # ✅ CORRECT: Deferred import
        from ...registry import ModuleRegistry
        from .schemas import UnifiedProfile
        
        calculated = await ModuleRegistry.get_calculated_modules_for_user(user_id, db)
        ...
```

### ✅ Resolution: Explicit Mapper Configuration
When circular dependencies between models use string forward references (e.g., `User` <-> `ChatSession`), the SQLAlchemy registry must be explicitly initialized in tests.

```python
# tests/conftest.py
@pytest_asyncio.fixture(scope="session", autouse=True)
def configure_mappers_session():
    """Force SQLAlchemy to resolve all string references once definitions are collected."""
    from sqlalchemy.orm import configure_mappers
    configure_mappers()
```

---

---

## Test File Locations

### Module-Level Tests
```
src/app/modules/{layer}/{module}/tests/
├── __init__.py          # REQUIRED (empty is fine)
└── test_{module}.py
```

### Integration/E2E Tests
```
src/tests/integration/
├── __init__.py
└── test_{feature}_e2e.py
```

### Project Root Tests
```
tests/
├── conftest.py          # Fixtures using src.app imports
└── test_*.py

### conftest.py Shadowing Warning
⚠️ DO NOT shadow the `local_session` import from `src.app.core.db.database` with a module-level variable or fixture. Rename it for clarity:
```python
from src.app.core.db.database import local_session as async_session_maker
```
```

---

## Test Import Pattern

### In Test Files (ALWAYS use src.app)
```python
# ✅ CORRECT - Always use full path from project root
from src.app.modules.intelligence.synthesis import ProfileSynthesizer
from src.app.modules.registry import ModuleRegistry

# ❌ WRONG - Will fail with "No module named 'app'"
from app.modules.intelligence.synthesis import ProfileSynthesizer
```

### Running Tests
```bash
# From project root (c:\dev\FastAPI-boilerplate)
pytest src/app/modules/tests/test_registry.py -v

# NOT from src/ directory!
```

---

## Test Mocking Patterns

### Mocking Factory Functions (CORRECT)
```python
from unittest.mock import patch, MagicMock, AsyncMock

@pytest.mark.asyncio
async def test_with_mocked_llm():
    """Patch factory at module import location."""
    from src.app.modules.intelligence.query import QueryEngine
    
    # Create mock LLM
    mock_llm = MagicMock()
    mock_llm.ainvoke = AsyncMock(return_value=MagicMock(
        content='["astrology", "human_design"]'
    ))
    
    # Patch where it's IMPORTED, not where it's DEFINED
    with patch('src.app.modules.intelligence.query.engine.get_llm', 
               return_value=mock_llm):
        engine = QueryEngine()  # Create INSIDE the patch
        result = await engine._classify_question("test", "trace")
        assert "astrology" in result
```

### Common Mocking Mistakes
```python
# ❌ WRONG - Patching object attribute (property doesn't exist yet)
engine = QueryEngine()
with patch.object(engine, 'llm') as mock_llm:  # KeyError!
    ...

# ❌ WRONG - Patching at definition location
# ❌ WRONG (Naive) - `datetime.utcnow()` is BANNED
# ✅ CORRECT (Aware) - `dt.datetime.now(dt.timezone.utc)`
    ...

# ✅ CORRECT - Patch at import location
with patch('src.app.modules.intelligence.query.engine.get_llm', ...):
    ...
```

### Mocking Registry
```python
@pytest.mark.asyncio
async def test_with_mocked_registry():
    with patch('src.app.modules.intelligence.synthesis.synthesizer.ModuleRegistry') as mock_reg:
        mock_reg.get_calculated_modules_for_user = AsyncMock(return_value=["astrology"])
        mock_reg.get_user_profile_data = AsyncMock(return_value={"sun": "Leo"})
        
        synthesizer = ProfileSynthesizer()
        result = await synthesizer.synthesize_profile(1, mock_db)
```

---

## Conftest Pattern

### tests/conftest.py
```python
from src.app.core.config import settings
from src.app.main import app

# Note: uses src.app imports
```

### Module-Level conftest.py
```python
# src/app/modules/intelligence/synthesis/tests/conftest.py
import pytest
from unittest.mock import AsyncMock

@pytest_asyncio.fixture
async def mock_db():
    """Mock async database session."""
    return AsyncMock()

# ALWAYS use @pytest_asyncio.fixture for async fixtures to ensure they are handled by the event loop.
```

---

## Common Errors and Fixes

### ModuleNotFoundError: No module named 'app'
**Cause:** Using `from app.` instead of `from src.app.`
**Fix:** Always use `src.app.` prefix in test files

### KeyError when patching object
**Cause:** Trying to patch a property on an instance
**Fix:** Patch the factory function at import location

### Tests pass locally but fail in CI
**Cause:** Running from wrong directory
**Fix:** Always run pytest from project root

---

## Quick Reference

| Context | Import Pattern |
|---------|----------------|
| Test files | `from src.app.modules...` |
| Within module | Relative `from .schemas import...` |
| scripts/ | `from src.app...` |
| Conftest | `from src.app...` |

| What to Mock | Where to Patch |
|--------------|----------------|
| `get_llm` in synthesizer | `src.app.modules.intelligence.synthesis.synthesizer.get_llm` |
| `get_llm` in engine | `src.app.modules.intelligence.query.engine.get_llm` |
| ModuleRegistry | `src.app.modules.{module}.{file}.ModuleRegistry` |
