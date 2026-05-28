---
name: kapso-automation
description: Use this skill to manage Kapso workflows, functions, and databases, including editing workflow graphs, configuring triggers, managing executions, creating functions, and performing database CRUD operations.
---

# Kapso Automation

## When to use

Use this skill to build and run Kapso automation: workflow CRUD, graph edits, triggers, executions, function management, and D1 database operations.

## Setup

Env vars:
- `KAPSO_API_BASE_URL` (host only, no `/platform/v1`)
- `KAPSO_API_KEY`
- `PROJECT_ID`

## How to

### Edit a workflow graph

1. Fetch graph: `node scripts/get-graph.js <workflow_id>` (note the `lock_version`)
2. Edit the JSON (see graph rules below)
3. Validate: `node scripts/validate-graph.js --definition-file <path>`
4. Update: `node scripts/update-graph.js <workflow_id> --expected-lock-version <n> --definition-file <path>`
5. Re-fetch to confirm

For small edits, use `edit-graph.js` with `--old-file` and `--new-file` instead.

If you get a lock_version conflict: re-fetch, re-apply changes, retry with new lock_version.

### Manage triggers

1. List: `node scripts/list-triggers.js <workflow_id>`
2. Create: `node scripts/create-trigger.js <workflow_id> --trigger-type <type> --phone-number-id <id>`
3. Toggle: `node scripts/update-trigger.js --trigger-id <id> --active true|false`
4. Delete: `node scripts/delete-trigger.js --trigger-id <id>`

For inbound_message triggers, first run `node scripts/list-whatsapp-phone-numbers.js` to get `phone_number_id`.

### Debug executions

1. List: `node scripts/list-executions.js <workflow_id>`
2. Inspect: `node scripts/get-execution.js <execution-id>`
3. Get value: `node scripts/get-context-value.js <execution-id> --variable-path vars.foo`
4. Events: `node scripts/list-execution-events.js <execution-id>`

### Create and deploy a function

1. Write code with handler signature (see function rules below)
2. Create: `node scripts/create-function.js --name <name> --code-file <path>`
3. Deploy: `node scripts/deploy-function.js --function-id <id>`
4. Verify: `node scripts/get-function.js --function-id <id>`

### Set up agent node with app integrations

1. Find model: `node scripts/list-provider-models.js`
2. Find account: `node scripts/list-accounts.js --app-slug <slug>` (use `pipedream_account_id`)
3. Find action: `node scripts/search-actions.js --query <word> --app-slug <slug>` (action_id = key)
4. Create integration: `node scripts/create-integration.js`