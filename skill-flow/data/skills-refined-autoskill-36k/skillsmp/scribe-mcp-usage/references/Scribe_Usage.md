# Scribe MCP Tool Usage Guide

This document provides comprehensive usage instructions for all available Scribe MCP tools, including required parameters, optional parameters, and practical examples.

## Update v2.1.1

- `apply_patch` now supports **structured mode** with compiler-generated unified diffs.
- Unified diffs are **compiler output only** (do not hand-craft).
- Optional `patch_source_hash` enforces stale-source protection for patches.
- Reminders teach: scaffold with `replace_section`, then prefer structured/line edits.
- New lifecycle actions: `normalize_headers`, `generate_toc`, `create_doc`, `validate_crosslinks`.
- Structural actions validate `doc_name` against the project registry; unknown docs fail with `DOC_NOT_FOUND`.
- `normalize_headers` now supports ATX headers with or without a space plus Setext (`====` / `----`), skipping fenced code blocks.
- `generate_toc` uses GitHub-style anchors (NFKD normalization, ASCII folding, emoji removal, punctuation collapse, de-dup suffixes).
- `create_doc` preserves multiline body content in metadata (`body`, `snippet`, `content`).
- `read_file` adds repo-scoped scan/chunk/page/search modes with provenance logging for every read (optional `allow_outside_repo` for approved external reads).
- `read_file` **Phase 5 enhancements**: Full signature extraction (types, defaults, return types), line ranges for all functions/classes/methods, method display under classes, structure filtering (`structure_filter` for regex-based class/function search), and structure pagination (`structure_page`, `structure_page_size`) for browsing large classes with 50+ methods.
- `scribe_doctor` provides environment readiness diagnostics (repo root, config, plugin status, vector readiness).
- `manage_docs` adds semantic search via `action="search"` with `search_mode="semantic"` and doc/log separation.
- Semantic search supports `project_slug`, `project_slugs`, `project_slug_prefix`, `doc_type`, `file_path`, `time_start/time_end`.
- Per-type defaults: `vector_search_doc_k` / `vector_search_log_k` (overrides via `doc_k` / `log_k`).
- Vector indexing uses registry-managed docs only; log/rotated-log files are excluded from doc indexing.
- `scripts/reindex_vector.py` supports `--rebuild` for clean index rebuilds, `--safe` for low-thread fallback, and `--wait-for-drain` to block until embeddings are written.

## Readable Output Formatting (v2.1.1+)

Scribe MCP tools support a `format` parameter that controls output rendering for agent readability.

### Format Options

| Format | Returns | Use Case |
|--------|---------|----------|
| `readable` (default) | `CallToolResult` with `TextContent` | Clean display in Claude Code with actual newlines |
| `structured` | Raw dict/JSON | Programmatic parsing, backward compatibility |
| `compact` | Minimal dict | Token conservation |
| `both` | `CallToolResult` + `structuredContent` | Future use when Issue #9962 is resolved |

### ANSI Color Policy

**Critical design decision for token conservation and agent experience:**

| Tool Type | ANSI Colors | Rationale |
|-----------|-------------|-----------|
| **High-frequency tools** (`append_entry`, `set_project`, confirmations) | **OFF (hardcoded)** | Called 10-30x/session; ANSI codes are visual clutter for agents |
| **Display-heavy tools** (`read_file`, `read_recent`, `query_entries`) | **Config-driven** | Called 1-5x/session; colors aid human scanning of large outputs |

**Config setting** (`.scribe/config/scribe.yaml`):
```yaml
use_ansi_colors: true  # Enable ANSI colors for display-heavy tools
```

### Implementation Pattern for Tool Authors

When adding readable format support to a new tool:

```python
# 1. Add format parameter to tool signature
async def my_tool(
    ...,
    format: str = "readable",  # readable (default), structured, compact
) -> Union[Dict[str, Any], str]:

# 2. Build response data as usual
response = {"ok": True, "data": ...}

# 3. Route through formatter at the end
return await default_formatter.finalize_tool_response(
    data=response,
    format=format,
    tool_name="my_tool"
)
```

**For high-frequency tools** (confirmations, logging):
```python
# In format_readable_my_tool():
USE_COLORS = False  # Hardcode OFF - no config check needed
```

**For display-heavy tools** (file content, log queries):
```python
# Uses self.USE_COLORS property which reads from config
if self.USE_COLORS:
    # Apply ANSI formatting
```

### Reasoning Block Display

The `append_entry` readable format parses `meta.reasoning` JSON and displays it as a tree:

```
Reasoning:
├─ Why: <decision context>
├─ What: <constraints and alternatives>
└─ How: <methodology and steps>
```

This makes the audit trail immediately scannable without parsing JSON.

### Conditional Sections

Readable formats only display sections when they contain data:
- **Reminders**: Only shown if `len(reminders) > 0`
- **Metadata**: Only shown if explicitly set and non-empty
- **Errors**: Formatted prominently with suggestions

---

## Quick Start (High Level)

Scribe tools follow a simple flow:

1. **Pick or create a project** with `set_project(...)` so the tool knows where to read/write.
2. **Use the tool for the job**:
   - `append_entry` for logging actions/results.
   - `manage_docs` for structured doc edits (sections, patches, ranges).
   - `read_recent` and `query_entries` for log retrieval/search.
3. **Check outputs** for `ok`, `error`, and any `parameter_healing` notes.

If you skip step 1, most tools will error because no active project context exists.

---

## Concurrent Agent Naming (Session Isolation)

**MCP Transport Limitation:** Session identity is `{repo_root}:{transport}:{agent_name}`. When multiple agents with the **same name** work on **different Scribe projects** within the **same repository** concurrently, sessions collide and logs may route incorrectly.

**Collision occurs when ALL match:**
- Same repository root
- Same MCP server process
- Same agent name

### Best Practice: Scoped Agent Names

For concurrent agents in the same repo, use task-scoped names:

```python
# ❌ COLLISION - same name, different projects
Task(prompt="...agent='CoderAgent'...")  # project: feature_x
Task(prompt="...agent='CoderAgent'...")  # project: bugfix_y → WRONG LOGS!

# ✅ SAFE - scoped names
Task(prompt="...agent='CoderAgent-FeatureX'...")  # project: feature_x
Task(prompt="...agent='CoderAgent-BugfixY'...")   # project: bugfix_y → CORRECT!
```

**Naming Format:** `{BaseAgent}-{TaskScope}` (e.g., `CoderAgent-AuthRefactor`)

