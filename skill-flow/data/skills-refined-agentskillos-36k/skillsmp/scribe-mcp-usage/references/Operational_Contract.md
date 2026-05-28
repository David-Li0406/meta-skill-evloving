---
name: scribe-mcp-usage
description: Operate the local Scribe MCP for any repo; use when registering projects, logging work, managing docs via manage_docs (including auto-registration), or using Scribe tools like append_entry/read_recent/query_entries/read_file.
---

# 🚨 SUBAGENT QUICK START (READ THIS FIRST)

**You are a subagent. Your orchestrator gave you a project name. Follow these steps:**

## Step 1: Activate Project (MANDATORY)
```python
set_project(agent="<YourAgentName>", name="<project_name_from_orchestrator>")
```

## Step 2: Log Your Start
```python
append_entry(
    agent="<YourAgentName>",
    message="Starting <your_task>",
    status="info",
    meta={"task": "<task>", "reasoning": {"why": "...", "what": "...", "how": "..."}}
)
```

## Step 3: Do Your Work (agent-specific)

### Research Agent Deliverables
1. **Create research doc** (REQUIRED):
   ```python
   manage_docs(
       action="create_research_doc",
       doc_name="RESEARCH_<TOPIC>_<YYYYMMDD>",
       metadata={"research_goal": "<what you're investigating>"}
   )
   ```
2. **Update it with findings** using `apply_patch`:
   ```python
   manage_docs(
       action="apply_patch",
       doc_name="research_report_RESEARCH_<TOPIC>_<YYYYMMDD>",
       edit={"type": "replace_range", "start_line": X, "end_line": Y, "content": "..."},
       dry_run=True  # ALWAYS dry_run first!
   )
   ```
3. **Log every 2-3 findings** with `append_entry`

### Architect Agent Deliverables
1. Read research docs first
2. Update `ARCHITECTURE_GUIDE.md`, `PHASE_PLAN.md`, `CHECKLIST.md` via `manage_docs`
3. Log architectural decisions

### Coder Agent Deliverables
1. Follow the PHASE_PLAN task packages
2. Log every 3 edits with `append_entry`
3. Run tests and log results

### Review Agent Deliverables
1. Create review report: `manage_docs(action="create_review_report", metadata={"stage": "3"})`
2. Grade each agent, verify ≥93% to pass
3. Log findings

## Step 4: Log Completion
```python
append_entry(
    agent="<YourAgentName>",
    message="Completed <your_task>: <summary>",
    status="success",
    meta={"deliverables": [...], "confidence": 0.9}
)
```

---

## Required Reading (After Quick Start)

- Codex: read and follow `AGENTS.md`.
- Claude Code: read and follow `CLAUDE.md`.
- For tool schemas and examples: `read_file(agent="<YourAgentName>", path="references/Scribe_Usage.md", mode="search", query="<tool_name>")`

This skill is the minimal, enforceable tool-and-logging contract. Deeper rationale belongs in wiki or code.

---

## Curated Resources (Use read_file)

- `references/Scribe_Usage.md` (canonical tool behaviors, schemas, and examples)
- `tools/manage_docs.py` (manage_docs validation, auto-registration rules)
- `doc_management/manager.py` (create_doc content rules, frontmatter behavior)
- `.scribe/docs/dev_plans/<project>/` (ARCH/PHASE/CHECKLIST and managed artifacts)

---

## Core Rules (Brief, Enforced)

- MCP tools are mandatory: if a tool exists, call it directly via MCP; do not script substitutes.
- Log intent only after the tool succeeds or fails.
- Confirmation flags (e.g., `confirm`, `dry_run`) must be passed as actual tool parameters.
- All file reads must use `read_file` (scan/search/chunk/page/line_range). Do not read file contents with `cat`/`rg`; use `rg --files` only for filename discovery.
- For parameter discovery, use `read_file` with `mode="search"` and `query="search term"` against tool docs or sources. This mode allows regex. Most notably: `references/Scribe_Usage.md`. **Keep this document updated with changes to tools or usage.**
- If a tool call fails, fix the payload and retry; never fall back to shell reads for content.
- Always rehydrate context when required:
  - Project mode: `read_recent` or `query_entries` (last 5 entries minimum).
  - Cross-project/global: `query_entries` with `search_scope="global"` or `"all_projects"`.
  - You only need to rehydrate when unsure of next steps, on a fresh context window, or we need previous architectural decisions brought back.
