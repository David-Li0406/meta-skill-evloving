# GEngine

This project supports a local `.gengine/config.yaml` for development overrides. See the `Configuration` section below for how to tune the Director and proxy settings.

GEngine is an InkJS-based interactive story demo (static HTML/JS) with Playwright smoke tests.

## Repository layout (high-level)
- `docs/` — project docs, workflow notes, PRDs
- `web/` — InkJS demo (`/demo`) and stories (`/stories`)
- `tests/` — Playwright smoke tests

## Prerequisites

### Node.js
- Node.js + npm

## InkJS web demo
The demo is a static site under `web/` that fetches `web/stories/demo.ink` at runtime.

### Run locally

You can provide local development overrides in `.gengine/config.yaml`. Example keys are in `.gengine/config.example.yaml` and include `directorConfig` for Director tuning.

```bash
npm install
npm run serve-demo
```

Then open:
- `http://127.0.0.1:8080/demo/`

Notes:
- Serve from repo root or `web/` so `/stories/demo.ink` is reachable.

More details: `docs/InkJS_README.md`.

## GitHub Pages demo
When a commit lands on `main`, GitHub Pages publishes the static demo from `web/demo` at:

- https://thewizardscode.github.io/GEngine/demo/

Notes:
- Assets (stories) are fetched relative to the repo path, so the demo works from both local `http://127.0.0.1:8080/demo/` and Pages.

## Tests (web demo)
Playwright tests run against the hosted demo.

```
npm test
```

If Playwright browsers are not installed yet:
```
npx playwright install
```

## Key docs
- `docs/InkJS_README.md`
- `docs/prd/GDD_M1_dynamic_interactive_story_engine.md`
- `docs/prd/GDD_M2_ai_assisted_branching.md` — AI Writer design
- `docs/dev/Workflow.md`

## AI Writer (Milestone 2)

The demo includes an experimental AI Writer that generates additional story choices at each decision point using OpenAI-compatible APIs.

### How to use

1. Click **AI Settings** in the demo header
2. Enter your API key (stored locally in browser)
3. (Optional) Configure a custom API endpoint for Ollama, LM Studio, vLLM, or other OpenAI-compatible servers
4. Enable AI-generated choices
5. Play the story — AI choices appear with a distinctive style at each decision point

### Features
- **LORE Context Assembly**: Extracts player state and narrative context from the Ink runtime
- **Two Prompt Templates**: Dialogue and exploration templates for different narrative contexts
- **Naive Branch Injection**: AI choices appear at every choice point (Director filtering coming in M3)
- **Safety Validation**: Basic profanity filter and schema validation
- **Configurable**: Toggle AI, adjust creativity, change choice styling
- **OpenAI-Compatible Endpoints**: Works with OpenAI, Ollama, LM Studio, vLLM, and other compatible servers

### Configuration
- **API Endpoint**: Custom endpoint URL for OpenAI-compatible servers (defaults to OpenAI)
- **JSON Mode**: Toggle off for endpoints that don't support `response_format: { type: 'json_object' }` (e.g., Ollama)
- **Creativity**: 0.0 (deterministic) to 1.0 (creative) — maps to temperature 0.0-2.0
- **Choice Style**: Distinct (highlighted with AI badge) or Normal (blends in)
- **Loading Indicator**: Show/hide while AI generates

### Using with Local Models

To use with local models via Ollama or LM Studio:

1. Start your local server (e.g., `ollama serve`)
2. In AI Settings, set the API Endpoint to your local server URL:
   - Ollama: `http://localhost:11434/v1/chat/completions`
   - LM Studio: `http://localhost:1234/v1/chat/completions`
3. Disable **Use JSON response mode** if your model doesn't support structured output
4. Enter any non-empty API key (local servers may not require authentication)

### CORS Limitations

**Browser-based API calls are blocked by CORS on many enterprise endpoints** including:
- Azure OpenAI
- Anthropic API
- Most enterprise/self-hosted APIs

These APIs don't include CORS headers for browser requests. Local models (Ollama, LM Studio) typically work because they allow localhost origins.

#### Development Workaround: CORS Proxy

For development, run the built-in proxy and demo server together, or separately if you prefer:

```bash
# Option A: single command (proxy + demo server)
# Set GENGINE_AI_ENDPOINT env var and run dev:demo (recommended):
GENGINE_AI_ENDPOINT="https://your-endpoint.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview" npm run dev:demo

# Option B: manual control
# Start the proxy separately and the demo server separately (use --target or GENGINE_AI_ENDPOINT):
npm run dev:cors-proxy -- --target https://...
npm run serve-demo -- --port 8080

# Or place settings in .gengine/config.yaml and run without env vars:
# .gengine/config.yaml example keys:
# GENGINE_AI_ENDPOINT: "https://your-endpoint.openai.azure.com"
# GENGINE_CORS_PROXY_PORT: 8010
# GENGINE_CORS_PROXY_VERBOSE: false
```

Then in AI Settings:
- Set **API Endpoint** to the proxied URL, e.g. `http://localhost:8010/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview`
- Leave **CORS Proxy** empty (since the endpoint already points at the proxy)
- Enable the **Azure OpenAI** toggle if you are proxying an Azure deployment (ensures `api-key` header + Azure-safe payload)

The proxy intercepts requests to `localhost:8010/...` and forwards them to your actual endpoint with proper CORS headers.

> Need more logging? Add `--verbose` to the proxy command (works with both `dev:demo` and `dev:cors-proxy`).

#### Production Solution

For production deployments, a backend API relay is needed to:
- Proxy requests server-side (avoids CORS entirely)
- Protect API keys from browser exposure
- Enable usage telemetry and rate limiting

See issue `ge-hch.5.20.1` (Backend API Relay) for the planned implementation.

### Modules
| Module | Path | Description |
|--------|------|-------------|
| LORE Assembler | `web/demo/js/lore-assembler.js` | Extracts context from Ink runtime |
| Prompt Engine | `web/demo/js/prompt-engine.js` | Builds prompts for the LLM |
| LLM Adapter | `web/demo/js/llm-adapter.js` | OpenAI-compatible API integration |
| API Key Manager | `web/demo/js/api-key-manager.js` | Key storage and settings UI |
| Proposal Validator | `web/demo/js/proposal-validator.js` | Schema and safety validation |

