# Providers & Models

## Overview

OpenCode supports multiple LLM providers. Available providers are determined by user configuration at runtime, combining local settings and cloud services.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/config/providers` | User's configured providers only |
| GET | `/provider` | All available providers (including unconnected) |

### `/config/providers` Response

```typescript
{
  providers: Provider[],  // Only connected/configured providers
  default: {              // Default model per provider
    [providerID: string]: modelID
  }
}
```

### `/provider` Response

```typescript
{
  all: Provider[],        // All providers from models.dev
  default: { ... },
  connected: string[]     // IDs of connected providers
}
```

## Provider Detection Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    Provider.list()                               │
│                          │                                       │
│    ┌─────────────────────┼─────────────────────┐                │
│    ▼                     ▼                     ▼                │
│ ┌────────┐        ┌───────────┐        ┌───────────┐           │
│ │ Local  │        │  Cloud    │        │ Plugins   │           │
│ └───┬────┘        └─────┬─────┘        └─────┬─────┘           │
│     │                   │                    │                  │
│     ├── Env vars        ├── OpenCode free    ├── GitHub Copilot │
│     ├── Auth storage    │   models           └── Custom plugins │
│     └── opencode.json   │                                       │
│                         │                                       │
│                         ▼                                       │
│              ┌─────────────────────┐                            │
│              │  Merged Providers   │                            │
│              └─────────────────────┘                            │
└─────────────────────────────────────────────────────────────────┘
```

## Provider Sources

| Source | Type | Detection |
|--------|------|-----------|
| `env` | Local | Environment variables (`ANTHROPIC_API_KEY`, etc.) |
| `api` | Local | Saved API keys via `opencode auth` command |
| `custom` | Local/Cloud | Plugin authentication (GitHub Copilot OAuth) |
| `config` | Local | `opencode.json` configuration file |

### 1. Environment Variables

```typescript
// packages/opencode/src/provider/provider.ts:741-751
const env = Env.all()
for (const [providerID, provider] of Object.entries(database)) {
  const apiKey = provider.env.map((item) => env[item]).find(Boolean)
  if (!apiKey) continue
  mergeProvider(providerID, { source: "env", key: apiKey })
}
```

Common env vars:
- `ANTHROPIC_API_KEY` - Anthropic/Claude
- `OPENAI_API_KEY` - OpenAI
- `GOOGLE_API_KEY` - Google AI
- `OPENROUTER_API_KEY` - OpenRouter

### 2. Saved API Keys

```typescript
// packages/opencode/src/provider/provider.ts:754-762
for (const [providerID, provider] of Object.entries(await Auth.all())) {
  if (provider.type === "api") {
    mergeProvider(providerID, { source: "api", key: provider.key })
  }
}
```

Keys saved via `opencode auth` stored in `~/.opencode/auth.json`.

### 3. Plugin Authentication

```typescript
// packages/opencode/src/provider/provider.ts:764-809
for (const plugin of await Plugin.list()) {
  if (!plugin.auth) continue
  const auth = await Auth.get(providerID)
  if (!auth) continue
  // Load plugin options
}
```

Example: GitHub Copilot uses OAuth flow via plugin.

### 4. OpenCode Free Models (Auto-loaded)

```typescript
// packages/opencode/src/provider/provider.ts:86-107
async opencode(input) {
  const hasKey = await (async () => {
    if (input.env.some((item) => env[item])) return true
    if (await Auth.get(input.id)) return true
    if (config.provider?.["opencode"]?.options?.apiKey) return true
    return false
  })()

  // No API key? Filter to FREE models only
  if (!hasKey) {
    for (const [key, value] of Object.entries(input.models)) {
      if (value.cost.input === 0) continue  // Keep free
      delete input.models[key]              // Remove paid
    }
  }

  return {
    autoload: Object.keys(input.models).length > 0,
    options: hasKey ? {} : { apiKey: "public" },
  }
}
```

Free models (`cost.input === 0`) are always available without configuration.

### 5. Config File

```typescript
// packages/opencode/src/provider/provider.ts:824-830
for (const [providerID, provider] of configProviders) {
  mergeProvider(providerID, { source: "config", ...provider })
}
```

User can define custom providers in `opencode.json`:

```json
{
  "provider": {
    "custom-llm": {
      "name": "My Custom LLM",
      "api": "https://api.example.com/v1",
      "npm": "@ai-sdk/openai-compatible",
      "models": {
        "my-model": {
          "name": "My Model"
        }
      }
    }
  }
}
```

## SDK Usage

```typescript
import { createOpencodeClient } from "@opencode-ai/sdk"

const client = createOpencodeClient({ baseUrl: "http://localhost:4096" })

// Get user's available providers
const { data } = await client.config.providers()

for (const provider of data.providers) {
  console.log(`Provider: ${provider.name} (${provider.source})`)
  console.log(`  Models: ${Object.keys(provider.models).length}`)
  console.log(`  Default: ${data.default[provider.id]}`)
}
```

## Provider Type Definition

```typescript
interface Provider {
  id: string
  name: string
  source: "env" | "config" | "custom" | "api"
  env?: string[]          // Env var names to check
  key?: string            // API key (if available)
  options?: object        // Provider-specific options
  models: {
    [modelID: string]: Model
  }
}

interface Model {
  id: string
  providerID: string
  name: string
  capabilities: {
    temperature: boolean
    reasoning: boolean
    attachment: boolean
    toolcall: boolean
    input: { text, audio, image, video, pdf: boolean }
    output: { text, audio, image, video, pdf: boolean }
  }
  cost: {
    input: number   // per million tokens, 0 = free
    output: number
    cache?: { read: number, write: number }
  }
  limit: {
    context: number
    output: number
  }
  status: "alpha" | "beta" | "deprecated" | "active"
}
```

## Key Files

| File | Purpose |
|------|---------|
| `packages/opencode/src/provider/provider.ts` | Provider detection logic |
| `packages/opencode/src/provider/models.ts` | models.dev integration |
| `packages/opencode/src/server/server.ts:1721` | `/config/providers` endpoint |
| `packages/opencode/src/auth.ts` | API key storage |
