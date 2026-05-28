# Transcript JSONL Types Reference

Comprehensive documentation of Claude Code transcript file structure and types.

## File Location

Transcripts are stored at:
```
~/.claude/projects/<project-hash>/<session-id>.jsonl
```

**Path Components:**
- `<project-hash>`: Working directory path with slashes replaced by dashes
  - Example: `/Users/hgeldenhuys/WebstormProjects/claude-code-sdk` becomes `-Users-hgeldenhuys-WebstormProjects-claude-code-sdk`
- `<session-id>`: UUID for the session
  - Main session: `f9804c2a-4f33-4066-992f-34114590955b.jsonl`
  - Agent transcripts: `agent-<7-char-id>.jsonl` (e.g., `agent-a056a23.jsonl`)

---

## Core Types

### TranscriptLine (Base)

Every line in the JSONL file is one of these types:

```typescript
type TranscriptLineType =
  | 'user'                  // User prompts, tool results
  | 'assistant'             // Claude responses, tool calls
  | 'file-history-snapshot' // File state tracking
  | 'system'                // System messages (hooks, etc.)
  | 'progress'              // Progress updates (hook events, etc.)
  | 'summary'               // Session summary
  | 'queue-operation';      // Background task notifications
```

### Common Fields

Fields present on most message types:

```typescript
interface TranscriptLineBase {
  type: TranscriptLineType;
  uuid: string;                    // Unique ID for this line
  parentUuid: string | null;       // Parent message for threading
  sessionId: string;               // Session UUID
  timestamp: string;               // ISO 8601 timestamp
  cwd: string;                     // Current working directory
  version: string;                 // Claude Code version (e.g., "2.0.76")
  gitBranch?: string;              // Current git branch (if in repo)
  slug?: string;                   // Human-readable session name
  isSidechain?: boolean;           // True for agent/sub-agent sessions
  userType?: 'external';           // Always 'external' for CLI sessions
  agentId?: string;                // Agent ID (for agent transcripts)
}
```

---

## Message Types

### 1. User Message

User prompts and tool results.

```typescript
interface UserMessage extends TranscriptLineBase {
  type: 'user';
  message: {
    role: 'user';
    content: string | ContentBlock[];
  };
  isMeta?: boolean;                // True for meta prompts (/init, etc.)
  toolUseResult?: ToolUseResult;   // Present when this is a tool result
}
```

#### Example: Initial Prompt

```json
{
  "parentUuid": null,
  "isSidechain": true,
  "userType": "external",
  "cwd": "/Users/hgeldenhuys/WebstormProjects/claude-code-sdk",
  "sessionId": "be59ef1a-4085-4f98-84ce-e9cbcb9500cc",
  "version": "2.0.76",
  "gitBranch": "main",
  "agentId": "a056a23",
  "slug": "stateless-floating-squirrel",
  "type": "user",
  "message": {
    "role": "user",
    "content": "Create a TypeScript utility function to parse JSON safely."
  },
  "uuid": "538eddd9-caab-4a69-b34e-1aeff1d1cc6e",
  "timestamp": "2026-01-07T03:35:26.374Z"
}
```

#### Example: Tool Result

```json
{
  "parentUuid": "41cdfb6e-e802-49d6-899b-66dd6d0c02a5",
  "isSidechain": true,
  "userType": "external",
  "cwd": "/Users/hgeldenhuys/WebstormProjects/claude-code-sdk",
  "sessionId": "be59ef1a-4085-4f98-84ce-e9cbcb9500cc",
  "version": "2.0.76",
  "gitBranch": "main",
  "agentId": "a056a23",
  "slug": "stateless-floating-squirrel",
  "type": "user",
  "message": {
    "role": "user",
    "content": [
      {
        "tool_use_id": "toolu_01Sn7sJJy8hPGVLQNihopjYo",
        "type": "tool_result",
        "content": "total 32\ndrwxr-xr-x@   8 hgeldenhuys  staff    256 Jan  6 15:00 .\n...",
        "is_error": false
      }
    ]
  },
  "uuid": "2585b352-d99a-456f-9c30-56f1df024042",
  "timestamp": "2026-01-07T03:35:33.356Z",
  "toolUseResult": {
    "stdout": "total 32\ndrwxr-xr-x@   8 hgeldenhuys  staff...",
    "stderr": "",
    "interrupted": false,
    "isImage": false
  }
}
```