- Logging discipline:
  - Project mode: use `append_entry` after every meaningful action (every 2-3 edits or 5 minutes). You MUST log during investigation as well.
  - Sentinel mode (only if preconfigured): use `append_event`.
- Reasoning block is mandatory in every `append_entry`:
  - `why` (goal/decision point)
  - `what` (constraints/alternatives)
  - `how` (method/uncertainty)
- New project workflow (Codex): call `set_project` (with repo root) then `manage_docs` to draft ARCHITECTURE_GUIDE, PHASE_PLAN, CHECKLIST before any feature code.
- Codex agent name must be `Codex`.


**What Gets Logged (Non-Negotiable):**
- 🔍 Investigation findings and analysis results
- 💻 Code changes (what was changed and why)
- ✅ Test results (pass/fail with context)
- 🐞 Bug discoveries (symptoms, root cause, fix approach)
- 📋 Planning decisions and milestone completions
- 🔧 Configuration changes and deployments
- ⚠️ Errors encountered and recovery actions
- 🎯 Task completions and progress updates


## Readable vs Structured Modes
- Readable mode is the preferred way to use Scribe Tools, however, if you need to debug or require additional information, structured mode will output the entire payload.   This can be token heavy!

## Sentinel vs Project Mode

- Project mode: call `set_project` and use `append_entry`, `manage_docs`, `read_recent`, `query_entries`.
- If you are unsure which project is active, call `list_projects` first, then `set_project` to create/switch.
- Sentinel mode is not switchable once a project is set in this session. If sentinel is preconfigured, use `append_event`, `open_bug`, `open_security`, `link_fix` for repo-wide issues.



## Tool Signatures (Authoritative)

All MCP tool calls and parameters must match these signatures.

### Core Project Tools

```
append_entry(
  agent,              # REQUIRED
  message="",
  status=None,
  emoji=None,
  meta=None,
  timestamp_utc=None,
  items=None,
  items_list=None,
  auto_split=True,
  split_delimiter="\n",
  stagger_seconds=1,
  agent_id=None,
  log_type="progress",
  priority=None,
  category=None,
  tags=None,
  confidence=None,
  config=None,
  format="readable"
)

set_project(
  agent,              # REQUIRED
  name,               # REQUIRED
  root=None,
  progress_log=None,
  defaults=None,
  author=None,
  overwrite_docs=False,
  agent_id=None,
  expected_version=None,
  description=None,
  tags=None,
  template=None,
  auto_create_dirs=True,
  skip_validation=False,
  reminder_settings=None,
  notification_config=None,
  reset_reminders=False,
  emoji=None,
  project_agent=None,
  format="readable"
)

get_project(
  agent,              # REQUIRED
  project=None,
  format="structured"
)

manage_docs(
  action,
  doc_name=None,          # UNIQUE identifier - REQUIRED for all doc operations (e.g., "architecture", "RESEARCH_AUTH_20260108")
  doc_category="",        # Category for filtering/routing (e.g., "research", "bugs", "standard")
  section=None,
  content=None,
  patch=None,             # Unified diff content (defaults to unified mode when provided)
  patch_source_hash=None,
  edit=None,              # Structured edit dict (defaults to structured mode when provided)
  patch_mode=None,        # "unified" or "structured" - auto-detected from patch/edit if not specified
  start_line=None,
  end_line=None,
  template=None,
  metadata=None,
  dry_run=False,
  target_dir=None,
  project=None            # Explicit project override (cross-project doc management)
)

generate_doc_templates(
  agent,              # REQUIRED
  project_name,       # REQUIRED
  author=None,
  overwrite=False,
  force=False,
  documents=None,
  base_dir=None,
  custom_context=None,
  legacy_fallback=False,
  include_template_metadata=False,
  validate_only=False
)

read_recent(
  agent,              # REQUIRED
  project=None,
  n=None,
  limit=None,
  filter=None,
  page=1,
  page_size=10,
  compact=False,
  fields=None,
  include_metadata=True,
  format="readable",
  priority=None,
  category=None,
  min_confidence=None,
  priority_sort=False
)

query_entries(
  agent,              # REQUIRED
  project=None,
  start=None,
  end=None,
  message=None,
  message_mode="substring",
  case_sensitive=False,
  emoji=None,
  status=None,
  agent=None,
  agents=None,
  meta_filters=None,
  limit=50,
  page=1,
  page_size=10,
  compact=False,
  fields=None,
  include_metadata=True,
  search_scope="project",
  document_types=None,
  include_outdated=True,
  verify_code_references=False,
  time_range=None,
  relevance_threshold=0.0,
  max_results=None,
  config=None,
  format="readable",
  priority=None,
  category=None,
  min_confidence=None,
  priority_sort=False
)

read_file(
  agent,              # REQUIRED
  path,               # REQUIRED
  mode="scan_only",
  chunk_index=None,
  start_chunk=None,
  max_chunks=None,
  start_line=None,
  end_line=None,
  page_number=None,
  page_size=None,
  search=None,
  query=None,
  search_mode="regex",
  case_insensitive=None,
  context_lines=0,
  max_matches=None,
  fuzzy_threshold=None,
  include_dependencies=False,
  include_impact=False,
  structure_filter=None,
  structure_page=1,
  structure_page_size=10,
  allow_outside_repo=False,
  format="readable"
)

list_projects(
  agent,              # REQUIRED
  limit=5,
  filter=None,
  compact=False,
  fields=None,
  include_test=False,
  page=1,
  page_size=None,
  status=None,
  tags=None,
  order_by=None,
  direction="desc",
  format="structured"
)

rotate_log(
  agent,              # REQUIRED
  project=None,
  suffix=None,
  custom_metadata=None,
  confirm=None,
  dry_run=None,
  dry_run_mode=None,
  log_type=None,
  log_types=None,
  rotate_all=None,
  auto_threshold=None,
  threshold_entries=None,
  config=None
)

delete_project(
  agent,              # REQUIRED
  name,               # REQUIRED
  mode="archive",
  confirm=False,
  force=False,
  archive_path=None,
  agent_id=None
)

scribe_doctor(
  agent               # REQUIRED
)
```

