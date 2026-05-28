# Advanced Guides & Recipes

## When to use

- To build complex, stateful conversational UIs with generative components and tool-calling capabilities.
- When you need to persist and rehydrate chat conversations across different user sessions.
- To proactively suggest context-aware actions or shortcuts to the user.
- To integrate with external services by allowing the model to call tools hosted on a remote server.

## Core concepts

- **UI Chatbot**: A stateful conversational agent, orchestrated by the `useUiChat` hook, that can both call tools and render generative UI in response to user prompts.
- **Chat Threads**: A mechanism for persisting conversation history on a server. The client rehydrates the chat using a `threadId`, and subsequent messages are sent as deltas.
- **Predictive Actions**: Using an LLM, typically with `useStructuredCompletion`, to anticipate a user's next action based on their recent activity and the current application state.
- **Remote Tools (MCP)**: The Model Context Protocol (MCP) allows the LLM to call tools hosted on a remote server, separate from your main application backend.
- **Streaming Markdown**: Using a streaming-safe renderer like `Streamdown` to display Markdown content that arrives incrementally, without layout shifts or errors from incomplete syntax.

## Rules & constraints

- **MUST**: When building a UI chatbot, explicitly define and expose every tool (`useTool`) and UI component (`exposeComponent`) the model is permitted to use.
- **MUST**: To enable chat threads, you must implement the `loadThread` and `saveThread` async functions on your server-side adapter configuration.
- **SHOULD**: When generating predictive actions, provide the model with tools to read the current application state to ensure its suggestions are relevant and not duplicative.
- **SHOULD**: Use a streaming-safe Markdown renderer like `Streamdown` for assistant messages to prevent UI glitches.

## Key Learning Points

### Point 1: Building a UI Chatbot

The core pattern is to define your application's state and actions (e.g., in a React Context), expose capabilities to the model through tools (`useTool`), whitelist UI components for rendering (`exposeComponent`), and then orchestrate the interaction using the `useUiChat` hook.

```ts
// High-level structure of a UI Chatbot component
const tools = [useGetLightsTool(), useControlLightTool()]
const components = [exposedCardComponent, exposedLightListItemComponent]

const { messages, sendMessage } = useUiChat({
  model: 'gpt-4o',
  system: 'You are a smart home assistant.',
  tools,
  components,
})

// Render messages, switching between user content and assistant UI
messages.map(msg => (msg.role === 'user' ? msg.content : msg.ui))
```

### Point 2: Persisting Conversations with Threads

Enable chat persistence by implementing two functions on your server's adapter and passing a `threadId` to the client-side hook. This makes conversations stateful across sessions.

```ts
// Server-side (in your /api/chat endpoint)
const stream = HashbrownOpenAI.stream.text({
  apiKey: process.env.OPENAI_API_KEY,
  request: req.body,
  loadThread: async threadId => db.threads.get(threadId),
  saveThread: async (thread, threadId) => db.threads.put(threadId, thread),
})

// Client-side (in your React component)
const chat = useChat({
  model: 'gpt-4o',
  threadId: 'some-persistent-id', // from URL, user session, etc.
})
```

### Point 3: Creating Predictive Suggestions

Use `useStructuredCompletion` with a detailed schema to ask the model for a list of suggested next actions. Provide the model with the user's last action as `input` and give it `tools` to inspect the current application state.

```ts
const { output } = useStructuredCompletion({
  model: 'gpt-4o',
  input: lastUserAction, // Triggers re-computation
  tools: [getLightsTool, getScenesTool], // Gives model context
  schema: s.object('Response', {
    predictions: s.streaming.array('Suggestions', predictionSchema),
  }),
  system: 'Predict the next action a user might take...',
})
```

### Point 4: Rendering Streaming Markdown

For a smooth user experience, use a streaming-safe renderer for assistant text content. `Streamdown` is a drop-in replacement for `react-markdown` that handles incomplete markdown without errors.

```tsx
import { useChat } from '@hashbrownai/react';
import { Streamdown } from 'streamdown';

const { messages } = useChat(...);

// In your render logic for assistant messages:
messages.map(message =>
  message.role === 'assistant' ? (
    <Streamdown>{message.content}</Streamdown>
  ) : (
    //...
  )
);
```

## Pitfalls

- **Model Confusion**: Exposing too many complex or similarly described tools and components can degrade the model's ability to make correct choices.
- **Poor UX with Threads**: Not handling the `isLoadingThread` and `isSavingThread` states in your UI can make the application feel unresponsive during persistence operations.
- **Irrelevant Predictions**: Failing to provide the model with tools to read the current application state will lead to generic or duplicative suggestions.

## Source map

- `/recipes/ui-chatbot.md` — A comprehensive, step-by-step guide to building a conversational UI.
- `/recipes/threads.md` — Details on persisting and rehydrating chat conversations.
- `/recipes/predictive-actions.md` — A recipe for generating context-aware user suggestions.
- `/recipes/remote-mcp.md` — Guide for integrating with tools hosted on external servers.
- `/recipes/magic-text.md` — How to use `Streamdown` for streaming-safe Markdown rendering.