#### Example: Meta Prompt (/init)

```json
{
  "parentUuid": "e1dcd67e-01da-453e-a55c-e5eaa2936376",
  "isSidechain": false,
  "userType": "external",
  "cwd": "/Users/hgeldenhuys/WebstormProjects/claude-code-sdk",
  "sessionId": "114fdaf5-594a-4bd2-bed1-8dc30589df2a",
  "version": "2.0.69",
  "gitBranch": "",
  "type": "user",
  "message": {
    "role": "user",
    "content": [
      {
        "type": "text",
        "text": "Please analyze this codebase and create a CLAUDE.md file..."
      }
    ]
  },
  "isMeta": true,
  "uuid": "a2042c47-6700-47d5-bbd2-14e260a51f40",
  "timestamp": "2025-12-14T20:23:43.886Z"
}
```

---

### 2. Assistant Message

Claude's responses including tool calls.

```typescript
interface AssistantMessage extends TranscriptLineBase {
  type: 'assistant';
  message: {
    model: string;                 // Model ID (e.g., "claude-opus-4-5-20251101")
    id: string;                    // API message ID (e.g., "msg_01FjnaBj42...")
    type: 'message';
    role: 'assistant';
    content: ContentBlock[];       // Text and/or tool_use blocks
    stop_reason: string | null;    // "end_turn", "tool_use", null
    stop_sequence: string | null;
    usage: TokenUsage;
  };
  requestId?: string;              // Request ID for tracking
}
```

#### Example: Text Response

```json
{
  "parentUuid": "538eddd9-caab-4a69-b34e-1aeff1d1cc6e",
  "isSidechain": true,
  "userType": "external",
  "cwd": "/Users/hgeldenhuys/WebstormProjects/claude-code-sdk",
  "sessionId": "be59ef1a-4085-4f98-84ce-e9cbcb9500cc",
  "version": "2.0.76",
  "gitBranch": "main",
  "agentId": "a056a23",
  "slug": "stateless-floating-squirrel",
  "message": {
    "model": "claude-opus-4-5-20251101",
    "id": "msg_01FjnaBj42YBJE9BdrP44R9Z",
    "type": "message",
    "role": "assistant",
    "content": [
      {
        "type": "text",
        "text": "I'll create a safe JSON parser utility..."
      }
    ],
    "stop_reason": "end_turn",
    "stop_sequence": null,
    "usage": {
      "input_tokens": 1500,
      "cache_creation_input_tokens": 0,
      "cache_read_input_tokens": 9000,
      "output_tokens": 250
    }
  },
  "type": "assistant",
  "uuid": "d38a4b9a-91a1-49c3-914d-629a7c6cc719",
  "timestamp": "2026-01-07T03:35:33.163Z"
}
```

#### Example: Tool Use (Multiple Tools)

```json
{
  "parentUuid": "538eddd9-caab-4a69-b34e-1aeff1d1cc6e",
  "type": "assistant",
  "message": {
    "model": "claude-opus-4-5-20251101",
    "id": "msg_01FjnaBj42YBJE9BdrP44R9Z",
    "type": "message",
    "role": "assistant",
    "content": [
      {
        "type": "tool_use",
        "id": "toolu_01Sn7sJJy8hPGVLQNihopjYo",
        "name": "Bash",
        "input": {
          "command": "ls -la ~/.claude/projects/ | head -20",
          "description": "List Claude projects directory"
        }
      },
      {
        "type": "tool_use",
        "id": "toolu_014DjXVhPmzmNF9iixw9S8zh",
        "name": "Bash",
        "input": {
          "command": "ls ~/.claude/projects/ | head -5",
          "description": "Get project folder names"
        }
      }
    ],
    "stop_reason": "tool_use",
    "stop_sequence": null,
    "usage": {
      "input_tokens": 3,
      "cache_creation_input_tokens": 9767,
      "cache_read_input_tokens": 12497,
      "cache_creation": {
        "ephemeral_5m_input_tokens": 9767,
        "ephemeral_1h_input_tokens": 0
      },
      "output_tokens": 147,
      "service_tier": "standard"
    }
  },
  "uuid": "d38a4b9a-91a1-49c3-914d-629a7c6cc719",
  "timestamp": "2026-01-07T03:35:33.163Z"
}
```

