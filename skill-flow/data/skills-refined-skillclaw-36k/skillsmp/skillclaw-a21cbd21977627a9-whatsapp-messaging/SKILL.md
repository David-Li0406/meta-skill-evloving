---
name: whatsapp-messaging
description: Use this skill when working with WhatsApp messaging via Kapso, including sending messages, managing templates, uploading media, or reading inbox history.
---

# WhatsApp Messaging

## When to use

Use this skill when working with WhatsApp messaging via Kapso: sending messages, creating/managing templates, uploading media, or reading inbox history.

## Setup

### Environment Variables
- `KAPSO_API_BASE_URL` (host only, no `/platform/v1`)
- `KAPSO_API_KEY`
- `PROJECT_ID`
- `KAPSO_META_GRAPH_VERSION` (optional, default `v24.0`)

## Discover IDs

Two Meta IDs are needed for different operations:

| ID | Used for | How to discover |
|----|----------|-----------------|
| `business_account_id` (WABA) | Template CRUD | `node scripts/list-platform-phone-numbers.mjs` |
| `phone_number_id` | Sending messages, media upload | `node scripts/list-platform-phone-numbers.mjs` |

## SDK Setup

Install the SDK:
```bash
npm install @kapso/whatsapp-cloud-api
```

Create the client:
```ts
import { WhatsAppClient } from "@kapso/whatsapp-cloud-api";

const client = new WhatsAppClient({
  baseUrl: "https://api.kapso.ai/meta/whatsapp",
  kapsoApiKey: process.env.KAPSO_API_KEY!
});
```

## How to Use

### Send a Text Message

Via SDK:
```ts
await client.messages.sendText({
  phoneNumberId: "<PHONE_NUMBER_ID>",
  to: "+15551234567",
  body: "Hello from Kapso"
});
```

### Send a Template Message

1. Discover IDs: `node scripts/list-platform-phone-numbers.mjs`
2. Draft template payload from `assets/template-utility-order-status-update.json`
3. Create the template: `node scripts/create-template.mjs --business-account-id <WABA_ID> --file <payload.json>`
4. Check status: `node scripts/template-status.mjs --business-account-id <WABA_ID> --name <name>`
5. Send the template: `node scripts/send-template.mjs --phone-number-id <ID> --file <send-payload.json>`

### Send an Interactive Message

Interactive messages require an active 24-hour session window. For outbound notifications outside the window, use templates.

1. Discover `phone_number_id`
2. Pick payload from `assets/send-interactive-*.json`
3. Send: `node scripts/send-interactive.mjs --phone-number-id <ID> --file <payload.json>`

### Read Inbox Data

Use Meta proxy or SDK:
- Proxy: `GET /{phone_number_id}/messages`, `GET /{phone_number_id}/conversations`
- SDK: `client.messages.query()`, `client.conversations.list()`

## Template Rules

Creation:
- Use `parameter_format: "NAMED"` with `{{param_name}}` (preferred over positional parameters).