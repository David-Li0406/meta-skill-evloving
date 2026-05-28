# OpenAI-Compatible API Reference

Use Vercel AI Gateway with any OpenAI SDK client (Python, Rust, curl, etc.)

## Base Configuration

**Endpoint:** `https://ai-gateway.vercel.sh/v1`
**Auth Header:** `Authorization: Bearer $AI_GATEWAY_API_KEY`
**Model Format:** `provider/model-name`

## Python Integration

### Setup
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv('AI_GATEWAY_API_KEY'),
    base_url='https://ai-gateway.vercel.sh/v1'
)
```

### Basic Chat Completion
```python
response = client.chat.completions.create(
    model='anthropic/claude-sonnet-4',
    messages=[
        {'role': 'user', 'content': 'Hello, how are you?'}
    ],
    stream=False
)

print(response.choices[0].message.content)
print(f'Tokens: {response.usage.total_tokens}')
```

### Streaming
```python
stream = client.chat.completions.create(
    model='openai/gpt-5',
    messages=[
        {'role': 'user', 'content': 'Write a story'}
    ],
    stream=True
)

for chunk in stream:
    content = chunk.choices[0].delta.content
    if content:
        print(content, end='', flush=True)
```

### Provider Routing
```python
response = client.chat.completions.create(
    model='anthropic/claude-sonnet-4',
    messages=[{'role': 'user', 'content': 'Hello'}],
    extra_body={
        'providerOptions': {
            'gateway': {
                'order': ['vertex', 'anthropic'],
                'only': ['vertex', 'anthropic'],
            }
        }
    }
)
```

### Model Fallbacks
```python
response = client.chat.completions.create(
    model='openai/gpt-5',  # Primary
    messages=[{'role': 'user', 'content': 'Hello'}],
    extra_body={
        'models': ['openai/gpt-5-mini', 'anthropic/claude-sonnet-4']  # Fallbacks
    }
)

print(f'Model used: {response.model}')
```

### Zero Data Retention
```python
response = client.chat.completions.create(
    model='anthropic/claude-sonnet-4',
    messages=[{'role': 'user', 'content': 'Sensitive data...'}],
    extra_body={
        'providerOptions': {
            'gateway': {
                'zeroDataRetention': True
            }
        }
    }
)
```

### Embeddings
```python
response = client.embeddings.create(
    model='openai/text-embedding-3-small',
    input='Your text here'
)

embedding = response.data[0].embedding
print(f'Dimensions: {len(embedding)}')
```

### Batch Embeddings
```python
response = client.embeddings.create(
    model='openai/text-embedding-3-small',
    input=['Text 1', 'Text 2', 'Text 3']
)

for item in response.data:
    print(f'Index {item.index}: {len(item.embedding)} dims')
```

## Rust Integration (async-openai)

### Setup
```rust
use async_openai::{
    Client, 
    config::OpenAIConfig,
    types::{CreateChatCompletionRequestArgs, ChatCompletionRequestMessage, Role}
};
use std::env;

let config = OpenAIConfig::new()
    .with_api_key(env::var("AI_GATEWAY_API_KEY").unwrap())
    .with_api_base("https://ai-gateway.vercel.sh/v1");

let client = Client::with_config(config);
```

### Chat Completion
```rust
let request = CreateChatCompletionRequestArgs::default()
    .model("anthropic/claude-sonnet-4")
    .messages(vec![
        ChatCompletionRequestMessage {
            role: Role::User,
            content: Some("Hello, world!".to_string()),
            ..Default::default()
        }
    ])
    .build()?;

let response = client.chat().create(request).await?;
println!("{}", response.choices[0].message.content.as_ref().unwrap());
```

### Streaming
```rust
use futures::StreamExt;

let request = CreateChatCompletionRequestArgs::default()
    .model("openai/gpt-5")
    .messages(vec![/* ... */])
    .stream(true)
    .build()?;

let mut stream = client.chat().create_stream(request).await?;

while let Some(result) = stream.next().await {
    match result {
        Ok(response) => {
            if let Some(content) = &response.choices[0].delta.content {
                print!("{}", content);
            }
        }
        Err(e) => eprintln!("Error: {}", e),
    }
}
```

## curl Integration

### Basic Request
```bash
curl -X POST "https://ai-gateway.vercel.sh/v1/chat/completions" \
  -H "Authorization: Bearer $AI_GATEWAY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/gpt-5",
    "messages": [
      {"role": "user", "content": "Hello, world!"}
    ]
  }'
```

### Streaming
```bash
curl -X POST "https://ai-gateway.vercel.sh/v1/chat/completions" \
  -H "Authorization: Bearer $AI_GATEWAY_API_KEY" \
  -H "Content-Type: application/json" \
  -N \
  -d '{
    "model": "anthropic/claude-sonnet-4",
    "messages": [
      {"role": "user", "content": "Tell me a story"}
    ],
    "stream": true
  }'
