# TypeScript SDK Reference

Complete API reference for Claude Agent SDK TypeScript package.

## Installation

```bash
npm install @anthropic/claude-sdk
# or
yarn add @anthropic/claude-sdk
```

## Core Functions

### query()

One-shot task execution with full autonomy.

```typescript
import { query } from '@anthropic/claude-sdk';

const result = await query({
  prompt: string,                     // Task description
  model?: string,                     // Default: "claude-sonnet-4-20250514"
  maxTokens?: number,                 // Default: 4096
  tools?: string[],                   // Built-in tools to enable
  mcpServers?: MCPServer[],           // MCP servers to connect
  allowedCommands?: string[],         // Bash command whitelist
  deniedCommands?: string[],          // Bash command blacklist
  workingDirectory?: string,          // Working directory
  timeout?: number,                   // Timeout in seconds
  hooks?: Hook[],                     // Behavior hooks
}): Promise<QueryResult>
```

**Returns**: `QueryResult` object

```typescript
interface QueryResult {
  content: string;           // Final response text
  toolCalls: ToolCall[];     // Tools that were used
  tokensUsed: number;        // Total tokens consumed
  duration: number;          // Execution time in seconds
  status: 'success' | 'error' | 'timeout';
}
```

**Example**:

```typescript
import { query } from '@anthropic/claude-sdk';

const result = await query({
  prompt: "Find all TypeScript files with TODO comments",
  tools: ["Glob", "Grep", "Read"],
  workingDirectory: "/path/to/project"
});

console.log(`Found: ${result.content}`);
console.log(`Used ${result.tokensUsed} tokens in ${result.duration}s`);
```

---

## ClaudeSDKClient

Multi-turn conversation client for complex tasks.

### Constructor

```typescript
import { ClaudeSDKClient } from '@anthropic/claude-sdk';

const client = new ClaudeSDKClient({
  model?: string,                     // Default: "claude-sonnet-4-20250514"
  systemPrompt?: string,              // System instructions
  maxTokens?: number,                 // Max tokens per turn
  tools?: string[],                   // Built-in tools
  mcpServers?: MCPServer[],
  hooks?: Hook[],
  apiKey?: string,                    // Override ANTHROPIC_API_KEY env
  baseUrl?: string,                   // Custom API endpoint
});
```

### createSession()

Create a new conversation session.

```typescript
async createSession(options?: {
  sessionId?: string,                 // Custom session ID
  context?: Record<string, any>,      // Initial context variables
  history?: Message[],                // Pre-load conversation history
}): Promise<Session>
```

**Example**:

```typescript
const client = new ClaudeSDKClient({
  model: "claude-sonnet-4-20250514",
  systemPrompt: "You are a code reviewer focusing on security.",
  tools: ["Read", "Grep", "Glob"]
});

const session = await client.createSession();
try {
  await session.query("Read the authentication module");
  await session.query("What security issues do you see?");
  const recommendations = await session.query("Provide recommendations");
} finally {
  await session.close();
}
```

---

## Session

Active conversation session with context.

### query()

Send a query within the session.

```typescript
async query(
  prompt: string,
  options?: {
    tools?: string[],                 // Override session tools
    maxTokens?: number,               // Override max tokens
    stream?: boolean,                 // Enable streaming
  }
): Promise<SessionResponse>
```

### getHistory()

Get conversation history.

```typescript
getHistory(): Message[]
```

### addContext()

Add context variables accessible to the agent.

```typescript
addContext(key: string, value: any): void
```

### fork()

Create a branched session for exploration.

```typescript
async fork(branchName?: string): Promise<Session>
```

**Example**:

```typescript
const session = await client.createSession();

await session.query("Analyze options for refactoring");

// Fork to explore different approaches
const branchA = await session.fork("approach-a");
const branchB = await session.fork("approach-b");

const resultA = await branchA.query("Try extracting to separate class");
const resultB = await branchB.query("Try using composition pattern");

// Compare results
await session.query(`Compare: ${resultA.content} vs ${resultB.content}`);
```

---

## TypeScript-Specific Features

### Type-Safe Tool Definitions

```typescript
import { defineTool, ToolInput, ToolOutput } from '@anthropic/claude-sdk';

interface AnalyzeInput extends ToolInput {
  filePath: string;
  analysisType: 'security' | 'performance' | 'quality';
}

interface AnalyzeOutput extends ToolOutput {
  issues: Array<{
    severity: 'high' | 'medium' | 'low';
    message: string;
    line: number;
  }>;
}

const analyzeTool = defineTool<AnalyzeInput, AnalyzeOutput>({
  name: 'analyze',
  description: 'Analyze a file for issues',
  inputSchema: {
    type: 'object',
    properties: {
      filePath: { type: 'string' },
      analysisType: { type: 'string', enum: ['security', 'performance', 'quality'] }
    },
    required: ['filePath', 'analysisType']
  },
  execute: async (input) => {
    // Implementation
    return { issues: [] };
  }
});
```

### Generic Session Types

```typescript
interface MySessionContext {
  projectPath: string;
  language: 'typescript' | 'python';
}

const session = await client.createSession<MySessionContext>({
  context: {
    projectPath: '/path/to/project',
    language: 'typescript'
  }
});

// Type-safe context access
const context = session.getContext();
console.log(context.projectPath); // Typed as string
```

---

## Error Handling