**Review Agent:** Grades filed under base name (without scope) for consistent tracking.

**When NOT required:**
- Sequential dispatches (one agent at a time)
- Different repositories (different repo roots)
- Single agent switching projects (cache handles this)

---

## Skill Pack (Generated References)

This document is the **single source of truth** for the `scribe-mcp-usage` skill pack.

The skill build scripts extract specific sections from this file into modular reference docs so agents can find answers quickly without scrolling a 1k+ line guide.

### Skill Reference: quickstart

Use this as the minimal correct workflow for any session.

1) Activate project:
```python
set_project(agent="<agent_name>", name="<project_name>", root="<repo_root>")
```

2) Rehydrate context:
```python
read_recent(agent="<agent_name>", n=5)
```

3) Log start (required):
```python
append_entry(
  agent="Codex",
  message="Starting <task>",
  status="info",
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
  agent="Codex",
  message="Completed <task>: <summary>",
  status="success",
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

## Document Editing (manage_docs)

Scribe supports three document edit modes, in increasing precision order:

### 1. apply_patch (recommended; structured by default)
Describe intent and let Python compile a valid unified diff. This avoids manual diff errors.

- Intent-based edits (range, block, or section)
- `patch_mode` enum: `structured` (default) or `unified` (advanced)
- Compiler emits a valid diff; no hand-written hunks
- Idempotent behavior is easier to guarantee
- `replace_block` ignores fenced code blocks and fails on ambiguous anchors with a line list.

Example:
```json
{
  "action": "apply_patch",
  "doc_name": "architecture",
  "edit": {
    "type": "replace_range",
    "start_line": 1,
    "end_line": 1,
    "content": "# Architecture (Updated)\n"
  }
}
```

Block replacement example:
```json
{
  "action": "apply_patch",
  "doc_name": "architecture",
  "edit": {
    "type": "replace_block",
    "anchor": "**Solution Summary:**",
    "new_content": "**Solution Summary:** Updated summary here."
  }
}
```

Structured edit types:
- `replace_range`: swap explicit line ranges (body-relative).
- `replace_block`: replace from an anchor line to the next blank line; fails on ambiguous anchors.
- `replace_section`: legacy anchor-by-ID (scaffolding only).

Common structured errors:
- `DOC_NOT_FOUND`: doc key is not registered for the project.
- `STRUCTURED_EDIT_ANCHOR_NOT_FOUND`: anchor not found in body.
- `STRUCTURED_EDIT_ANCHOR_AMBIGUOUS`: anchor matched multiple lines; includes line list.
- `PATCH_MODE_CONFLICT`: `patch_mode` argument conflicts with metadata.

### YAML frontmatter (automatic)
All managed docs are expected to use YAML frontmatter. When a document is edited via `manage_docs`,
Scribe will automatically add frontmatter if missing and update `last_updated` on each edit.

Manual overrides are supported via `metadata.frontmatter` (merged into the frontmatter map).

Line numbers for `apply_patch` (structured mode) and `replace_range` are **body-relative** (frontmatter lines are excluded).
If a `doc_name` is not registered, edit actions attempt auto-registration first (file must exist or be creatable via templates); otherwise you get `DOC_NOT_FOUND`.

Example:
```json
{
  "action": "apply_patch",
  "doc_name": "architecture",
  "edit": { "type": "replace_range", "start_line": 12, "end_line": 12, "content": "..." },
  "metadata": {
    "frontmatter": {
      "status": "authoritative",
      "tags": ["scribe", "documentation"]
    }
  }
}
```

### 2. replace_range
Replace an explicit 1-based line range (inclusive).

```json
{
  "action": "replace_range",
  "doc_name": "architecture",
  "start_line": 12,
  "end_line": 15,
  "content": "replacement text\n"
}
```

### Checklist helper: list_checklist_items
Return checklist items with line numbers so you can feed replace_range without guessing.

```json
{
  "action": "list_checklist_items",
  "doc_name": "checklist",
  "metadata": { "text": "Phase 0 item", "case_sensitive": true }
}
```
The response includes `body_line_offset` and `file_line` for mapping body-relative lines back to the file.

### 3. apply_patch (unified diff mode, advanced)
Apply a unified diff generated by the diff compiler. Avoid hand-written diffs.

```json
{
  "action": "apply_patch",
  "doc_name": "architecture",
  "patch": "<compiler output>"
}
```
Note: `patch_mode` defaults to `"unified"` when `patch` is provided.

### 4. replace_section (legacy)
Replace content using HTML section markers (`<!-- ID: ... -->`). This is best suited for templates and scaffolding.

Note: New agents should prefer `apply_patch` (structured mode) or `replace_range` whenever possible.

### 5. normalize_headers (structure)
Normalizes markdown headers into canonical ATX form with numbering. This action is **body-only** and skips fenced code blocks.

Current support: ATX headers with or without a space after `#`, plus Setext headers (`====` for H1, `----` for H2). Output is canonical ATX and idempotent.

```json
{
  "action": "normalize_headers",
  "doc_name": "architecture"
}
```

### 6. generate_toc (derived)
Generates or replaces a table of contents between `<!-- TOC:start -->` / `<!-- TOC:end -->`. Inserted at top of body if missing.

Anchors match GitHub-style behavior (NFKD normalization, ASCII folding, emoji removal, punctuation collapse, whitespace to `-`, de-dup with `-1`).

```json
{
  "action": "generate_toc",
  "doc_name": "architecture"
}
```

### 7. create_doc (custom docs)
Creates a new document from plain content. Users do **not** supply Jinja; pass content/body/snippets/sections and optional frontmatter.
Multiline content in `metadata.body`/`metadata.snippet` is preserved as-is.

```json
{
  "action": "create_doc",
  "doc_name": "custom_doc",
  "metadata": {
    "doc_name": "release_brief_003",
    "doc_type": "release_brief",
    "body": "# Release Brief\nSummary details here.",
    "target_dir": ".scribe/docs/dev_plans/my_project/custom",
    "frontmatter": { "category": "release" },
    "register_doc": false
  }
}
```

### 8. validate_crosslinks (read-only)
Validates `related_docs` without writing. Optional anchor checks are controlled by `metadata.check_anchors=true`.

