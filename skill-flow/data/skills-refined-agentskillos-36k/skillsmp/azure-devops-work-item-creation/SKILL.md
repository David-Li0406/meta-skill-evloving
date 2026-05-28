---
name: azure-devops-work-item-creation
description: Create Azure DevOps work items (Epics, Features, User Stories) from generated markdown documentation with automatic UCP calculation and parent-child linking. Use when creating epics in DevOps, creating features in DevOps, creating user stories in DevOps, or any Azure DevOps work item creation task. Ensures required fields are captured including Objective UCP and maintains naming consistency for traceability.
---

# Azure DevOps Work Item Creation

Automate creation of Azure DevOps work items from epic, feature, and sprint markdown files with automatic UCP calculation and proper hierarchical linking.

## Quick Start

Given an epic markdown file:
```bash
python scripts/parse_markdown.py epic-1-update-services.md
# � Extracts structured data

# Use ucp-calculator skill to calculate UCP from tasks

# Create work item in Azure DevOps with calculated UCP
```

## Core Workflow

### Step 1: Parse Markdown File

Execute `parse_markdown.py` to extract structured data:

```bash
python scripts/parse_markdown.py <path_to_markdown> --pretty
```

**Output**: JSON with work_item_type, id, name, status, priority, description, tasks, parent_id, acceptance_criteria.

### Step 2: Calculate Objective UCP

**CRITICAL**: Use the `ucp-calculator` skill to calculate UCP from extracted tasks.

**Invoke the UCP skill**:
```
Use the ucp-calculator skill to calculate Objective UCP from these tasks:
[paste tasks array from Step 1 output]
```

The UCP skill will analyze task estimates and return the Objective UCP value.

### Step 3: Format for Azure DevOps

Execute `create_work_item.py` to format data for MCP tool:

```bash
python scripts/create_work_item.py \
  --project "ProjectName" \
  --data '<json_from_step1>' \
  --objective-ucp <ucp_from_step2> \
  --pretty
```

**Output**: JSON with `mcp_tool` and `parameters` ready for direct use.

### Step 4: Create Work Item

Call the Azure DevOps MCP tool with formatted parameters:

```
mcp__azure-devops__wit_create_work_item(
  project: <project_name>,
  workItemType: <type>,
  fields: <fields_array>
)
```

**Capture work item ID** from response.

### Step 5: Link Parent (if applicable)

If work item has a parent (Features link to Epics, User Stories link to Features):

1. **Find or create parent work item** first
2. **Link child to parent**:

```
mcp__azure-devops__wit_work_items_link(
  project: <project_name>,
  updates: [{
    id: <child_id>,
    linkToId: <parent_id>,
    type: "parent"
  }]
)
```

## Key Concepts

- **Work Item Types**: Epic (top level) � Feature (mid level) � User Story (sprint level)
- **Objective UCP**: Custom field calculated from task estimates using `ucp-calculator` skill
- **Hierarchical Linking**: Parent-child relationships must be established after creation
- **Title Format**: Consistent naming - "Epic 1: Name", "Feature 1.1: Name", "Sprint 1.1.1: Name"
- **Description**: Combines overview sections and acceptance criteria

## Available Resources

### Scripts

- **`scripts/parse_markdown.py`**  Extract structured data from epic/feature/sprint markdown files
  ```bash
  python scripts/parse_markdown.py <file_path> [--pretty]
  # Returns: JSON with all metadata, tasks, and acceptance criteria
  ```

- **`scripts/create_work_item.py`**  Format data for Azure DevOps MCP tool
  ```bash
  python scripts/create_work_item.py \
    --project "ProjectName" \
    --data '<json>' \
    --objective-ucp <value> \
    [--pretty]
  # Returns: Formatted MCP tool parameters
  ```


- **`scripts/create_work_items_batch.py`**  Format multiple work items for batch operations
  ```bash
  python scripts/create_work_items_batch.py \
    --project "ProjectName" \
    --data '[{...}, {...}]' \
    --operation create \
    --batch-size 10 \
    [--pretty]
  # Returns: Batched items ready for MCP tool execution

  # For batch updates:
  python scripts/create_work_items_batch.py \
    --data '[{"id": 923, "path": "/fields/System.AssignedTo", "value": "user@example.com"}]' \
    --operation update \
    --batch-size 10 \
    [--pretty]
  ```

### References

- **`references/priority-mapping.md`**  Priority and state mapping tables (CRITICAL�1, Planning�New, etc.)
- **`references/devops-fields.md`**  Required fields by work item type with linking instructions
- **`references/markdown-templates.md`**  Expected markdown format examples for epic/feature/sprint files
- **`references/batch-operations.md`**  Batch processing guide with best practices (batch size: 10)

