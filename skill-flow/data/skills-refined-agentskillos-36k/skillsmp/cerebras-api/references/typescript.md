# Cerebras TypeScript SDK Reference

## Installation

```bash
npm install @cerebras/cerebras_cloud_sdk
```

## Client Initialization

```typescript
import Cerebras from '@cerebras/cerebras_cloud_sdk';

// From environment variable (recommended)
const client = new Cerebras();  // Uses CEREBRAS_API_KEY

// Explicit API key
const client = new Cerebras({ apiKey: 'your-api-key' });

// Full configuration
const client = new Cerebras({
    apiKey: 'your-api-key',
    maxRetries: 3,              // Default: 2
    timeout: 30 * 1000,         // Default: 60000ms
    warmTCPConnection: true     // Default: true (reduces TTFT)
});
```

## Chat Completions

### Basic Request

```typescript
const response = await client.chat.completions.create({
    model: 'llama-3.3-70b',
    messages: [
        { role: 'system', content: 'You are helpful.' },
        { role: 'user', content: 'Hello' }
    ],
    temperature: 0.7,
    max_completion_tokens: 1000
});

console.log(response.choices[0].message.content);
```

### With Type Definitions

```typescript
const params: Cerebras.Chat.ChatCompletionCreateParams = {
    model: 'llama-3.3-70b',
    messages: [{ role: 'user', content: 'Hello' }]
};

const response: Cerebras.Chat.ChatCompletion =
    await client.chat.completions.create(params);
```

### Streaming

```typescript
const stream = await client.chat.completions.create({
    model: 'llama-3.3-70b',
    messages: [{ role: 'user', content: 'Write a story' }],
    stream: true
});

for await (const chunk of stream) {
    const content = chunk.choices[0]?.delta?.content;
    if (content) {
        process.stdout.write(content);
    }
}

// Note: usage and time_info only in final chunk
```

### Cancel Streaming

```typescript
const stream = await client.chat.completions.create({
    model: 'llama-3.3-70b',
    messages: [{ role: 'user', content: 'Long response' }],
    stream: true
});

for await (const chunk of stream) {
    if (shouldStop) {
        stream.controller.abort();
        break;
    }
    process.stdout.write(chunk.choices[0]?.delta?.content || '');
}
```

### Multi-turn Conversation

```typescript
const messages: Cerebras.Chat.ChatCompletionMessageParam[] = [
    { role: 'system', content: 'You are a helpful assistant.' },
    { role: 'user', content: 'My name is Alice.' }
];

let response = await client.chat.completions.create({
    model: 'llama-3.3-70b',
    messages
});

// Add assistant response
messages.push({
    role: 'assistant',
    content: response.choices[0].message.content || ''
});

// Continue conversation
messages.push({ role: 'user', content: "What's my name?" });

response = await client.chat.completions.create({
    model: 'llama-3.3-70b',
    messages
});
```

## Text Completions

```typescript
const completion = await client.completions.create({
    model: 'llama3.1-8b',
    prompt: 'Once upon a time',
    max_tokens: 100,
    temperature: 0.8
});

console.log(completion.choices[0].text);
```

### Streaming Text Completions

```typescript
const stream = await client.completions.create({
    model: 'llama3.1-8b',
    prompt: 'The future of AI is',
    stream: true
});

for await (const chunk of stream) {
    process.stdout.write(chunk.choices[0]?.text || '');
}
```

## Tool Calling

### Single Tool

```typescript
const tools: Cerebras.Chat.ChatCompletionTool[] = [{
    type: 'function',
    function: {
        name: 'get_weather',
        strict: true,
        description: 'Get weather for a location',
        parameters: {
            type: 'object',
            properties: {
                location: {
                    type: 'string',
                    description: 'City name'
                },
                unit: {
                    type: 'string',
                    enum: ['celsius', 'fahrenheit']
                }
            },
            required: ['location'],
            additionalProperties: false
        }
    }
}];

const response = await client.chat.completions.create({
    model: 'zai-glm-4.7',
    messages: [{ role: 'user', content: 'Weather in Paris?' }],
    tools
});

if (response.choices[0].message.tool_calls) {
    const toolCall = response.choices[0].message.tool_calls[0];
    console.log(`Call: ${toolCall.function.name}`);
    console.log(`Args: ${toolCall.function.arguments}`);
}
```

### Multi-turn Tool Calling

