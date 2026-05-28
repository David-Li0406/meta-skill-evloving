---
name: assistant-ui
description: Use this skill when you need guidance on the assistant-ui library for building AI chat interfaces, including architecture, debugging, and codebase understanding.
---

# assistant-ui

**Always consult [assistant-ui.com/llms.txt](https://assistant-ui.com/llms.txt) for the latest API.**

The assistant-ui is a React library designed for creating AI chat interfaces using composable primitives.

## References

- [Architecture Overview](./references/architecture.md) -- Core architecture and layered system
- [Package Selection Guide](./references/packages.md) -- Overview of available packages

## When to Use

| Use Case               | Best For                               |
|-----------------------|----------------------------------------|
| Chat UI from scratch   | Full control over UX                   |
| Existing AI backend     | Connects to any streaming backend      |
| Custom message types    | Tools, images, files, custom parts    |
| Multi-thread apps       | Built-in thread list management        |
| Production apps         | Cloud persistence, auth, analytics     |

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  UI Components (Primitives)             │
│    ThreadPrimitive, MessagePrimitive, ComposerPrimitive │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                   Context Hooks                         │
│   useAssistantApi, useAssistantState, useAssistantEvent │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                    Runtime Layer                        │
│  AssistantRuntime → ThreadRuntime → MessageRuntime      │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                   Adapters/Backend                      │
│   AI SDK · LangGraph · Custom · Cloud Persistence       │
└─────────────────────────────────────────────────────────┘
```

## Pick a Runtime

```
Using AI SDK?
├─ Yes → useChatRuntime (recommended)
└─ No
   ├─ External state (Redux/Zustand)? → useExternalStoreRuntime
   ├─ LangGraph agent? → useLangGraphRuntime
   ├─ AG-UI protocol? → useAgUiRuntime
   ├─ A2A protocol? → useA2ARuntime
   └─ Custom API → useLocalRuntime
```

## Core Packages

| Package                          | Purpose                          |
|----------------------------------|----------------------------------|
| `@assistant-ui/react`            | UI primitives & hooks            |
| `@assistant-ui/react-ai-sdk`     | Vercel AI SDK v6 adapter         |