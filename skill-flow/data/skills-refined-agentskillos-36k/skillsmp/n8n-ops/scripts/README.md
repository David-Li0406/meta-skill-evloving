# n8n-ops Scripts

Command-line scripts for managing n8n workflows.

## Setup Required

Before using these scripts, you must configure your n8n instance:

### Option 1: Environment Variables

```bash
export N8N_BASE_URL=https://n8n.your-domain.com
export N8N_API_KEY=your-api-key-here
```

### Option 2: .env File

Add to `.env` in repo root:

```bash
N8N_BASE_URL=https://n8n.your-domain.com
N8N_API_KEY=your-api-key-here
```

### Getting an API Key

1. Open your n8n instance
2. Go to Settings → API
3. Click "Create API Key"
4. Copy the key (it won't be shown again)

## Available Scripts

| Script | Purpose |
|--------|---------|
| `list-workflows.sh` | List all workflows |
| `get-workflow.sh` | Get workflow details |
| `export-workflow.sh` | Export workflow to JSON |
| `import-workflow.sh` | Import workflow from JSON |
| `activate-workflow.sh` | Activate a workflow |
| `deactivate-workflow.sh` | Deactivate a workflow |
| `reactivate-workflow.sh` | Deactivate + wait + activate |
| `list-executions.sh` | List workflow executions |
| `get-execution.sh` | Get execution details |
| `test-webhook.sh` | Test a webhook endpoint |

## Usage Examples

```bash
# List all workflows
./list-workflows.sh

# List only active workflows
./list-workflows.sh --active

# Get workflow details
./get-workflow.sh abc123def456

# Export workflow to file
./export-workflow.sh abc123def456 backup.json

# Export workflow by name
./export-workflow.sh "My Workflow" backup.json

# Import workflow (creates new)
./import-workflow.sh workflow.json

# Import workflow (updates if exists)
./import-workflow.sh workflow.json --update

# Activate/deactivate
./activate-workflow.sh abc123def456
./deactivate-workflow.sh abc123def456

# Reactivate (refresh webhooks)
./reactivate-workflow.sh abc123def456

# List recent executions
./list-executions.sh

# List executions for specific workflow
./list-executions.sh abc123def456 --limit 20

# List failed executions
./list-executions.sh --status error

# Get execution details
./get-execution.sh 12345

# Test webhook
./test-webhook.sh https://n8n.example.com/webhook/abc123
./test-webhook.sh /webhook/abc123 payload.json
```

## Multiple Instances

To work with multiple n8n instances, override the URL per-command:

```bash
# Use different instance
N8N_BASE_URL=https://other-n8n.example.com ./list-workflows.sh
```

Or create wrapper scripts:

```bash
#!/bin/bash
# my-instance.sh
export N8N_BASE_URL=https://my-n8n.example.com
export N8N_API_KEY=my-api-key
exec "$(dirname "$0")/$1.sh" "${@:2}"
```

Then use: `./my-instance.sh list-workflows`

## Shared Configuration

All scripts source `_config.sh` which:
- Loads `.env` from repo root
- Validates required environment variables
- Provides helper functions for API calls
- Shows clear error messages if not configured

## Error Handling

Scripts will error with helpful messages if:
- `N8N_BASE_URL` is not set
- `N8N_API_KEY` is not set
- API returns an error
- Workflow/execution not found
