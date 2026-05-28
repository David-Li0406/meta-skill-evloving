# Shared Memory Patterns

write_to_memory(), read_relevant(), and coordination patterns.

## Writing to Memory

```python
self.write_to_memory(
    content=result,
    tags=["processing"],
    importance=0.9
)
```

## Reading from Memory

```python
insights = shared_pool.read_relevant(
    agent_id="analyst",
    tags=["research"],
    exclude_own=True,
    limit=5
)
```

## References
- **Specialist**: `.claude/agents/frameworks/kaizen-specialist.md` lines 94-113
- **UX Helpers**: `kaizen-ux-helpers.md`
