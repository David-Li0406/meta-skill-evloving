# TypeScript SDK Reference

## Installation

```bash
npm install @anthropic-ai/sdk
# or
pnpm add @anthropic-ai/sdk
```

## Client Initialization

```typescript
import Anthropic from "@anthropic-ai/sdk";

// Uses ANTHROPIC_API_KEY env var by default
const client = new Anthropic();

// Or explicit key
const client = new Anthropic({ apiKey: "sk-ant-..." });
```

## Messages API

### Basic Message

```typescript
const message = await client.messages.create({
  model: "claude-sonnet-4-5-20250929",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello, Claude" }],
});

if (message.content[0].type === "text") {
  console.log(message.content[0].text);
}
```

### Multi-turn Conversation

```typescript
const messages: Anthropic.MessageParam[] = [
  { role: "user", content: "My name is Alice." },
  { role: "assistant", content: "Hello Alice! Nice to meet you." },
  { role: "user", content: "What's my name?" },
];

const message = await client.messages.create({
  model: "claude-sonnet-4-5-20250929",
  max_tokens: 1024,
  messages,
});
```

### System Prompt

```typescript
const message = await client.messages.create({
  model: "claude-sonnet-4-5-20250929",
  max_tokens: 1024,
  system: "You are a helpful assistant that speaks like a pirate.",
  messages: [{ role: "user", content: "Hello" }],
});
```

### Streaming

```typescript
const stream = client.messages.stream({
  model: "claude-sonnet-4-5-20250929",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Write a poem" }],
});

for await (const event of stream) {
  if (
    event.type === "content_block_delta" &&
    event.delta.type === "text_delta"
  ) {
    process.stdout.write(event.delta.text);
  }
}

// Or use helper
const stream = client.messages.stream({...});
for await (const text of stream.textStream) {
  process.stdout.write(text);
}

// Get final message
const finalMessage = await stream.finalMessage();
```

### Streaming with Callbacks

```typescript
client.messages
  .stream({
    model: "claude-sonnet-4-5-20250929",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello" }],
  })
  .on("text", (text) => process.stdout.write(text))
  .on("message", (message) => console.log("\nDone:", message.usage))
  .on("error", (error) => console.error(error));
```

## Vision / Images

### Base64 Image

```typescript
import * as fs from "fs";

const imageData = fs.readFileSync("image.png").toString("base64");

const message = await client.messages.create({
  model: "claude-sonnet-4-5-20250929",
  max_tokens: 1024,
  messages: [
    {
      role: "user",
      content: [
        {
          type: "image",
          source: {
            type: "base64",
            media_type: "image/png",
            data: imageData,
          },
        },
        { type: "text", text: "Describe this image" },
      ],
    },
  ],
});
```

### URL Image

```typescript
const message = await client.messages.create({
  model: "claude-sonnet-4-5-20250929",
  max_tokens: 1024,
  messages: [
    {
      role: "user",
      content: [
        {
          type: "image",
          source: {
            type: "url",
            url: "https://example.com/image.png",
          },
        },
        { type: "text", text: "What's in this image?" },
      ],
    },
  ],
});
```

### Multiple Images

```typescript
const message = await client.messages.create({
  model: "claude-sonnet-4-5-20250929",
  max_tokens: 1024,
  messages: [
    {
      role: "user",
      content: [
        {
          type: "image",
          source: { type: "base64", media_type: "image/png", data: img1Data },
        },
        {
          type: "image",
          source: { type: "base64", media_type: "image/png", data: img2Data },
        },
        { type: "text", text: "Compare these two images" },
      ],
    },
  ],
});
```

## Tool Use

### Define Tools

```typescript
const tools: Anthropic.Tool[] = [
  {
    name: "get_weather",
    description: "Get current weather for a location",
    input_schema: {
      type: "object" as const,
      properties: {
        location: {
          type: "string",
          description: "City and state, e.g. San Francisco, CA",
        },
        unit: {
          type: "string",
          enum: ["celsius", "fahrenheit"],
          description: "Temperature unit",
        },
      },
      required: ["location"],
    },
  },
];
```

### Tool Use Flow

