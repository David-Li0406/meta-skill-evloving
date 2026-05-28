# Batch Operations Reference

Guide for creating and updating Azure DevOps work items in batches using the MCP server.

## Key Principles

### Batch Size
- **Optimal batch size: 10 items**
- MCP server performs best with batches of 10 or fewer
- Larger batches may timeout or fail
- Process multiple batches sequentially

### Error Handling
- Process batches sequentially to detect failures early
- If a batch fails, identify which items succeeded before retrying
- Log work item IDs from successful batches for tracking

## Batch Creation

Create multiple work items in batches of 10.

### Step 1: Prepare Data Array

```json
[
  {
    "work_item_type": "User Story",
    "id": "6.1.1",
    "name": "Backend Foundation",
    "description": "Initialize FastAPI...",
    "priority": "High",
    "status": "Planning",
    "objective_ucp": 45.2,
    "tasks": [...]
  },
  {
    "work_item_type": "User Story",
    "id": "6.1.2",
    "name": "Frontend Setup",
    ...
  }
]
```

### Step 2: Generate Batches

```bash
python scripts/create_work_items_batch.py \
  --project "AI Traceability SOC Monitoring" \
  --data '[...]' \
  --operation create \
  --batch-size 10 \
  --pretty
```

**Output Structure:**
```json
{
  "batches": [
    {
      "batch_number": 1,
      "mcp_tool": "mcp__azure-devops__wit_create_work_item",
      "items": [
        {
          "project": "AI Traceability SOC Monitoring",
          "workItemType": "User Story",
          "fields": [...]
        }
      ]
    }
  ],
  "summary": {
    "total_items": 15,
    "total_batches": 2,
    "batch_size": 10
  }
}
```

### Step 3: Execute Batches

Process each batch using a loop:

```
For each batch in batches:
  For each item in batch.items:
    Call mcp__azure-devops__wit_create_work_item(
      project: item.project,
      workItemType: item.workItemType,
      fields: item.fields
    )
    Capture work_item_id from response
```

## Batch Updates

Update multiple work items efficiently (e.g., bulk assignment, state changes).

### Step 1: Prepare Updates Array

```json
[
  {
    "id": 923,
    "path": "/fields/System.AssignedTo",
    "value": "keith.lampe@onshoreoutsourcing.com",
    "op": "Add"
  },
  {
    "id": 924,
    "path": "/fields/System.AssignedTo",
    "value": "keith.lampe@onshoreoutsourcing.com",
    "op": "Add"
  }
]
```

### Step 2: Generate Update Batches

```bash
python scripts/create_work_items_batch.py \
  --data '[...]' \
  --operation update \
  --batch-size 10 \
  --pretty
```

**Output Structure:**
```json
{
  "batches": [
    {
      "batch_number": 1,
      "mcp_tool": "mcp__azure-devops__wit_update_work_items_batch",
      "updates": [
        {"id": 923, "path": "/fields/System.AssignedTo", "value": "...", "op": "Add"},
        {"id": 924, "path": "/fields/System.AssignedTo", "value": "...", "op": "Add"}
      ]
    }
  ],
  "summary": {
    "total_updates": 15,
    "total_batches": 2,
    "batch_size": 10
  }
}
```

### Step 3: Execute Update Batches

Process batches using the batch update MCP tool:

```
For each batch in batches:
  Call mcp__azure-devops__wit_update_work_items_batch(
    updates: batch.updates
  )
  Verify all updates succeeded
```

## Common Batch Operations

### Bulk Assignment

Assign 15 work items to a user in batches of 10:

```json
[
  {"id": 923, "path": "/fields/System.AssignedTo", "value": "user@example.com"},
  {"id": 924, "path": "/fields/System.AssignedTo", "value": "user@example.com"},
  ...
  {"id": 937, "path": "/fields/System.AssignedTo", "value": "user@example.com"}
]
```

### Bulk State Change

Move multiple items to "Active":

```json
[
  {"id": 923, "path": "/fields/System.State", "value": "Active"},
  {"id": 924, "path": "/fields/System.State", "value": "Active"},
  ...
]
```

### Bulk Priority Update

Set priority for multiple items:

```json
[
  {"id": 923, "path": "/fields/Microsoft.VSTS.Common.Priority", "value": "1"},
  {"id": 924, "path": "/fields/Microsoft.VSTS.Common.Priority", "value": "1"},
  ...
]
```

## Update Operations

