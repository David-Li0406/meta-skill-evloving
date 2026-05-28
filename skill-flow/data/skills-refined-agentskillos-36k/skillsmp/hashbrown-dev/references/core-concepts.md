# Core Concepts

## When to use

- To build advanced AI interactions beyond simple text generation.
- When you need the LLM to generate dynamic user interfaces using your components.
- To allow the model to call client-side functions to access application state or perform actions.
- For safely executing LLM-generated JavaScript for tasks like data transformation or visualization.
- When streaming structured data is necessary for a responsive user experience.
- To modify requests on the server-side for security, context injection, or dynamic configuration.

## Core concepts

- **System Instructions**: High-level guidance (role, tone, rules, examples) that steers the model's behavior for the entire conversation.
- **Generative UI**: The practice of allowing an LLM to render whitelisted, trusted React components to form a user interface.
- **Tool Calling**: A mechanism that enables the LLM to execute predefined client-side functions to interact with the application.
- **JS Runtime**: A sandboxed WebAssembly-based environment (QuickJS) for safely executing LLM-generated JavaScript code in the browser.
- **Streaming**: The process of receiving and rendering data from the model incrementally as it's being generated, improving perceived performance.
- **Request Transformation**: A server-side interceptor (`transformRequestOptions`) to modify requests before they are sent to the LLM provider.

## Rules & constraints

- **MUST**: Provide clear, structured system instructions to guide the model. Use sections for `ROLE & TONE`, `RULES`, and `EXAMPLES`.
- **MUST**: Use `exposeComponent()` to explicitly whitelist React components that the LLM is allowed to render.
- **MUST**: Use the `useTool()` hook to define any client-side function you want the model to be able to call.
- **SHOULD**: Use the JS Runtime for complex logic or mathematical operations to reduce hallucinations and improve accuracy.
- **MUST NOT**: Inject raw, unescaped user input directly into system instructions to prevent prompt injection.

## Key Learning Points

### Point 1: Authoring System Instructions

Structure prompts logically with clear delimiters. Define a role and tone, set explicit rules, and provide few-shot examples of desired behavior.

```ts
// System instructions are passed to hooks like useChat
const chat = useChat({
  model: 'gpt-4',
  system: `
    ### ROLE & TONE
    You are a helpful assistant.
    ### RULES
    1. Be concise.
    2. Do not make up facts.
    ### EXAMPLES
    <user>Hello</user>
    <assistant>Hi there! How can I help?</assistant>
  `,
})
```

### Point 2: Generating UI with Components

Use `exposeComponent()` to define the component's name, description, and props schema. Pass the exposed components to the `useUiChat` hook. The model's response will contain a `ui` property with the rendered React elements.

```tsx
import { useUiChat, exposeComponent } from '@hashbrownai/react'
import { s } from '@hashbrownai/core'
import { MyCard } from './MyCard'

// Expose the component with a schema for its props
const exposedCard = exposeComponent(MyCard, {
  name: 'MyCard',
  description: 'A card to display information',
  props: { title: s.string('The title of the card') },
})

// Pass the component to the useUiChat hook
const { messages } = useUiChat({
  components: [exposedCard],
  model: 'gpt-4',
  system: 'Render a card with the title "Hello World".',
})

// Render the generated UI
// messages[1].ui will contain <MyCard title="Hello World" />
```

### Point 3: Defining Tools for the Model

Use the `useTool` hook to create a tool with a name, description, optional schema for arguments, and a handler function. Provide the tool to a chat hook via the `tools` array.

```tsx
import { useChat, useTool } from '@hashbrownai/react'
import { s } from '@hashbrownai/core'

const getUserTool = useTool({
  name: 'getUser',
  description: 'Get the current user info',
  handler: async () => ({ name: 'Jane Doe' }),
  deps: [],
})

const { messages } = useChat({
  tools: [getUserTool],
  model: 'gpt-4',
  messages: [{ role: 'user', content: 'Who am I?' }],
})
```

### Point 4: Using the Sandboxed JS Runtime

For agent-like behavior, create a runtime with `useRuntime`, define functions with `useRuntimeFunction`, and expose it to the model as a tool using `useToolJavaScript`.

```ts
const runtime = useRuntime({
  functions: [
    /* runtime functions */
  ],
})
const jsTool = useToolJavaScript({ runtime })
const chat = useChat({ tools: [jsTool] })
```

### Point 5: Streaming Structured Data

Use the `s.streaming` keyword within a Skillet schema to enable streaming for arrays, objects, or strings. Hashbrown handles the eager parsing, and you can render the partial data as it arrives.

```ts
import { s } from '@hashbrownai/core'

const schema = s.object('Response', {
  items: s.streaming.array('A list of items', s.string('An item')),
})
```

## Pitfalls

- **Prompt Injection**: Directly concatenating user input into system instructions can make the application vulnerable.
- **Over-exposure**: Exposing components or tools that can perform sensitive operations or modify critical application state without proper checks.
- **Unbounded Execution**: Failing to provide an `AbortSignal` with a timeout to the JS runtime's `run` method can lead to long-running or infinite loops.

## Source map

- `/concept/system-instructions.md` — Guidance on authoring system prompts.
- `/concept/components.md` — Details on generative UI with `exposeComponent` and `useUiChat`.
- `/concept/functions.md` — Explanation of tool calling with `useTool`.
- `/concept/runtime.md` — Information on the sandboxed JS runtime.
- `/concept/streaming.md` — How to use Skillet for streaming responses.
- `/concept/transform-request-options.md` — Server-side request modification.
