# Getting Started with Hashbrown React

## When to use

- To build generative user interfaces where the AI can render your existing React components.
- When you need a hook-based, reactive approach for integrating LLMs.
- For applications requiring platform-agnostic support for various LLM providers (OpenAI, Google, etc.).
- When streaming responses is critical for user experience.
- To safely execute LLM-generated JavaScript in the client using a WASM sandbox.

## Core concepts

- **Message**: A single unit of conversation, with a role and content.
- **Role**: The sender of a message, either `user`, `assistant`, or `error`.
- **Turn**: The sequence of actions an assistant takes (including tool calls) to produce a final response to a user message.
- **Completion**: The assistant's entire response payload for a given prompt.
- **Hook-Based**: Core functionality is exposed through React hooks like `useChat` and `useCompletion`.
- **Components**: You can expose your React components to the LLM, allowing it to generate UI.
- **Runtime**: A sandboxed environment for safely executing LLM-generated JavaScript.

## Rules & constraints

- **MUST**: Install the necessary packages: `@hashbrownai/core`, `@hashbrownai/react`, and a platform-specific package (e.g., `@hashbrownai/openai`).
- **MUST**: Wrap your application in the `HashbrownProvider` component.
- **SHOULD**: Run a corresponding Node.js adapter for your chosen LLM provider to handle API requests securely.

## Key Learning Points

### Point 1: Installation & Setup

Install the required packages and configure the `HashbrownProvider` at the root of your application.

```sh
npm install @hashbrownai/{core,react,openai} --save
```

```tsx
import { HashbrownProvider } from '@hashbrownai/react'

export function Providers({ children }) {
  // The URL should point to your backend adapter
  return <HashbrownProvider url="/api/chat">{children}</HashbrownProvider>
}
```

### Point 2: Choosing the Right Hook

Hashbrown provides different hooks for different tasks.

| Hook                      | Multi-turn Chat | Single Input | Structured Output | Tool Calling | Generate UI |
| ------------------------- | :-------------: | :----------: | :---------------: | :----------: | :---------: |
| `useChat`                 |       ✅        |      ❌      |        ❌         |      ✅      |     ❌      |
| `useStructuredChat`       |       ✅        |      ❌      |        ✅         |      ✅      |     ❌      |
| `useCompletion`           |       ❌        |      ✅      |        ❌         |      ✅      |     ❌      |
| `useStructuredCompletion` |       ❌        |      ✅      |        ✅         |      ✅      |     ❌      |
| `useUiChat`               |       ✅        |      ❌      |        ✅         |      ✅      |     ✅      |

### Point 3: Basic Chat with `useChat`

Use the `useChat` hook for stateful, multi-turn conversations.

```tsx
import { useChat } from '@hashbrownai/react'

export function Chat() {
  const { messages, sendMessage } = useChat({
    model: 'gpt-4',
    system: 'You are a helpful assistant.',
  })

  const handleSend = e => {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)
    const userInput = formData.get('message') as string
    sendMessage({ role: 'user', content: userInput })
  }

  return (
    <div>
      {messages.map((m, i) => (
        <div key={i}>
          {m.role}: {m.content}
        </div>
      ))}
      <form onSubmit={handleSend}>
        <input name="message" />
        <button type="submit">Send</button>
      </form>
    </div>
  )
}
```

## Pitfalls

- Not running a backend Node adapter. Hashbrown's React library is headless and requires a backend to securely communicate with LLM providers.
- Forgetting to provide a `model` and `system` message to the hooks, which are often required options.

## Source map

- `/start/intro.md` — Core concepts and features.
- `/start/overview.md` — Hook comparison table.
- `/start/quick.md` — Installation, setup, and `useChat` example.
- `/concept/ai-basics.md` — Definitions of message, role, turn, and completion.
- `/start/sample.md` — Sample app setup instructions.