---

### 3. File History Snapshot

Tracks file state for undo/restore functionality.

```typescript
interface FileHistorySnapshot {
  type: 'file-history-snapshot';
  messageId: string;               // Associated message UUID
  snapshot: {
    messageId: string;
    trackedFileBackups: Record<string, FileBackup>;
    timestamp: string;             // ISO 8601
  };
  isSnapshotUpdate: boolean;       // True if updating existing snapshot
}

interface FileBackup {
  path: string;
  content: string;
  hash: string;
}
```

#### Example

```json
{
  "type": "file-history-snapshot",
  "messageId": "a966c5ff-1deb-4ba3-a0d0-d1d1307b8d29",
  "snapshot": {
    "messageId": "a966c5ff-1deb-4ba3-a0d0-d1d1307b8d29",
    "trackedFileBackups": {},
    "timestamp": "2026-01-02T19:58:23.012Z"
  },
  "isSnapshotUpdate": false
}
```

---

### 4. System Message

System-level messages, primarily hook summaries.

```typescript
interface SystemMessage extends TranscriptLineBase {
  type: 'system';
  subtype: SystemSubtype;
  // Additional fields depend on subtype
}

type SystemSubtype =
  | 'stop_hook_summary'    // Hook execution summary
  | 'turn_duration'        // Turn timing metrics
  | 'permission_granted'   // Permission was granted
  | 'permission_denied'    // Permission was denied
  | 'error';               // System error

interface StopHookSummary extends SystemMessage {
  subtype: 'stop_hook_summary';
  hookCount: number;                          // Number of hooks executed
  hookInfos: Array<{ command: string }>;      // Hook commands
  hookErrors: string[];                       // Any errors
  preventedContinuation: boolean;
  stopReason: string;
  hasOutput: boolean;
  level: string;
}

interface TurnDuration extends SystemMessage {
  subtype: 'turn_duration';
  durationMs: number;                         // Turn duration in milliseconds
  isMeta?: boolean;
}
```

#### Example: Stop Hook Summary

```json
{
  "parentUuid": "7617db2e-29d2-40e0-8d64-5c370be5050b",
  "isSidechain": false,
  "userType": "external",
  "cwd": "/Users/hgeldenhuys/WebstormProjects/claude-code-sdk",
  "sessionId": "114fdaf5-594a-4bd2-bed1-8dc30589df2a",
  "version": "2.0.69",
  "gitBranch": "",
  "slug": "glimmering-swinging-cocoa",
  "type": "system",
  "subtype": "stop_hook_summary",
  "hookCount": 4,
  "hookInfos": [
    {"command": "bun \"$CLAUDE_PROJECT_DIR\"/hooks/notification-hook.ts"},
    {"command": "bun \"$CLAUDE_PROJECT_DIR\"/.agent/hooks/Stop.ts"},
    {"command": "bun \"$CLAUDE_PROJECT_DIR\"/.agent/hooks/conversation-logger.ts"},
    {"command": "bun \"$CLAUDE_PROJECT_DIR\"/.agent/hooks/weave-analytics.ts"}
  ],
  "hookErrors": [],
  "preventedContinuation": false,
  "stopReason": "",
  "hasOutput": true,
  "level": "suggestion",
  "timestamp": "2025-12-15T03:17:51.080Z",
  "uuid": "e323c59c-6123-4eae-b9e6-1fce36e9544c",
  "toolUseID": "9a0d068a-d555-4e08-99d5-2889484c9a96"
}
```

#### Example: Turn Duration

```json
{
  "parentUuid": "abc123...",
  "type": "system",
  "subtype": "turn_duration",
  "durationMs": 65000,
  "timestamp": "2026-01-06T10:00:00Z",
  "uuid": "def456...",
  "sessionId": "session-123"
}
```

---

### 5. Progress Message

Progress updates during execution for hooks, bash commands, and agents.

