# Vercel AI SDK

**Category**: ai-ml/frameworks
**Description**: The AI Toolkit for TypeScript - unified API for building AI-powered applications with streaming text, chat UIs, tool calling, and agents
**Homepage**: https://ai-sdk.dev
**Repository**: https://github.com/vercel/ai

## Package Detection

### NPM - Core Package
*Main AI SDK package*

- `ai`

### NPM - Provider Packages
*Official AI SDK provider packages for different LLM providers*

- `@ai-sdk/openai` - OpenAI (GPT-4, GPT-4o, o1, etc.)
- `@ai-sdk/anthropic` - Anthropic (Claude 3.5, Claude 3, etc.)
- `@ai-sdk/google` - Google Generative AI (Gemini)
- `@ai-sdk/google-vertex` - Google Vertex AI
- `@ai-sdk/mistral` - Mistral AI
- `@ai-sdk/cohere` - Cohere
- `@ai-sdk/amazon-bedrock` - Amazon Bedrock
- `@ai-sdk/azure` - Azure OpenAI
- `@ai-sdk/groq` - Groq
- `@ai-sdk/xai` - xAI Grok
- `@ai-sdk/deepseek` - DeepSeek
- `@ai-sdk/togetherai` - Together AI
- `@ai-sdk/fireworks` - Fireworks AI
- `@ai-sdk/perplexity` - Perplexity AI

### NPM - Utility Packages
*Supporting packages in the AI SDK ecosystem*

- `@ai-sdk/provider` - Provider utilities base
- `@ai-sdk/provider-utils` - Provider utility functions
- `@ai-sdk/ui-utils` - UI utility functions
- `@ai-sdk/react` - React hooks and components
- `@ai-sdk/svelte` - Svelte integration
- `@ai-sdk/vue` - Vue integration
- `@ai-sdk/solid` - Solid.js integration

### Community Provider Packages
*Community-maintained providers*

- `@openrouter/ai-sdk-provider` - OpenRouter
- `ollama-ai-provider` - Ollama local models
- `@ai-sdk/portkey` - Portkey AI Gateway

## Import Detection

### JavaScript/TypeScript
File extensions: .js, .ts, .jsx, .tsx, .mjs

#### Core AI SDK Imports

**Pattern**: `import\s+\{[^}]*\}\s+from\s+['"]ai['"]`
- Named imports from core AI SDK
- Example: `import { generateText, streamText } from 'ai';`

**Pattern**: `import\s+\{[^}]*generateText[^}]*\}\s+from\s+['"]ai['"]`
- Text generation import
- Example: `import { generateText } from 'ai';`

**Pattern**: `import\s+\{[^}]*streamText[^}]*\}\s+from\s+['"]ai['"]`
- Streaming text generation
- Example: `import { streamText } from 'ai';`

**Pattern**: `import\s+\{[^}]*generateObject[^}]*\}\s+from\s+['"]ai['"]`
- Structured object generation
- Example: `import { generateObject } from 'ai';`

**Pattern**: `import\s+\{[^}]*streamObject[^}]*\}\s+from\s+['"]ai['"]`
- Streaming object generation
- Example: `import { streamObject } from 'ai';`

**Pattern**: `import\s+\{[^}]*embed[^}]*\}\s+from\s+['"]ai['"]`
- Embedding generation
- Example: `import { embed, embedMany } from 'ai';`

**Pattern**: `import\s+\{[^}]*tool[^}]*\}\s+from\s+['"]ai['"]`
- Tool definition helper
- Example: `import { tool } from 'ai';`

#### Provider Imports

**Pattern**: `import\s+\{[^}]*\}\s+from\s+['"]@ai-sdk/openai['"]`
- OpenAI provider
- Example: `import { openai } from '@ai-sdk/openai';`

**Pattern**: `import\s+\{[^}]*\}\s+from\s+['"]@ai-sdk/anthropic['"]`
- Anthropic provider
- Example: `import { anthropic } from '@ai-sdk/anthropic';`

**Pattern**: `import\s+\{[^}]*\}\s+from\s+['"]@ai-sdk/google['"]`
- Google AI provider
- Example: `import { google } from '@ai-sdk/google';`

**Pattern**: `import\s+\{[^}]*\}\s+from\s+['"]@ai-sdk/[a-z-]+['"]`
- Any AI SDK provider import
- Example: `import { mistral } from '@ai-sdk/mistral';`

#### React/UI Hooks

**Pattern**: `import\s+\{[^}]*useChat[^}]*\}\s+from\s+['"]ai/react['"]`
- Chat UI hook
- Example: `import { useChat } from 'ai/react';`

**Pattern**: `import\s+\{[^}]*useCompletion[^}]*\}\s+from\s+['"]ai/react['"]`
- Completion UI hook
- Example: `import { useCompletion } from 'ai/react';`

