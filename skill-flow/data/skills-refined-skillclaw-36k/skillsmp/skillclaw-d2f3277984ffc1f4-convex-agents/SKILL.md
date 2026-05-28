---
name: convex-agents
description: Use this skill when you want to build persistent, stateful AI agents with the Convex framework, including features like thread management, tool integration, streaming responses, RAG patterns, and workflow orchestration.
---

# Skill body

## Documentation Sources

Before implementing, do not assume; fetch the latest documentation:

- Primary: [Convex AI Documentation](https://docs.convex.dev/ai)
- Convex Agent Component: [NPM Package](https://www.npmjs.com/package/@convex-dev/agent)
- For broader context: [LLMs Overview](https://docs.convex.dev/llms.txt)

## Instructions

### Why Convex for AI Agents

- **Persistent State**: Conversation history survives restarts.
- **Real-time Updates**: Stream responses to clients automatically.
- **Tool Execution**: Run Convex functions as agent tools.
- **Durable Workflows**: Long-running agent tasks with reliability.
- **Built-in RAG**: Vector search for knowledge retrieval.

### Setting Up Convex Agent

```bash
npm install @convex-dev/agent ai openai
```

```typescript
// convex/agent.ts
import { Agent } from "@convex-dev/agent";
import { components } from "./_generated/api";
import { OpenAI } from "openai";

const openai = new OpenAI();

export const agent = new Agent(components.agent, {
  chat: openai.chat,
  textEmbedding: openai.embeddings,
});
```

### Thread Management

```typescript
// convex/threads.ts
import { mutation, query } from "./_generated/server";
import { v } from "convex/values";
import { agent } from "./agent";

// Create a new conversation thread
export const createThread = mutation({
  args: {
    userId: v.id("users"),
    title: v.optional(v.string()),
  },
  returns: v.id("threads"),
  handler: async (ctx, args) => {
    const threadId = await agent.createThread(ctx, {
      userId: args.userId,
      metadata: {
        title: args.title ?? "New Conversation",
        createdAt: Date.now(),
      },
    });
    return threadId;
  },
});

// List user's threads
export const listThreads = query({
  args: { userId: v.id("users") },
  returns: v.array(v.object({
    _id: v.id("threads"),
    title: v.string(),
    lastMessageAt: v.optional(v.number()),
  })),
  handler: async (ctx, args) => {
    return await agent.listThreads(ctx, {
      userId: args.userId,
    });
  },
});

// Get thread messages
export const getMessages = query({
  args: { threadId: v.id("threads") },
  returns: v.array(v.object({
    _id: v.id("messages"),
    content: v.string(),
    createdAt: v.number(),
  })),
  handler: async (ctx, args) => {
    return await agent.getMessages(ctx, {
      threadId: args.threadId,
    });
  },
});
```