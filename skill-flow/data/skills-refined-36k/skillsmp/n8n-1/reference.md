# n8n Reference

## REST API (authoring)

- Base path: `/api/v1`
- Auth header: `X-N8N-API-KEY: <key>`
- Docs: `<N8N_BASE_URL>/api/v1/docs`

Common endpoints:
- `GET /api/v1/workflows`
- `POST /api/v1/workflows`
- `PUT /api/v1/workflows/{id}`
- `POST /api/v1/workflows/{id}/activate`
- `POST /api/v1/workflows/{id}/deactivate`
- `GET /api/v1/executions`

## MCP (runtime)

- Instance-level MCP for listing and running enabled workflows.

Notes:
 - Use `supergateway` for streamable HTTP endpoints.

## Node lookup

- Exa: built-in node library docs (`https://docs.n8n.io/integrations/builtin/node-types/`).
- Context7: `/n8n-io/n8n-docs` for node docs + examples.
- DeepWiki: repo Q&A over `n8n-io/n8n-docs`; pair with `gh` or workflow export to confirm `type` strings.
- `gh`: list node folders, then search by keyword and open the `*.node.json` file to read the `node` field.
- Inspect `type` fields from exported workflows to confirm exact identifiers.

## MCP config snippet (template)

Add after you have the MCP URL and token:

```json
{
  "mcpServers": {
    "n8n": {
      "description": "n8n MCP",
      "command": "bun",
      "args": [
        "x",
        "supergateway",
        "--streamableHttp",
        "<N8N_MCP_URL>",
        "--header",
        "Authorization: Bearer <N8N_MCP_TOKEN>"
      ]
    }
  }
}
```

## n8nctl (uv script)

The `scripts/n8nctl.py` helper wraps REST calls and avoids curl/jq.

Required env vars:
- `N8N_BASE_URL`
- `N8N_API_KEY`

Examples:

```bash
uv run scripts/n8nctl.py list --limit 5
uv run scripts/n8nctl.py export <WORKFLOW_ID> <OUT.json>
uv run scripts/n8nctl.py mcp-enable <WORKFLOW_ID>
uv run scripts/n8nctl.py validate <WORKFLOW.json>
```
