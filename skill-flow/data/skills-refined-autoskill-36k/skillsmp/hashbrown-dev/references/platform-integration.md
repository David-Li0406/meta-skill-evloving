# Platform Integration

## When to use

- To connect your Hashbrown application to a specific LLM provider like OpenAI, Google, or Anthropic.
- When setting up a required backend service to securely handle API keys and requests.
- To use local, on-device models in the browser for improved privacy, offline capability, and zero cost.
- To create a custom adapter for an LLM provider not officially supported.

## Core concepts

- **Adapter Pattern**: Hashbrown uses a dedicated NPM package for each LLM provider (e.g., `@hashbrownai/openai`, `@hashbrownai/google`).
- **Backend Service**: A server-side application (e.g., in Node.js) is required to securely use an adapter, manage API keys, and stream responses to the client.
- **Streaming API**: All official adapters expose a `stream.text(options)` method that returns a stream of encoded `Uint8Array` frames, which are sent to the client.
- **Request Transformation**: A server-side `transformRequestOptions` function can be provided to any adapter to intercept and modify requests before they are sent to the LLM.
- **Local Transport**: An experimental feature (`experimental_local`) allows running models directly on-device in compatible browsers, with a seamless fallback to a cloud-based model.

## Rules & constraints

- **MUST**: Run platform adapters within a backend service (e.g., using Express, Fastify, Next.js).
- **MUST NOT**: Expose LLM provider API keys in client-side code. They must remain on the server.
- **MUST**: Install the specific adapter package for your chosen platform (e.g., `npm install @hashbrownai/openai`).
- **SHOULD**: Use the `transformRequestOptions` function on the server to inject sensitive context or add server-side system instructions.

## Key Learning Points

### Point 1: Standard Backend Adapter Setup

All adapters follow the same pattern on your Node.js server. Create an endpoint that takes the request body from the Hashbrown client, passes it to the adapter's `stream.text` method, and pipes the resulting `Uint8Array` stream back to the client.

```ts
// Example using Express.js and the OpenAI adapter
import { HashbrownOpenAI } from '@hashbrownai/openai'
import express from 'express'

const app = express()
app.use(express.json())

app.post('/api/chat', async (req, res) => {
  try {
    const stream = HashbrownOpenAI.stream.text({
      apiKey: process.env.OPENAI_API_KEY!,
      request: req.body, // Forward the client request body
    })

    res.header('Content-Type', 'application/octet-stream')

    for await (const chunk of stream) {
      res.write(chunk) // Pipe each Uint8Array chunk
    }
  } catch (error) {
    console.error(error)
    res.status(500).send('An error occurred.')
  } finally {
    res.end()
  }
})

app.listen(3001)
```

### Point 2: Platform-Specific Configuration

Each adapter requires slightly different configuration options, passed to the `stream.text` method.

| Platform      | Key Configuration Options                        | NPM Package              |
| :------------ | :----------------------------------------------- | :----------------------- |
| **OpenAI**    | `apiKey`                                         | `@hashbrownai/openai`    |
| **Azure**     | `apiKey`, `endpoint`                             | `@hashbrownai/azure`     |
| **Anthropic** | `apiKey` (requires `@anthropic-ai/sdk` peer dep) | `@hashbrownai/anthropic` |
| **Bedrock**   | `region`, `credentials` (optional)               | `@hashbrownai/bedrock`   |
| **Google**    | `apiKey`                                         | `@hashbrownai/google`    |
| **Ollama**    | `turbo.apiKey` (for cloud) or none (for local)   | `@hashbrownai/ollama`    |
| **Writer**    | `apiKey`                                         | `@hashbrownai/writer`    |

### Point 3: Emulating Structured Output on the Client

Some providers (like Amazon Bedrock and Google Gemini) do not natively enforce a JSON schema. For these, you must enable client-side enforcement in the `HashbrownProvider`.

```tsx
// In your React application's root
import { HashbrownProvider } from '@hashbrownai/react'

function App({ children }) {
  return (
    <HashbrownProvider url="/api/chat" emulateStructuredOutput>
      {children}
    </HashbrownProvider>
  )
}
```

### Point 4: Using Local On-Device Models

For ultimate privacy and zero cost, use the `experimental_local` transport. It attempts to use a browser's built-in model and falls back to a cloud model if the local model is unavailable or doesn't support a required feature (like tool calling).

```tsx
// In your React component
import { experimental_local } from '@hashbrownai/core/transport'
import { useCompletion } from '@hashbrownai/react'

const { output } = useCompletion({
  model: [
    experimental_local(), // Try browser's local model first
    'gpt-4o-mini', // Fall back to cloud model if local fails
  ],
  // ... other options
})
```

## Pitfalls

- **Exposing API Keys**: Attempting to use an adapter directly in client-side code is a critical security risk.
- **Missing Peer Dependencies**: The Anthropic adapter will fail without installing `@anthropic-ai/sdk`.
- **Structured Output Mismatch**: Forgetting to enable `emulateStructuredOutput` for providers like Bedrock will result in unvalidated and potentially incorrect JSON.

## Source map

- `/start/platforms.md` — Overview of supported platforms and their capabilities.
- `/platform/openai.md` — Setup guide for the OpenAI adapter.
- `/platform/azure.md` — Setup guide for the Azure OpenAI adapter.
- `/platform/anthropic.md` — Setup guide for the Anthropic adapter.
- `/platform/bedrock.md` — Setup guide for the Amazon Bedrock adapter.
- `/platform/google.md` — Setup guide for the Google Gemini adapter.
- `/platform/ollama.md` — Setup guide for the Ollama adapter.
- `/platform/writer.md` — Setup guide for the Writer adapter.
- `/platform/custom.md` — Guide for creating a new, custom adapter.
- `/recipes/local-models.md` — How-to guide for using on-device browser models.