```typescript
const messages: Cerebras.Chat.ChatCompletionMessageParam[] = [
    { role: 'user', content: 'Weather in Tokyo?' }
];

let response = await client.chat.completions.create({
    model: 'zai-glm-4.7',
    messages,
    tools
});

// Process tool calls
while (response.choices[0].message.tool_calls) {
    // Add assistant message with tool calls
    messages.push(response.choices[0].message as Cerebras.Chat.ChatCompletionMessageParam);

    for (const toolCall of response.choices[0].message.tool_calls) {
        // Execute tool (your implementation)
        const result = await executeTool(
            toolCall.function.name,
            JSON.parse(toolCall.function.arguments)
        );

        // Add tool result
        messages.push({
            role: 'tool',
            tool_call_id: toolCall.id,
            content: JSON.stringify(result)
        });
    }

    // Continue conversation
    response = await client.chat.completions.create({
        model: 'zai-glm-4.7',
        messages,
        tools
    });
}

console.log(response.choices[0].message.content);
```

### Parallel Tool Calling

```typescript
// Enabled by default
const response = await client.chat.completions.create({
    model: 'zai-glm-4.7',
    messages: [{ role: 'user', content: 'Weather in Tokyo and Paris?' }],
    tools,
    parallel_tool_calls: true  // Default
});

// May return multiple tool_calls
for (const toolCall of response.choices[0].message.tool_calls || []) {
    console.log(`Tool: ${toolCall.function.name}`);
}
```

## Structured Outputs

### With JSON Schema

```typescript
const schema = {
    type: 'object',
    properties: {
        name: { type: 'string' },
        age: { type: 'integer' },
        skills: {
            type: 'array',
            items: { type: 'string' }
        }
    },
    required: ['name', 'age', 'skills'],
    additionalProperties: false
} as const;

const response = await client.chat.completions.create({
    model: 'llama-3.3-70b',
    messages: [{ role: 'user', content: 'Create a developer profile' }],
    response_format: {
        type: 'json_schema',
        json_schema: {
            name: 'profile',
            strict: true,
            schema
        }
    }
});

interface Profile {
    name: string;
    age: number;
    skills: string[];
}

const data: Profile = JSON.parse(response.choices[0].message.content || '{}');
```

### With Zod

```typescript
import { z } from 'zod';
import { zodToJsonSchema } from 'zod-to-json-schema';

const PersonSchema = z.object({
    name: z.string(),
    email: z.string().email(),
    age: z.number().int(),
    tags: z.array(z.string())
});

type Person = z.infer<typeof PersonSchema>;

const response = await client.chat.completions.create({
    model: 'llama-3.3-70b',
    messages: [{ role: 'user', content: 'Generate a person record' }],
    response_format: {
        type: 'json_schema',
        json_schema: {
            name: 'person',
            strict: true,
            schema: zodToJsonSchema(PersonSchema)
        }
    }
});

const person: Person = PersonSchema.parse(
    JSON.parse(response.choices[0].message.content || '{}')
);
```

### JSON Mode (Less Strict)

```typescript
const response = await client.chat.completions.create({
    model: 'llama-3.3-70b',
    messages: [
        { role: 'system', content: 'Respond in JSON format' },
        { role: 'user', content: 'List 3 colors' }
    ],
    response_format: { type: 'json_object' }
});
```

## Reasoning Models

### Parsed Format (Separate Field)

```typescript
const response = await client.chat.completions.create({
    model: 'qwen-3-32b',
    messages: [{ role: 'user', content: 'What is 15% of 240?' }],
    reasoning_format: 'parsed'
});

console.log('Reasoning:', response.choices[0].message.reasoning);
console.log('Answer:', response.choices[0].message.content);
```

### Raw Format (In Content)

```typescript
const response = await client.chat.completions.create({
    model: 'qwen-3-32b',
    messages: [{ role: 'user', content: 'Solve: 2x + 5 = 15' }],
    reasoning_format: 'raw'
});

// Content includes <think>...</think> tags for Qwen/GLM
console.log(response.choices[0].message.content);
```

### Hidden Format

```typescript
const response = await client.chat.completions.create({
    model: 'qwen-3-32b',
    messages: [{ role: 'user', content: 'Complex problem' }],
    reasoning_format: 'hidden'  // Reasoning not returned but still computed
});
```

### GPT-OSS Reasoning Effort

