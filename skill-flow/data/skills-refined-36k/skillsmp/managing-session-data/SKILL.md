---
name: managing-session-data
description: >-
  Guides agents through managing acquisition session data using the sl-manage MCP server. Covers preprocessing sessions
  (single, by animal, by project, or all available), transferring animals between projects with health checks, and
  deleting sessions with mandatory user confirmation. Use when users ask to preprocess, migrate, or delete session data.
---

# Managing Session Data

Guides agents through managing acquisition session data using MCP tools from the sl-manage MCP server. Supports session
preprocessing, animal migration between projects, and session deletion with mandatory safety confirmations.

---

## MCP Server Requirements

This skill requires the sl-manage MCP server for management operations and the sl-get MCP server for discovery.

| Server    | CLI Command     | Purpose                                           |
|-----------|-----------------|---------------------------------------------------|
| sl-manage | `sl-manage mcp` | Session preprocessing, deletion, animal migration |
| sl-get    | `sl-get mcp`    | Project listing, session discovery                |

If a required MCP server is unavailable, inform the user which server is needed and the command to start it.

### MCP Server Verification

**Before performing any data management operation, verify the required MCP servers are running.**

**Verification workflow:**

1. **Test sl-get connectivity**: Run `get_projects_tool()` as a connectivity check
   - If successful: sl-get MCP server is running
   - If fails: Inform user to start with `sl-get mcp`

2. **Test sl-manage connectivity** (before preprocessing/deletion/migration): Attempt the operation
   - If the tool fails with a connection error: Inform user to start with `sl-manage mcp`

**Verification checklist for each workflow:**

```text
MCP Server Verification:
- [ ] Attempted get_projects_tool() to verify sl-get MCP server
- [ ] If using management tools: confirmed sl-manage MCP server is running
- [ ] Reported any connection failures with start commands
```

**Important:** Always verify MCP server availability before presenting workflow options to the user. This prevents
failed operations partway through a workflow.

---

## When to Use This Skill

**Preprocessing sessions:**
- "Preprocess all sessions for project X"
- "Preprocess all sessions for animal 12345"
- "Preprocess the session at /path/to/session"
- "Preprocess all available sessions"

**Transferring animals:**
- "Move animal 12345 from project A to project B"
- "Transfer the animal to a different project"
- "Migrate animal data between projects"

**Deleting sessions:**
- "Delete the session at /path/to/session"
- "Remove failed session data"
- "Clean up the broken session"

---

## Available MCP Tools

### Management Tools (sl-manage MCP)

| Tool                      | Purpose                                               |
|---------------------------|-------------------------------------------------------|
| `preprocess_session_tool` | Preprocesses a single session's data                  |
| `delete_session_tool`     | Removes a session from all storage locations          |
| `migrate_animal_tool`     | Transfers all sessions for an animal between projects |

### Discovery Tools (sl-get MCP)

| Tool                | Purpose                                  |
|---------------------|------------------------------------------|
| `get_projects_tool` | Lists all projects in the data directory |

---

## Session Discovery

The MCP servers do not provide tools to list animals or sessions. You MUST discover sessions using filesystem patterns
with the Glob tool.

### Directory Structure

Sessions follow this filesystem layout:
```text
{root_directory}/
└── {project}/
    └── {animal_id}/
        └── {session_name}/
            └── raw_data/
                └── session_data.yaml
```

### Discovering Sessions by Project

```text
Glob pattern: {root_directory}/{project}/**/session_data.yaml
```

### Discovering Sessions by Animal

```text
Glob pattern: {root_directory}/*/{animal_id}/**/session_data.yaml
```

### Discovering All Sessions

```text
Glob pattern: {root_directory}/**/session_data.yaml
```

### Extracting Session Path

The session directory is two levels above the `session_data.yaml` file:
```python
session_path = session_data_yaml_path.parents[1]
```

---

## Preprocessing Workflow

Preprocessing aggregates session data, compresses mesoscope frames, updates Google Sheets logs, and transfers data to
long-term storage (NAS and BioHPC server).

### Single Session

```text
preprocess_session_tool(session_path="/path/to/project/animal/session")
-> Session preprocessed: /path/to/project/animal/session
```

### Multiple Sessions (by project, animal, or all)

You MUST follow this workflow for bulk preprocessing:

