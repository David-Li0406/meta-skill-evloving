# Events & Messages

## Event System Overview

OpenCode uses Server-Sent Events (SSE) for real-time updates. Connect to `/event` endpoint to receive all events.

## Subscribing to Events

```typescript
// Using SDK
const events = await client.event.subscribe()
for await (const event of events.stream) {
  console.log(event.type, event.properties)
}

// Using raw HTTP (Node.js)
const response = await fetch("http://localhost:4096/event", {
  headers: { Accept: "text/event-stream" }
})
const reader = response.body.getReader()
// Parse SSE format: data: {...}\n\n
```

## Event Types

### Connection Events

| Event | Description |
|-------|-------------|
| `server.connected` | Initial connection established |
| `server.instance.disposed` | Server instance disposed |

### Session Events

| Event | Properties | Description |
|-------|------------|-------------|
| `session.idle` | `sessionID` | Session finished processing |
| `session.error` | `sessionID, error` | Session error occurred |
| `session.updated` | `session` | Session metadata changed |

### Message Events

| Event | Properties | Description |
|-------|------------|-------------|
| `message.updated` | `info` | Message metadata updated |
| `message.removed` | `sessionID, messageID` | Message removed |
| `message.part.updated` | `part, delta` | Part content changed |

### Installation Events

| Event | Description |
|-------|-------------|
| `installation.updated` | OpenCode was updated |
| `installation.update-available` | Update available |

## Message Structure

### Message Types

```typescript
type Message = UserMessage | AssistantMessage

interface UserMessage {
  id: string
  sessionID: string
  role: "user"
  time: { created: number }
  agent: string
  model: { providerID: string, modelID: string }
  summary?: { title?: string, body?: string, diffs: FileDiff[] }
}

interface AssistantMessage {
  id: string
  sessionID: string
  role: "assistant"
  parentID: string
  modelID: string
  providerID: string
  mode: string
  path: { cwd: string, root: string }
  time: { created: number, completed?: number }
  tokens: {
    input: number
    output: number
    reasoning: number
    cache: { read: number, write: number }
  }
  cost: number
  finish?: string
  error?: ProviderAuthError | UnknownError | MessageOutputLengthError | MessageAbortedError | ApiError
}
```

### Message Parts

Each message contains multiple parts:

```typescript
type Part = TextPart | ReasoningPart | ToolPart | FilePart

interface TextPart {
  id: string
  sessionID: string
  messageID: string
  type: "text"
  text: string
  synthetic?: boolean
  time?: { start: number, end?: number }
}

interface ReasoningPart {
  id: string
  sessionID: string
  messageID: string
  type: "reasoning"
  text: string
  time: { start: number, end?: number }
}

interface FilePart {
  id: string
  sessionID: string
  messageID: string
  type: "file"
  mime: string
  filename?: string
  url: string
}

interface ToolPart {
  id: string
  sessionID: string
  messageID: string
  type: "tool"
  callID: string
  tool: string  // e.g., "bash", "edit", "read"
  state: ToolState
}
```

### Tool States

```typescript
type ToolState =
  | ToolStatePending
  | ToolStateRunning
  | ToolStateCompleted
  | ToolStateError

interface ToolStatePending {
  status: "pending"
  input: Record<string, unknown>
  raw: string
}

interface ToolStateRunning {
  status: "running"
  input: Record<string, unknown>
  title?: string
  metadata?: Record<string, unknown>
  time: { start: number }
}

interface ToolStateCompleted {
  status: "completed"
  input: Record<string, unknown>
  output: string
  title: string
  metadata: Record<string, unknown>
  time: { start: number, end: number }
  attachments?: FilePart[]
}

interface ToolStateError {
  status: "error"
  input: Record<string, unknown>
  error: string
  metadata?: Record<string, unknown>
  time: { start: number, end: number }
}
```

## Handling `message.part.updated`

This is the most important event for building UIs:

```typescript
// Event structure
interface MessagePartUpdatedEvent {
  type: "message.part.updated"
  properties: {
    part: Part       // Current state of the part
    delta?: string   // For text/reasoning: the new content since last update
  }
}

// Handling in UI
for await (const event of events.stream) {
  if (event.type !== "message.part.updated") continue

  const { part, delta } = event.properties

  // Filter by session
  if (part.sessionID !== mySessionId) continue

  switch (part.type) {
    case "text":
      // Append delta to UI
      if (delta) appendText(delta)
      break

    case "reasoning":
      // Show thinking indicator
      if (delta) appendThinking(delta)
      break

    case "tool":
      const { status, input, output, error, title } = part.state
      switch (status) {
        case "pending":
          // Tool call parsed but empty input - often skip this
          break
        case "running":
          // Show tool running indicator
          showToolRunning(part.tool, input, title)
          break
        case "completed":
          // Show tool result
          showToolResult(part.id, output)
          break
        case "error":
          // Show tool error
          showToolError(part.id, error)
          break
      }
      break
  }
}
```

## Detecting Response Completion

```typescript
for await (const event of events.stream) {
  // Response complete when session becomes idle
  if (event.type === "session.idle" &&
      event.properties.sessionID === mySessionId) {
    console.log("Response complete!")
    break
  }

  // Or handle errors
  if (event.type === "session.error" &&
      event.properties.sessionID === mySessionId) {
    console.error("Error:", event.properties.error)
    break
  }
}
```

## Input Part Types (for prompts)

When sending prompts, use these part types:

```typescript
// Text prompt
{ type: "text", text: "Your message" }

// File attachment
{ type: "file", mime: "text/plain", url: "file:///path/to/file" }

// Image (base64)
{ type: "file", mime: "image/png", url: "data:image/png;base64,..." }
```

## Error Types

```typescript
interface ProviderAuthError {
  name: "ProviderAuthError"
  data: { providerID: string, message: string }
}

interface UnknownError {
  name: "UnknownError"
  data: { message: string }
}

interface MessageOutputLengthError {
  name: "MessageOutputLengthError"
  data: {}
}

interface MessageAbortedError {
  name: "MessageAbortedError"
  data: { message: string }
}

interface ApiError {
  name: "APIError"
  data: {
    message: string
    statusCode?: number
    isRetryable: boolean
    responseHeaders?: Record<string, string>
    responseBody?: string
  }
}
```