```typescript
const response = await client.chat.completions.create({
    model: 'gpt-oss-120b',
    messages: [{ role: 'user', content: 'Prove the Pythagorean theorem' }],
    reasoning_effort: 'high'  // 'low', 'medium', 'high'
});
```

### GLM Disable Reasoning

```typescript
const response = await client.chat.completions.create({
    model: 'zai-glm-4.7',
    messages: [{ role: 'user', content: 'Quick answer needed' }],
    disable_reasoning: true
});
```

## Error Handling

```typescript
try {
    const response = await client.chat.completions.create({
        model: 'llama-3.3-70b',
        messages: [{ role: 'user', content: 'Hello' }]
    });
} catch (err) {
    if (err instanceof Cerebras.APIError) {
        console.log('Status:', err.status);
        console.log('Name:', err.name);
        console.log('Headers:', err.headers);

        if (err instanceof Cerebras.RateLimitError) {
            const retryAfter = err.headers?.['retry-after'];
            console.log(`Rate limited. Retry after: ${retryAfter}`);
        } else if (err instanceof Cerebras.AuthenticationError) {
            console.log('Invalid API key');
        } else if (err instanceof Cerebras.BadRequestError) {
            console.log('Bad request:', err.message);
        }
    }
}
```

### Error Types

| Status | Exception |
|--------|-----------|
| 400 | `BadRequestError` |
| 401 | `AuthenticationError` |
| 403 | `PermissionDeniedError` |
| 404 | `NotFoundError` |
| 422 | `UnprocessableEntityError` |
| 429 | `RateLimitError` |
| >= 500 | `InternalServerError` |
| Network | `APIConnectionError` |

## Response Objects

### ChatCompletion

```typescript
const response = await client.chat.completions.create({...});

// Access fields
response.id;              // Completion ID
response.model;           // Model used
response.created;         // Unix timestamp
response.choices;         // Array of choices
response.usage;           // Token usage

// Choice fields
const choice = response.choices[0];
choice.index;             // Choice index
choice.finish_reason;     // 'stop', 'length', 'tool_calls'
choice.message.role;      // 'assistant'
choice.message.content;   // Response text
choice.message.tool_calls;  // Tool calls (if any)
choice.message.reasoning;   // Reasoning (if parsed format)

// Usage fields
response.usage?.prompt_tokens;
response.usage?.completion_tokens;
response.usage?.total_tokens;
```

### Raw Response Access

```typescript
// Get Response object
const response = await client.chat.completions
    .create({...})
    .asResponse();

console.log(response.headers.get('X-Request-Id'));
console.log(response.statusText);

// Get both data and response
const { data, response: raw } = await client.chat.completions
    .create({...})
    .withResponse();

console.log(data.choices[0].message.content);
console.log(raw.headers.get('X-Request-Id'));
```

## Configuration Options

### Per-Request Overrides

```typescript
// Override timeout
const response = await client.chat.completions.create(
    { model: 'llama-3.3-70b', messages: [...] },
    { timeout: 10 * 1000 }
);

// Override retries
const response = await client.chat.completions.create(
    { model: 'llama-3.3-70b', messages: [...] },
    { maxRetries: 5 }
);
```

### Custom Fetch

```typescript
import fetch from 'node-fetch';

const client = new Cerebras({
    fetch: fetch as unknown as typeof globalThis.fetch
});
```

## Model Listing

```typescript
const models = await client.models.list();
for await (const model of models) {
    console.log(`${model.id}: ${model.owned_by}`);
}

// Get specific model
const model = await client.models.retrieve('llama-3.3-70b');
```

## ESM and CommonJS

### ESM (Recommended)

```typescript
import Cerebras from '@cerebras/cerebras_cloud_sdk';
```

### CommonJS

```javascript
const Cerebras = require('@cerebras/cerebras_cloud_sdk').default;
```

## Deno

```typescript
import Cerebras from 'npm:@cerebras/cerebras_cloud_sdk';
```

## Cloudflare Workers

```typescript
import Cerebras from '@cerebras/cerebras_cloud_sdk';

export default {
    async fetch(request: Request, env: Env): Promise<Response> {
        const client = new Cerebras({ apiKey: env.CEREBRAS_API_KEY });

        const response = await client.chat.completions.create({
            model: 'llama3.1-8b',
            messages: [{ role: 'user', content: 'Hello' }]
        });

        return new Response(response.choices[0].message.content);
    }
};
```
