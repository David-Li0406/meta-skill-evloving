# Developer Experience Architecture

**Feature:** Developer Experience & Integration  
**Status:** Architecture Design

---

## Overview

This document describes the architecture for developer-friendly features in AISTRALE, including SDKs, CLI tools, VS Code extension, framework integrations, and webhook system.

---

## Architecture Principles

1. **Simplicity:** One-line integration
2. **Consistency:** Same API across all SDKs
3. **Type Safety:** Strong typing in all SDKs
4. **Documentation:** Comprehensive docs and examples
5. **Developer First:** Built for developers, by developers

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Developer Tools                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Python     │  │ TypeScript   │  │     CLI      │      │
│  │     SDK      │  │     SDK      │  │    Tool      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  VS Code     │  │  LangChain  │  │  LlamaIndex │      │
│  │  Extension   │  │ Integration │  │ Integration  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    API Layer (FastAPI)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   REST API   │  │  WebSocket  │  │   Webhook    │      │
│  │   (Existing) │  │     API     │  │     API      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  Service Layer                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Webhook     │  │  Event       │  │  Framework   │      │
│  │  Service     │  │  Service     │  │  Adapter     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  Data Layer                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  PostgreSQL   │  │   Redis     │  │   Queue      │      │
│  │  (Metadata)   │  │  (Events)   │  │  (Webhooks)  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. Python SDK

**Purpose:** Simple Python integration

**Architecture:**

```python
# Simple API
import aistrale

# One-line inference
result = aistrale.run("Hello, world!")

# Async support
result = await aistrale.run_async("Hello, world!")

# With context
with aistrale.session() as session:
    result = session.run("Hello, world!")

# With options
result = aistrale.run(
    "Hello, world!",
    model="gpt-4",
    provider="openai",
    temperature=0.7
)
```

**SDK Structure:**

```
aistrale-python/
├── aistrale/
│   ├── __init__.py
│   ├── client.py          # Main client
│   ├── models.py          # Data models
│   ├── exceptions.py      # Custom exceptions
│   ├── prompts.py         # Prompt management
│   ├── tokens.py          # Token management
│   └── telemetry.py       # Telemetry access
├── tests/
├── examples/
└── README.md
```

**Features:**

- Simple API
- Async/await support
- Type hints
- Error handling
- Retry logic
- Connection pooling

---

### 2. TypeScript SDK

**Purpose:** TypeScript/JavaScript integration

**Architecture:**

```typescript
// Simple API
import { Aistrale } from "@aistrale/sdk";

const client = new Aistrale();

// One-line inference
const result = await client.run("Hello, world!");

// With options
const result = await client.run("Hello, world!", {
  model: "gpt-4",
  provider: "openai",
  temperature: 0.7,
});
```

**SDK Structure:**

```
aistrale-typescript/
├── src/
│   ├── index.ts           # Main export
│   ├── client.ts          # Main client
│   ├── models.ts          # Type definitions
│   ├── prompts.ts         # Prompt management
│   ├── tokens.ts          # Token management
│   └── telemetry.ts       # Telemetry access
├── tests/
├── examples/
└── README.md
```

**Features:**

- TypeScript types
- Promise-based async
- Browser and Node.js support
- React hooks (optional)
- Error handling

---

### 3. CLI Tool

**Purpose:** Command-line interface for development

**Architecture:**

```bash
# Run inference
aistrale run "Hello, world!"

# List prompts
aistrale prompts list

# View telemetry
aistrale telemetry view --last 24h

# Add token
aistrale tokens add --provider openai --token sk-...

# Configure
aistrale config set api_url http://localhost:16000
```

**CLI Structure:**

```
aistrale-cli/
├── aistrale_cli/
│   ├── __init__.py
│   ├── main.py            # CLI entry point
│   ├── commands/
│   │   ├── run.py         # Run inference
│   │   ├── prompts.py     # Prompt commands
│   │   ├── telemetry.py   # Telemetry commands
│   │   └── tokens.py      # Token commands
│   └── config.py          # Configuration
├── tests/
└── README.md
```

**Features:**

- Simple commands
- Interactive mode
- Batch processing
- Output formatting (JSON, table, plain)
- Configuration management

---

### 4. VS Code Extension

**Purpose:** VS Code integration for prompt testing

**Architecture:**

```typescript
// Extension structure
extension/
├── src/
│   ├── extension.ts       # Extension entry
│   ├── panels/
│   │   ├── promptTest.ts  # Prompt testing panel
│   │   └── telemetry.ts   # Telemetry viewer
│   ├── commands/
│   │   ├── runPrompt.ts   # Run prompt command
│   │   └── viewTelemetry.ts
│   └── api/
│       └── client.ts      # API client
└── package.json
```

**Features:**

