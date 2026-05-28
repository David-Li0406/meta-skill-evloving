# Research Node Workflow

**Entry:** Routed here from Task Type Dispatch when task has `type: "research"`

## Mark Task In Progress

```bash
mcp__plugin_foundry_foundry-mcp__task action="start" spec_id={spec-id} task_id={task-id}
```

## Check Node Status

Check if research has already been executed:

```bash
mcp__plugin_foundry_foundry-mcp__research action="node-status" spec_id={spec-id} research_node_id={task-id}
```

**Response includes:**
- `status`: Node status (pending, in_progress, completed)
- `research_type`: Workflow type (chat, consensus, thinkdeep, ideate, deep-research)
- `blocking_mode`: How research blocks dependents (none, soft, hard)
- `has_findings`: Whether findings have been recorded
- `session_id`: Linked research session ID (if executed)

## Route by Status

| Status | Action |
|--------|--------|
| `completed` with findings | Show findings, continue to next task |
| `pending` or `in_progress` | Execute research workflow |

### If Already Completed

Retrieve and display existing findings:

```bash
mcp__plugin_foundry_foundry-mcp__research action="node-findings" spec_id={spec-id} research_node_id={task-id}
```

Present findings to user, then continue to **Surface Next Recommendation**.

### If Pending/In Progress

Present gate to user via `AskUserQuestion`:
- **Options:** "Execute Research", "Skip for Now", "View Query"

## Execute Research Workflow

Run the research workflow linked to this node:

```bash
mcp__plugin_foundry_foundry-mcp__research action="node-execute" spec_id={spec-id} research_node_id={task-id}
```

**This command:**
1. Reads `research_type` and `query` from node metadata
2. Executes the appropriate workflow (chat, consensus, thinkdeep, ideate, deep-research)
3. Links the research session to the node
4. Records execution in `research_history`

**Optional prompt override:**
```bash
mcp__plugin_foundry_foundry-mcp__research action="node-execute" spec_id={spec-id} research_node_id={task-id} prompt="Additional context for the query"
```

## Present Results

After execution completes:
1. Display the research results (synthesis, findings, ideas)
2. Highlight key insights
3. Show confidence level if available

## User Review Gate

Present results for approval via `AskUserQuestion`:
- **Options:** "Approve Findings", "Re-run Research", "Request Clarification"

## Record Findings

After user approval, record findings to the node:

```bash
mcp__plugin_foundry_foundry-mcp__research action="node-record" spec_id={spec-id} research_node_id={task-id} result="completed" summary="Key findings summary" key_insights='["insight1", "insight2"]' recommendations='["recommendation1"]' confidence="high"
```

**Result values:**
| Result | Meaning |
|--------|---------|
| `completed` | Research finished successfully |
| `inconclusive` | Research didn't yield clear findings |
| `blocked` | Research blocked by external factors |
| `cancelled` | User chose to skip |

**Findings fields:**
- `summary`: Brief synthesis of findings
- `key_insights`: Array of key insights discovered
- `recommendations`: Array of recommendations for implementation
- `sources`: Array of source references (for deep-research)
- `confidence`: Confidence level (high, medium, low)

## Complete Research Task

After recording findings:

```bash
mcp__plugin_foundry_foundry-mcp__task action="complete" spec_id={spec-id} task_id={task-id} completion_note="Research completed with {result}. Key findings: {summary}"
```

## Handle Blocking Behavior

If `blocking_mode="hard"`, check for unblocked dependents:

1. Research completion may unblock dependent tasks
2. The next task recommendation will reflect newly available tasks
3. Tasks with `depends_on: ["{research-node-id}"]` become actionable

If `blocking_mode="soft"` or `"none"`:
- Dependents were never blocked
- Findings are informational for context

## Return to Main Workflow

After research task is complete, go to **Surface Next Recommendation** to continue with the next task.

## MCP Tool Reference

| Action | Required | Optional |
|--------|----------|----------|
| `node-status` | `spec_id`, `research_node_id` | - |
| `node-execute` | `spec_id`, `research_node_id` | `prompt` |
| `node-record` | `spec_id`, `research_node_id`, `result` | `summary`, `key_insights`, `recommendations`, `sources`, `confidence` |
| `node-findings` | `spec_id`, `research_node_id` | - |