```

### Provider Options
```bash
curl -X POST "https://ai-gateway.vercel.sh/v1/chat/completions" \
  -H "Authorization: Bearer $AI_GATEWAY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "anthropic/claude-sonnet-4",
    "messages": [
      {"role": "user", "content": "Hello"}
    ],
    "providerOptions": {
      "gateway": {
        "order": ["vertex", "anthropic"],
        "zeroDataRetention": true
      }
    }
  }'
```

### Model Fallbacks
```bash
curl -X POST "https://ai-gateway.vercel.sh/v1/chat/completions" \
  -H "Authorization: Bearer $AI_GATEWAY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/gpt-5",
    "models": ["openai/gpt-5-mini", "google/gemini-2.0-flash"],
    "messages": [
      {"role": "user", "content": "Hello"}
    ]
  }'
```

### Embeddings
```bash
curl -X POST "https://ai-gateway.vercel.sh/v1/embeddings" \
  -H "Authorization: Bearer $AI_GATEWAY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/text-embedding-3-small",
    "input": "Your text to embed"
  }'
```

### App Attribution
```bash
curl -X POST "https://ai-gateway.vercel.sh/v1/chat/completions" \
  -H "Authorization: Bearer $AI_GATEWAY_API_KEY" \
  -H "Content-Type: application/json" \
  -H "HTTP-Referer: https://myapp.vercel.app" \
  -H "X-Title: MyApp" \
  -d '{
    "model": "openai/gpt-5",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

## Response Format

### Chat Completion Response
```json
{
  "id": "chatcmpl-xyz123",
  "object": "chat.completion",
  "created": 1700000000,
  "model": "anthropic/claude-sonnet-4",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Hello! How can I help you today?"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 15,
    "total_tokens": 25
  }
}
```

### Streaming Chunk
```json
{
  "id": "chatcmpl-xyz123",
  "object": "chat.completion.chunk",
  "created": 1700000000,
  "model": "openai/gpt-5",
  "choices": [
    {
      "index": 0,
      "delta": {
        "content": "Hello"
      },
      "finish_reason": null
    }
  ]
}
```

### Embedding Response
```json
{
  "object": "list",
  "data": [
    {
      "object": "embedding",
      "embedding": [0.0023, -0.0092, ...],
      "index": 0
    }
  ],
  "model": "openai/text-embedding-3-small",
  "usage": {
    "prompt_tokens": 5,
    "total_tokens": 5
  }
}
```

## Error Handling

### Error Response Format
```json
{
  "error": {
    "message": "Invalid API key",
    "type": "authentication_error",
    "code": "invalid_api_key"
  }
}
```

### Status Codes
| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad Request |
| 401 | Invalid API Key |
| 429 | Rate Limited (auto-retry) |
| 500 | Server Error |
| 503 | Provider Unavailable (tries fallbacks) |

### Python Error Handling
```python
from openai import OpenAI, APIError, AuthenticationError, RateLimitError

try:
    response = client.chat.completions.create(...)
except AuthenticationError:
    print('Invalid API key')
except RateLimitError:
    print('Rate limited - Gateway auto-retries')
except APIError as e:
    print(f'API error: {e.status_code} - {e.message}')
```

## Framework Integrations

### LangChain
```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model='anthropic/claude-sonnet-4',
    api_key=os.getenv('AI_GATEWAY_API_KEY'),
    base_url='https://ai-gateway.vercel.sh/v1'
)

response = llm.invoke('Hello, world!')
```

### LlamaIndex
```python
from llama_index.llms.openai import OpenAI

llm = OpenAI(
    model='openai/gpt-5',
    api_key=os.getenv('AI_GATEWAY_API_KEY'),
    api_base='https://ai-gateway.vercel.sh/v1'
)
```

### Pydantic AI
```python
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

model = OpenAIModel(
    'anthropic/claude-sonnet-4',
    base_url='https://ai-gateway.vercel.sh/v1',
    api_key=os.getenv('AI_GATEWAY_API_KEY')
)

agent = Agent(model=model)
result = agent.run_sync('Hello')
```

## Environment Variables

```bash
# Required
AI_GATEWAY_API_KEY=your_api_key_here

# Optional (Vercel deployments)
VERCEL_OIDC_TOKEN=auto_populated_on_vercel

# BYOK (optional)
ANTHROPIC_API_KEY=your_anthropic_key
OPENAI_API_KEY=your_openai_key
```

## Rate Limits & Quotas

- Gateway handles rate limits automatically with retries
- Per-user quotas tracked via `user` parameter
- Cost limits configurable in Dashboard → AI Gateway → Settings
- Usage attribution via `tags` parameter for analytics