```typescript
interface ProgressMessage extends TranscriptLineBase {
  type: 'progress';
  data: ProgressData;
  toolUseID?: string;
  parentToolUseID?: string;
}

type ProgressData = HookProgressData | BashProgressData | AgentProgressData;

// Hook execution progress
interface HookProgressData {
  type: 'hook_progress';
  hookEvent: HookEvent;          // Hook event type
  hookName: string;              // Hook name (e.g., "Stop", "PreToolUse:Read")
  command: string;               // Hook command being run
}

// Bash command execution progress
interface BashProgressData {
  type: 'bash_progress';
  output: string;                // Current output
  fullOutput: string;            // Complete output so far
  elapsedTimeSeconds: number;    // Time elapsed
  totalLines: number;            // Lines of output
}

// Subagent execution progress
interface AgentProgressData {
  type: 'agent_progress';
  agentId: string;               // Agent identifier
  prompt: string;                // Prompt sent to agent
  message: UserMessage;          // Full message object
  normalizedMessages: UserMessage[];  // Normalized message history
}

type HookEvent =
  | 'PreToolUse'
  | 'PostToolUse'
  | 'Stop'
  | 'SubagentStop'
  | 'SessionStart'
  | 'SessionEnd'
  | 'UserPromptSubmit'
  | 'PreCompact'
  | 'Notification';
```

#### Example: Hook Progress

```json
{
  "parentUuid": "82668b9b-b6ba-4eaf-b5ba-408c8c1c9f82",
  "type": "progress",
  "data": {
    "type": "hook_progress",
    "hookEvent": "Stop",
    "hookName": "Stop",
    "command": "bun \"$CLAUDE_PROJECT_DIR\"/hooks/notification-hook.ts"
  },
  "toolUseID": "276ccff2-5f4b-4547-8367-a4bf2acfac92",
  "parentToolUseID": "276ccff2-5f4b-4547-8367-a4bf2acfac92",
  "timestamp": "2026-01-16T22:51:55.393Z",
  "uuid": "82668b9b-b6ba-4eaf-b5ba-408c8c1c9f82",
  "sessionId": "be59ef1a-4085-4f98-84ce-e9cbcb9500cc"
}
```

#### Example: Bash Progress

```json
{
  "type": "progress",
  "data": {
    "type": "bash_progress",
    "output": "",
    "fullOutput": "",
    "elapsedTimeSeconds": 2,
    "totalLines": 0
  },
  "toolUseID": "bash-progress-0",
  "parentToolUseID": "toolu_012whDpXyHYdc9x8dGeyMmQD",
  "uuid": "011f76ed-2e9c-423a-9c77-35ab27729985",
  "timestamp": "2026-01-16T17:57:04.065Z"
}
```

#### Example: Agent Progress

```json
{
  "type": "progress",
  "data": {
    "type": "agent_progress",
    "agentId": "afd584e",
    "prompt": "Transform this feature idea into a structured story...",
    "message": {
      "type": "user",
      "message": { "role": "user", "content": [...] },
      "uuid": "ca628575-bc63-469c-b1ec-e530d332e3c4"
    },
    "normalizedMessages": [...]
  },
  "toolUseID": "agent_msg_015m677AXZ6jL3c3E5SriGxb",
  "parentToolUseID": "toolu_01NBGoTDbvsRCcWgFRGbDa1c",
  "uuid": "be38f7c5-9b93-46a8-8905-fa34268597d9",
  "timestamp": "2026-01-16T20:03:59.810Z"
}
```

---

### 6. Summary

Session summary for display and search.

```typescript
interface SummaryMessage {
  type: 'summary';
  summary: string;                 // Human-readable summary
  leafUuid: string;                // UUID of the last message
}
```

#### Example

```json
{
  "type": "summary",
  "summary": "Claude Code SDK: Tracking Changes & Plugin Marketplace",
  "leafUuid": "65dc9578-e41f-4873-8c73-ebc49c937afd"
}
```

---

### 7. Queue Operation

Background task notifications (e.g., agent completion).

```typescript
interface QueueOperationMessage {
  type: 'queue-operation';
  operation: 'enqueue' | 'dequeue';  // Queue operation type
  content: string;                   // Notification content (often XML)
  sessionId: string;
  timestamp: string;
}
```

#### Example

```json
{
  "type": "queue-operation",
  "operation": "enqueue",
  "timestamp": "2026-01-07T01:33:02.119Z",
  "sessionId": "be59ef1a-4085-4f98-84ce-e9cbcb9500cc",
  "content": "<agent-notification>\n<agent-id>a3564bc</agent-id>\n<output-file>/tmp/claude/.../tasks/a3564bc.output</output-file>\n<status>completed</status>\n<summary>Agent \"Create documentation\" completed.</summary>\nRead the output file to retrieve the full result.\n</agent-notification>"
}
```

