# n8n Blueprint Cookbook

End-to-end flow: natural language → workflow JSON → apply → enable MCP → run.

---

## NL to JSON to MCP Run

**Problem**: Start from a plain-English request and end with a runnable MCP workflow.

**Solution**:
```bash
# 1) Export or create a JSON blueprint (by hand or with agent help)
# Save as <WORKFLOW.json>

# 2) Create or update
uv run scripts/n8nctl.py create <WORKFLOW.json>
# or
uv run scripts/n8nctl.py update <WORKFLOW_ID> <WORKFLOW.json>

# 3) Enable MCP + activate
uv run scripts/n8nctl.py mcp-enable <WORKFLOW_ID>
uv run scripts/n8nctl.py activate <WORKFLOW_ID>

# 4) Run via MCP client (example: chat trigger)
# Call n8n.execute_workflow with inputs {"type":"chat","chatInput":"hello"}
```

**Tip**: Use `n8n.get_workflow_details` to confirm the trigger type before executing.

---

## Safe Iteration Loop

**Problem**: Keep updating a workflow without breaking MCP access.

**Solution**:
```bash
uv run scripts/n8nctl.py export <WORKFLOW_ID> <WORKFLOW.json>
# edit <WORKFLOW.json>
uv run scripts/n8nctl.py update <WORKFLOW_ID> <WORKFLOW.json>
uv run scripts/n8nctl.py mcp-enable <WORKFLOW_ID>
uv run scripts/n8nctl.py activate <WORKFLOW_ID>
```

**Tip**: Always re-apply `mcp-enable` after major edits to ensure `availableInMCP` stays true.
