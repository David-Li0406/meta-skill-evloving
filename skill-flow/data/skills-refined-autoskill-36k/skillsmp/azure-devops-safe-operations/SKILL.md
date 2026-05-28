---
name: azure-devops-safe-operations
description: Safe Azure DevOps operations wrapper using Azure DevOps MCP server. Validates operations before execution, provides rollback support, and enforces work item management best practices. Use for work item operations, queries, board management, and git operations with built-in safety checks. Always uses Azure DevOps MCP server for reliable, auditable operations.
---

# Azure DevOps Safe Operations

Wrapper for common Azure DevOps operations with safety checks, validation, and error handling via Azure DevOps MCP server.

## Quick Start

**Get work item safely:**
```
"Get work item 1234 from project MyProject"
```

**Query work items:**
```
"Query all active User Stories assigned to me in current sprint"
```

**Create work item with validation:**
```
"Create Task in project MyProject with title 'Implement authentication' and description 'Add JWT validation'"
```

**Update work item safely:**
```
"Update work item 1234 to Ready for Testing status with implementation summary"
```

## Core Operations

### Operation 1: Get Work Item

**Purpose**: Retrieve work item details with validation

**Pre-Checks**:
- ✅ Work item ID is valid (numeric)
- ✅ Project exists
- ✅ MCP server configured

**MCP Operation**:
```
mcp__azure-devops__wit_get_work_item(
  project: "MyProject",
  id: 1234
)
```

**Response Validation**:
- Work item exists (not null)
- Work item has expected fields (id, title, state)
- Work item type valid (Task, User Story, Bug, etc.)

**Error Handling**:
- Work item not found (404) → Return error with suggestion to verify ID
- Invalid project → Return error with valid project list
- Permission denied → Return error with required permissions

---

### Operation 2: Query Work Items

**Purpose**: Query work items with WIQL (Work Item Query Language)

**Pre-Checks**:
- ✅ WIQL query is valid syntax
- ✅ Project exists
- ✅ Referenced fields exist

**MCP Operation**:
```
mcp__azure-devops__wit_query_work_items(
  project: "MyProject",
  wiql: "SELECT [System.Id], [System.Title], [System.State] FROM WorkItems WHERE [System.WorkItemType] = 'Task' AND [System.State] = 'Active' ORDER BY [System.ChangedDate] DESC"
)
```

**Common Query Patterns**:

**My active work items:**
```sql
SELECT [System.Id], [System.Title], [System.State]
FROM WorkItems
WHERE [System.AssignedTo] = @Me
  AND [System.State] <> 'Closed'
  AND [System.State] <> 'Removed'
ORDER BY [System.ChangedDate] DESC
```

**Current sprint items:**
```sql
SELECT [System.Id], [System.Title], [System.State]
FROM WorkItems
WHERE [System.IterationPath] = @CurrentIteration
  AND [System.WorkItemType] IN ('User Story', 'Task', 'Bug')
ORDER BY [System.State], [Microsoft.VSTS.Common.Priority]
```

**Bugs by priority:**
```sql
SELECT [System.Id], [System.Title], [Microsoft.VSTS.Common.Priority]
FROM WorkItems
WHERE [System.WorkItemType] = 'Bug'
  AND [System.State] = 'Active'
ORDER BY [Microsoft.VSTS.Common.Priority], [System.CreatedDate]
```

**Response Validation**:
- Query returned results
- Results contain expected fields
- No query timeout errors

---

### Operation 3: Create Work Item

**Purpose**: Create new work item with validation

**Pre-Checks**:
- ✅ Required fields provided (title, work item type)
- ✅ Work item type valid (Task, User Story, Bug, Feature, Epic)
- ✅ Project exists
- ✅ Title not empty
- ✅ Assigned user exists (if provided)
- ✅ Area path exists (if provided)
- ✅ Iteration path exists (if provided)

**MCP Operation**:
```
mcp__azure-devops__wit_create_work_item(
  project: "MyProject",
  workItemType: "Task",
  fields: {
    "System.Title": "Implement JWT authentication",
    "System.Description": "<p>Add JWT token validation to API endpoints</p>",
    "System.AssignedTo": "user@example.com",
    "System.AreaPath": "MyProject\\Backend",
    "System.IterationPath": "MyProject\\Sprint 5",
    "Microsoft.VSTS.Scheduling.RemainingWork": 8,
    "Microsoft.VSTS.Common.Priority": 2
  }
)
```

**Field Validation**:

**Required fields:**
- `System.Title` - Must not be empty, max 255 characters

**Common optional fields:**
- `System.Description` - HTML formatted description
- `System.AssignedTo` - Email or display name
- `System.State` - Initial state (defaults to "New")
- `System.AreaPath` - Area path (must exist)
- `System.IterationPath` - Sprint/iteration (must exist)
- `Microsoft.VSTS.Scheduling.RemainingWork` - Hours remaining
- `Microsoft.VSTS.Common.Priority` - 1-4 (1=highest)