---

## Content Block Types

Content within messages uses these block types:

```typescript
type ContentBlock = TextBlock | ToolUseBlock | ToolResultBlock | ThinkingBlock;

interface TextBlock {
  type: 'text';
  text: string;
}

interface ThinkingBlock {
  type: 'thinking';
  thinking: string;                // Claude's reasoning/chain-of-thought
  signature?: string;              // Cryptographic signature (for verification)
}

interface ToolUseBlock {
  type: 'tool_use';
  id: string;                      // Tool use ID (e.g., "toolu_01Sn7sJJy...")
  name: string;                    // Tool name (e.g., "Bash", "Read", "Write")
  input: Record<string, any>;      // Tool-specific input parameters
}

interface ToolResultBlock {
  type: 'tool_result';
  tool_use_id: string;             // Matches the tool_use id
  content: string;                 // Result content (often stdout)
  is_error: boolean;               // True if tool execution failed
}
```

### Example: Thinking Block

```json
{
  "type": "assistant",
  "message": {
    "content": [
      {
        "type": "thinking",
        "thinking": "The user is asking about session management. Let me analyze the codebase structure first to understand how sessions are currently handled...",
        "signature": "ErUBCkYIAxgC..."
      },
      {
        "type": "text",
        "text": "I'll help you with session management..."
      }
    ]
  }
}
```

---

## Tool Input Schemas

Common tool input structures:

### Bash Tool

```typescript
interface BashInput {
  command: string;                 // Shell command to execute
  description?: string;            // Human-readable description
  timeout?: number;                // Timeout in milliseconds
  run_in_background?: boolean;     // Run asynchronously
}
```

### Read Tool

```typescript
interface ReadInput {
  file_path: string;               // Absolute path to file
  offset?: number;                 // Line number to start from
  limit?: number;                  // Number of lines to read
}
```

### Write Tool

```typescript
interface WriteInput {
  file_path: string;               // Absolute path to file
  content: string;                 // File content to write
}
```

### Edit Tool

```typescript
interface EditInput {
  file_path: string;               // Absolute path to file
  old_string: string;              // Text to find
  new_string: string;              // Replacement text
  replace_all?: boolean;           // Replace all occurrences
}
```

### Glob Tool

```typescript
interface GlobInput {
  pattern: string;                 // Glob pattern (e.g., "**/*.ts")
  path?: string;                   // Directory to search in
}
```

### Grep Tool

```typescript
interface GrepInput {
  pattern: string;                 // Regex pattern to search
  path?: string;                   // File or directory to search
  glob?: string;                   // File pattern filter
  output_mode?: 'content' | 'files_with_matches' | 'count';
}
```

---

## Tool Use Result

Extended result information attached to user messages:

```typescript
interface ToolUseResult {
  // Bash tool results
  stdout?: string;                 // Standard output
  stderr?: string;                 // Standard error
  interrupted?: boolean;           // True if command was interrupted

  // Read/Write tool results
  filenames?: string[];            // Files affected

  // Image/screenshot results
  isImage?: boolean;               // True if result is an image

  // Generic
  content?: string;                // Raw content
}
```

---

## Token Usage

API usage tracking:

```typescript
interface TokenUsage {
  input_tokens: number;            // Input tokens used
  output_tokens: number;           // Output tokens generated
  cache_creation_input_tokens?: number;  // Tokens used for cache creation
  cache_read_input_tokens?: number;      // Tokens read from cache
  cache_creation?: {
    ephemeral_5m_input_tokens: number;   // 5-minute cache
    ephemeral_1h_input_tokens: number;   // 1-hour cache
  };
  service_tier?: string;           // API service tier
}
```

---

## Threading Model

Messages form a tree structure via `uuid` and `parentUuid`:

```
Initial prompt (parentUuid: null)
  |
  +-- Assistant response
        |
        +-- Tool result 1
        |     |
        |     +-- Assistant continues
        |
        +-- Tool result 2
              |
              +-- Assistant continues
```

