# Scribe MCP Quickstart

Use this as the minimal correct workflow for any session.

1) Activate project:
```python
set_project(name="<project_name>", root="<repo_root>")
```

2) Rehydrate context:
```python
read_recent(n=5)
```

3) Log start (required):
```python
append_entry(
  message="Starting <task>",
  status="info",
  agent="Codex",
  meta={"task": "<task>", "reasoning": {"why": "...", "what": "...", "how": "..."}}
)
```

4) Do work using tools:
- Use `manage_docs` for managed docs in `.scribe/docs/dev_plans/<project>/`.
- Use `read_file` for file reads (avoid shell reads).
- Use `append_entry` after each meaningful step.

5) Log completion:
```python
append_entry(
  message="Completed <task>: <summary>",
  status="success",
  agent="Codex",
  meta={"deliverables": [...], "confidence": 0.9, "reasoning": {"why": "...", "what": "...", "how": "..."}}
)
```