## Output Format

Work items created with:

**Title**: "[Type] [ID]: [Name]"
- Example: "Epic 1: Update Existing Services"
- Example: "Feature 101.1: Core Architecture & TDD Implementation"

**Description**: Combined overview + acceptance criteria (HTML format)

**Required Fields**:
- System.Title
- System.Description (HTML)
- Microsoft.VSTS.Common.Priority (1-4)
- System.State (New, Active, Resolved, Closed)
- Custom.ObjectiveUCP (calculated via ucp-calculator skill)

**Effort Field** (User Stories only):
- Microsoft.VSTS.Scheduling.Effort = sum of task hours

**Parent Linking**:
- Features linked to Epics
- User Stories linked to Features

## Special Handling

### Epic Creation
- Top-level work item (no parent)
- Captures business context and success criteria
- Tasks extracted for UCP calculation

### Feature Creation
- **Requires**: Parent Epic must exist
- **Parent ID**: Inferred from Feature ID (Feature 101.1 � Epic 101)
- Create Epic first if it doesn't exist

### User Story (Sprint) Creation
- **Requires**: Parent Feature must exist
- **Parent ID**: Inferred from Sprint ID (Sprint 101.1.1 � Feature 101.1)
- Includes Effort field calculated from task hours
- Create Feature first if it doesn't exist

### Priority Mapping
| Markdown | DevOps |
|----------|--------|
| CRITICAL, HIGH | 1 |
| MEDIUM, NORMAL | 2 |
| LOW | 3 |

### State Mapping
| Markdown Status | DevOps State |
|-----------------|--------------|
| Planning, Ready for Implementation | New |
| In Progress, Active | Active |
| Completed, Done | Resolved |

## Error Handling

### Missing Parent
If parent work item doesn't exist:
1. Parse parent markdown file first
2. Create parent work item
3. Then create child with parent link

### Invalid Fields
If work item creation fails:
- Check `references/devops-fields.md` for required fields
- Verify project name is correct
- Ensure parent ID exists (for Features/User Stories)

### UCP Calculation Failure
If UCP skill returns error:
- Create work item WITHOUT Objective UCP field
- Log warning to update manually later
- UCP can be added via update operation

## Integration with Other Skills

This skill **orchestrates** with:

1. **`ucp-calculator`**  Calculate Objective UCP from task estimates
   - Invoked in Step 2 of workflow
   - Required for accurate UCP field population

2. **`onshore-git-workflow`**  Work item IDs used in commit messages
   - Format: `git commit -m "feat(#123): Description"`

3. **`baseline-analysis`**  References work items for project tracking
   - Work item IDs link code to planning artifacts

## Example: Complete Epic Creation

```bash
# Step 1: Parse epic markdown
python scripts/parse_markdown.py epic-1-update-services.md --pretty
# Output: {"work_item_type": "Epic", "id": "1", "tasks": [...], ...}

# Step 2: Calculate UCP (invoke ucp-calculator skill)
"Use ucp-calculator skill to calculate UCP from tasks: [paste tasks]"
# Output: Objective UCP = 23.5

# Step 3: Format for DevOps
python scripts/create_work_item.py \
  --project "Onshore-Catalog-Master" \
  --data '<json_from_step1>' \
  --objective-ucp 23.5 \
  --pretty
# Output: {"mcp_tool": "mcp__azure-devops__wit_create_work_item", "parameters": {...}}

# Step 4: Create work item
mcp__azure-devops__wit_create_work_item(
  project: "Onshore-Catalog-Master",
  workItemType: "Epic",
  fields: [...]
)
# Output: {"id": 804, "url": "https://..."}

# Step 5: No parent linking (Epic is top-level)
# Done! Work item created with ID 804
```

## Tips for Effective Use

1. **Always calculate UCP**  Don't skip Step 2; Objective UCP is critical for tracking
2. **Check parent hierarchy**  Create parent work items before children
3. **Use consistent naming**  Follow "[Type] [ID]: [Name]" format
4. **Capture acceptance criteria**  Include in description for traceability
5. **Link work items**  Parent-child relationships enable rollup reporting
6. **Verify project name**  Use exact Azure DevOps project name (case-sensitive)

## Validation Checklist

Before creating work item:
- [ ] Markdown file parsed successfully
- [ ] Objective UCP calculated via ucp-calculator skill
- [ ] Work item type correct (Epic/Feature/User Story)
- [ ] Parent work item exists (for Feature/User Story)
- [ ] Title follows naming convention
- [ ] Description includes overview and acceptance criteria
- [ ] Priority mapped correctly
- [ ] Project name is correct
