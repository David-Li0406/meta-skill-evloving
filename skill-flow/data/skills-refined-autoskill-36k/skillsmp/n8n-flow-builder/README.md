# n8n Flow Builder

## Description
Expert guidance for designing, building, and maintaining n8n workflows across dev/staging/prod environments on Railway with MCP integration. Handles flow authoring, node configuration, error handling, and deployment patterns.

## Installation
This skill is part of the mapache-skills repository.

For Claude Code CLI:
```bash
ln -s "C:\Users\Kurt Anderson\github projects\mapache-skills\skills" ~/.claude/skills
```

For Claude Desktop:
1. Zip the skills/n8n-flow-builder/ directory
2. Upload via Settings > Capabilities > Upload skill

## What This Skill Provides

### Workflow Design Patterns
- Webhook-triggered workflows
- Scheduled automation (cron jobs)
- Long-running processes with approvals
- Multi-step integrations

### Node Configuration
- HTTP Request best practices
- Function node patterns
- Error handling strategies
- Conditional branching (IF nodes)
- Data merging and transformation

### Deployment Process
- Dev (local Docker) → Staging (Railway) → Prod (Railway)
- JSON export/import workflow
- Acceptance testing checklist
- Rollback procedures

### Integration Guidance
- GitHub webhooks and API
- Linear GraphQL integration
- Slack notifications and commands
- Database queries (PostgreSQL)

## Usage
Claude automatically loads this skill when you:
- Mention n8n, workflows, or automation
- Ask to create integrations
- Need to deploy to Railway environments
- Debug n8n executions

## Version History
- v1.0.0 - Initial release (2025-10-18)