### Sentinel Tools (Sentinel Mode Only)

```
append_event(
  message=None,
  status=None,
  emoji=None,
  agent=None,
  meta=None,
  timestamp_utc=None,
  items=None,
  items_list=None,
  auto_split=True,
  split_delimiter="\n",
  stagger_seconds=1,
  event_type=None,
  data=None
)

open_bug(title, symptoms, affected_paths=None)

open_security(title, symptoms, affected_paths=None)

link_fix(case_id, execution_id, artifact_ref, landing_status)
```

### Vector Tools (Registered Only When Vector Indexer Plugin Is Active)

```
vector_search(
  query,
  k=10,
  project_slug=None,
  project_slugs=None,
  project_slug_prefix=None,
  agent_name=None,
  content_type=None,
  doc_type=None,
  file_path=None,
  time_start=None,
  time_end=None,
  min_similarity=None
)

semantic_search(
  query,
  k=10,
  project_slug=None,
  project_slugs=None,
  project_slug_prefix=None,
  agent_name=None,
  time_start=None,
  time_end=None,
  min_similarity=None
)

retrieve_by_uuid(entry_id)

 vector_index_status()

 rebuild_vector_index()
 ```
 
 ## Tool Usage Notes (Best Practices)
 
 - `append_entry`: include a reasoning block in meta; log after each meaningful step.
 - `set_project`: pass `root` when known; avoid `overwrite_docs` unless explicitly requested.
 - `get_project`: use to confirm active project + docs registry before `manage_docs`.
- `read_recent`/`query_entries`: rehydrate last 5; use `search_scope` and `time_range` for targeted queries.
- `read_file`: scan/search first; use `include_dependencies` only when needed; use `allow_outside_repo=true` for out-of-repo reads (denylist still enforced). `.claude/skills` and `.codex/skills` are always allowed.
 - `manage_docs`: use for managed docs; `dry_run` first for edits; prefer `create_*` for reports.
 - `generate_doc_templates`: bootstrap ARCH/PHASE/CHECKLIST; use `force` only when regen is safe.
 - `list_projects`: use when unsure of active project; `filter` to narrow results.
 - `rotate_log`: use `dry_run` or `auto_threshold` first; pass `confirm=true` to rotate.
 - `delete_project`: default `archive`; use `permanent` only when explicitly requested.
 - `scribe_doctor`: run when repo root/config/plugin state is unclear.
 - Sentinel tools (`append_event`, `open_bug`, `open_security`, `link_fix`): sentinel-only.
 - Vector tools: only when the vector indexer plugin is active.
 
 ---