1. **Get the working directory** using the acquisition-system-setup skill's `get_working_directory_tool()`
2. **Discover sessions** using Glob with appropriate patterns (see Session Discovery above)
3. **Present the list** of discovered sessions to the user for confirmation
4. **Preprocess each session** sequentially using `preprocess_session_tool`
5. **Report results** including any failures

**Workflow Checklist:**

```text
Bulk Preprocessing Progress:
- [ ] Step 1: Get working directory from system configuration
- [ ] Step 2: Discover sessions using Glob (by project/animal/all)
- [ ] Step 3: Present discovered sessions to user for confirmation
- [ ] Step 4: Preprocess each session sequentially
- [ ] Step 5: Report results (success count, failures)
```

### Example: Preprocess All Sessions for a Project

```text
Agent: I'll preprocess all sessions for project "my_project". Let me first discover the available sessions.

1. Get working directory:
   get_working_directory_tool()
   -> Working directory: /data/sun_lab_data

2. Discover sessions:
   Glob("/data/sun_lab_data/my_project/**/session_data.yaml")
   -> Found 5 session_data.yaml files

3. Extract session paths (two levels above each file):
   - /data/sun_lab_data/my_project/12345/20250115_session_1
   - /data/sun_lab_data/my_project/12345/20250116_session_2
   - /data/sun_lab_data/my_project/67890/20250115_session_1
   ...

4. Present to user: "I found 5 sessions to preprocess. Proceed?"

5. Preprocess each:
   preprocess_session_tool(session_path="/data/sun_lab_data/my_project/12345/20250115_session_1")
   preprocess_session_tool(session_path="/data/sun_lab_data/my_project/12345/20250116_session_2")
   ...

6. Report: "Successfully preprocessed 5 sessions."
```

---

## Animal Migration Workflow

Migration transfers all sessions for an animal from one project to another across all storage locations (VRPC, NAS, and
BioHPC server).

### Prerequisites

The migration tool enforces these health checks automatically:

1. **Target project must exist** - Create it first using `create_project_tool` if needed
2. **All local sessions must be preprocessed** - No unprocessed sessions can exist on the VRPC for the source animal
3. **Source animal must have sessions on the server** - Migration pulls data from the BioHPC server

### Migration Tool

```text
migrate_animal_tool(
    source_project="old_project",
    destination_project="new_project",
    animal_id="12345"
)
-> Animal 12345 migrated: old_project -> new_project
```

### Workflow Checklist

```text
Animal Migration Progress:
- [ ] Step 1: Verify source project exists (get_projects_tool)
- [ ] Step 2: Verify target project exists, create if needed (create_project_tool)
- [ ] Step 3: Check for unprocessed local sessions (Glob for session_data.yaml in source project)
- [ ] Step 4: If unprocessed sessions exist, preprocess them first
- [ ] Step 5: Confirm migration with user (source, destination, animal_id)
- [ ] Step 6: Execute migration (migrate_animal_tool)
- [ ] Step 7: Report completion
```

### Example Migration

```text
User: Move animal 12345 from project_a to project_b

Agent: I'll help migrate animal 12345 from project_a to project_b. Let me verify the prerequisites.

1. Check projects:
   get_projects_tool()
   -> Projects: project_a, project_b

2. Check for unprocessed sessions:
   Glob("/data/sun_lab_data/project_a/12345/**/session_data.yaml")
   -> Found 0 files (no unprocessed sessions on VRPC)

3. Confirm with user: "Ready to migrate animal 12345 from project_a to project_b. This will:
   - Pull all sessions from the server
   - Re-preprocess and transfer to the new project location
   - Remove old project data from all storage locations
   Proceed?"

4. Execute migration:
   migrate_animal_tool(source_project="project_a", destination_project="project_b", animal_id="12345")
   -> Animal 12345 migrated: project_a -> project_b
```

---

## Session Deletion Workflow

**CRITICAL: Session deletion is irreversible and removes data from ALL storage locations (VRPC, NAS, and BioHPC
server). You MUST always obtain explicit user confirmation before proceeding.**

### Mandatory Confirmation Requirements

You MUST follow this exact workflow for ALL deletion requests:

1. **Warn the user** about the consequences of deletion
2. **Use AskUserQuestion** to get explicit confirmation
3. **Only proceed** if the user explicitly confirms

**Never call `delete_session_tool` with `confirm_deletion=True` without first obtaining user confirmation through
AskUserQuestion.**

### delete_session_tool Parameters

