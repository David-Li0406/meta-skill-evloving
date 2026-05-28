# n8n Cookbook

Practical recipes for authoring workflows via REST and running them via MCP.

---

## List Workflows

**Problem**: See what workflows exist.

**Solution**:
```bash
uv run scripts/n8nctl.py list --limit 10
```

**Tip**: Add `--active true` to see only active workflows.

---

## Enable MCP for a Workflow

**Problem**: Expose a workflow so MCP can list/execute it.

**Solution**:
```bash
uv run scripts/n8nctl.py mcp-enable <WORKFLOW_ID>
uv run scripts/n8nctl.py activate <WORKFLOW_ID>
```

**Tip**: MCP lists workflows that are active and marked `availableInMCP`.

---

## Run a Chat Workflow via MCP

**Problem**: Execute a chat-triggered workflow.

**Solution**:
```bash
# Call n8n.execute_workflow via your MCP client
# inputs: {"type":"chat","chatInput":"hello"}
```

**Tip**: Use `n8n.get_workflow_details` first to confirm the trigger type.

---

## Export Workflow JSON

**Problem**: Capture a workflow definition to edit or version-control.

**Solution**:
```bash
uv run scripts/n8nctl.py export <WORKFLOW_ID> <OUT.json>
```

**Tip**: Edit JSON, then apply with `n8nctl.py update`.

---

## Find Node Type Identifiers

**Problem**: Get exact `type` strings (e.g., `n8n-nodes-base.httpRequest`).

**Solution (gh)**:
```bash
# list node folders
gh api repos/n8n-io/n8n/contents/packages/nodes-base/nodes \
  --jq '.[].name' | head

# search by keyword (example: openAi)
gh search code "openAi" --repo n8n-io/n8n --limit 20

# LangChain node type constants
gh api repos/n8n-io/n8n/contents/packages/workflow/src/constants.ts \
  --jq '.content' | base64 -d | rg "OPENAI"
```

**Solution (DeepWiki)**:
Use DeepWiki on `n8n-io/n8n-docs` to list OpenAI‑compatible LLM nodes and locate their doc paths.

**Tip**: After you find a file, fetch it with `gh api .../contents/... | base64 -d` to read the `node` field.
**Tip**: Confirm exact `type` strings with `gh` or workflow export.


---

## Validate a Workflow JSON

**Problem**: Check a workflow file for missing fields or bad references.

**Solution**:
```bash
uv run scripts/n8nctl.py validate <WORKFLOW.json>
```

**Tip**: Validate, then apply `create` or `update`.