```json
{
  "action": "validate_crosslinks",
  "doc_name": "architecture",
  "metadata": { "check_anchors": true }
}
```

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Core Project Management](#core-project-management)
3. [Logging Operations](#logging-operations)
4. [Query and Analysis](#query-and-analysis)
5. [Documentation Management](#documentation-management)
6. [Log Maintenance](#log-maintenance)
7. [Project Cleanup](#project-cleanup)

---

## Prerequisites

### **IMPORTANT: Project Context Required**

Most Scribe tools require an active project context. Before using any tool, you MUST set a project:

```python
await set_project(agent="<agent_name>", name="your-project-name", root="<repo_root>")
```

**Failure to set a project first will result in errors like:**
- `"No project configured. Invoke set_project before using this tool."`
- `"No project configured. Invoke set_project before reading logs"`

---

## Core Project Management

### `set_project`
**Purpose**: Create/select a project and bootstrap documentation structure.

**Required Parameters:**
- `agent` (string): Agent identifier for session tracking and logging
- `name` (string): Project name (automatically normalized - hyphens, underscores, spaces all work)
- `root` (string): Project root directory (must be provided)

**Optional Parameters:**
- `progress_log` (string): Path to progress log file
- `defaults` (dict): Default settings for the project

**Project Name Normalization:**
Project names are automatically normalized to use underscores. You can use any of these formats:
- `"my-project"` → normalized to `"my_project"`
- `"my_project"` → kept as `"my_project"`
- `"My Project"` → normalized to `"my_project"`

This means all tools (`manage_docs`, `query_entries`, etc.) accept any format and resolve to the same project.

**Example Usage:**
```python
# Basic usage
await set_project(agent="Codex", name="my-project", root="/path/to/repo")

# With custom defaults
await set_project(
    agent="Codex",
    name="my-project",
    root="/path/to/repo",
    defaults={"emoji": "🧪"}
)
```

**Returns:**
```json
{
  "ok": true,
  "project": {
    "name": "my-project",
    "root": "/path/to/project",
    "progress_log": "/path/to/progress/log.md",
    "docs_dir": "/path/to/docs",
    "docs": {
      "architecture": "/path/to/ARCHITECTURE_GUIDE.md",
      "phase_plan": "/path/to/PHASE_PLAN.md",
      "checklist": "/path/to/CHECKLIST.md",
      "progress_log": "/path/to/PROGRESS_LOG.md"
    },
    "defaults": {"agent": "Scribe"},
    "author": "Scribe"
  }
}
```

### `get_project`
**Purpose**: Retrieve current active project context and configuration.

**Required Parameters:**
- `agent` (string): Agent identifier for session tracking

**Optional Parameters:**
- `project` (string): Optional project name override
- `format` (string): Output format - "readable", "structured", or "compact"
- `verbose` (bool): Include recent log entries if True

**Example Usage:**
```python
await get_project(agent="Codex")
```

**Returns:**
```json
{
  "ok": true,
  "project": {
    "name": "current-project",
    "root": "/path/to/project",
    "progress_log": "/path/to/log.md",
    "docs_dir": "/path/to/docs",
    "defaults": {"agent": "Scribe"},
    "author": "Scribe"
  }
}
```

### `list_projects`
**Purpose**: Discover available projects and their configurations.

**Required Parameters:**
- `agent` (string): Agent identifier for session tracking

**Optional Parameters:**
- `limit` (int, default: 5): Maximum number of projects to return
- `filter` (string): Filter projects by name (case-insensitive substring match)
- `root` (string): Filter projects by repo root path (exact match, path-normalized). Useful for bridge integrations that need to resolve workspace → project mappings.
- `compact` (bool): Use compact response format
- `fields` (list): Specific fields to include in response
- `include_test` (bool, default: false): Include test/temp projects
- `page` (int, default: 1): Page number for pagination
- `page_size` (int): Number of items per page

**Example Usage:**
```python
# Basic usage
await list_projects(agent="Codex")

# With pagination
await list_projects(agent="Codex", limit=10, page=1)

# Filtered by name
await list_projects(agent="Codex", filter="my-project", limit=3)

# Filtered by repo root (for bridge workspace resolution)
await list_projects(agent="Codex", root="/home/austin/projects/MCP_SPINE/council_mcp")
```

**Returns:**
```json
{
  "ok": true,
  "projects": [
    {
      "name": "project-name",
      "root": "/path/to/project",
      "progress_log": "/path/to/log.md"
    }
  ],
  "count": 1,
  "pagination": {
    "page": 1,
    "page_size": 5,
    "total_count": 10,
    "has_next": true,
    "has_prev": false
  }
}
```

---

## Logging Operations

### `append_entry`
**Purpose**: **PRIMARY TOOL** - Add structured log entries with metadata.

#### Single Entry Mode

**Required Parameters:**
- `agent` (string): Agent identifier for session tracking
- `message` (string): Log message content

**Optional Parameters:**
- `status` (string): Status type - "info", "success", "warn", "error", "bug", "plan"
- `emoji` (string): Custom emoji override
- `meta` (dict): Metadata dictionary for context
- `timestamp_utc` (string): Custom UTC timestamp
- `log_type` (string): Target log identifier (defaults to "progress")

**Example Usage:**
```python
# Basic entry
await append_entry(agent="Codex", message="Fixed authentication bug")

# With full context
await append_entry(
    agent="DebugBot",
    message="Fixed authentication bug",
    status="success",
    meta={"component": "auth", "tests_fixed": 5}
)

# Planning entry
await append_entry(
    agent="Codex",
    message="Beginning database migration phase",
    status="plan",
    emoji="🗄️",
    meta={"phase": "migration", "priority": "high"}
)
```

#### Bulk Entry Mode

**Required Parameters:**
- `agent` (string): Agent identifier for session tracking
- `items` (string or list): JSON string array or direct list of entry dictionaries

**Each Entry Requires:**
- `message` (string): Log message content

**Each Entry Optional:**
- `status`, `emoji`, `meta`, `timestamp_utc`, `log_type`

**Example Usage:**
```python
# As JSON string
await append_entry(agent="Codex", items=json.dumps([
  {"message": "First task completed", "status": "success"},
  {"message": "Bug found in auth module", "status": "bug"},
  {"message": "Database migration finished", "status": "info",
   "meta": {"component": "database", "phase": "deployment"}}
]))

# As direct list
await append_entry(agent="Codex", items=[
  {"message": "Code review completed", "status": "success"},
  {"message": "Tests passing", "status": "success", "meta": {"tests_run": 25}}
])
```

**Returns:**
```json
{
  "ok": true,
  "written_line": "[ℹ️] [2025-11-02 07:39:07 UTC] [Agent: AgentName] [Project: project] [ID: hash] Your message",
  "path": "/path/to/progress/log.md",
  "meta": {"log_type": "progress"}
}
```

---

## Query and Analysis

### `read_recent`
**Purpose**: Retrieve recent log entries with pagination.

**Required Parameters:**
- `agent` (string): Agent identifier for session tracking

**Optional Parameters:**
- `n` (int, default: 50): Number of recent entries to return
- `filter` (dict): Optional filters for agent, status, emoji
- `page` (int, default: 1): Page number for pagination
- `page_size` (int): Number of entries per page
- `compact` (bool): Use compact response format
- `fields` (list): Specific fields to include
- `include_metadata` (bool): Include metadata field in entries

**Example Usage:**
```python
# Basic usage
await read_recent(agent="Codex")

# Limited entries
await read_recent(agent="Codex", n=10)

# With filters
await read_recent(agent="Codex", n=5, filter={"agent": "DebugBot", "status": "success"})
```

**Returns:**
```json
{
  "ok": true,
  "entries": [
    {
      "id": "entry_id",
      "ts": "2025-11-02 07:39:07 UTC",
      "emoji": "ℹ️",
      "agent": "AgentName",
      "message": "Log message",
      "meta": {"log_type": "progress"},
      "raw_line": "Full log line"
    }
  ],
  "count": 1,
  "pagination": {
    "page": 1,
    "page_size": 50,
    "total_count": 1,
    "has_next": false,
    "has_prev": false
  }
}
```

### `query_entries`
**Purpose**: Advanced log searching and filtering.

**Required Parameters:**
- `agent` (string): Agent identifier for session tracking

**Optional Parameters:**
- `project` (string): Project name (uses active project if None)
- `start` (string): Start timestamp filter
- `end` (string): End timestamp filter
- `message` (string): Message text filter
- `message_mode` (string): How to match message - "substring", "regex", "exact"
- `case_sensitive` (bool): Case sensitive message matching
- `emoji` (string or list): Filter by emoji(s)
- `status` (string or list): Filter by status(es)
- `agents` (string or list): Filter by agent name(s)
- `meta_filters` (dict): Filter by metadata key/value pairs
- `limit` (int): Maximum results to return
- `page` (int): Page number for pagination
- `page_size` (int): Number of results per page

**Enhanced Search Parameters:**
- `search_scope`: "project", "global", "all_projects", "research", "bugs", "all"
- `document_types`: ["progress", "research", "architecture", "bugs", "global"]
- `relevance_threshold`: Minimum relevance score (0.0-1.0)
- `verify_code_references`: Check if mentioned code exists
- `time_range`: Temporal filtering ("last_30d", "last_7d", "today")

**Example Usage:**
```python
# Basic message search
await query_entries(agent="Codex", message="bug", message_mode="substring")

# Date range search
await query_entries(agent="Codex", start="2025-10-23", end="2025-10-24")

# Enhanced cross-project search
await query_entries(
    agent="Codex",
    message="authentication",
    search_scope="all_projects",
    document_types=["progress", "bugs"],
    relevance_threshold=0.8
)

# Metadata filtering
await query_entries(
    agent="Codex",
    meta_filters={"component": "auth", "severity": "high"}
)
```

**Returns:**
```json
{
  "ok": true,
  "entries": [/* matching entries */],
  "count": 5,
  "pagination": {/* pagination info */}
}
```

---

### `read_file`
**Purpose**: Repo-scoped file access (by default) with deterministic scan/chunk/page/search modes, dependency analysis, and read provenance logging. Optional out-of-repo reads are allowed when explicitly enabled.

**Required Parameters:**
- `agent` (string): Agent identifier for session tracking
- `path` (string): File path (absolute or repo-relative)

**Optional Parameters:**
- `mode`: `scan_only` (default), `chunk`, `line_range`, `page`, `full_stream`, `search`
- `chunk_index`: Chunk index or list of indices (for `chunk` mode)
- `start_line` / `end_line`: Explicit line range (for `line_range`)
- `page_number` / `page_size`: Pagination controls (for `page`)
- `start_chunk` / `max_chunks`: Streaming controls (for `full_stream`)
- `search`: Search term (for `search` mode)
- `query`: Alias for `search` (for `search` mode, defaults to smart inference)
- `search_mode`: `regex` (default) or `literal` - **Note: Default changed from literal to regex**
- `context_lines`: Lines of context around matches (search mode)
- `max_matches`: Max matches to return (search mode)
- `include_dependencies`: `False` (default) or `True` - Enable dependency analysis (Python files only)
- `include_impact`: `False` (default) or `True` - Include impact radius (requires `include_dependencies=True`)
- `allow_outside_repo`: `False` (default) or `True` - Allow reads outside repo_root (denylist still enforced). Paths under `/.claude/skills/` or `/.codex/skills/` are always allowed.
- `format`: `readable` (default), `structured`, or `compact` - Output format

**Scan Mode Enhancements:**
When `mode="scan_only"`, the tool automatically detects file type and extracts structure:

- **Python files**: AST analysis showing functions, classes, methods with line numbers and signatures
- **Markdown files**: Heading hierarchy with line numbers (max 100 headings)
- **JavaScript/TypeScript**: Basic structure detection
- **SKILL.md detection**: Special urgent warning when reading SKILL.md files
- **Navigation hints**: Suggested chunk sizes and example calls for large files

**Dependency Analysis (`include_dependencies=True`):**
Provides static analysis of Python imports with governance features:

1. **Import Categorization**:
   - **Standard Library**: Python stdlib imports (detected via sys.stdlib_module_names)
   - **Third-Party Packages**: External dependencies from pip/conda
   - **Local Modules**: Project-internal imports with path resolution and existence checks

2. **Path Resolution**:
   - Resolves relative imports (e.g., `from ..utils import helper`)
   - Resolves absolute imports (e.g., `from scribe_mcp.tools import append_entry`)
   - Shows resolved file paths with ✓ checkmarks when files exist
   - Detects workspace root automatically (.git, pyproject.toml markers)

3. **Impact Radius (Blast Radius)**:
   - Shows how many files import the current file
   - Categorized by impact level:
     - **Low**: 0-4 importers
     - **Medium**: 5-15 importers (⚠️ warning)
     - **High**: 16+ importers (🚨 high impact)
   - Lists up to 20 files that import this module
   - Helps assess change risk before modifications

4. **Boundary Enforcement**:
   - Checks imports against `.scribe/config/boundary_rules.yaml` rules
   - Detects forbidden import patterns (e.g., "sentinel layer must not import tools")
   - Shows violations with severity levels: ERROR, WARNING, INFO
   - Supports glob patterns with `**` for recursive matching
   - Respects `allowed_exceptions` for legitimate edge cases

5. **Static Analysis Disclaimer**:
   - Automatically included when dependencies or impact radius shown
   - Clarifies that only import-time relationships are detected
   - Honest about limitations: no runtime dependencies, dynamic imports, or reflection patterns

**Example Usage:**
```python
# Basic scan (metadata + structure)
await read_file(agent="Codex", path="tools/read_file.py", mode="scan_only")

# Scan with dependency analysis
await read_file(agent="Codex", path="tools/read_file.py", mode="scan_only", include_dependencies=True)

# Read specific chunk
await read_file(agent="Codex", path="docs/Scribe_Usage.md", mode="chunk", chunk_index=[0])

# Regex search (default mode)
await read_file(agent="Codex", path="tools/read_file.py", mode="search", query=r"async\s+def\s+\w+")

# Literal search (explicit)
await read_file(agent="Codex", path="docs/Scribe_Usage.md", mode="search", search="semantic", search_mode="literal")

# Search with context lines
await read_file(agent="Codex", path="server.py", mode="search", query="async def", context_lines=2)
```

**Configuration:**
Boundary rules are defined in `.scribe/config/boundary_rules.yaml`:
```yaml
version: 1.0
enabled: true
rules:
  - name: "Sentinel Layer Isolation"
    severity: "error"
    pattern:
      source: "sentinel/**/*.py"
      forbidden_imports:
        - "tools/**"
        - "scribe_mcp.tools.*"
```

**Performance:**
- Dependency analysis: ~20% overhead when enabled (opt-in)
- Impact radius: <3s for typical repositories (<500 Python files)
- Boundary checking: <20ms overhead per file
- Zero overhead when `include_dependencies=False` (default)

**Notes:**
- Every read is logged with provenance (absolute path, hash, byte size, encoding, read mode)
- Enforces repo scope by default; out-of-scope paths are denied
- Dependency analysis is static only - does not execute code or resolve runtime imports
- Impact radius requires workspace root detection (looks for .git, pyproject.toml markers)

### `scribe_doctor`
**Purpose**: Diagnostics for repo root, config resolution, plugin status, and vector readiness.

**Required Parameters:**
- `agent` (string): Agent identifier for session tracking

**Example Usage:**
```python
await scribe_doctor(agent="Codex")
```

**Returns:**
- Repo root, cwd, config paths
- Plugin status (including vector indexer availability)
- Vector index metadata and queue depth (if enabled)

---

## Documentation Management

### `manage_docs`
**Purpose**: Structured documentation system for projects.

**Required Parameters:**
- `agent` (string): Agent identifier for session tracking
- `action` (string): Action type (see all 17 actions below)
- `doc_name` (string): Document identifier/filename key (e.g., `architecture`, `phase_plan`, `checklist`, `implementation`)

**Important:** `doc_name` is the unique document identifier (and drives filename resolution). `doc_category` is a semantic label only and must not be used as a filename or registry key.

**All Available Actions (7 primary + 5 deprecated + 7 hidden = 19 total):**

**PRIMARY ACTIONS** (7 actions - main user-facing operations):
- `create` - Unified creation with `doc_type` routing (replaces create_* actions)
- `replace_section` - Replace content using section anchors (scaffolder support)
- `apply_patch` - Apply unified diff patches
- `replace_range` - Replace explicit line ranges
- `replace_text` - Find/replace text patterns
- `append` - Append content to document or section
- `status_update` - Update checklist item status

**DEPRECATED ACTIONS** (5 actions - still work but route to `create` with `doc_type` in metadata):
- `create_doc` → `create(metadata={"doc_type": "custom", ...})`
- `create_research_doc` → `create(metadata={"doc_type": "research", ...})`
- `create_bug_report` → `create(metadata={"doc_type": "bug", ...})`
- `create_review_report` → `create(metadata={"doc_type": "review", ...})`
- `create_agent_report_card` → `create(metadata={"doc_type": "agent_card", ...})`

**HIDDEN ACTIONS** (7 actions - supported but not promoted, for backwards compatibility):
- `normalize_headers` - Normalize markdown headers to ATX format
- `generate_toc` - Generate table of contents
- `validate_crosslinks` - Validate cross-document references
- `list_sections` - List all section anchors in a document
- `list_checklist_items` - List all checklist items
- `search` - Semantic search across documents
- `batch` - Execute multiple operations sequentially

**Action-Specific Parameters:**

#### `create` (UNIFIED CREATION ACTION)
- `doc_name` (string, required): Document identifier used for naming/registration
- `content` (string, optional): Document content (alternative to `metadata.body`)
- `template` (string, optional): Template name override
- `metadata` (dict, required for type routing): Document metadata with type-specific fields
  - `doc_type` (string): Document type - `custom`, `research`, `bug`, `review`, `agent_card` (defaults to `custom`)
  - For `research`: `research_goal` (required), `confidence_areas` (optional)
  - For `bug`: `category`, `slug`, `severity`, `title` (all required), `component` (optional)
  - For `review`: Review report metadata
  - For `agent_card`: Agent performance metadata
  - For `custom`: `body`/`snippet`/`sections` for content, `register_doc`/`register_as` for control

**Migration Examples:**
```python
# OLD: create_research_doc
manage_docs(action="create_research_doc", doc_name="RESEARCH_AUTH", metadata={"research_goal": "..."})

# NEW: create with doc_type
manage_docs(action="create", doc_name="RESEARCH_AUTH", metadata={"doc_type": "research", "research_goal": "..."})

# OLD: create_bug_report
manage_docs(action="create_bug_report", metadata={"category": "logic", "slug": "auth_bug", ...})

# NEW: create with doc_type
manage_docs(action="create", metadata={"doc_type": "bug", "category": "logic", "slug": "auth_bug", ...})
```

#### `replace_section`
- `section` (string, required): Section anchor ID (e.g., "problem_statement")
- `content` (string, required): New section content

#### `append`
- `content` (string, required): Content to append
- `section` (string, optional): Section anchor to append near. When omitted the content is appended to the end of the file.
- `metadata.position` (string, optional): Insert placement relative to the section. Supported values: `before`, `inside` (immediately after the anchor), and `after` (default).

#### `status_update`
- `section` (string, required): Checklist item ID
- `metadata` (dict, optional): Status info such as `{"status": "done", "proof": "evidence"}`. When omitted the existing status is preserved and proofs can still be updated.

#### `apply_patch`
- `edit` (dict, required): Patch specification with `type` field
  - Format: `{"type": "structured"|"unified", ...}` for structured patches
  - Or: Full patch dict for unified diffs
- `patch` (string, optional): Unified diff patch string
- `patch_source_hash` (string, optional): Source content hash for verification
- `patch_mode` (string, optional): Patch application mode

#### `replace_range`
- `start_line` (int, required): Starting line number (1-indexed)
- `end_line` (int, required): Ending line number (inclusive)
- `content` (string, required): Replacement content

#### `replace_text`
- `metadata` (dict, required): Find/replace configuration with:
  - `find` (string, required): Text pattern to find
  - `replace` (string, optional): Replacement text (defaults to empty string)
  - `match_mode` (string, optional): `literal` (default) or `regex`
  - `replace_all` (bool, optional): Replace all occurrences (default: true)
  - `scope` (string, optional): Limit to specific section ID
  - `allow_no_match` (bool, optional): Don't error if no match (default: false)

**Example:**
```python
manage_docs(
    action="replace_text",
    doc_name="architecture",
    metadata={"find": "old_text", "replace": "new_text", "replace_all": True}
)
```

---

### Deprecated Actions (Backwards Compatibility)

The following actions are **DEPRECATED** but still work. They automatically route to the unified `create` action with appropriate `doc_type`:

#### `create_research_doc` → `create(metadata={"doc_type": "research"})`
**Migration:** Use `manage_docs(action="create", doc_name="RESEARCH_...", metadata={"doc_type": "research", ...})` instead.

#### `create_bug_report` → `create(metadata={"doc_type": "bug"})`
**Migration:** Use `manage_docs(action="create", metadata={"doc_type": "bug", ...})` instead.

#### `create_review_report` → `create(metadata={"doc_type": "review"})`
**Migration:** Use `manage_docs(action="create", metadata={"doc_type": "review", ...})` instead.

#### `create_agent_report_card` → `create(metadata={"doc_type": "agent_card"})`
**Migration:** Use `manage_docs(action="create", metadata={"doc_type": "agent_card", ...})` instead.

#### `create_doc` → `create(metadata={"doc_type": "custom"})`
**Migration:** Use `manage_docs(action="create", doc_name="...", metadata={"doc_type": "custom", "body": "..."})` instead.

**Note:** All deprecated actions accept the same parameters as before, but internally route to the new `create` action. See the `create` action documentation above for detailed parameter specifications.

---

### Hidden Actions (Advanced/Internal Use)

The following actions are **HIDDEN** - they still work but are not promoted in standard workflows. These are for backwards compatibility and advanced use cases:

#### `normalize_headers` (HIDDEN ACTION)
- No additional parameters required
- Normalizes all markdown headers to ATX format (# style)

#### `generate_toc` (HIDDEN ACTION)
- `metadata` (dict, optional): TOC generation options

#### `validate_crosslinks` (HIDDEN ACTION)
- No additional parameters required
- Validates all cross-document references

#### `list_sections` (HIDDEN ACTION)
- No additional parameters required
- Returns the discovered section anchors for the requested document, including line numbers

#### `list_checklist_items` (HIDDEN ACTION)
- No additional parameters required
- Returns all checklist items with their IDs and status

#### `search` (HIDDEN ACTION)
- Semantic search across documents (see dedicated search documentation)

#### `batch` (HIDDEN ACTION)
- `metadata.operations` (list, required): Sequence of manage_docs payloads executed in order. Nested batches are rejected for safety

**Global Optional Parameters:**
- `doc_name` (string): Document identifier (required for most actions except bug reports which auto-generate)
- `project` (string): Explicit project override for cross-project doc management
- `metadata` (dict): Additional metadata for the operation
- `dry_run` (bool): Preview changes without applying
- `target_dir` (string): Custom target directory for CREATE operations
- Metadata payloads are auto-normalized; dicts, JSON strings, and legacy key/value sequences are all accepted.

**MCP Schema Fix (v2.2.0+):**
All parameters now properly exposed via MCP with correct JSON Schema types. Previously, parameters like `doc_name`, `edit`, `section`, and `metadata` appeared as empty schemas `{}` due to string annotations from `from __future__ import annotations`. Fixed by using `typing.get_type_hints()` to resolve annotations at runtime.

**Example Usage:**
```python
# Replace architecture section
await manage_docs(
    agent="Codex",
    action="replace_section",
    doc_name="architecture",  # REQUIRED: unique doc identifier
    section="problem_statement",
    content="## Problem Statement\n**Context:** ..."
)

# Append within a section
await manage_docs(
    agent="Codex",
    action="append",
    doc_name="architecture",
    section="problem_statement",
    content="Updated scope paragraph",
    metadata={"position": "inside"}
)

# Update checklist status
await manage_docs(
    agent="Codex",
    action="status_update",
    doc_name="checklist",
    section="phase_1_task_1",
    metadata={"status": "done", "proof": "code_review_completed"}
)

# Create research document (NEW SYNTAX - doc_type goes IN metadata)
await manage_docs(
    agent="Codex",
    action="create",
    doc_name="RESEARCH_AUTH_SYSTEM_20251102",
    metadata={
        "doc_type": "research",  # REQUIRED: specifies document type
        "research_goal": "Analyze authentication flow",
        "confidence_areas": ["security"]
    }
)

# Create bug report (NEW SYNTAX - doc_type goes IN metadata)
await manage_docs(
    agent="Codex",
    action="create",
    metadata={
        "doc_type": "bug",  # REQUIRED: specifies document type
        "category": "database",
        "slug": "connection_leak",
        "severity": "high",
        "title": "Database connection pool exhaustion",
        "component": "storage/sqlite.py"
    }
)

# Create custom document (NEW SYNTAX - doc_type goes IN metadata)
await manage_docs(
    agent="Codex",
    action="create",
    doc_name="COORDINATION_PROTOCOL",
    metadata={
        "doc_type": "custom",  # REQUIRED: specifies document type
        "body": "# Coordination Protocol\n\n..."
    }
)

# Apply unified patch (patch_mode defaults to "unified" when patch is provided)
await manage_docs(
    agent="Codex",
    action="apply_patch",
    doc_name="architecture",
    patch="--- a/file.md\n+++ b/file.md\n@@ -10,3 +10,4 @@\n existing line\n+new line",
    dry_run=True  # Always dry_run first!
)

# Batch multiple updates (executed sequentially)
await manage_docs(
    agent="Codex",
    action="batch",
    doc_name="architecture",
    metadata={
        "operations": [
            {
                "action": "append",
                "doc_name": "architecture",
                "section": "requirements_constraints",
                "content": "Documented latency targets",
                "metadata": {"position": "after"}
            },
            {
                "action": "status_update",
                "doc_name": "checklist",
                "section": "documentation_hygiene",
                "metadata": {"status": "done", "proof": "PROGRESS_LOG#2025-11-02"}
            }
        ]
    }
)
```

**Returns:**
```json
{
  "ok": true,
  "doc_name": "architecture",
  "action": "replace_section",
  "path": "/path/to/document.md",
  "verification_passed": true,
  "dry_run": false
}
```

### `manage_docs` semantic search
**Purpose**: Semantic retrieval across registry-managed docs and logs (doc-first results by default).

**Required Parameters:**
- `action`: `"search"`
- `doc_name`: `"*"` (search all) or specific document identifier
- `metadata.query`: search string
- `metadata.search_mode`: `"semantic"`

**Optional Filters:**
- `content_type`: `"doc"` or `"log"` (default is both)
- `project_slug` / `project_slugs` / `project_slug_prefix`
- `doc_type`, `file_path`
- `time_start` / `time_end`
- `k` (total results), `doc_k` / `log_k` overrides
- `min_similarity` (float)

**Example Usage:**
```python
# Semantic search across docs + logs
await manage_docs(
    agent="Codex",
    action="search",
    doc_name="*",
    metadata={"query": "ExecutionContext", "search_mode": "semantic", "k": 8}
)

# Doc-only semantic search scoped to a project
await manage_docs(
    agent="Codex",
    action="search",
    doc_name="*",
    metadata={
        "query": "ExecutionContext",
        "search_mode": "semantic",
        "content_type": "doc",
        "project_slug": "scribe_sentinel_concurrency_v1",
        "doc_k": 5
    }
)
```

### `generate_doc_templates`
**Purpose**: Create/update documentation templates for a project.

**Required Parameters:**
- `agent` (string): Agent identifier for session tracking
- `project_name` (string): Name of the project

**Optional Parameters:**
- `author` (string): Document author
- `overwrite` (bool, default: false): Overwrite existing templates
- `documents` (list): Specific documents to generate
- `base_dir` (string): Base directory for templates

**Example Usage:**
```python
# Basic usage
await generate_doc_templates(agent="Codex", project_name="my-project")

# With author and specific documents
await generate_doc_templates(
    agent="Codex",
    project_name="my-project",
    author="MyAgent",
    documents=["architecture", "phase_plan"]
)
```

**Returns:**
```json
{
  "ok": true,
  "files": ["/paths/to/generated/files.md"],
  "skipped": ["/paths/to/existing/files.md"],
  "directory": "/path/to/docs/dir",
  "validation": {/* template validation results */}
}
```

### Auto-Registration for EDIT Operations (v2.2.0+)

Starting in v2.2.0, `manage_docs` automatically registers unregistered documents when you perform EDIT operations. This eliminates "DOC_NOT_FOUND" errors and streamlines workflows for both AI agents and human users.

#### How It Works

When you call `manage_docs` with an EDIT action, the system automatically:
1. Checks if the document is registered in the project's `docs` metadata
2. If unregistered, resolves the document path based on the document key
3. Verifies the file exists on disk
4. Computes the SHA256 hash for integrity tracking
5. Updates the project's `docs_json` database field
6. Logs the registration to the progress log
7. Proceeds with your requested edit operation

**EDIT operations (auto-register if needed):**
- `list_sections` - List all section anchors in a document
- `replace_section` - Replace content using section anchors
- `apply_patch` - Apply structured or unified diff patches
- `replace_range` - Replace explicit line ranges
- `append` - Append content to document or section
- `status_update` - Update checklist item status
- `normalize_headers` - Normalize markdown headers to ATX format
- `generate_toc` - Generate table of contents
- `search` - Semantic search across documents
- `replace_text` - Replace text patterns
- `validate_crosslinks` - Validate cross-document references

**CREATE operations (explicit registration):**
These actions handle document creation and registration internally, so auto-registration is not needed:
- `create_research_doc` - Create structured research documents
- `create_bug_report` - Create structured bug reports
- `create_review_report` - Create review reports
- `create_agent_report_card` - Create agent performance reports
- `create_doc` - Create custom documents

#### Example Workflow

**Before v2.2.0 (manual registration required):**
```python
# Step 1: Explicitly register documents first
await generate_doc_templates(project_name="my_project")

# Step 2: Then perform edits
await manage_docs(
    action="replace_section",
    doc_name="architecture",
    section="problem_statement",
    content="Updated content..."
)
```

**v2.2.0+ (auto-registration):**
```python
# Just call manage_docs directly - auto-registration handles the rest
await manage_docs(
    action="replace_section",
    doc_name="architecture",
    section="problem_statement",
    content="Updated content..."
)
# Auto-registers 'architecture' if needed, then performs the edit
```

#### What Gets Registered

When auto-registration triggers, the following happens:

1. **Document Path Resolution**: The document key (e.g., "architecture") is mapped to its canonical filename (e.g., `ARCHITECTURE_GUIDE.md`)

2. **File Verification**: The system checks that the file exists at the expected path within the project's documentation directory

3. **Hash Computation**: A SHA256 hash is computed for the file contents to enable integrity tracking and change detection

4. **Database Update**: The project's `docs_json` field in the database is updated with the new registration

5. **Progress Log Entry**: A log entry is created documenting the auto-registration event:
   ```
   [ℹ️] [timestamp] Auto-registered 'architecture' → ARCHITECTURE_GUIDE.md
   ```

#### Requirements for Auto-Registration

Auto-registration requires all of the following conditions:

- **Database Backend**: SQLite or PostgreSQL storage must be active (auto-registration uses database-backed project metadata)
- **File Must Exist**: The document file must exist on disk at the expected path
- **Resolvable `doc_name`**: The `doc_name` must resolve to a file path under the project root. Standard keys map to canonical filenames (e.g., `architecture` → `ARCHITECTURE_GUIDE.md`); unknown keys map to `<DOC_NAME>.md` under the project's docs directory. The resolved file must exist for auto-registration to succeed.
- **Active Project Context**: A project must be set via `set_project()` before calling `manage_docs`

#### Troubleshooting

**Error: "DOC_NOT_FOUND: Document 'X' not registered"**

This error occurs when:
- Auto-registration is disabled (should not happen in v2.2.0+)
- The action is not an EDIT operation (use CREATE operations for new docs)
- Something prevented auto-registration from completing

*Solution:*
1. Verify you're using an EDIT action (see list above)
2. Check that the file exists: `ls .scribe/docs/dev_plans/<project>/<DOC_FILE>.md`
3. Review progress log for auto-registration errors
4. Try manual registration: `await generate_doc_templates(project_name="<project>")`

**Error: "Cannot auto-register: file does not exist at path X"**

The document file doesn't exist at the expected location.

*Solution:*
1. Create the file first: `await generate_doc_templates(project_name="<project>")`
2. Or use a CREATE action to generate a new document
3. Verify the project name matches the directory structure

**Auto-registration logs but edit fails**

Registration succeeded, but the edit operation encountered an issue.

*Solution:*
1. For `replace_section`: Verify section anchors exist using `list_sections`
2. For `replace_range`: Check that line numbers are valid and within bounds
3. For `apply_patch`: Ensure YAML frontmatter is valid and not corrupted
4. Review the error message for specific guidance

**Database connectivity issues**

Auto-registration requires database write access.

*Solution:*
1. Verify database backend is configured: Check `SCRIBE_STORAGE_BACKEND` environment variable
2. For SQLite: Ensure write permissions on the database file
3. For PostgreSQL: Verify connection string and credentials
4. Run diagnostics: `await scribe_doctor()` to check system health

#### Best Practices

**For AI Agents:**
- Don't worry about pre-registering documents - just call `manage_docs` with EDIT actions directly
- Use CREATE actions (`create_research_doc`, `create_bug_report`) for new documents
- Check error messages for actionable guidance if auto-registration fails

**For Human Users:**
- Auto-registration works transparently - no workflow changes needed
- Use `generate_doc_templates()` to create initial project scaffolding
- Monitor progress logs to see when auto-registration occurs

**For Tool Developers:**
- Auto-registration is handled in the `manage_docs` tool entry point
- No changes needed to individual action handlers
- All EDIT actions benefit automatically

---

## Log Maintenance

### `rotate_log`
**Purpose**: Archive current progress log and start fresh file.

**Required Parameters:**
- `agent` (string): Agent identifier for session tracking

**Optional Parameters:**
- `confirm` (bool): When True, perform actual rotation
- `dry_run` (bool, default: true): Preview rotation without changes
- `log_type` (string): Specific log type to rotate
- `log_types` (list): Multiple log types to rotate
- `rotate_all` (bool): Rotate every configured log type
- `auto_threshold` (bool): Only rotate if entry count exceeds threshold
- `threshold_entries` (int): Override entry threshold
- `suffix` (string): Optional suffix for archive filenames
- `custom_metadata` (string): JSON metadata for rotation record

**Example Usage:**
```python
# Preview rotation
await rotate_log(agent="Codex", dry_run=True)

# Actually rotate progress log
await rotate_log(agent="Codex", confirm=True)

# Rotate multiple log types
await rotate_log(
    agent="Codex",
    confirm=True,
    log_types=["progress", "doc_updates"]
)

# Auto-threshold rotation
await rotate_log(
    agent="Codex",
    confirm=True,
    auto_threshold=True,
    threshold_entries=1000
)
```

**Returns:**
```json
{
  "ok": true,
  "rotations": [
    {
      "log_type": "progress",
      "dry_run": false,
      "rotation_id": "unique-id",
      "project": "project-name",
      "current_file_path": "/path/to/current.md",
      "archived_to": "/path/to/archive.md",
      "entry_count": 150,
      "requires_confirmation": false,
      "auto_threshold_triggered": false
    }
  ]
}
```

### `verify_rotation_integrity`
**Purpose**: Verify the integrity of a specific rotation archive.

**Required Parameters:**
- `archive_path` (string): Path to rotation archive to verify

**Example Usage:**
```python
await verify_rotation_integrity(
    archive_path="/path/to/archive.md"
)
```

### `get_rotation_history`
**Purpose**: Return recent rotation history entries for the active project.

**Parameters:** None (requires active project)

**Example Usage:**
```python
await get_rotation_history()
```

**Returns:**
```json
{
  "ok": true,
  "project": "project-name",
  "rotation_count": 3,
  "rotations": [
    {
      "rotation_id": "id",
      "timestamp": "2025-11-02 07:40:21 UTC",
      "log_type": "progress",
      "entry_count": 150
    }
  ]
}
```

---

## Project Cleanup

### `delete_project`
**Purpose**: Delete or archive a project and all associated data.

**Required Parameters:**
- `agent` (string): Agent identifier for session tracking
- `name` (string): Project name to delete
- `confirm` (bool): Must be True to proceed with deletion

**Optional Parameters:**
- `mode` (string, default: "archive"): "archive" or "permanent"
- `force` (bool): Override safety checks (not recommended)
- `archive_path` (string): Custom archive directory

**Example Usage:**
```python
# Archive project (safe default)
await delete_project(
    agent="Codex",
    name="old-project",
    confirm=True
)

# Permanent deletion (dangerous)
await delete_project(
    agent="Codex",
    name="temp-project",
    confirm=True,
    mode="permanent"
)
```

**Returns:**
```json
{
  "success": true,
  "project_name": "project-name",
  "mode": "archive",
  "message": "Project 'project-name' archived to path",
  "archive_location": "/path/to/archive",
  "database_cleanup": true
}
```

---

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

## Error Handling

Common errors and solutions:

1. **"No project configured"** → Call `set_project()` first
2. **"Invalid arguments for tool"** → Check parameter names and types
3. **"dictionary update sequence element #0 has length 1; 2 is required"** → `meta` parameter format issue

---

## Tool Summary Quick Reference

| Tool | Purpose | Required Params | Project Context |
|------|---------|----------------|-----------------|
| `set_project` | Initialize project | `name` | No |
| `get_project` | Get current context | None | Yes |
| `list_projects` | Browse projects | None | No |
| `append_entry` | **PRIMARY** logging | `message` or `items` | Yes |
| `read_recent` | Recent entries | None | Yes |
| `query_entries` | Search logs | None | Yes |
| `manage_docs` | Documentation | `action`, `doc_name` | Yes |
| `generate_doc_templates` | Create templates | `project_name` | No |
| `rotate_log` | Archive logs | None | Yes |
| `verify_rotation_integrity` | Verify archive | `archive_path` | No |
| `get_rotation_history` | Rotation history | None | Yes |
| `delete_project` | Remove project | `name`, `confirm` | No |
