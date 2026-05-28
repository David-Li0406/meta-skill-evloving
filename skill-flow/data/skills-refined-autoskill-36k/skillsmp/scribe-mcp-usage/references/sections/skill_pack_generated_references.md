## Skill Pack (Generated References)

This document is the **single source of truth** for the `scribe-mcp-usage` skill pack.

The skill build scripts extract specific sections from this file into modular reference docs so agents can find answers quickly without scrolling a 1k+ line guide.

### Skill Reference: quickstart

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

### Skill Reference: index

Use `read_file(mode="search")` against skill reference docs. Default `search_mode` is `regex`.

Common searches:
```python
# Doc registration (create/register/auto-register)
read_file(path="references/Scribe_Usage.md", mode="search", query=r"register_doc|register_existing|auto-registration|DOC_NOT_FOUND", context_lines=2)

# manage_docs actions and required params
read_file(path="references/Scribe_Usage.md", mode="search", query=r"### `manage_docs`|#### `create_doc`|#### `apply_patch`|#### `status_update`", context_lines=2)

# doc_name vs doc_category semantics
read_file(path="references/Scribe_Usage.md", mode="search", query=r"doc_name|doc_category", context_lines=2)

# read_file scope rules
read_file(path="references/Scribe_Usage.md", mode="search", query=r"allow_outside_repo|denylist|\\.codex/skills|\\.claude/skills", context_lines=2)

# tight search within a single top-level section (generated section pack)
read_file(path="references/sections/INDEX.md", mode="search", query=r"Document Editing|Documentation Management|read_file|manage_docs", context_lines=1)
```

### Skill Reference: modes

Project mode:
- Enter with `set_project(name, root=...)`.
- Use `append_entry`, `manage_docs`, `read_recent`, `query_entries`, `read_file`.

Sentinel mode:
- Do not call `set_project` in the session.
- Use `append_event` and sentinel case tools (`open_bug`, `open_security`, `link_fix`).

### Skill Reference: logging

Every `append_entry` must include a reasoning block:
```json
{"reasoning": {"why": "...", "what": "...", "how": "..."}}
```

Log after each meaningful step (every 2-3 edits or ~5 minutes) and after investigations, decisions, tests, errors, and completions.

### Skill Reference: doc_naming

`doc_name`:
- Unique document identifier and filename key.
- Used for registry keys and path resolution.

`doc_category`:
- Semantic classification only.
- Must not be used as a filename or registry key.

Registration rules:
- `create_doc` registers by default unless `metadata.register_doc=false`.
- Edit actions attempt auto-registration by `doc_name` when the resolved file exists.
- For non-standard `doc_name`, the fallback filename is `<DOC_NAME>.md` under the project's docs directory.

### Skill Reference: sentinel_cases

These tools are sentinel-only. Do not call `set_project()` in the session.

Create cases:
```python
open_bug(title="<short title>", symptoms="<symptoms + repro + expected vs actual>", affected_paths=["path/one", "path/two"])
open_security(title="<short title>", symptoms="<threat model + impact + repro>", affected_paths=["path/one", "path/two"])
```

Link fix artifacts:
```python
link_fix(case_id="BUG-YYYYMMDD-XXX", execution_id="<run id / CI id>", artifact_ref="<commit/PR/url>", landing_status="merged|shipped|staged|reverted|wip")
```

### Skill Reference: troubleshooting

`DOC_NOT_FOUND` in `manage_docs`:
- Meaning: `doc_name` is not registered and could not be auto-registered.
- Fix: standard docs → `generate_doc_templates`; custom docs → `create_doc`.

`read_file denied` / scope violations:
- Meaning: denylist hit, or outside allowlist without override.
- Fix: `.claude/skills` and `.codex/skills` are always allowed; otherwise pass `allow_outside_repo=true` (denylist still enforced).
