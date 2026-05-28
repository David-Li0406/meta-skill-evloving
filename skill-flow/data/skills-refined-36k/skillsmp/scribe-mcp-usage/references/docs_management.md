# Documentation (manage_docs + templates)

## Contents
- `manage_docs`
- `generate_doc_templates`

### `manage_docs`
**Purpose**: Structured documentation system for projects.

**Required Parameters:**
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
    action="replace_section",
    doc_name="architecture",  # REQUIRED: unique doc identifier
    section="problem_statement",
    content="## Problem Statement\n**Context:** ..."
)

# Append within a section
await manage_docs(
    action="append",
    doc_name="architecture",
    section="problem_statement",
    content="Updated scope paragraph",
    metadata={"position": "inside"}
)

# Update checklist status
await manage_docs(
    action="status_update",
    doc_name="checklist",
    section="phase_1_task_1",
    metadata={"status": "done", "proof": "code_review_completed"}
)

# Create research document (NEW SYNTAX - doc_type goes IN metadata)
await manage_docs(
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
    action="create",
    doc_name="COORDINATION_PROTOCOL",
    metadata={
        "doc_type": "custom",  # REQUIRED: specifies document type
        "body": "# Coordination Protocol\n\n..."
    }
)

# Apply unified patch (patch_mode defaults to "unified" when patch is provided)
await manage_docs(
    action="apply_patch",
    doc_name="architecture",
    patch="--- a/file.md\n+++ b/file.md\n@@ -10,3 +10,4 @@\n existing line\n+new line",
    dry_run=True  # Always dry_run first!
)

# Batch multiple updates (executed sequentially)
await manage_docs(
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

### `generate_doc_templates`
**Purpose**: Create/update documentation templates for a project.

**Required Parameters:**
- `project_name` (string): Name of the project

**Optional Parameters:**
- `author` (string): Document author
- `overwrite` (bool, default: false): Overwrite existing templates
- `documents` (list): Specific documents to generate
- `base_dir` (string): Base directory for templates

**Example Usage:**
```python
# Basic usage
await generate_doc_templates(project_name="my-project")

# With author and specific documents
await generate_doc_templates(
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
