## Developer Guide: Database Abstraction Layer

**For contributors adding/modifying tools that touch the database.**

All database operations MUST go through the `StorageBackend` API (`storage/base.py`). Direct SQL via `_execute()` is prohibited in tool code.

### Canonical StorageBackend Methods

| Method | Purpose |
|--------|---------|
| `upsert_project(name, repo_root, progress_log_path, docs_json)` | Create/update project |
| `fetch_project(name)` | Get project by name |
| `list_projects()` | List all projects |
| `delete_project(name)` | Delete project |
| `update_project_docs(name, docs_json)` | Partial update - docs_json only |
| `insert_entry(...)` | Add log entry |
| `fetch_recent_entries(...)` | Get recent log entries |
| `query_entries(...)` | Search log entries |

### Why Use the API

Direct `_execute()` calls bypass:
- Write locking (`_write_lock`) - causes race conditions
- Initialization (`_initialise()`) - tables may not exist
- Backend abstraction - breaks Postgres support

### Correct Pattern

```python
# ❌ WRONG - Direct SQL
await backend._execute("UPDATE scribe_projects SET docs_json = ?", (json, name))

# ✅ CORRECT - Use API
await backend.update_project_docs(name, docs_json)
```

### Adding New Operations

If no API method exists for your operation:
1. Add abstract method to `storage/base.py`
2. Implement in `storage/sqlite.py`
3. Implement in `storage/postgres.py` (if applicable)
4. Call from tool code

---
