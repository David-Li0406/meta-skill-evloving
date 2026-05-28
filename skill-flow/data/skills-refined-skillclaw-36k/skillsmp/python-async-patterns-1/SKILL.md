---
name: python-async-patterns
description: Best practices for async Python code, avoiding common pitfalls like await precedence bugs and sync-in-async anti-patterns.
---

# Python Async Patterns Skill

Expert guidance on writing correct and performant async Python code. These patterns prevent common bugs discovered in code reviews.

## Activation

Use this skill when:

- Writing `async def` functions
- Working with asyncio event loops
- Integrating sync libraries in async code
- Defining type hints for async functions

---

## Critical Patterns

### 1. Await Precedence Bug

**Problem**: The comma operator has higher precedence than `await`.

```python
# ❌ WRONG - Returns (coroutine, value) instead of (result, value)
async def search(query: str) -> tuple[list, str]:
    return await repository.search(query), query  # BUG!

# ✅ CORRECT - Assign result first, then create tuple
async def search(query: str) -> tuple[list, str]:
    results = await repository.search(query)
    return results, query
```

**Rule**: Never use `await` inside a tuple literal. Always assign the awaited result to a variable first.

---

### 2. Sync-in-Async Anti-Pattern

**Problem**: Calling synchronous I/O inside async functions blocks the event loop.

```python
# ❌ WRONG - Blocks event loop
async def save_document(doc: Document) -> str:
    result = sync_client.insert(doc)  # BLOCKING!
    return result.id

# ✅ CORRECT - Wrap with asyncio.to_thread()
import asyncio

async def save_document(doc: Document) -> str:
    result = await asyncio.to_thread(
        lambda: sync_client.insert(doc)
    )
    return result.id
```

**Rule**: If using a sync library in async code, wrap calls with `asyncio.to_thread()`.

---

### 3. Type Hints for Async Functions

**Problem**: Return type doesn't match what the function actually returns.

```python
# ❌ WRONG - Says it returns List but actually returns tuple
async def search(query: str) -> List[Match]:
    results = await repo.search(query)
    return results, query  # Actually tuple!

# ✅ CORRECT - Accurate type hint
async def search(query: str) -> tuple[List[Match], str]:
    results = await repo.search(query)
    return results, query
```

**Rule**: Always verify return type matches the actual return value. Use `tuple[T1, T2]` for tuples.

---

### 4. Domain Exceptions Over Generic Exceptions

**Problem**: Generic exceptions lack context for debugging.

```python
# ❌ WRONG - No context
if not result.data:
    raise Exception("Failed to save")

# ✅ CORRECT - Rich context
from src.core.exceptions import DocumentSaveError

if not result.data:
    raise DocumentSaveError(
        cause="No data returned from insert",
        document_id=doc.id
    )
```

**Rule**: Create domain-specific exceptions that capture relevant context.

---

## Quick Reference

| Anti-Pattern               | Fix                                            |
| -------------------------- | ---------------------------------------------- |
| `return await foo(), bar`  | Assign first: `x = await foo(); return x, bar` |
| `sync_call()` in async     | Wrap: `await asyncio.to_thread(sync_call)`     |
| `-> List[T]` returns tuple | Fix: `-> tuple[List[T], str]`                  |
| `raise Exception(msg)`     | Use: `raise DomainError(context)`              |

---

## Related Files

- [exceptions.py](file:///home/franblakia/blakia/blakiaxhagalink/Hybrid-RAG-Agent/src/core/exceptions.py) - Domain exceptions
- [supabase_repository.py](file:///home/franblakia/blakia/blakiaxhagalink/Hybrid-RAG-Agent/src/infrastructure/database/supabase_repository.py) - Example async wrapper usage
