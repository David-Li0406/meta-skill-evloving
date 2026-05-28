---
name: assistant-ui-tools
description: Use this skill when implementing LLM tools, tool call rendering, or human-in-the-loop patterns in the assistant UI.
---

# Skill body

## Overview

Tools allow LLMs to trigger actions with custom UI rendering. This guide covers tool registration and UI integration in the assistant UI.

**Always consult [assistant-ui.com/llms.txt](https://assistant-ui.com/llms.txt) for the latest API.**

## Tool Types

```
Where does the tool execute?
├─ Backend (LLM calls API) → AI SDK tool()
│  └─ Want custom UI? → makeAssistantToolUI
└─ Frontend (browser-only) → makeAssistantTool
   └─ Want custom UI? → makeAssistantToolUI
```

## Backend Tool with UI

To create a backend tool with a UI, follow these steps:

1. **Define the Tool**: Create a tool using the `tool` function.
2. **Implement Execution Logic**: Define how the tool will execute.
3. **Stream Text**: Use the `streamText` function to integrate the tool into your application.

```ts
// Backend (app/api/chat/route.ts)
import { tool, stepCountIs } from "ai";
import { z } from "zod";

const tools = {
  get_weather: tool({
    description: "Get weather for a city",
    inputSchema: z.object({ city: z.string() }),
    execute: async ({ city }) => ({ temp: 22, city }),
  }),
};

const result = streamText({
  model: openai("gpt-4o"),
  messages,
  tools,
  stopWhen: stepCountIs(5),
});
```

## Frontend Tool with UI

To create a frontend-only tool, follow these steps:

1. **Define the Tool**: Use `makeAssistantTool` to create the tool.
2. **Implement Execution Logic**: Define the parameters and execution logic.
3. **Render the UI**: Use `makeAssistantToolUI` to create the UI component.

```tsx
// Frontend
import { makeAssistantToolUI } from "@assistant-ui/react";

const WeatherToolUI = makeAssistantToolUI({
  toolName: "get_weather",
  render: ({ args, result, status }) => {
    if (status === "running") return <div>Loading weather...</div>;
    return <div>{result?.city}: {result?.temp}°C</div>;
  },
});

// Register in app
<AssistantRuntimeProvider runtime={runtime}>
  <WeatherToolUI />
  <Thread />
</AssistantRuntimeProvider>
```

## Frontend-Only Tool Example

```tsx
import { makeAssistantTool } from "@assistant-ui/react";
import { z } from "zod";

const CopyTool = makeAssistantTool({
  toolName: "copy_to_clipboard",
  parameters: z.object({ text: z.string() }),
  execute: async ({ text }) => {
    await navigator.clipboard.writeText(text);
    return { success: true };
  },
});

// Register in app
<AssistantRuntimeProvider runtime={runtime}>
  <CopyTool />
  <Thread />
</AssistantRuntimeProvider>
```

## API Reference

```tsx
// makeAssistantToolUI props
interface ToolUIProps {
  toolCallId: string;
  toolName: string;
  args: Record<string, unknown>;
  argsText: string;
  result?: unknown;
  status: "running" | "complete" | "incomplete" | "required";
}
```