| Parameter          | Type | Required | Description                                           |
|--------------------|------|----------|-------------------------------------------------------|
| `session_path`     | str  | Yes      | Absolute path to the session directory                |
| `confirm_deletion` | bool | No       | Must be True to execute deletion (default: False)     |

When called with `confirm_deletion=False` (the default), the tool returns a safety warning instead of deleting data.

### Deletion Workflow Checklist

```text
Session Deletion Progress:
- [ ] Step 1: Verify session path exists
- [ ] Step 2: Display deletion warning to user
- [ ] Step 3: Use AskUserQuestion to get explicit confirmation
- [ ] Step 4: If confirmed, execute deletion with confirm_deletion=True
- [ ] Step 5: Report result
```

### Example Deletion

```text
User: Delete the session at /data/sun_lab_data/project_a/12345/20250115_broken_session

Agent: I understand you want to delete the session at /data/sun_lab_data/project_a/12345/20250115_broken_session.

WARNING: This operation is IRREVERSIBLE and will:
- Remove the session from the local machine (VRPC)
- Remove the session from the NAS backup storage
- Remove the session from the BioHPC server
- Permanently delete all data associated with this session

[Uses AskUserQuestion with options: "Yes, permanently delete this session" / "No, cancel deletion"]

User selects: "Yes, permanently delete this session"

Agent: Proceeding with deletion...

delete_session_tool(
    session_path="/data/sun_lab_data/project_a/12345/20250115_broken_session",
    confirm_deletion=True
)
-> Session deleted: /data/sun_lab_data/project_a/12345/20250115_broken_session
```

### Bulk Deletion

For multiple session deletions, you MUST obtain confirmation for EACH session individually:

1. Present the complete list of sessions to be deleted
2. For EACH session in the list:
   - Display the session path and deletion warning
   - Use AskUserQuestion to get explicit confirmation for that specific session
   - Only proceed with deletion if the user confirms
   - Report the result before moving to the next session

**Batch confirmation is NOT allowed.** Each session deletion requires its own separate user confirmation. This ensures
the user consciously acknowledges each irreversible deletion.

```text
Bulk Deletion Progress:
- [ ] Step 1: Discover sessions to delete using Glob
- [ ] Step 2: Present full list to user
- [ ] For EACH session:
  - [ ] Display session path and deletion warning
  - [ ] Use AskUserQuestion to confirm THIS specific session
  - [ ] If confirmed: delete and report success
  - [ ] If declined: skip and continue to next session
- [ ] Step 3: Report final summary (deleted count, skipped count)
```

---

## Error Handling

### Common Errors

| Error                                          | Cause                                      | Solution                                    |
|------------------------------------------------|--------------------------------------------|---------------------------------------------|
| "Session directory must be inside root"        | Path is on NAS/server, not local VRPC      | Only process sessions in root_directory     |
| "target project does not exist"                | Destination project not created            | Use create_project_tool first               |
| "non-preprocessed session data"                | Unprocessed sessions exist for animal      | Preprocess all sessions before migration    |
| "requires explicit confirmation"               | confirm_deletion not set to True           | Get user confirmation, then set to True     |

### Session Path Validation

Sessions must be located inside the system's root directory (typically the local VRPC data directory). The MCP tools
will reject paths pointing to NAS or server storage locations.

To find the root directory:
```text
get_working_directory_tool()
-> Working directory: /path/to/sun_lab_data
```

The root directory is specified in the system configuration as `filesystem.root_directory`.

---

## Quick Reference

### Preprocessing

```text
# Single session
preprocess_session_tool(session_path="/path/to/session")

# Discover sessions (use Glob)
Glob("{root_directory}/{project}/**/session_data.yaml")  # By project
Glob("{root_directory}/*/{animal}/**/session_data.yaml") # By animal
Glob("{root_directory}/**/session_data.yaml")            # All sessions
```

### Migration

```text
# Check projects exist
get_projects_tool()

# Create target project if needed
create_project_tool(project="new_project")

# Migrate animal
migrate_animal_tool(source_project="old", destination_project="new", animal_id="12345")
```

### Deletion (ALWAYS CONFIRM FIRST)

```text
# Preview only (no deletion)
delete_session_tool(session_path="/path/to/session")

# After user confirmation via AskUserQuestion
delete_session_tool(session_path="/path/to/session", confirm_deletion=True)
```