**Pattern**: `import\s+\{[^}]*useAssistant[^}]*\}\s+from\s+['"]ai/react['"]`
- OpenAI Assistant hook
- Example: `import { useAssistant } from 'ai/react';`

**Pattern**: `import\s+\{[^}]*useObject[^}]*\}\s+from\s+['"]ai/react['"]`
- Streaming object hook
- Example: `import { useObject } from 'ai/react';`

#### RSC (React Server Components)

**Pattern**: `import\s+\{[^}]*streamUI[^}]*\}\s+from\s+['"]ai/rsc['"]`
- Server-side streaming UI
- Example: `import { streamUI } from 'ai/rsc';`

**Pattern**: `import\s+\{[^}]*createStreamableUI[^}]*\}\s+from\s+['"]ai/rsc['"]`
- Streamable UI creation
- Example: `import { createStreamableUI } from 'ai/rsc';`

**Pattern**: `import\s+\{[^}]*createStreamableValue[^}]*\}\s+from\s+['"]ai/rsc['"]`
- Streamable value creation
- Example: `import { createStreamableValue } from 'ai/rsc';`

## Code Pattern Detection

### Text Generation

**Pattern**: `generateText\s*\(\s*\{`
- Synchronous text generation
- Example: `const { text } = await generateText({ model: openai('gpt-4'), prompt: '...' });`

**Pattern**: `streamText\s*\(\s*\{`
- Streaming text generation
- Example: `const result = await streamText({ model: anthropic('claude-3'), messages });`

**Pattern**: `\.textStream`
- Accessing text stream
- Example: `for await (const chunk of result.textStream) { ... }`

### Object Generation (Structured Output)

**Pattern**: `generateObject\s*\(\s*\{`
- Structured object generation
- Example: `const { object } = await generateObject({ model, schema, prompt });`

**Pattern**: `streamObject\s*\(\s*\{`
- Streaming object generation
- Example: `const result = await streamObject({ model, schema, prompt });`

**Pattern**: `\.partialObjectStream`
- Partial object streaming
- Example: `for await (const partial of result.partialObjectStream) { ... }`

### Tool Calling / Function Calling

**Pattern**: `tool\s*\(\s*\{`
- Tool definition using helper
- Example: `const weatherTool = tool({ description: '...', parameters: z.object({...}), execute: async () => {...} });`

**Pattern**: `tools:\s*\{`
- Tools configuration in generateText/streamText
- Example: `await generateText({ model, prompt, tools: { weather: weatherTool } });`

**Pattern**: `maxSteps:\s*\d+`
- Multi-step agent execution
- Example: `await generateText({ model, prompt, tools, maxSteps: 10 });`

**Pattern**: `toolChoice:`
- Tool choice configuration
- Example: `toolChoice: 'auto'` or `toolChoice: { type: 'tool', toolName: 'search' }`

### Embeddings

**Pattern**: `embed\s*\(\s*\{`
- Single embedding generation
- Example: `const { embedding } = await embed({ model: openai.embedding('text-embedding-3-small'), value: 'text' });`

**Pattern**: `embedMany\s*\(\s*\{`
- Batch embedding generation
- Example: `const { embeddings } = await embedMany({ model, values: ['text1', 'text2'] });`

### Model Instantiation

**Pattern**: `openai\s*\(\s*['"][^'"]+['"]\s*\)`
- OpenAI model instantiation
- Example: `openai('gpt-4-turbo')`

**Pattern**: `anthropic\s*\(\s*['"][^'"]+['"]\s*\)`
- Anthropic model instantiation
- Example: `anthropic('claude-3-5-sonnet-20241022')`

**Pattern**: `google\s*\(\s*['"][^'"]+['"]\s*\)`
- Google AI model instantiation
- Example: `google('gemini-1.5-pro')`

**Pattern**: `mistral\s*\(\s*['"][^'"]+['"]\s*\)`
- Mistral model instantiation
- Example: `mistral('mistral-large-latest')`

**Pattern**: `xai\s*\(\s*['"][^'"]+['"]\s*\)`
- xAI Grok model instantiation
- Example: `xai('grok-2')`

**Pattern**: `groq\s*\(\s*['"][^'"]+['"]\s*\)`
- Groq model instantiation
- Example: `groq('llama-3.3-70b-versatile')`

**Pattern**: `cohere\s*\(\s*['"][^'"]+['"]\s*\)`
- Cohere model instantiation
- Example: `cohere('command-a-03-2025')`

### Advanced Patterns

**Pattern**: `customProvider\s*\(\s*\{`
- Custom provider definition
- Example: `const myProvider = customProvider({ languageModels: {...} });`

**Pattern**: `wrapLanguageModel\s*\(\s*\{`
- Model wrapping with middleware
- Example: `wrapLanguageModel({ model, middleware: [...] })`

**Pattern**: `extractReasoningMiddleware`
- Reasoning extraction middleware
- Example: `const middleware = extractReasoningMiddleware({ tagName: 'think' });`

