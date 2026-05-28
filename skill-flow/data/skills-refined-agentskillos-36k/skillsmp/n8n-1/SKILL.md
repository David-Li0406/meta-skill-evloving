---
name: n8n
description: "n8n automation via REST API (authoring) and MCP (runtime). Use REST for workflow CRUD; use MCP for listing/triggering enabled workflows."
---

# n8n

Use **REST API** to create/update/activate workflows. Use **MCP** to list and run enabled workflows.

## When to use

- Authoring (no UI): REST API
- Running/triggering workflows: MCP
- Use `n8nctl` (uv script) for REST without curl/jq

## Preconditions

- n8n instance URL (cloud, self-hosted, or local)
- REST API key (X-N8N-API-KEY)
- MCP URL + access token (instance-level MCP)
- Workflows marked `availableInMCP`

## Node discovery (tested)

- Exa: built-in node library docs (`https://docs.n8n.io/integrations/builtin/node-types/`).
- Context7: `/n8n-io/n8n-docs` for node docs + examples.
- DeepWiki: repo Q&A over `n8n-io/n8n-docs`; pair with `gh` or workflow export to confirm `type` strings.
- `gh`: list node folders, then search by keyword and open the `*.node.json` file to read the `node` field.
- Export workflows to confirm exact `type` strings in your instance.

## Quick start (REST)

```bash
# list workflows
curl -sS -H "X-N8N-API-KEY: <N8N_API_KEY>" \
  "<N8N_BASE_URL>/api/v1/workflows?active=true"

# create workflow (body from template)
curl -sS -X POST -H "X-N8N-API-KEY: <N8N_API_KEY>" \
  -H "Content-Type: application/json" \
  -d @workflow.json \
  "<N8N_BASE_URL>/api/v1/workflows"
```

## MCP (runtime)

Use the MCP URL for your instance (example: `N8N_MCP_URL`).

```bash
# stdio proxy for MCP clients that need headers
bun x supergateway --streamableHttp "<N8N_MCP_URL>" \
  --header "Authorization: Bearer <N8N_MCP_TOKEN>"
```

## Notes

- Workflows include a trigger node for MCP execution.
- Keep `--header "Authorization: Bearer <...>"` as a single, quoted argument.
- `n8nctl` uses REST endpoints and requires `N8N_BASE_URL` + `N8N_API_KEY`.
- Replace `<N8N_CONTAINER>` with your Docker container name.

## CLI (self-hosted)

For Docker installs, run inside the container:

```bash
docker exec -it "<N8N_CONTAINER>" n8n export:workflow --all
docker exec -it "<N8N_CONTAINER>" n8n import:workflow --input=/path/to/workflow.json
```

## Scripts

Minimal REST CLI (no curl):

```bash
uv run scripts/n8nctl.py list --limit 5
uv run scripts/n8nctl.py get <WORKFLOW_ID>
uv run scripts/n8nctl.py create <WORKFLOW.json>
uv run scripts/n8nctl.py update <WORKFLOW_ID> <WORKFLOW.json>
uv run scripts/n8nctl.py activate <WORKFLOW_ID>
uv run scripts/n8nctl.py mcp-enable <WORKFLOW_ID>
uv run scripts/n8nctl.py validate <WORKFLOW.json>
```

## Query templates

See `assets/query-templates.json`.

## Reference

See `reference.md`.

## Cookbook

See `cookbook/basics.md` and `cookbook/blueprints.md`.