**Key Rules:**
- First message has `parentUuid: null`
- Tool results reference the assistant message that invoked the tool
- Multiple tool results can share the same parent (parallel tool calls)
- The `leafUuid` in summary points to the last message in the main chain

---

## Agent vs Main Session

**Main Session** (`<uuid>.jsonl`):
- `isSidechain: false` (or absent)
- `agentId` absent
- Primary conversation with user

**Agent Session** (`agent-<id>.jsonl`):
- `isSidechain: true`
- `agentId` present (e.g., "a056a23")
- Spawned by main session for sub-tasks
- Links back via `sessionId` (matches main session)

---

## Parsing Example (TypeScript)

```typescript
import { readFileSync } from 'fs';

interface TranscriptLine {
  type: string;
  uuid?: string;
  parentUuid?: string | null;
  sessionId?: string;
  timestamp?: string;
  message?: {
    role: string;
    content: any;
    model?: string;
    usage?: Record<string, number>;
  };
  toolUseResult?: Record<string, any>;
}

function parseTranscript(filePath: string): TranscriptLine[] {
  const content = readFileSync(filePath, 'utf-8');
  const lines = content.trim().split('\n');

  const entries: TranscriptLine[] = [];
  for (const line of lines) {
    if (line.trim()) {
      try {
        entries.push(JSON.parse(line));
      } catch (e) {
        console.warn('Failed to parse line:', line.slice(0, 100));
      }
    }
  }

  return entries;
}

// Filter by type
function getAssistantMessages(entries: TranscriptLine[]) {
  return entries.filter(e => e.type === 'assistant');
}

// Extract tool calls
function getToolCalls(entry: TranscriptLine) {
  if (entry.type !== 'assistant' || !entry.message?.content) {
    return [];
  }

  const content = entry.message.content;
  if (!Array.isArray(content)) return [];

  return content.filter((block: any) => block.type === 'tool_use');
}

// Calculate token usage
function getTotalTokens(entries: TranscriptLine[]) {
  let input = 0;
  let output = 0;
  let cacheRead = 0;
  let cacheCreation = 0;

  for (const entry of entries) {
    if (entry.type === 'assistant' && entry.message?.usage) {
      const usage = entry.message.usage;
      input += usage.input_tokens || 0;
      output += usage.output_tokens || 0;
      cacheRead += usage.cache_read_input_tokens || 0;
      cacheCreation += usage.cache_creation_input_tokens || 0;
    }
  }

  return { input, output, cacheRead, cacheCreation };
}
```

---

## Common Patterns

### Finding All Files Modified

```typescript
function getModifiedFiles(entries: TranscriptLine[]): Set<string> {
  const files = new Set<string>();

  for (const entry of entries) {
    if (entry.type !== 'assistant') continue;

    const toolCalls = getToolCalls(entry);
    for (const call of toolCalls) {
      if (call.name === 'Write' || call.name === 'Edit') {
        const filePath = call.input?.file_path || call.input?.filePath;
        if (filePath) files.add(filePath);
      }
    }
  }

  return files;
}
```

### Extracting Conversation Flow

```typescript
function buildConversationTree(entries: TranscriptLine[]) {
  const byUuid = new Map<string, TranscriptLine>();
  const children = new Map<string, TranscriptLine[]>();

  for (const entry of entries) {
    if (entry.uuid) {
      byUuid.set(entry.uuid, entry);
    }

    const parent = entry.parentUuid || 'root';
    if (!children.has(parent)) {
      children.set(parent, []);
    }
    children.get(parent)!.push(entry);
  }

  return { byUuid, children };
}
```

### Calculating Session Duration

```typescript
function getSessionDuration(entries: TranscriptLine[]): number {
  const timestamps = entries
    .filter(e => e.timestamp)
    .map(e => new Date(e.timestamp!).getTime());

  if (timestamps.length < 2) return 0;

  return Math.max(...timestamps) - Math.min(...timestamps);
}
```

---

## Version History

| Version | Changes |
|---------|---------|
| 2.1.9 | Added `thinking` blocks, `queue-operation`, `bash_progress`, `agent_progress` |
| 2.0.76 | Current format documented here |
| 2.0.69 | Added hook summary system messages |
| 2.0.x | Introduced agent transcripts |

---

## Hook Event JSONL Files