**Response Validation**:
- Work item created successfully
- Work item ID returned
- All fields set correctly

---

### Operation 4: Update Work Item

**Purpose**: Update work item fields with validation

**Pre-Checks**:
- ✅ Work item exists
- ✅ Current work item state known
- ✅ State transition valid (if changing state)
- ✅ Required fields for state provided
- ✅ No duplicate updates

**MCP Operation**:
```
mcp__azure-devops__wit_update_work_items_batch(
  project: "MyProject",
  updates: [
    {
      id: 1234,
      updates: [
        {
          op: "add",
          path: "/fields/System.State",
          value: "Ready for Testing"
        },
        {
          op: "add",
          path: "/fields/System.History",
          value: "<p><b>Implementation Complete</b></p><p>Implemented JWT authentication with tests.</p>"
        }
      ]
    }
  ]
)
```

**Update Operations**:

**op: "add"** - Add or update field value
**op: "remove"** - Remove field value
**op: "replace"** - Replace existing value
**op: "test"** - Test field has expected value before update

**Common Update Patterns**:

**Update state:**
```json
{
  "op": "add",
  "path": "/fields/System.State",
  "value": "Active"
}
```

**Add comment:**
```json
{
  "op": "add",
  "path": "/fields/System.History",
  "value": "<p>Moved to active, starting implementation.</p>"
}
```

**Update assigned user:**
```json
{
  "op": "add",
  "path": "/fields/System.AssignedTo",
  "value": "user@example.com"
}
```

**Link to another work item:**
```json
{
  "op": "add",
  "path": "/relations/-",
  "value": {
    "rel": "System.LinkTypes.Related",
    "url": "https://dev.azure.com/org/project/_apis/wit/workItems/5678"
  }
}
```

**State Transition Validation**:
- Check valid state transitions for work item type
- Verify required fields for target state
- Warn if invalid transition

---

### Operation 5: Batch Update Work Items

**Purpose**: Update multiple work items in single operation

**Pre-Checks**:
- ✅ All work item IDs valid
- ✅ All work items exist
- ✅ All updates valid
- ✅ No conflicting updates

**MCP Operation**:
```
mcp__azure-devops__wit_update_work_items_batch(
  project: "MyProject",
  updates: [
    {
      id: 1234,
      updates: [...]
    },
    {
      id: 5678,
      updates: [...]
    }
  ]
)
```

**Validation**:
- All work items updated successfully
- No partial failures
- All state transitions valid

**Error Handling**:
- If any update fails, report which work item failed
- Provide rollback guidance if needed

---

### Operation 6: Get Work Item Relations

**Purpose**: Get related work items (parent, child, related)

**Pre-Checks**:
- ✅ Work item ID valid
- ✅ Work item exists

**MCP Operation**:
```
mcp__azure-devops__wit_get_work_item(
  project: "MyProject",
  id: 1234,
  expand: "relations"
)
```

**Parse Relations**:
```typescript
const workItem = await mcp__azure-devops__wit_get_work_item(...);

// Extract relations
const relations = workItem.relations || [];

// Parse by type
const parentLinks = relations.filter(r => r.rel === "System.LinkTypes.Hierarchy-Reverse");
const childLinks = relations.filter(r => r.rel === "System.LinkTypes.Hierarchy-Forward");
const relatedLinks = relations.filter(r => r.rel === "System.LinkTypes.Related");
const hyperlinks = relations.filter(r => r.rel === "Hyperlink");
```

---

### Operation 7: Validate State Transition

**Purpose**: Check if state transition is valid before updating

**Pre-Checks**:
- ✅ Work item type known
- ✅ Current state known
- ✅ Target state provided

**Validation Logic**:
```typescript
const stateTransitions = {
  Task: {
    "New": ["Active", "Removed"],
    "Active": ["Closed", "Removed"],
    "Closed": ["Active", "New"],
    "Removed": []
  },
  "User Story": {
    "New": ["Active", "Removed"],
    "Active": ["Resolved", "Removed"],
    "Resolved": ["Closed", "Active"],
    "Closed": ["Active"],
    "Removed": []
  },
  Bug: {
    "New": ["Active", "Resolved", "Removed"],
    "Active": ["Resolved", "Removed"],
    "Resolved": ["Closed", "Active"],
    "Closed": ["Active"],
    "Removed": []
  }
};

function isValidTransition(workItemType, currentState, targetState) {
  const validStates = stateTransitions[workItemType]?.[currentState] || [];
  return validStates.includes(targetState);
}
```