**Pattern**: `createOpenAI\s*\(\s*\{`
- OpenAI-compatible provider creation
- Example: `const provider = createOpenAI({ baseURL: 'https://...', apiKey: '...' });`

**Pattern**: `gateway\s*\(\s*['"][^'"]+['"]\s*\)`
- AI Gateway model reference
- Example: `gateway('deepseek/deepseek-v3')`

### Chat/UI Hooks Usage

**Pattern**: `useChat\s*\(\s*\{?`
- Chat hook initialization
- Example: `const { messages, input, handleSubmit } = useChat();`

**Pattern**: `useCompletion\s*\(\s*\{?`
- Completion hook initialization
- Example: `const { completion, complete } = useCompletion();`

### Streaming Response Handling

**Pattern**: `\.toDataStreamResponse\s*\(`
- Convert to data stream response (Next.js API routes)
- Example: `return result.toDataStreamResponse();`

**Pattern**: `\.toTextStreamResponse\s*\(`
- Convert to text stream response
- Example: `return result.toTextStreamResponse();`

**Pattern**: `\.pipeDataStreamToResponse\s*\(`
- Pipe stream to response (Express/Node)
- Example: `result.pipeDataStreamToResponse(res);`

## Environment Variables

*Common environment variables used with AI SDK*

- `OPENAI_API_KEY` - OpenAI API key
- `ANTHROPIC_API_KEY` - Anthropic API key
- `GOOGLE_GENERATIVE_AI_API_KEY` - Google AI API key
- `GOOGLE_VERTEX_PROJECT` - Google Vertex project
- `MISTRAL_API_KEY` - Mistral API key
- `COHERE_API_KEY` - Cohere API key
- `GROQ_API_KEY` - Groq API key
- `XAI_API_KEY` - xAI API key
- `DEEPSEEK_API_KEY` - DeepSeek API key
- `TOGETHER_AI_API_KEY` - Together AI API key
- `FIREWORKS_API_KEY` - Fireworks AI API key
- `PERPLEXITY_API_KEY` - Perplexity API key
- `AWS_ACCESS_KEY_ID` - AWS for Bedrock
- `AWS_SECRET_ACCESS_KEY` - AWS for Bedrock
- `AZURE_OPENAI_API_KEY` - Azure OpenAI key
- `AZURE_OPENAI_ENDPOINT` - Azure OpenAI endpoint

## Configuration Files

### Next.js with AI SDK

**File**: `next.config.js` or `next.config.mjs`
**Pattern**: `experimental:\s*\{[^}]*serverActions`
- Server Actions config for AI SDK RSC
- Example: `experimental: { serverActions: true }`

### API Route Patterns

**File**: `app/api/**/route.ts` or `pages/api/**/*.ts`
**Pattern**: `POST.*streamText|streamText.*POST`
- AI streaming endpoint
- Example: API route handler with streamText

## Detection Notes

- The core `ai` package is the primary indicator
- Provider packages (`@ai-sdk/*`) indicate which AI services are used
- `ai/react`, `ai/svelte`, `ai/vue` imports indicate frontend framework
- `ai/rsc` imports indicate React Server Components usage
- Tool definitions with Zod schemas indicate function calling
- `maxSteps` parameter indicates agentic workflows
- Multiple provider packages suggest multi-model architecture

## Related Technologies

- Next.js (most common framework pairing)
- React Server Components
- Zod (schema validation for tools/objects)
- OpenAI, Anthropic, Google AI (commonly used providers)

## Security Considerations

- API keys should be server-side only (never exposed to client)
- Tool execution should validate inputs
- Streaming responses may expose partial data
- Consider rate limiting on AI endpoints
- Validate and sanitize user prompts
- Monitor token usage and costs

## Detection Confidence

- **Package Detection (ai)**: 95% (HIGH) - The `ai` package on NPM is exclusively the Vercel AI SDK (owned by Vercel)
- **Package Detection (@ai-sdk/*)**: 98% (HIGH) - Scoped provider packages are unambiguous identifiers
- **Package Corroboration**: 99% (VERY HIGH) - If both `ai` and any `@ai-sdk/*` package detected
- **Import Detection**: 90% (HIGH) - Unique function names like `generateText`, `streamText`
- **Code Pattern Detection**: 85% (MEDIUM) - May overlap with other AI libraries
- **Environment Variable Detection**: 70% (MEDIUM) - Shared with direct API usage

## Detection Notes

- The NPM package `ai` is owned by Vercel and is exclusively the Vercel AI SDK
- Detection of any `@ai-sdk/*` scoped package confirms Vercel AI SDK usage
- Provider packages (`@ai-sdk/openai`, `@ai-sdk/anthropic`, etc.) are the most reliable indicators
- The combination of core `ai` package + provider packages gives highest confidence
- Earlier versions used different patterns (`OpenAIStream`, `StreamingTextResponse`) - still valid