## `manage_docs` Action Schemas (ENFORCED)

**CRITICAL: Each action has specific required parameters. Using wrong params = failure.**

### Introspection Actions
```
list_sections:
  doc_name: "<registered_doc_name>"  # REQUIRED - unique doc identifier
  # Returns: section IDs with line numbers + hint for read_file scan_only

list_checklist_items:
  doc_name: "checklist" | "<doc_with_checklist_items>"  # REQUIRED
  # Returns: checklist items with status and line numbers
```

### Edit Actions
```
replace_range:
  doc_name: "<registered_doc_name>"  # REQUIRED
  start_line: int                                         # REQUIRED
  end_line: int                                           # REQUIRED
  content: "new content"                                  # REQUIRED
  dry_run: true | false                                   # recommended

append:
  doc_name: "<registered_doc_name>"  # REQUIRED
  content: "content to append"                            # REQUIRED
  dry_run: true | false                                   # recommended

replace_section:
  doc_name: "<registered_doc_name>"  # REQUIRED
  section: "section_id"                                   # REQUIRED (from list_sections)
  content: "new section content"                          # REQUIRED
  dry_run: true | false                                   # recommended

status_update:
  doc_name: "checklist"                                   # REQUIRED
  section: "checklist_item_id"                            # REQUIRED
  metadata: {"status": "done", "proof": "..."}            # REQUIRED

replace_text:
  doc_name: "<registered_doc_name>"  # REQUIRED
  metadata:
    find: "old text"                                      # REQUIRED
    replace: "new text"                                   # optional (defaults to empty string)
    match_mode: "literal|regex"                           # optional (default: literal)
    replace_all: true | false                             # optional (default: true)
    scope: "section_id"                                   # optional (limit replacements)
    allow_no_match: true | false                          # optional
  dry_run: true | false                                   # recommended
```

### Batch Action
```
batch:
  metadata:
    operations: [ {action: "...", doc_name: "...", ...}, ... ]  # REQUIRED
  # Nested batch operations are rejected
```

### `apply_patch` — THE PRIMARY EDITING METHOD

**`apply_patch` is the MAIN way to edit managed docs.** It supports two modes:

#### Mode 1: Structured Edit — Use `edit` parameter

The `edit` parameter takes a dict with a `type` field that determines the edit behavior.
When `edit` is provided, `patch_mode` defaults to "structured".

```
apply_patch (structured - replace_range):
  doc_name: "architecture" | "phase_plan" | "checklist"  # REQUIRED
  edit: {                                                 # REQUIRED
    "type": "replace_range",                              # REQUIRED
    "start_line": 10,                                     # REQUIRED (1-indexed)
    "end_line": 15,                                       # REQUIRED (inclusive)
    "content": "new content here"                         # REQUIRED
  }
  dry_run: true                                           # ALWAYS use first!

apply_patch (structured - replace_section):
  doc_name: "architecture" | "phase_plan" | "checklist"  # REQUIRED
  edit: {                                                 # REQUIRED
    "type": "replace_section",                            # REQUIRED
    "section": "problem_statement",                       # REQUIRED (section ID from <!-- ID: xxx -->)
    "content": "## New Section Content\n\nBody text here."
  }
  dry_run: true                                           # ALWAYS use first!

apply_patch (structured - replace_block):
  doc_name: "architecture" | "phase_plan" | "checklist"  # REQUIRED
  edit: {                                                 # REQUIRED
    "type": "replace_block",                              # REQUIRED
    "anchor": "**Author:**",                              # REQUIRED (unique text in file)
    "new_content": "**Author:** NewAgent\n**Version:** v2.0"
  }
  dry_run: true                                           # ALWAYS use first!
  # NOTE: Replaces from anchor line through next blank line
```

#### Mode 2: Unified Diff (DEFAULT) — Use `patch` parameter

When `patch` is provided, `patch_mode` defaults to "unified" — no need to specify it!

```
apply_patch (unified diff):
  doc_name: "architecture" | "phase_plan" | "checklist"  # REQUIRED
  patch: |                                                # REQUIRED - unified diff format
    --- a/file.md
    +++ b/file.md
    @@ -28,4 +28,4 @@
     **Author:** ArchitectAgent
    -**Version:** v1.0
    +**Version:** v1.1
     **Status:** Active
  dry_run: true                                           # ALWAYS use first!
```

