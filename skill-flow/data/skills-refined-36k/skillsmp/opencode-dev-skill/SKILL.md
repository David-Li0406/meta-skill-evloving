---
name: opencode-dev-skill
description: |
  OpenCode development skill for building applications on top of OpenCode.
  Use when: (1) developing integrations with OpenCode SDK/API, (2) building custom UIs that consume OpenCode server,
  (3) understanding OpenCode message/event streaming, (4) working with OpenCode CLI programmatically,
  (5) contributing to OpenCode codebase, or (6) user mentions "opencode" in development context.
---

# OpenCode Development Guide

OpenCode is an open source AI coding agent with a client/server architecture. This skill helps you build applications on top of OpenCode.

## Quick Reference

| Component | Purpose | Location |
|-----------|---------|----------|
| SDK (`@opencode-ai/sdk`) | Type-safe JS client | `packages/sdk/js` |
| Server | HTTP API + SSE events | `packages/opencode/src/server` |
| TUI | Terminal UI (SolidJS) | `packages/opencode/src/cli/cmd/tui` |
| Core | Business logic | `packages/opencode/src` |

## Core Concepts

### Architecture
OpenCode uses client/server architecture:
- **Server**: HTTP API (OpenAPI 3.1) + SSE event stream
- **Clients**: TUI, Web, Desktop, SDK consumers
- Default: `http://localhost:4096`

### Key Abstractions
- **Session**: A conversation context with message history
- **Message**: User or Assistant message with parts
- **Part**: Text, File, Tool, Reasoning content within a message
- **Event**: Real-time updates via SSE (Server-Sent Events)

## SDK Quick Start

```typescript
import { createOpencode, createOpencodeClient } from "@opencode-ai/sdk"

// Option 1: Start server + create client
const { client, server } = await createOpencode()

// Option 2: Connect to existing server
const client = createOpencodeClient({ baseUrl: "http://localhost:4096" })

// Create session and send prompt
const session = await client.session.create({ body: { title: "My Session" } })
const result = await client.session.prompt({
  path: { id: session.data.id },
  body: {
    parts: [{ type: "text", text: "Hello!" }],
    model: { providerID: "anthropic", modelID: "claude-sonnet-4-20250514" }
  }
})
```

## Event Streaming Pattern

For real-time UI updates, subscribe to SSE events:

```typescript
// Subscribe to events
const events = await client.event.subscribe()
for await (const event of events.stream) {
  switch (event.type) {
    case "message.part.updated":
      // Handle streaming text/tool updates
      const { part, delta } = event.properties
      if (part.type === "text" && delta) {
        // Append delta to UI
      }
      break
    case "session.idle":
      // Response complete
      break
  }
}
```

## Common Event Types

| Event | Description |
|-------|-------------|
| `server.connected` | Initial connection established |
| `message.updated` | Message metadata changed |
| `message.part.updated` | Part content updated (with delta) |
| `session.idle` | Session finished processing |
| `session.error` | Error occurred |

## Message Part Types

| Type | Description |
|------|-------------|
| `text` | Text content from assistant |
| `reasoning` | Thinking/reasoning content |
| `tool` | Tool invocation with state (pending/running/completed/error) |
| `file` | File attachment |

## References

For detailed information:
- **Architecture & Project Structure**: See `references/architecture.md`
- **SDK & Server API**: See `references/sdk-and-server.md`
- **Events & Messages**: See `references/events-and-messages.md`
- **Providers & Models**: See `references/providers-and-models.md`
- **CLI Commands**: See `references/cli.md`

## Common Patterns

### Sending Async Prompt (Non-blocking)
Use `/session/:id/prompt_async` for fire-and-forget, then listen to events:

```typescript
// POST /session/:id/prompt_async returns 204 immediately
// Listen to events for actual response
```

### Handling Tool States
```typescript
if (part.type === "tool") {
  const { status, input, output, error } = part.state
  switch (status) {
    case "pending": // Tool call parsed, not started
    case "running": // Tool executing
    case "completed": // Tool finished, output available
    case "error": // Tool failed, error available
  }
}
```

### Session Management
```typescript
// List sessions
const sessions = await client.session.list()

// Continue existing session
const session = await client.session.get({ path: { id: sessionId } })

// Abort running session
await client.session.abort({ path: { id: sessionId } })
```

### Getting Available Providers & Models
```typescript
// Get user's configured providers (env vars, API keys, plugins, free models)
const { providers, default: defaults } = await client.config.providers()

for (const provider of providers) {
  console.log(`${provider.name}: ${Object.keys(provider.models).length} models`)
  // provider.source: "env" | "config" | "custom" | "api"
}
```

See `references/providers-and-models.md` for detailed provider detection logic.
