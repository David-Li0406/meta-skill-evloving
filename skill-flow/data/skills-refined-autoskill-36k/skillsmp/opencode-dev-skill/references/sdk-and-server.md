# SDK & Server API

## SDK Installation

```bash
npm install @opencode-ai/sdk
```

## SDK Usage

### Creating Client + Server

```typescript
import { createOpencode } from "@opencode-ai/sdk"

// Starts server and creates client
const { client, server } = await createOpencode({
  hostname: "127.0.0.1",  // default
  port: 4096,             // default
  timeout: 5000,          // ms, default
  config: {
    model: "anthropic/claude-sonnet-4-20250514",
    // ... other config overrides
  }
})

// When done
server.close()
```

### Client-Only (Connect to Existing Server)

```typescript
import { createOpencodeClient } from "@opencode-ai/sdk"

const client = createOpencodeClient({
  baseUrl: "http://localhost:4096",
  // Optional:
  // fetch: customFetch,
  // throwOnError: false,
})
```

### TUI Spawning

```typescript
import { createOpencodeTui } from "@opencode-ai/sdk"

const tui = createOpencodeTui({
  project: "/path/to/project",
  model: "anthropic/claude-sonnet-4-20250514",
  session: "session-id",
  agent: "build",
})

tui.close()
```

## Server API Reference

Base URL: `http://localhost:4096`

### Global

| Method | Path | Description |
|--------|------|-------------|
| GET | `/global/health` | Health check, returns `{ healthy, version }` |
| GET | `/global/event` | Global SSE event stream |

### Sessions

| Method | Path | Description |
|--------|------|-------------|
| GET | `/session` | List all sessions |
| POST | `/session` | Create session, body: `{ parentID?, title? }` |
| GET | `/session/:id` | Get session details |
| DELETE | `/session/:id` | Delete session |
| PATCH | `/session/:id` | Update session, body: `{ title? }` |
| POST | `/session/:id/abort` | Abort running session |
| POST | `/session/:id/share` | Share session publicly |
| DELETE | `/session/:id/share` | Unshare session |

### Messages

| Method | Path | Description |
|--------|------|-------------|
| GET | `/session/:id/message` | List messages in session |
| POST | `/session/:id/message` | Send prompt (blocking, waits for response) |
| POST | `/session/:id/prompt_async` | Send prompt (non-blocking, 204 response) |
| GET | `/session/:id/message/:messageID` | Get message details with parts |
| POST | `/session/:id/command` | Execute slash command |
| POST | `/session/:id/shell` | Run shell command |
| POST | `/session/:id/revert` | Revert a message |
| POST | `/session/:id/unrevert` | Restore reverted messages |

### Message Body Format

```typescript
// POST /session/:id/message or /session/:id/prompt_async
{
  // Message parts (required)
  parts: [
    { type: "text", text: "Your prompt" },
    { type: "file", mime: "text/plain", url: "file:///path/to/file" }
  ],

  // Model selection (optional)
  model: {
    providerID: "anthropic",
    modelID: "claude-sonnet-4-20250514"
  },

  // Agent selection (optional)
  agent: "build",  // or "plan"

  // Don't trigger AI response (optional)
  noReply: true,

  // Tool configuration (optional)
  tools: {
    "bash": true,
    "edit": false
  }
}
```

### Files

| Method | Path | Description |
|--------|------|-------------|
| GET | `/find?pattern=<pat>` | Search text in files (ripgrep) |
| GET | `/find/file?query=<q>` | Find files by name |
| GET | `/find/symbol?query=<q>` | Find workspace symbols |
| GET | `/file?path=<path>` | List files/directories |
| GET | `/file/content?path=<p>` | Read file content |
| GET | `/file/status` | Get status of tracked files |

### Events

| Method | Path | Description |
|--------|------|-------------|
| GET | `/event` | SSE event stream for all events |

### Config

| Method | Path | Description |
|--------|------|-------------|
| GET | `/config` | Get current config |
| PATCH | `/config` | Update config |
| GET | `/config/providers` | List providers and default models |

### TUI Control

| Method | Path | Description |
|--------|------|-------------|
| POST | `/tui/append-prompt` | Append text to prompt |
| POST | `/tui/submit-prompt` | Submit current prompt |
| POST | `/tui/clear-prompt` | Clear prompt |
| POST | `/tui/show-toast` | Show toast notification |
| POST | `/tui/execute-command` | Execute command |

### Auth

| Method | Path | Description |
|--------|------|-------------|
| PUT | `/auth/:id` | Set auth credentials for provider |

## SDK Client Methods

All methods return `{ data, error, response }` unless `throwOnError: true`.

```typescript
// Sessions
client.session.list()
client.session.get({ path: { id } })
client.session.create({ body: { title? } })
client.session.delete({ path: { id } })
client.session.abort({ path: { id } })
client.session.messages({ path: { id } })
client.session.prompt({ path: { id }, body: { parts, model?, ... } })

// Events
const events = await client.event.subscribe()
for await (const event of events.stream) { ... }

// Files
client.find.text({ query: { pattern } })
client.find.files({ query: { query, type?, limit? } })
client.file.read({ query: { path } })

// Config
client.config.get()
client.config.providers()

// TUI
client.tui.appendPrompt({ body: { text } })
client.tui.showToast({ body: { message, variant } })
```

## Common Integration Pattern

```typescript
import { createOpencodeClient } from "@opencode-ai/sdk"

async function chat(prompt: string) {
  const client = createOpencodeClient({ baseUrl: "http://localhost:4096" })

  // Create or reuse session
  const session = await client.session.create({ body: { title: "Chat" } })
  const sessionId = session.data.id

  // Subscribe to events first
  const events = await client.event.subscribe()

  // Send prompt async
  await fetch(`http://localhost:4096/session/${sessionId}/prompt_async`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      parts: [{ type: "text", text: prompt }]
    })
  })

  // Process events
  for await (const event of events.stream) {
    if (event.type === "message.part.updated") {
      const { part, delta } = event.properties
      if (part.sessionID === sessionId && part.type === "text" && delta) {
        process.stdout.write(delta)
      }
    }
    if (event.type === "session.idle" && event.properties.sessionID === sessionId) {
      break
    }
  }
}
```
