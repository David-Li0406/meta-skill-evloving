---
name: gemini-cli
description: Use Gemini CLI for web search powered by Google. Triggers on search requests where Google's search quality matters. Use for "google this", "search for...", "find information about...", "what's the latest on...".
---

# Gemini CLI

Google's Gemini CLI for web search. Leverages Google's superior search infrastructure.

## Web Search

Default: `gemini-3-flash-preview` with auto-approve (`--yolo`).

```bash
gemini -m gemini-3-flash-preview "your search query" -o text --yolo
```

## Models

| Model | Use Case |
|-------|----------|
| `gemini-3-flash-preview` | Default - fast, balanced (search) |
| `gemini-3-pro-preview` | Complex reasoning |
