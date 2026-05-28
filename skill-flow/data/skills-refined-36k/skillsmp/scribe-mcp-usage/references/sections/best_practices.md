## Best Practices

### 1. **Always Set Project First**
```python
await set_project(name="your-project")
# Now use other tools
```

### 2. **Use Structured Metadata**
```python
await append_entry(
    message="Fixed critical bug",
    status="success",
    meta={
        "component": "auth",
        "bug_id": "BUG-123",
        "tests_fixed": 5,
        "phase": "bugfix"
    }
)
```

### 3. **Log Meaningful Events**
- Code changes and why they were made
- Test results and failures
- Decisions and reasoning
- Bug discoveries and fixes
- Milestone completions

### 4. **Use Bulk Mode for Backfilling**
```python
# If you forget to log, use bulk mode immediately
await append_entry(items=[
    {"message": "Step 1 completed", "status": "success"},
    {"message": "Step 2 completed", "status": "success"},
    {"message": "Bug discovered", "status": "bug", "agent": "DebugBot"}
])
```

### 5. **Leverage Enhanced Search**
```python
# Cross-project learning
await query_entries(
    message="authentication pattern",
    search_scope="all_projects",
    document_types=["architecture", "progress"],
    relevance_threshold=0.9
)
```

---
