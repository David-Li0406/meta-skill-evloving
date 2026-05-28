---
name: use-dedalus-sdk
description: 'Use when building AI-powered applications with the Dedalus SDK (dedalus_labs)—covers orchestrating agents with DedalusRunner, defining local tools, using structured outputs with Pydantic/Zod schemas, streaming responses, routing via handoffs across models, connecting to MCP servers, and working across providers (OpenAI, Anthropic, Google, xAI, DeepSeek, Mistral).'
---

# Dedalus SDK

The Dedalus SDK (`dedalus_labs`) provides agent orchestration with automatic tool execution, multi-provider model support, and MCP integration.

## Installation

```bash
# TypeScript
npm install dedalus-labs

# Python
pip install dedalus-labs
```

Set your API key:
```bash
export DEDALUS_API_KEY=your_key
```

## DedalusRunner

The core orchestration class that handles tool execution loops automatically.

### TypeScript

```typescript
import Dedalus, { DedalusRunner } from 'dedalus-labs';

const client = new Dedalus();
const runner = new DedalusRunner(client);

const result = await runner.run({
  input: "What's the weather in Paris?",
  model: 'openai/gpt-4o-mini',
});

console.log(result.finalOutput);
```

### Python

```python
from dedalus_labs import AsyncDedalus, DedalusRunner

client = AsyncDedalus()
runner = DedalusRunner(client)

result = await runner.run(
    input="What's the weather in Paris?",
    model="openai/gpt-4o-mini",
)
print(result.final_output)
```

### Key Parameters

| Parameter | Description |
|-----------|-------------|
| `input` | User message (string) |
| `model` | Model ID with provider prefix (e.g., `anthropic/claude-sonnet-4-20250514`) |
| `tools` | List of local functions |
| `mcp_servers` | List of MCP server slugs or URLs |
| `instructions` | System prompt |
| `stream` | Enable streaming (`True`/`False`) |
| `maxSteps` | Maximum tool execution steps |

## Tools

Pass functions directly—the SDK auto-generates schemas from type hints.

### TypeScript

```typescript
function add(a: number, b: number): number {
  return a + b;
}

function multiply(a: number, b: number): number {
  return a * b;
}

const result = await runner.run({
  input: 'Calculate (15 + 27) * 2',
  model: 'openai/gpt-4o-mini',
  tools: [add, multiply],
});
```

### Python

```python
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

result = await runner.run(
    input="Calculate (15 + 27) * 2",
    model="openai/gpt-4o-mini",
    tools=[add, multiply],
)
```

### Async Tools

```typescript
async function fetchUser(userId: number): Promise<object> {
  const result = await db.query('SELECT * FROM users WHERE id = $1', [userId]);
  return result.rows[0];
}
```

### Agent as Tool

Wrap a specialized agent as a tool for delegation:

```typescript
async function researchSpecialist(query: string): Promise<string> {
  const result = await runner.run({
    input: query,
    model: 'openai/gpt-4o',
    instructions: 'You are a research analyst. Be thorough.',
    mcpServers: ['tsion/exa'],
  });
  return result.finalOutput;
}

// Coordinator delegates to specialist
const result = await runner.run({
  input: 'Research AI trends, then summarize',
  model: 'openai/gpt-4o-mini',
  tools: [researchSpecialist],
});
```

## Structured Outputs

Use `response_format` with Pydantic (Python) or Zod (TypeScript) schemas.

### TypeScript (Zod)

```typescript
import { zodResponseFormat } from 'dedalus-labs/helpers/zod';
import { z } from 'zod';

const PersonSchema = z.object({
  name: z.string(),
  age: z.number(),
  occupation: z.string(),
});

const result = await client.chat.completions.parse({
  model: 'openai/gpt-4o-mini',
  messages: [{ role: 'user', content: 'Profile for Bob, 32, engineer' }],
  response_format: zodResponseFormat(PersonSchema, 'person'),
});

const person = result.choices[0]?.message.parsed;
```

### Python (Pydantic)

```python
from pydantic import BaseModel

class PersonInfo(BaseModel):
    name: str
    age: int
    occupation: str

result = await client.chat.completions.parse(
    model="openai/gpt-4o-mini",
    messages=[{"role": "user", "content": "Profile for Bob, 32, engineer"}],
    response_format=PersonInfo,
)
person = result.choices[0].message.parsed
```

### Schema Enforcement by Provider

| Provider | Enforcement |
|----------|-------------|
| `openai/*` | ✓ Strict (CFG-based) |
| `xai/*` | ✓ Strict |
| `deepseek/*` | ✓ Strict (select models) |
| `google/*` | 🟡 Best-effort |
| `anthropic/*` | 🟡 Best-effort (~85-90%) |

