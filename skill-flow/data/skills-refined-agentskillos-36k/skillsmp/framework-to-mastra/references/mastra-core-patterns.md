# Mastra Core Patterns

Essential patterns for Mastra v1 Beta agent development.

**Target version**: Mastra v1 Beta (stable release expected January 2026)
**Required**: Node.js 22.13.0+

## Installation

```bash
# Install v1 Beta packages
npm install @mastra/core@beta @mastra/hono@beta
npm install @ai-sdk/openai  # or other provider
npm install zod hono @hono/node-server
```

## Agent Definition

```typescript
import { Agent } from "@mastra/core/agent";
import { openai } from "@ai-sdk/openai";

export const myAgent = new Agent({
  name: "my-agent",                             // Required: unique identifier
  instructions: "You are a helpful assistant.", // Required: system prompt
  model: openai("gpt-4o-mini"),                 // Required: LLM model
  tools: { weatherTool, searchTool },           // Optional: named tools object
});
```

### Model Options

```typescript
// SDK instances
model: openai("gpt-4o-mini")
model: anthropic("claude-3-5-sonnet-20241022")

// Router strings
model: "openai/gpt-4o-mini"
model: "anthropic/claude-3-5-sonnet"

// Fallback array
model: [
  { model: "openai/gpt-4o", maxRetries: 3 },
  { model: "anthropic/claude-3-5-sonnet", maxRetries: 2 },
]
```

### Dynamic Instructions

```typescript
const agent = new Agent({
  name: "personalized-agent",
  instructions: ({ runtimeContext }) => {
    const userName = runtimeContext.get("user-name");
    const preferences = runtimeContext.get("preferences");

    return `You are a personal assistant for ${userName}.

Their preferences:
${JSON.stringify(preferences, null, 2)}

Always address them by name and respect their preferences.`;
  },
  model: openai("gpt-4o-mini"),
});
```

## Tool Signatures (v1 Beta - CRITICAL)

```typescript
import { createTool } from "@mastra/core/tools";
import { z } from "zod";

export const myTool = createTool({
  id: "my-tool",
  description: "Description for LLM to understand when to use this tool",
  inputSchema: z.object({
    query: z.string().describe("The search query"),
  }),
  outputSchema: z.object({
    results: z.array(z.string()),
  }),

  // v1 Beta signature: execute(inputData, context)
  execute: async (inputData, context) => {
    const { query } = inputData;  // First parameter: parsed input
    const { mastra, runtimeContext, abortSignal } = context;  // Second: context

    // Access nested agents via mastra
    const helper = mastra?.getAgent("helperAgent");

    // Always check abort signal for long operations
    if (abortSignal?.aborted) throw new Error("Aborted");

    return { results: ["result1", "result2"] };
  },
});
```

**WRONG for v1 Beta:**
```typescript
execute: async ({ context }) => { ... }  // This is stable 0.24.x signature
```

## Memory Configuration

```typescript
// Using memory in agent calls
const response = await agent.generate("Remember my name is Alex", {
  memory: {
    thread: "conversation-123",   // Isolates conversation
    resource: "user-456",         // Associates with user
  },
});

// Memory with storage
import { LibSQLStore } from "@mastra/libsql";

const mastra = new Mastra({
  agents: { myAgent },
  storage: new LibSQLStore({
    url: "file:./mastra.db",
  }),
});
```

## Structured Output

```typescript
import { z } from "zod";

const response = await agent.generate("List three cities in Japan", {
  output: z.object({
    cities: z.array(z.object({
      name: z.string(),
      population: z.number().optional(),
    })),
  }),
});

// response.object is typed as { cities: { name: string; population?: number }[] }
console.log(response.object.cities);
```

## Mastra Instance

```typescript
import { Mastra } from "@mastra/core/mastra";

export const mastra = new Mastra({
  agents: { weatherAgent, assistantAgent },
  workflows: { dataPipeline },
  storage: new LibSQLStore({ url: "file:./mastra.db" }),
});

// Accessing agents
const agent = mastra.getAgent("weather-agent");
const result = await agent?.generate("Hello");
```

## Common Mistakes Quick Reference

| Topic | Wrong | Correct |
|-------|-------|---------|
| Imports | `import { Agent } from "@mastra/core"` | `import { Agent } from "@mastra/core/agent"` |
| Tools array | `tools: [tool1, tool2]` | `tools: { tool1, tool2 }` |
| Memory context | `{ threadId: "123" }` | `{ memory: { thread: "123", resource: "user" } }` |
| Workflow data | `context.steps.step1.output` | `inputData` or `getStepResult("step-1")` |
| After parallel | `inputData.result` | `inputData["step-id"].result` |
| After branch | `inputData.result` | `inputData["step-id"]?.result` (optional) |
| Nested agents | `import agent; agent.generate()` | `mastra.getAgent("name").generate()` |
| State mutation | `state.counter++` | `setState({ ...state, counter: state.counter + 1 })` |
| v1 tool exec | `execute: async ({ context })` | `execute: async (inputData, context)` |

## Project Structure

```
my-agent/
├── src/
│   ├── mastra/
│   │   ├── agents/
│   │   │   └── my-agent.ts
│   │   ├── tools/
│   │   │   └── my-tool.ts
│   │   ├── workflows/
│   │   │   └── my-workflow.ts
│   │   └── index.ts          # Mastra instance
│   ├── schemas/
│   │   └── my-schemas.ts     # Zod schemas
│   └── index.ts              # Hono server
├── package.json
├── tsconfig.json
└── Dockerfile
```

## TypeScript Configuration

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "outDir": "./dist"
  },
  "include": ["src/**/*"]
}
```

## Package.json Scripts

```json
{
  "scripts": {
    "dev": "tsx watch src/index.ts",
    "build": "tsc",
    "start": "node dist/index.js",
    "test": "vitest"
  }
}
```