### Operation Types (`op` field)

- **`Add`**: Add or update a field (most common)
- **`Replace`**: Replace existing value
- **`Remove`**: Remove field value

Most updates use `Add` (default in script).

### Field Path Format

Field paths use JSON Patch format:
- `/fields/System.Title`
- `/fields/System.State`
- `/fields/System.AssignedTo`
- `/fields/Microsoft.VSTS.Common.Priority`
- `/fields/Custom.ObjectiveUCP`

See `devops-fields.md` for complete field reference.

## Batch Linking

Link multiple work items to parents in batches.

### Step 1: Prepare Link Updates

```json
[
  {"id": 923, "linkToId": 908, "type": "parent"},
  {"id": 924, "linkToId": 909, "type": "parent"},
  ...
]
```

### Step 2: Process in Batches

```bash
For each batch of 10 links:
  Call mcp__azure-devops__wit_work_items_link(
    project: "ProjectName",
    updates: batch
  )
```

## Performance Tips

1. **Sequential Processing**: Process batches one at a time, not in parallel
2. **Batch Size**: Stick to 10 items per batch for reliability
3. **Error Recovery**: Log successful item IDs before each batch
4. **Rate Limiting**: Add small delays between batches if needed (e.g., 1 second)
5. **Validation**: Verify data before batching to avoid partial failures

## Error Scenarios

### Partial Batch Failure

If batch fails midway:
1. Check which items completed successfully
2. Create new batch with remaining items
3. Retry failed items

### Field Validation Errors

Common causes:
- Invalid field names (check `devops-fields.md`)
- Missing required fields
- Invalid field values (wrong type or format)
- Parent work item doesn't exist (for linking)

### Timeout

If MCP server times out:
- Reduce batch size (try 5 items)
- Simplify field data (remove unnecessary fields)
- Check network connectivity

## Example Workflows

### Workflow 1: Bulk Create User Stories

```bash
# Step 1: Parse all markdown files
for file in sprint-*.md; do
  python scripts/parse_markdown.py $file >> items.json
done

# Step 2: Format for batch creation
python scripts/create_work_items_batch.py \
  --project "ProjectName" \
  --data "$(cat items.json)" \
  --operation create \
  --batch-size 10 \
  --pretty > batches.json

# Step 3: Process batches with Claude/MCP
# (Claude processes batches.json and calls MCP tools)
```

### Workflow 2: Bulk Update Assignments

```bash
# Step 1: Generate update list (from work item IDs 923-937)
python -c "
import json
updates = [
  {'id': i, 'path': '/fields/System.AssignedTo', 'value': 'user@example.com'}
  for i in range(923, 938)
]
print(json.dumps(updates))
" > updates.json

# Step 2: Format for batch update
python scripts/create_work_items_batch.py \
  --data "$(cat updates.json)" \
  --operation update \
  --batch-size 10 \
  --pretty > update_batches.json

# Step 3: Execute batches via MCP
# (Claude processes update_batches.json)
```

### Workflow 3: Bulk Linking

```bash
# Create links for User Stories to Features
python -c "
import json
links = [
  {'id': 938, 'linkToId': 917, 'type': 'parent'},
  {'id': 939, 'linkToId': 917, 'type': 'parent'},
  # ... more links
]
print(json.dumps(links))
" > links.json

# Process in batches with wit_work_items_link tool
# (use standard batch approach with 10 items per batch)
```

## Validation Checklist

Before executing batches:
- [ ] Batch size is 10 or less
- [ ] All required fields present for each item
- [ ] Parent work items exist (for creation with hierarchy)
- [ ] Field paths are correct (for updates)
- [ ] Operation type specified (for updates)
- [ ] Project name is correct
- [ ] Data format validated (JSON array)

## Troubleshooting

### Issue: Batch takes too long
**Solution**: Reduce batch size to 5, ensure simple field data

### Issue: Random failures
**Solution**: Process batches sequentially, add 1-second delay between batches

### Issue: Missing work item IDs
**Solution**: Verify parent work items exist, check ID format

### Issue: Field update fails
**Solution**: Verify field name in `devops-fields.md`, check value format

## Best Practices

1. **Test First**: Try single item before batching
2. **Log Progress**: Track which batches completed successfully
3. **Validate Data**: Check all fields before batch processing
4. **Handle Errors**: Plan for partial failures and retries
5. **Document IDs**: Save work item IDs from each batch for reference