## Streaming

Enable real-time responses with `stream=True`.

### Python

```python
from dedalus_labs.utils.stream import stream_async

result = runner.run(
    input="Explain neural networks",
    model="anthropic/claude-opus-4-5",
    stream=True
)

await stream_async(result)
```

### TypeScript

```typescript
const result = await runner.run({
  model: 'anthropic/claude-opus-4-5',
  input: 'Count from 1 to 5',
  stream: true,
});

if (Symbol.asyncIterator in result) {
  for await (const chunk of result) {
    if (chunk.choices?.[0]?.delta?.content) {
      process.stdout.write(chunk.choices[0].delta.content);
    }
  }
}
```

### Streaming with .stream()

```python
async with client.chat.completions.stream(
    model="anthropic/claude-opus-4-5",
    messages=[{"role": "user", "content": "Profile for Bob"}],
    response_format=PersonInfo,
) as stream:
    async for event in stream:
        if event.type == "content.delta":
            print(event.delta, end="", flush=True)
    
    final = await stream.get_final_completion()
    person = final.choices[0].message.parsed
```

## MCP Integration

Connect to any MCP server via `mcp_servers` parameter.

```typescript
const result = await runner.run({
  input: "What is React?",
  model: "openai/gpt-4o-mini",
  mcpServers: [
    "https://mcp.deepwiki.com/mcp",  // URL
    "windsor/brave-search-mcp",       // Marketplace slug
  ],
});
```

### Python

```python
result = await runner.run(
    input="Search for AI news",
    model="anthropic/claude-sonnet-4-20250514",
    mcp_servers=["windsor/brave-search-mcp"],
)
```

## Handoffs

Different models excel at different tasks. Handoffs route subtasks to the right model.

### When to Use

- **Research → Writing**: GPT gathers info, Claude writes prose
- **Analysis → Code**: Reasoning model plans, code model implements
- **Triage → Specialist**: General model routes to domain experts

### Agent-as-Tool Pattern

For tasks where a coordinator delegates without giving up control:

```typescript
async function codeSpecialist(spec: string): Promise<string> {
  const result = await runner.run({
    input: spec,
    model: 'anthropic/claude-sonnet-4-20250514',
    instructions: 'Write clean, production-ready code.',
  });
  return result.finalOutput;
}

const result = await runner.run({
  input: 'Create a Python script to parse JSON',
  model: 'openai/gpt-4o-mini',  // Cheap coordinator
  tools: [codeSpecialist],       // Expensive specialist
});
```

## Model Providers

Use `provider/model-name` format:

| Provider | API Key | Example Model |
|----------|---------|---------------|
| OpenAI | `OPENAI_API_KEY` | `openai/gpt-4o-mini` |
| Anthropic | `ANTHROPIC_API_KEY` | `anthropic/claude-sonnet-4-20250514` |
| Google | `GOOGLE_API_KEY` | `google/gemini-3-pro-preview` |
| xAI | `XAI_API_KEY` | `xai/grok-2` |
| DeepSeek | `DEEPSEEK_API_KEY` | `deepseek/deepseek-chat` |
| Mistral | `MISTRAL_API_KEY` | `mistral/mistral-large` |
| Groq | `GROQ_API_KEY` | `groq/llama-3.1-70b` |
| Perplexity | `PERPLEXITY_API_KEY` | `perplexity/sonar-large` |

With a `DEDALUS_API_KEY`, routing is handled automatically.

## Common Patterns

### Session Management

```python
async def chat(session_id: str, user_input: str, model: str) -> str:
    history = load_session(session_id)
    history.append({"role": "user", "content": user_input})
    
    result = await runner.run(
        messages=history,
        model=model,
    )
    
    save_session(session_id, result.to_input_list())
    return result.final_output
```

### FastAPI Streaming Endpoint

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.post("/api/chat")
async def chat(request: Request):
    body = await request.json()
    
    stream = runner.run(
        messages=body.get("messages"),
        model=body.get("model", "openai/gpt-4o-mini"),
        stream=True,
    )
    
    async def generate():
        async for chunk in stream:
            yield f"data: {chunk.model_dump_json()}\n\n"
        yield "data: [DONE]\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")
```

## References

- **Tools**: See [references/tools.md](references/tools.md) for advanced patterns
- **Structured Outputs**: See [references/structured-outputs.md](references/structured-outputs.md) for Zod helpers
- **Authentication**: See [references/authentication.md](references/authentication.md) for DAuth and OAuth
