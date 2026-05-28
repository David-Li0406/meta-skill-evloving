---
name: mcp-manual-tests
description: Trigger Associate MCP tools and check results.
---

# Associate MCP Server Manual Testing

**IMPORTANT: You have direct access to MCP tools as functions. Call them directly - do NOT use HTTP, curl, scripts, or any other method.**

## How to Run Tests

The MCP tools are available to you as callable functions with the `mcp_associate_` prefix:

- `mcp_associate_add_memory` - Add a memory
- `mcp_associate_get_memory` - Get a memory by ID  
- `mcp_associate_search_memories` - Search memories
- `mcp_associate_update_memory` - Update a memory
- `mcp_associate_delete_memory` - Delete a memory
- `mcp_associate_create_plan` - Create a plan
- `mcp_associate_get_plan` - Get a plan by ID
- `mcp_associate_list_plans` - List plans
- `mcp_associate_update_plan` - Update a plan
- `mcp_associate_delete_plan` - Delete a plan
- `mcp_associate_create_task` - Create a task
- `mcp_associate_get_task` - Get a task by ID
- `mcp_associate_list_tasks` - List tasks
- `mcp_associate_update_task` - Update a task
- `mcp_associate_delete_task` - Delete a task
- `mcp_associate_get_related` - Get related nodes

**Call these tools directly like any other tool. Do NOT search for scripts, curl endpoints, or inspect code.**

## Test Sequence

Generate a unique test token first: `mcp-test-<current_timestamp>`

### Phase 1: Memory Lifecycle

1. Call `mcp_associate_add_memory` with content containing token, tags=["mcp-test"], type="Note"
   - Extract the `id` from response
2. Call `mcp_associate_get_memory` with extracted id - verify content matches
3. Call `mcp_associate_search_memories` with the token as query - verify memory found
4. Call `mcp_associate_update_memory` with extracted id, new content with " - updated" appended
5. Call `mcp_associate_get_memory` with extracted id - verify update applied

### Phase 2: Plan Lifecycle

1. Call `mcp_associate_create_plan` with name containing token, description="Test plan"
   - Extract the `id` from response (this is the plan_id)
2. Call `mcp_associate_get_plan` with extracted plan_id - verify name/description
3. Call `mcp_associate_list_plans` with status="active" - verify plan appears
4. Call `mcp_associate_update_plan` with extracted plan_id, new description="Updated description"
5. Call `mcp_associate_get_plan` with extracted plan_id - verify update applied

### Phase 3: Task Lifecycle

1. Call `mcp_associate_create_task` with content containing token, plan_ids=[extracted plan_id]
   - Extract the `id` from response (this is the task_id)
2. Call `mcp_associate_get_task` with extracted task_id - verify content and plan linkage
3. Call `mcp_associate_list_tasks` with plan_id filter - verify task appears
4. Call `mcp_associate_update_task` with extracted task_id, status="completed"
5. Call `mcp_associate_get_task` with extracted task_id - verify status updated

### Phase 4: Relationship Tests

1. Call `mcp_associate_get_related` with plan_id - should show the task
2. Call `mcp_associate_get_related` with task_id - should show the plan

### Phase 5: Cleanup

1. Call `mcp_associate_delete_task` with task_id - verify deleted=true
2. Call `mcp_associate_delete_plan` with plan_id - verify deleted=true, tasks_deleted=0
3. Call `mcp_associate_delete_memory` with memory_id - verify deleted=true

### Phase 6: Edge Cases

1. **Delete plan with no tasks**:
   - Call `mcp_associate_create_plan` - extract plan_id
   - Call `mcp_associate_delete_plan` with plan_id (no tasks created)
   - Verify response has tasks_deleted=0

2. **Cascade delete**:
   - Call `mcp_associate_create_plan` - extract plan_id
   - Call `mcp_associate_create_task` with plan_id - extract task_id
   - Call `mcp_associate_delete_plan` with plan_id
   - Verify response has tasks_deleted=1
   - Call `mcp_associate_get_task` with task_id - should error (task deleted)

## Report Format

For each tool call, report:
- **Tool**: The tool name called
- **Input**: Parameters passed
- **Response**: Key fields from response
- **Result**: PASS or FAIL

## Important Notes

- Run tests **sequentially** - each step depends on IDs from previous steps
- Extract the `id` field from each create response before proceeding
- The `plan_ids` parameter for create_task must be an array: `["<plan_id>"]`