**Return**:
```json
{
  "valid": true,
  "currentState": "Active",
  "targetState": "Closed",
  "workItemType": "Task"
}
```

Or if invalid:
```json
{
  "valid": false,
  "currentState": "New",
  "targetState": "Closed",
  "workItemType": "Task",
  "validTransitions": ["Active", "Removed"],
  "message": "Cannot transition from New to Closed. Valid transitions: Active, Removed"
}
```

---

## Safety Checks

### Pre-Operation Validation

**Work Item Existence Check**:
```python
def validate_work_item_exists(project, work_item_id):
    """Verify work item exists before operating on it."""
    try:
        work_item = mcp__azure_devops__wit_get_work_item(
            project=project,
            id=work_item_id
        )
        return {"exists": True, "work_item": work_item}
    except Exception as e:
        return {
            "exists": False,
            "error": str(e),
            "suggestion": f"Verify work item {work_item_id} exists in project {project}"
        }
```

**Project Validation**:
```python
def validate_project_exists(project):
    """Verify project exists before operating."""
    # Query any work item in project
    try:
        result = mcp__azure_devops__wit_query_work_items(
            project=project,
            wiql="SELECT [System.Id] FROM WorkItems WHERE [System.Id] = 1"
        )
        return {"exists": True}
    except Exception as e:
        if "project not found" in str(e).lower():
            return {
                "exists": False,
                "error": f"Project '{project}' not found",
                "suggestion": "Verify project name or check permissions"
            }
        return {"exists": True}  # Other errors don't indicate project missing
```

**Field Validation**:
```python
def validate_required_fields(work_item_type, fields):
    """Validate required fields present for work item type."""
    required = {
        "Task": ["System.Title"],
        "User Story": ["System.Title"],
        "Bug": ["System.Title"],
        "Feature": ["System.Title"],
        "Epic": ["System.Title"]
    }

    missing = []
    for field in required.get(work_item_type, []):
        if field not in fields or not fields[field]:
            missing.append(field)

    if missing:
        return {
            "valid": False,
            "missing_fields": missing,
            "message": f"Missing required fields: {', '.join(missing)}"
        }
    return {"valid": True}
```

---

### Post-Operation Validation

**Verify Work Item Created**:
```python
def verify_work_item_created(project, work_item_id):
    """Verify work item was created successfully."""
    result = validate_work_item_exists(project, work_item_id)
    if not result["exists"]:
        return {
            "success": False,
            "message": f"Work item {work_item_id} not found after creation"
        }
    return {"success": True, "work_item": result["work_item"]}
```

**Verify Update Applied**:
```python
def verify_update_applied(project, work_item_id, expected_state):
    """Verify work item update was applied."""
    work_item = mcp__azure_devops__wit_get_work_item(
        project=project,
        id=work_item_id
    )

    actual_state = work_item["fields"]["System.State"]
    if actual_state != expected_state:
        return {
            "success": False,
            "expected": expected_state,
            "actual": actual_state,
            "message": f"Expected state '{expected_state}' but got '{actual_state}'"
        }
    return {"success": True}
```

---

## Operation Examples

### Example 1: Create Task with Validation

**Scenario**: Create new task for implementing feature

**Operation**:
```markdown
## Create Task: Implement JWT Authentication

**Pre-Checks**:
- ✅ Project "MyProject" exists
- ✅ Title provided and valid length
- ✅ Work item type "Task" is valid
- ✅ Assigned user "dev@example.com" exists
- ✅ Area path "MyProject\\Backend" exists
- ✅ Iteration path "MyProject\\Sprint 5" exists

**MCP Operation**:
```
mcp__azure-devops__wit_create_work_item(
  project: "MyProject",
  workItemType: "Task",
  fields: {
    "System.Title": "Implement JWT authentication",
    "System.Description": "<p>Add JWT token validation to API endpoints</p><ul><li>Validate token signature</li><li>Check token expiration</li><li>Extract user claims</li></ul>",
    "System.AssignedTo": "dev@example.com",
    "System.AreaPath": "MyProject\\Backend",
    "System.IterationPath": "MyProject\\Sprint 5",
    "Microsoft.VSTS.Scheduling.RemainingWork": 8,
    "Microsoft.VSTS.Common.Priority": 2
  }
)
```

**Post-Validation**:
- ✅ Work item created with ID 1234
- ✅ All fields set correctly
- ✅ Work item accessible at URL
- ✅ Work item in correct project and area

**Result**: SUCCESS - Task #1234 created
```

---

### Example 2: Query and Update Multiple Work Items

**Scenario**: Update all active tasks in current sprint to "Ready for Testing"

