# Streaming & JSONL Patterns

`json-render` achieves sub-300ms latency by using **JSONL (JSON Lines)** and a sophisticated **Patch Engine**.

## 🧩 The Patch Engine
Instead of re-rendering the whole UI when new data arrives, `json-render` applies granular patches.

### JSONL Format Example
The AI streams lines of JSON. Each line is a discrete operation.

```json
{"op": "add", "path": "/components/0", "value": {"component": "Header", "props": {"title": "Hello"}}}
{"op": "add", "path": "/components/1", "value": {"component": "Metric", "props": {"value": 0}}}
{"op": "replace", "path": "/components/1/props/value", "value": 42}
```

## 🏎 Optimizing for Latency
### 1. Small Chunks
Configure your AI provider to emit tokens frequently. In Vercel AI SDK, use `toDataStreamResponse()`.

### 2. Priority Rendering
Mark critical components (like Headers or Navigation) as high priority in your catalog so the AI generates them first.

## 🛠 Troubleshooting the Stream
- **Broken JSON**: Ensure your model is specifically prompted for JSONL. Models like Gemini 3 and GPT-5 handle this natively, but smaller models might need more explicit instructions.
- **Race Conditions**: `json-render/core` handles out-of-order patches, but it's best to maintain a sequential sequence ID if using custom WebSocket implementations.

## 📊 Monitoring Stream Health
In production, track:
- **TTFR (Time to First Render)**: Goal < 250ms.
- **Completion Time**: Time for the full JSON to arrive.
- **Patch Count**: Too many small patches can cause high CPU usage on low-end devices.

*Updated: January 22, 2026 - 17:45*
