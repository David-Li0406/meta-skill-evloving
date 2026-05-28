---
name: whatsapp-flows
description: Use this skill to manage WhatsApp Flows via the Kapso Platform API, including creating, updating, publishing flows, and managing data endpoints.
---

# WhatsApp Flow Management

## When to use

Use this skill to manage WhatsApp Flows end-to-end: discover flows, edit flow JSON via versions, publish/test, attach data endpoints, and inspect responses/logs.

## Setup

Env vars:
- `KAPSO_API_BASE_URL` (host only, no `/platform/v1`)
- `KAPSO_API_KEY`
- `PROJECT_ID`
- `META_GRAPH_VERSION` (optional, default `v24.0`)

Run scripts with Node or Bun:
```bash
node scripts/list-flows.js
```

## How to

### Create and publish a flow

1. Create flow: `node scripts/create-flow.js --phone-number-id <id> --name <name>`
2. Read `references/whatsapp-flows-spec.md` for Flow JSON rules.
3. Update JSON: `node scripts/update-flow-json.js --flow-id <id> --json-file <path>`
4. Publish: `node scripts/publish-flow.js --flow-id <id>`
5. Test: `node scripts/send-test-flow.js --phone-number-id <id> --flow-id <id> --to <phone>`

### Attach a data endpoint (dynamic flows)

1. Set up encryption: `node scripts/setup-encryption.js --flow-id <id>`
2. Create endpoint: `node scripts/set-data-endpoint.js --flow-id <id> --code-file <path>`
3. Deploy: `node scripts/deploy-data-endpoint.js --flow-id <id>`
4. Register: `node scripts/register-data-endpoint.js --flow-id <id>`

### Debug flows

- List responses: `node scripts/list-flow-responses.js --flow-id <id>`
- Function logs: `node scripts/list-function-logs.js --flow-id <id>`
- Function invocations: `node scripts/list-function-invocations.js --flow-id <id>`

## Flow JSON rules

Static flows (no data endpoint):
- Use `version: "7.3"`
- `routing_model` and `data_api_version` are optional.
- See `assets/sample-flow.json`.

Dynamic flows (with data endpoint):
- Use `version: "7.3"` with `data_api_version: "3.0"`.
- `routing_model` is **required** - defines valid screen transitions.
- See `assets/dynamic-flow.json`.

## Data endpoint rules

Handler signature:
```js
async function handler(request, env) {
  const body = await request.json();
  // body.data_exchange.action: INIT | data_exchange | BACK
  // body.data_exchange.screen: current screen id
  // body.data_exchange.data: user inputs
  return Response.json({
    version: "3.0",
    screen: "NEXT_SCREEN_ID",
    data: { ... }
  });
}
```