**Operation**:
```markdown
## Batch Update: Sprint Tasks to Ready for Testing

**Step 1: Query Active Tasks**
```
mcp__azure-devops__wit_query_work_items(
  project: "MyProject",
  wiql: "SELECT [System.Id] FROM WorkItems WHERE [System.WorkItemType] = 'Task' AND [System.State] = 'Active' AND [System.IterationPath] = @CurrentIteration"
)
```

**Result**: Found 5 tasks [1234, 1235, 1236, 1237, 1238]

**Step 2: Validate State Transitions**
For each task:
- ✅ Current state: Active
- ✅ Target state: Ready for Testing
- ✅ Transition valid

**Step 3: Batch Update**
```
mcp__azure-devops__wit_update_work_items_batch(
  project: "MyProject",
  updates: [
    {
      id: 1234,
      updates: [
        { op: "add", path: "/fields/System.State", value: "Ready for Testing" },
        { op: "add", path: "/fields/System.History", value: "<p>Sprint complete, ready for QA</p>" }
      ]
    },
    // ... repeat for 1235, 1236, 1237, 1238
  ]
)
```

**Post-Validation**:
- ✅ All 5 work items updated
- ✅ All states changed to "Ready for Testing"
- ✅ Comments added to each work item

**Result**: SUCCESS - 5 tasks updated
```

---

### Example 3: Get Work Item with Relations

**Scenario**: Get user story with all child tasks

**Operation**:
```markdown
## Get User Story #5678 with Children

**Pre-Checks**:
- ✅ Work item 5678 exists
- ✅ Work item is User Story type

**MCP Operation**:
```
mcp__azure-devops__wit_get_work_item(
  project: "MyProject",
  id: 5678,
  expand: "relations"
)
```

**Parse Relations**:
```typescript
const userStory = await mcp__azure_devops__wit_get_work_item(...);

// Extract child tasks
const childLinks = userStory.relations
  .filter(r => r.rel === "System.LinkTypes.Hierarchy-Forward");

const childIds = childLinks.map(link => {
  const url = link.url;
  const id = url.split('/').pop();
  return parseInt(id);
});

// Output: [1234, 1235, 1236]
```

**Query Child Details**:
For each child ID, get work item details

**Result**: User Story #5678 has 3 child tasks:
- Task #1234: Implement authentication (Active)
- Task #1235: Add unit tests (Active)
- Task #1236: Update documentation (New)
```

---

## Integration with Workflow

### During Implementation (`/implement-waves`)

After implementing wave:
1. Query work item for wave
2. Update work item with implementation summary
3. Link git commit to work item
4. Update state to "Ready for Testing"
5. Verify update successful

### During Sprint Planning

1. Query backlog items
2. Create tasks for user stories
3. Assign tasks to team members
4. Set iteration paths to current sprint
5. Verify all tasks created

### During Code Review

1. Get work item for PR
2. Verify work item in correct state
3. Add PR link to work item
4. Update work item with review comments

---

## Available Resources

### Scripts

- **scripts/query_work_items.py** — Query work items with WIQL
- **scripts/validate_state_transition.py** — Validate state transition before update
- **scripts/batch_update.py** — Batch update multiple work items
- **scripts/get_work_item_relations.py** — Get parent/child/related work items

### References

- **references/wiql-patterns.md** — Common WIQL query patterns
- **references/state-transitions.md** — Valid state transitions by work item type
- **references/field-reference.md** — Azure DevOps field reference
- **references/relation-types.md** — Work item relation types

---

## Success Criteria

- ✅ Operation validated before execution
- ✅ Operation executed via Azure DevOps MCP server
- ✅ Post-validation confirms success
- ✅ Clear error messages on failure
- ✅ Work items tracked and updated correctly

---

## Tips for Safe Operations

1. **Always validate first** - Check work item exists before operating
2. **Use MCP server** - Don't bypass with direct REST API calls
3. **Query before batch update** - Verify all work items exist
4. **Check state transitions** - Validate before updating state
5. **Use batch operations** - More efficient than individual updates
6. **Add comments** - Document why state changed
7. **Link commits** - Maintain traceability

---

## Common Issues and Solutions

### Issue 1: Work Item Not Found
**Problem**: Work item ID doesn't exist in project
**Solution**: Query work items to find correct ID, verify project name

### Issue 2: Invalid State Transition
**Problem**: Cannot transition from current state to target state
**Solution**: Check valid transitions for work item type, use intermediate state if needed

### Issue 3: Permission Denied
**Problem**: User doesn't have permission to update work item
**Solution**: Verify user has "Contributor" role in project, check area path permissions

### Issue 4: Field Doesn't Exist
**Problem**: Trying to update field that doesn't exist on work item type
**Solution**: Check field reference for work item type, verify field name spelling

### Issue 5: Batch Update Partial Failure
**Problem**: Some work items updated, others failed
**Solution**: Check error for each work item, retry failed items individually

---

**Last Updated**: 2025-01-30