#### Workflow: How to Use `apply_patch` Safely

1. **Get line numbers first** (for replace_range):
   ```
   read_file(path="...", mode="search", query="text to find", context_lines=3)
   ```

2. **Or get section IDs** (for replace_section):
   ```
   manage_docs(action="list_sections", doc_name="architecture")
   ```

3. **Always dry_run first**:
   ```
   manage_docs(action="apply_patch", doc_name="architecture", edit={...}, dry_run=true)
   ```

4. **Review the diff output**, then apply for real:
   ```
   manage_docs(action="apply_patch", doc_name="architecture", edit={...}, dry_run=false)
   ```

#### Quick Reference: Which Edit Type to Use

| Scenario | Edit Type | Key Parameters |
|----------|-----------|----------------|
| Know exact line numbers | `replace_range` | `start_line`, `end_line`, `content` |
| Document has `<!-- ID: xxx -->` anchors | `replace_section` | `section`, `content` |
| Unique text exists (e.g., header) | `replace_block` | `anchor`, `new_content` |
| Have a unified diff ready | unified mode | `patch` (patch_mode auto-detects) |

#### Token Optimization

By default, `apply_patch` returns only:
- `diff` - the unified diff of changes
- `preview_windows` - bounded before/after context (3 lines)

The full file `preview` is **NOT included by default** (token-heavy!). To get it:
```
metadata: {"include_full_preview": true}  # Only if you really need it
```

### Search Action
```
search:
  doc_name: "<registered_doc_name>" | "*"  # REQUIRED ("*" for all docs)
  metadata:
    query: "search term"                 # REQUIRED (NOT content!)
    search_mode: "semantic"              # optional
  # Returns: matches with line numbers and snippets
```

### Create Actions (doc_name required for research + custom docs)
```
create_research_doc:
  doc_name: "RESEARCH_topic_YYYYMMDD"                # REQUIRED
  metadata: {"research_goal": "..."}                 # REQUIRED
  project: "project_name"                            # optional (defaults to session project)
  dry_run: true | false                              # recommended

create_bug_report:
  doc_name: "BUG_optional_name"                      # optional
  metadata: {                                        # REQUIRED - category is mandatory:
    "category": "infrastructure|logic|database|api|ui|misc",  # REQUIRED
    "slug": "descriptive-slug",                      # optional (auto-generated if missing)
    "severity": "low|medium|high|critical",          # optional
    "title": "Brief description"                     # optional
  }
  project: "project_name"                            # optional (defaults to session project)
  dry_run: true | false                              # recommended

create_review_report:
  doc_name: "REVIEW_optional_name"                   # optional
  metadata: {"stage": "3|5|unknown"}                 # optional (stage defaults to "unknown")
  project: "project_name"                            # optional (defaults to session project)
  dry_run: true | false                              # recommended

create_agent_report_card:
  doc_name: "AGENT_optional_name"                    # optional
  metadata: {                                        # optional
    "agent_name": "AgentName",                       # optional (defaults to caller agent_id)
    "stage": "3|5|unknown"                           # optional (defaults to "unknown")
  }
  project: "project_name"                            # optional (defaults to session project)
  dry_run: true | false                              # recommended

create_doc:
  doc_name: "CUSTOM_DOC_NAME"                        # REQUIRED - unique identifier for the doc
  content: "# Title\n\nDocument content here..."      # REQUIRED if metadata.body/snippet/sections omitted
  metadata: {                                        # optional - supports alternate content + registration
    "doc_name": "CUSTOM_DOC_NAME",                   # recommended - used for naming/registration
    "doc_type": "coordination|brief|custom",         # optional - used for naming if doc_name omitted
    "body": "# Title\n\nDocument content here...",   # optional (alternate to content)
    "snippet": "Short body...",                      # optional
    "sections": [{"title": "Section", "content": "..."}], # optional
    "target_dir": ".scribe/docs/dev_plans/<project>", # optional - defaults to project docs_dir
    "frontmatter": {"key": "value"},                 # optional - YAML frontmatter
    "register_doc": true,                            # optional - defaults true for docs under docs_dir
    "register_as": "custom_alias",                   # optional - registry key override
    "register_existing": true,                       # optional - register without writing content
    "overwrite": false                               # optional - overwrite existing file
  }
  doc_category: "coordination|brief|custom"           # optional - sets frontmatter category
  project: "project_name"                             # optional (defaults to session project)

# EXAMPLE - Creating a coordination protocol doc:
# manage_docs(
#   action="create_doc",
#   doc_name="COORDINATION_PROTOCOL",
#   metadata={
#     "doc_name": "COORDINATION_PROTOCOL",
#     "doc_type": "coordination",
#     "body": "# Coordination Protocol\n\n## Section 1\nContent...",
#     "target_dir": ".scribe/docs/dev_plans/my_project",
#     "register_doc": true
#   }
# )
```