```typescript
import {
  ClaudeSDKError,
  ToolError,
  RateLimitError,
  AuthenticationError,
  TimeoutError,
  HookRejectionError,
} from '@anthropic/claude-sdk';

try {
  const result = await query({ prompt: "Execute task" });
} catch (error) {
  if (error instanceof ToolError) {
    console.error(`Tool ${error.toolName} failed: ${error.message}`);
    console.error(`Arguments: ${JSON.stringify(error.args)}`);
  } else if (error instanceof RateLimitError) {
    console.error(`Rate limited. Retry after: ${error.retryAfter}s`);
  } else if (error instanceof TimeoutError) {
    console.error("Operation timed out");
  } else if (error instanceof ClaudeSDKError) {
    console.error(`SDK error: ${error.message}`);
  }
}
```

---

## Hooks System

### Creating Custom Hooks

```typescript
import { Hook, HookResult, ToolCallContext } from '@anthropic/claude-sdk';

class ApprovalHook implements Hook {
  async onToolCall(context: ToolCallContext): Promise<HookResult> {
    const { toolName, args } = context;

    if (['Write', 'Edit', 'Bash'].includes(toolName)) {
      const approved = await this.requestApproval(toolName, args);
      return approved ? HookResult.ALLOW : HookResult.REJECT;
    }

    return HookResult.ALLOW;
  }

  private async requestApproval(tool: string, args: any): Promise<boolean> {
    // Implementation - could be CLI prompt, API call, etc.
    console.log(`Approval needed for ${tool}:`, args);
    return true;
  }
}

class AuditHook implements Hook {
  async onToolCall(context: ToolCallContext): Promise<HookResult> {
    console.log(`[AUDIT] ${context.toolName}(${JSON.stringify(context.args)})`);
    return HookResult.ALLOW;
  }

  async onToolResult(context: ToolResultContext): Promise<void> {
    console.log(`[AUDIT] Result: ${context.result.substring(0, 100)}...`);
  }
}

// Use hooks
const client = new ClaudeSDKClient({
  hooks: [new ApprovalHook(), new AuditHook()]
});
```

---

## Streaming

```typescript
const session = await client.createSession();

// Streaming with async iterator
for await (const chunk of session.queryStream("Explain this code")) {
  process.stdout.write(chunk.content);
}

// Streaming with callbacks
await session.query("Explain this code", {
  stream: true,
  onChunk: (chunk) => {
    process.stdout.write(chunk.content);
  },
  onToolCall: (toolCall) => {
    console.log(`\n[Tool: ${toolCall.name}]`);
  }
});
```

---

## Configuration

### Environment Variables

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-...

# Optional
CLAUDE_SDK_MODEL=claude-sonnet-4-20250514
CLAUDE_SDK_MAX_TOKENS=8192
CLAUDE_SDK_TIMEOUT=300
```

### Configuration File

Create `claude-sdk.config.ts`:

```typescript
import { ClaudeSDKConfig } from '@anthropic/claude-sdk';

export const config: ClaudeSDKConfig = {
  model: 'claude-sonnet-4-20250514',
  maxTokens: 8192,
  timeout: 300,

  tools: {
    enabled: ['Read', 'Write', 'Edit', 'Bash', 'Grep', 'Glob'],
  },

  bash: {
    allowedCommands: ['npm', 'node', 'tsc', 'jest'],
    deniedCommands: ['rm -rf', 'sudo'],
  },
};
```

---

## Integration with Next.js / Node.js

### API Route Example

```typescript
// pages/api/agent.ts (Next.js)
import { NextApiRequest, NextApiResponse } from 'next';
import { query } from '@anthropic/claude-sdk';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { task } = req.body;

  try {
    const result = await query({
      prompt: task,
      tools: ['Read', 'Grep'],
      timeout: 60,
    });

    res.status(200).json({
      content: result.content,
      tokensUsed: result.tokensUsed,
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
}
```

### Express Middleware

```typescript
import express from 'express';
import { ClaudeSDKClient } from '@anthropic/claude-sdk';

const app = express();
const client = new ClaudeSDKClient();

// Session middleware
app.use('/agent', async (req, res, next) => {
  const sessionId = req.headers['x-session-id'] as string;

  if (sessionId) {
    req.agentSession = await client.resumeSession(sessionId);
  } else {
    req.agentSession = await client.createSession();
  }

  res.on('finish', async () => {
    // Cleanup or persist session
  });

  next();
});

app.post('/agent/query', async (req, res) => {
  const result = await req.agentSession.query(req.body.prompt);
  res.json(result);
});
```

---

## Best Practices

### 1. Use Proper TypeScript Types

```typescript
import type { QueryResult, Session, Hook } from '@anthropic/claude-sdk';

// Always type your results
async function analyze(file: string): Promise<QueryResult> {
  return query({
    prompt: `Analyze ${file}`,
    tools: ['Read'],
  });
}
```

### 2. Handle Cleanup Properly

```typescript
// Use try-finally for cleanup
const session = await client.createSession();
try {
  await session.query("...");
} finally {
  await session.close();
}

// Or use a helper function
async function withSession<T>(
  client: ClaudeSDKClient,
  fn: (session: Session) => Promise<T>
): Promise<T> {
  const session = await client.createSession();
  try {
    return await fn(session);
  } finally {
    await session.close();
  }
}

// Usage
const result = await withSession(client, async (session) => {
  return session.query("Analyze code");
});
```

### 3. Implement Retry Logic

```typescript
import { RateLimitError } from '@anthropic/claude-sdk';

async function queryWithRetry(
  prompt: string,
  maxRetries = 3
): Promise<QueryResult> {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await query({ prompt });
    } catch (error) {
      if (error instanceof RateLimitError && attempt < maxRetries - 1) {
        await new Promise(r => setTimeout(r, error.retryAfter * 1000));
      } else {
        throw error;
      }
    }
  }
  throw new Error('Max retries exceeded');
}
```