- Prompt testing panel
- Telemetry viewer
- Token management
- Quick inference
- Command palette integration
- Status bar integration

---

### 5. Framework Integrations

#### LangChain Integration

**Purpose:** LangChain LLM wrapper

**Architecture:**

```python
from langchain.llms import AistraleLLM
from langchain.chains import LLMChain

# Create LLM
llm = AistraleLLM(
    api_url="http://localhost:16000",
    model="gpt-4",
    provider="openai"
)

# Use in chain
chain = LLMChain(llm=llm, prompt=prompt)
result = chain.run("Hello, world!")
```

**Features:**

- LangChain LLM interface
- LangChain callback handler
- LangChain prompt template support
- LangChain chain support

#### LlamaIndex Integration

**Purpose:** LlamaIndex LLM wrapper

**Architecture:**

```python
from llama_index.llms import AistraleLLM

# Create LLM
llm = AistraleLLM(
    api_url="http://localhost:16000",
    model="gpt-4",
    provider="openai"
)

# Use in query engine
query_engine = index.as_query_engine(llm=llm)
response = query_engine.query("Hello, world!")
```

**Features:**

- LlamaIndex LLM interface
- LlamaIndex callback handler
- LlamaIndex query engine support

---

### 6. Webhook System

**Purpose:** Real-time event notifications

**Architecture:**

```python
class WebhookService:
    def register_webhook(
        self,
        url: str,
        events: List[str],
        secret: str
    ) -> Webhook:
        """Register webhook"""
        pass

    def deliver_event(
        self,
        event_type: str,
        payload: dict
    ):
        """Deliver event to webhooks"""
        # Find matching webhooks
        # Queue delivery
        # Retry on failure
        pass
```

**Webhook Events:**

- `inference.completed`
- `inference.failed`
- `cost.threshold_exceeded`
- `provider.failed`
- `prompt.updated`
- `token.added`

**Webhook Delivery:**

- HTTP POST to webhook URL
- Signature verification
- Retry logic (exponential backoff)
- Delivery status tracking

---

## Data Flow

### SDK Request Flow

```
1. SDK method called
2. SDK validates input
3. SDK sends HTTP request to API
4. API processes request
5. API returns response
6. SDK parses response
7. SDK returns result to user
```

### Webhook Delivery Flow

```
1. Event occurs in system
2. Webhook service finds matching webhooks
3. Webhook service queues delivery
4. Worker processes queue
5. HTTP POST to webhook URL
6. Verify signature
7. Log delivery status
8. Retry on failure
```

---

## API Design

### REST API (Existing)

- All existing endpoints
- Consistent response format
- Error handling
- Authentication

### WebSocket API (New)

- Real-time updates
- Event streaming
- Connection management
- Heartbeat

### Webhook API (New)

- Webhook registration
- Webhook management
- Webhook testing
- Webhook logs

---

## Authentication

### SDK Authentication

- API key in environment variable
- API key in config file
- API key in code (not recommended)
- Session-based (for web apps)

### CLI Authentication

- Login command
- Token storage (encrypted)
- Auto-refresh
- Logout command

### Extension Authentication

- VS Code settings
- Secure storage
- Auto-login
- Token refresh

---

## Error Handling

### SDK Error Handling

```python
try:
    result = aistrale.run("Hello, world!")
except aistrale.APIError as e:
    # Handle API error
    print(f"API Error: {e.message}")
except aistrale.NetworkError as e:
    # Handle network error
    print(f"Network Error: {e.message}")
except Exception as e:
    # Handle other errors
    print(f"Error: {e}")
```

### Retry Logic

- Automatic retry on transient errors
- Exponential backoff
- Max retry attempts
- Configurable retry behavior

---

## Performance Considerations

### SDK Performance

- Connection pooling
- Request batching
- Async operations
- Caching

### CLI Performance

- Fast command execution
- Efficient output formatting
- Cached configuration

### Extension Performance

- Lazy loading
- Efficient API calls
- Cached data

---

## Scalability Considerations

### SDK Distribution

- PyPI for Python
- NPM for TypeScript
- Version management
- Backward compatibility

### Webhook Delivery

- Queue system for webhooks
- Worker pool for delivery
- Retry mechanism
- Rate limiting

---

## Monitoring & Observability

### Metrics

- SDK usage
- CLI usage
- Extension usage
- Webhook delivery success rate
- API call latency

### Logging

- SDK debug logs
- CLI command logs
- Extension activity logs
- Webhook delivery logs

---

## Deployment Architecture

### SDK Distribution

- PyPI package
- NPM package
- Version tagging
- Release automation

### CLI Distribution

- PyPI package
- NPM package
- Homebrew (optional)
- Installation scripts

### Extension Distribution

- VS Code Marketplace
- Extension signing
- Update mechanism

---

**Last Updated:** 2025-01-27  
**Status:** Architecture Design