```typescript
// Step 1: Send message with tools
const response = await client.messages.create({
  model: "claude-sonnet-4-5-20250929",
  max_tokens: 1024,
  tools,
  messages: [{ role: "user", content: "What's the weather in Boston?" }],
});

// Step 2: Check if Claude wants to use a tool
if (response.stop_reason === "tool_use") {
  const toolUse = response.content.find(
    (block): block is Anthropic.ToolUseBlock => block.type === "tool_use"
  );

  if (toolUse) {
    // Step 3: Execute tool and get result
    const toolResult = await executeWeatherTool(toolUse.input);

    // Step 4: Send tool result back
    const finalResponse = await client.messages.create({
      model: "claude-sonnet-4-5-20250929",
      max_tokens: 1024,
      tools,
      messages: [
        { role: "user", content: "What's the weather in Boston?" },
        { role: "assistant", content: response.content },
        {
          role: "user",
          content: [
            {
              type: "tool_result",
              tool_use_id: toolUse.id,
              content: JSON.stringify(toolResult),
            },
          ],
        },
      ],
    });
  }
}
```

### Tool Choice

```typescript
// Force Claude to use a specific tool
const response = await client.messages.create({
  model: "claude-sonnet-4-5-20250929",
  max_tokens: 1024,
  tools,
  tool_choice: { type: "tool", name: "get_weather" },
  messages: [{ role: "user", content: "Boston" }],
});

// Let Claude decide (default)
tool_choice: { type: "auto" }

// Force Claude to use any tool
tool_choice: { type: "any" }

// Prevent tool use
tool_choice: { type: "none" }
```

### Streaming with Tools

```typescript
const stream = client.messages.stream({
  model: "claude-sonnet-4-5-20250929",
  max_tokens: 1024,
  tools,
  messages: [{ role: "user", content: "Weather in NYC?" }],
});

for await (const event of stream) {
  if (event.type === "content_block_start") {
    if (event.content_block.type === "tool_use") {
      console.log(`Tool: ${event.content_block.name}`);
    }
  } else if (event.type === "content_block_delta") {
    if (event.delta.type === "input_json_delta") {
      process.stdout.write(event.delta.partial_json);
    }
  }
}
```

## Response Structure

```typescript
const message = await client.messages.create({...});

// Response fields
message.id            // "msg_..."
message.type          // "message"
message.role          // "assistant"
message.content       // ContentBlock[]
message.model         // Model used
message.stop_reason   // "end_turn" | "max_tokens" | "tool_use" | "stop_sequence"
message.usage.input_tokens
message.usage.output_tokens

// Content blocks
for (const block of message.content) {
  if (block.type === "text") {
    console.log(block.text);
  } else if (block.type === "tool_use") {
    console.log(block.name, block.input);
  }
}
```

## TypeScript Types

```typescript
import Anthropic from "@anthropic-ai/sdk";

// Message types
type MessageParam = Anthropic.MessageParam;
type Message = Anthropic.Message;
type ContentBlock = Anthropic.ContentBlock;
type TextBlock = Anthropic.TextBlock;
type ToolUseBlock = Anthropic.ToolUseBlock;

// Tool types
type Tool = Anthropic.Tool;
type ToolChoice = Anthropic.ToolChoice;
type ToolResultBlockParam = Anthropic.ToolResultBlockParam;

// Content types
type ImageBlockParam = Anthropic.ImageBlockParam;
type TextBlockParam = Anthropic.TextBlockParam;
```

## Error Handling

```typescript
import Anthropic, {
  APIError,
  AuthenticationError,
  RateLimitError,
  APIConnectionError,
  BadRequestError,
} from "@anthropic-ai/sdk";

try {
  const message = await client.messages.create({...});
} catch (error) {
  if (error instanceof AuthenticationError) {
    console.log("Invalid API key");
  } else if (error instanceof RateLimitError) {
    console.log(`Rate limited. Retry after: ${error.headers?.["retry-after"]}`);
  } else if (error instanceof BadRequestError) {
    console.log(`Bad request: ${error.message}`);
  } else if (error instanceof APIConnectionError) {
    console.log("Network error");
  } else if (error instanceof APIError) {
    console.log(`API error: ${error.status} - ${error.message}`);
  }
}
```

## Available Models

| Model | Model ID |
|-------|----------|
| Claude Sonnet 4.5 | `claude-sonnet-4-5-20250929` |
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` |
| Claude Opus 4.5 | `claude-opus-4-5-20251101` |

## Parameters Reference

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | string | Required. Model ID |
| `max_tokens` | number | Required. Max output tokens |
| `messages` | MessageParam[] | Required. Conversation history |
| `system` | string | System prompt |
| `temperature` | number | 0.0-1.0, default 1.0 |
| `top_p` | number | Nucleus sampling |
| `top_k` | number | Top-k sampling |
| `stop_sequences` | string[] | Custom stop sequences |
| `tools` | Tool[] | Tool definitions |
| `tool_choice` | ToolChoice | Tool selection mode |
| `metadata` | object | Request metadata |