### Formatting Actions
```
normalize_headers:
  doc_name: "<registered_doc_name>"  # REQUIRED
  # No additional params

generate_toc:
  doc_name: "<registered_doc_name>"  # REQUIRED
  metadata: {...}                                         # optional

validate_crosslinks:
  doc_name: "<registered_doc_name>"  # REQUIRED
  # No additional params
```

### Common Mistakes to Avoid
- ❌ Using `doc=` instead of `doc_name=` → `doc_name` is the UNIQUE identifier
- ❌ `search` with `content="query"` → use `metadata={"query": "..."}`
- ❌ `apply_patch` without `dry_run=true` first → ALWAYS preview before applying
- ❌ `list_checklist_items` without `doc_name` → doc_name is REQUIRED
- ❌ `replace_block` with non-unique anchor → anchor must match exactly ONE line
- ❌ `create_doc` without content/body/snippet/sections → missing content is a hard error
- ❌ `register_existing` without `register_as`/`doc_name` → registry key is required

---

## `manage_docs` — How to Use It

`manage_docs` is the **only approved way** to create or change **managed project documentation** inside `.scribe/docs/dev_plans/<project>/`. Use it for dev-plan artifacts (architecture/phase/checklist) and structured reports (research/bug/review/agent card). **Do not hand-edit managed docs** unless the plan explicitly says to.

**Cross-project support**: Use `project="other_project"` to target a different project's docs (e.g., contributing to a shared wiki project).

**Sentinel mode**: Can now target explicit projects with `project="project_name"`. Without explicit project, sentinel mode cannot use `manage_docs` (no default project context).

**Auto-registration behavior**:
- Edit actions will auto-register unregistered docs **if the file exists** and `doc_name` resolves (otherwise use `generate_doc_templates` or `create_doc`).
- `create_doc` defaults `register_doc=true` for docs created under `docs_dir`; set `metadata.register_doc=false` to skip.
- Use `metadata.register_as` to control the registry key, and `metadata.register_existing=true` to register without writing.

### What you use `manage_docs` for

* Keeping the **doc suite** consistent:

  * `ARCHITECTURE_GUIDE.md` (source of truth for design)
  * `PHASE_PLAN.md` (execution plan)
  * `CHECKLIST.md` (status + proof)
* Producing **structured artifacts**:

  * research reports
  * bug reports
  * review reports
  * agent report cards
* Performing **safe, auditable edits**:

  * section replacement, patches, line-range edits, checklists updates
  * formatting helpers (TOC, header normalization)
  * crosslink validation

### Core editing actions (your daily bread)

These actions all share the same edit backend and should be treated as “**edit this doc safely**” variants:


**Use `apply_patch` when** you need precision edits and you can produce a clean patch.

* Best for surgical changes when section markers aren’t available.
* Prefer patch over “rewrite the whole file.”
* This is the most preferred method of updating managed_docs

**Use `replace_range` when** you know the exact line span you must replace.

* Only do this after inspecting structure (see introspection below).
* Fragile if the doc changes; use sparingly.

**Use `replace_text` for** simple find/replace transforms.

* Good for consistent renames or small substitutions.
* Dangerous if your “old text” matches too broadly—be explicit.


**Use `replace_section` when** you’re updating a named section that has a stable marker like:
`<!-- ID: section_name -->`

* Example pattern: “Update the ‘Constraints’ section in ARCHITECTURE_GUIDE.”
* Preferred for maintaining long-lived docs because it avoids line drift.
* Always prefer `apply_patch` over replace_section, this tool is meant to be used only during the templating/bootstrapping of initial plan documents.  It will overwrite/duplicate content.

**Use `append` when** you’re adding a new block at the end (notes, findings, new subsection).