When the `event-logger` built-in handler is enabled, hook events are logged to parallel JSONL files for analysis and indexing alongside transcripts.

### File Location

```
~/.claude/hooks/<project-hash>/<session-id>.hooks.jsonl
```

### Hook Event Structure

```typescript
interface HookEventLogEntry {
  /** Timestamp of the event */
  timestamp: string;               // ISO 8601
  /** Session ID (links to transcript file) */
  sessionId: string;
  /** Event type (PreToolUse, PostToolUse, etc.) */
  eventType: string;
  /** For tool events, the tool_use_id that links to transcript */
  toolUseId?: string;
  /** Tool name for tool events */
  toolName?: string;
  /** Handler decision (allow, block, etc.) */
  decision?: string;
  /** Results from all handlers */
  handlerResults?: Record<string, unknown>;
  /** Full hook input payload */
  input?: HookInput;
  /** Hook context (transcript_path, cwd, etc.) */
  context?: {
    hookEvent: string;
    transcriptPath: string;
    cwd: string;
    claudeCodeVersion: string;
  };
  /** Line number in the hooks log file */
  lineNumber?: number;
}
```

### Example Hook Event

```json
{
  "timestamp": "2026-01-17T18:30:00.000Z",
  "sessionId": "4b58bed8-133c-49b5-bba5-1de5c23a2aa0",
  "eventType": "PreToolUse",
  "toolUseId": "toolu_01Sn7sJJy8hPGVLQNihopjYo",
  "toolName": "Bash",
  "decision": "allow",
  "handlerResults": {
    "dangerous-command-guard": { "allowed": true }
  },
  "input": {
    "session_id": "4b58bed8-133c-49b5-bba5-1de5c23a2aa0",
    "tool_name": "Bash",
    "tool_input": { "command": "ls -la" },
    "tool_use_id": "toolu_01Sn7sJJy8hPGVLQNihopjYo"
  },
  "context": {
    "hookEvent": "PreToolUse",
    "transcriptPath": "~/.claude/projects/-Users-me-project/4b58bed8.jsonl",
    "cwd": "/Users/me/project",
    "claudeCodeVersion": "2.0.76"
  },
  "lineNumber": 42
}
```

### Linking Hook Events to Transcript Lines

Hook events can be joined with transcript lines using these keys:

| Hook Event | Join Key | Transcript Field |
|------------|----------|------------------|
| PreToolUse, PostToolUse | `toolUseId` | `message.content[].id` (tool_use blocks) |
| UserPromptSubmit | Prompt text match | `message.content` (user messages) |
| Stop, SubagentStop | `sessionId` | `sessionId` + last assistant message |
| SessionStart, SessionEnd | `sessionId` | Transcript filename |

### SQLite JOIN Example

With the unified transcript/hook indexer:

```sql
-- Find all hook decisions for a specific tool call
SELECT
  h.eventType,
  h.toolName,
  h.decision,
  l.content_text
FROM hook_events h
JOIN lines l ON h.session_id = l.session_id
  AND h.tool_use_id = l.uuid
WHERE h.tool_use_id = 'toolu_01Sn7sJJy8hPGVLQNihopjYo';

-- Find blocked tool calls
SELECT
  h.timestamp,
  h.toolName,
  h.decision,
  json_extract(h.handler_results, '$.dangerous-command-guard.reason') as block_reason
FROM hook_events h
WHERE h.decision = 'block';

-- Session statistics with hook events
SELECT
  s.session_id,
  s.slug,
  COUNT(DISTINCT l.id) as transcript_lines,
  COUNT(DISTINCT h.id) as hook_events
FROM sessions s
LEFT JOIN lines l ON s.session_id = l.session_id
LEFT JOIN hook_events h ON s.session_id = h.session_id
GROUP BY s.session_id;
```

### CLI Commands

```bash
# Build unified index (transcripts + hooks)
bun run bin/transcript.ts index build

# Check index status
bun run bin/transcript.ts index status
# Shows:
#   Transcripts: N lines, M sessions
#   Hook Events: X events, Y hook files

# Watch for changes (both transcripts and hooks)
bun run bin/transcript.ts index daemon start
```

---

## Related Files

- **SKILL.md** - Main transcript intelligence skill
- **PATTERNS.md** - Analysis patterns and recipes
- **EXAMPLES.md** - Complete analysis examples
