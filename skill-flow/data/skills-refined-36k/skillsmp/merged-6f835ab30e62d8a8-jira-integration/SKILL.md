---
name: jira-integration
description: Use this skill for mapping SpecWeave increments to JIRA epics and stories, as well as syncing content and status between the two systems. Ideal for exporting increments to JIRA, importing JIRA epics, and troubleshooting sync issues.
---

# JIRA Integration Skill

This skill provides comprehensive guidance for mapping SpecWeave concepts to JIRA and synchronizing data between the two systems.

## Core Responsibilities

1. **Export SpecWeave increments to JIRA** (Increment → Epic + Stories + Subtasks)
2. **Import JIRA epics as SpecWeave increments** (Epic → Increment structure)
3. **Bidirectional Sync**: Content flows SpecWeave→JIRA, status flows JIRA→SpecWeave
4. **Maintain traceability** across systems (store keys, URLs, timestamps)
5. **Validate mapping accuracy** using test cases
6. **Handle edge cases** (missing fields, invalid statuses, API errors)

## Concept Mappings

### SpecWeave → JIRA

| SpecWeave Concept | JIRA Concept | Mapping Rules |
|-------------------|--------------|---------------|
| **Increment** | Epic | Title: `[Increment ###] [Title]` |
| **User Story** | Story | Linked to parent Epic, includes acceptance criteria |
| **Task** | Subtask | Linked to parent Story, checkbox → Subtask |
| **Acceptance Criteria** | Story Description | Formatted as checkboxes in Story description |
| **Priority P1** | Priority: Highest | Critical path, must complete |
| **Priority P2** | Priority: High | Important but not blocking |
| **Priority P3** | Priority: Medium | Nice to have |
| **Status: planned** | Status: To Do | Not started |
| **Status: in-progress** | Status: In Progress | Active work |
| **Status: completed** | Status: Done | Finished |
| **spec.md** | Epic Description | Summary + link to spec (if GitHub repo) |
| **context-manifest.yaml** | Custom Field: Context | Serialized YAML in custom field (optional) |

### JIRA → SpecWeave

| JIRA Concept | SpecWeave Concept | Import Rules |
|--------------|-------------------|--------------|
| **Epic** | Increment | Auto-number next available (e.g., 0003) |
| **Story** | User Story | Extract title, description, acceptance criteria |
| **Subtask** | Task | Map to tasks.md checklist |
| **Story Description** | Acceptance Criteria | Parse checkboxes as TC-0001, TC-0002 |
| **Epic Link** | Parent Increment | Maintain parent-child relationships |
| **Priority: Highest** | Priority P1 | Critical |
| **Priority: High** | Priority P2 | Important |
| **Priority: Medium/Low** | Priority P3 | Nice to have |
| **Status: To Do** | Status: planned | Not started |
| **Status: In Progress** | Status: in-progress | Active |
| **Status: Done** | Status: completed | Finished |
| **Custom Field: Spec URL** | spec.md link | Cross-reference |

## Conversion Workflows

### 1. Export: Increment → JIRA Epic

**Input**: `.specweave/increments/<increment_id>/`

**Prerequisites**:
- Increment folder exists
- `spec.md` exists with valid frontmatter
- `tasks.md` exists
- JIRA connection configured

**Process**:
1. Read increment files and extract necessary data.
2. Create JIRA Epic with the extracted information.
3. Create JIRA Stories for each user story.
4. Create JIRA Subtasks from tasks.md.
5. Update increment frontmatter with JIRA keys.

**Output**: Summary of exported items including Epic and Story keys.

### 2. Import: JIRA Epic → Increment

**Input**: JIRA Epic key (e.g., `PROJ-123`)

**Prerequisites**:
- Valid JIRA Epic key
- Epic exists and is accessible
- JIRA connection configured

**Process**:
1. Fetch Epic details and linked Stories/Subtasks from JIRA.
2. Auto-number the next increment.
3. Generate `spec.md` and `tasks.md` based on the fetched data.
4. Update JIRA Epic with the new SpecWeave Increment ID.

**Output**: Summary of imported items including Increment location.

### 3. Bidirectional Sync

**Trigger**: Manual (`/sync-jira`) or webhook

**Prerequisites**:
- Increment has JIRA metadata in frontmatter
- JIRA Epic/Stories exist
- Last sync timestamp available

**Process**:
1. Detect changes since the last sync.
2. Compare SpecWeave and JIRA for conflicts.
3. Present conflicts to the user for resolution.
4. Apply sync changes in both directions.
5. Update sync timestamps.

**Output**: Summary of changes applied during sync.

## Edge Cases and Error Handling

### Missing Fields

**Problem**: Increment missing `spec.md` or JIRA Epic missing required fields.

**Solution**: Provide actionable error messages indicating what is missing.

### JIRA API Errors

**Problem**: JIRA API rate limit, authentication failure, network error.

**Solution**: Display appropriate error messages and suggest next steps.

### Invalid Status Mapping

**Problem**: JIRA uses custom workflow statuses not in standard mapping.

**Solution**: Provide options for mapping unknown statuses.

### Conflict Resolution

**Problem**: Same field changed in both SpecWeave and JIRA.

**Solution**: Always ask the user for resolution and provide options.

## Best Practices

1. Always validate before sync.
2. Preserve traceability across systems.
3. Ask before overwriting any data.
4. Log all operations for audit purposes.
5. Handle errors gracefully with clear messages.
6. Test mappings regularly to ensure accuracy.

## Usage Examples

### Export to JIRA

```
User: "Export increment <increment_id> to JIRA"
```

### Import from JIRA

```
User: "Import JIRA epic <epic_key>"
```

### Bidirectional Sync

```
User: "Sync increment <increment_id> with JIRA"
```

**You are the authoritative mapper between SpecWeave and JIRA. Your conversions must be accurate, traceable, and reversible.**