* Example pattern: “Append a new decision record / findings block.”
* Do *not* use append for checklist state changes (use `status_update`).

**Use `status_update` when** the change is “mark checklist items done” and attach proof.

* Example pattern: “Mark CHECKLIST item X as complete with test output reference.”
* Always include proof metadata (what verified it, where, and when).

**Use `normalize_headers` / `generate_toc` when** you want doc formatting to be standardized.

* Use after major structural edits, not constantly.

**Use `validate_crosslinks` when** the doc has internal links you might have broken.

* Run after reorganizing sections or renaming docs.

### Special document creation (templated “create_*” actions)

These are for creating structured docs that have a defined lifecycle and indexing:

* `create_research_doc` → creates a research report + updates `research/INDEX.md`
* `create_bug_report` → creates a bug report + updates `docs/bugs/INDEX.md`
* `create_review_report` → creates a review report + updates review index
* `create_agent_report_card` → creates evaluation + updates its index

**When to use these:** whenever you’re generating a **new report artifact** that should be discoverable later.
**When NOT to use these:** for routine progress logging (that’s `append_entry`) or repo-wide cases (that’s Sentinel mode case tools).

### Introspection actions (to avoid guessing)

Use these to locate structure before doing precise edits:

**Use `list_sections` when** you need to know what section IDs exist and where they live.

* Pair with `replace_section` or to find anchors.

**Use `list_checklist_items` when** you want the checklist items + line numbers + status.

* Pair with `status_update` to avoid mismatches.

### Lifecycle action

**Use `create_doc` when** you need a brand new managed document registered in project state.

* This is for “new managed doc types” within a project, not random repo files.
* Use `metadata.register_existing=true` to register an existing doc without writing content.

---

## Safe usage patterns (what agents should actually do)

### Pattern A: Update an architecture section safely

1. Rehydrate: `read_recent` / `query_entries` for relevant context
2. Inspect: `manage_docs(action="list_sections", doc_name="architecture")` if unsure
3. Edit: `manage_docs(action="replace_section", doc_name="architecture", section="constraints", content=...)`
4. Verify: tests or reasoning consistency check
5. Log: `append_entry` with what changed and why

### Pattern B: Close a checklist item with proof

1. Find item: `manage_docs(action="list_checklist_items", doc_name="checklist")`
2. Run tests / verification
3. Update item: `manage_docs(action="status_update", doc_name="checklist", section=..., metadata={"status": "done", "proof": "..."})`
4. Log: `append_entry` summarizing proof + link to outputs

### Pattern C: Create a bug report artifact

1. Confirm Project Mode is active
2. Create report: `manage_docs(action="create_bug_report", metadata={"category": "infrastructure", "slug": "my-bug", "severity": "medium", "title": "Bug description"})`
3. Log: `append_entry` with bug summary + link to report path

### Pattern D: Create + register a new managed doc

1. Confirm Project Mode is active
2. Create doc: `manage_docs(action="create_doc", doc_name="DECISION_LOG", content="# Decision Log\n\n...", metadata={"register_doc": true})`
3. Log: `append_entry` with doc purpose and location

---

## Hard rules (to prevent freestyle)

* `manage_docs` is **Project Mode only**. No project → no doc management.
* Use `doc_name` for registered docs (architecture, phase_plan, checklist) and `create_research_doc`.
* `doc_category` is semantic only (classification/filtering) and must not be used as a filename or registry key.
* For `create_bug_report`, category comes from `metadata.category`; `doc_name` is optional.
* `create_doc` requires content via `content` or `metadata.body`/`metadata.snippet`/`metadata.sections`.
* If an edit action fails with DOC_NOT_FOUND and the file exists, rely on auto-registration or use `create_doc` with `register_existing=true`.
* `edit` works for `apply_patch` to provide patch details (dict with type/start_line/end_line/content).
* Don't invent action names or parameters. If an action isn't supported: **stop and request a tool update**.  Be sure to check `references/Scribe_Usage.md` first.
* Prefer `replace_range` / `apply_patch` over whole-file rewrites. `read_file` can provide exact line numbers.
* `append_entry` is for progress logging; `manage_docs` is for managed doc artifacts. Use both when appropriate.

---

## Notes

- If a tool is unavailable (e.g., vector tools without plugin), stop and note the blocker; do not invent behaviors.
- Keep this skill minimal; link to wiki/code for extended rationale.
