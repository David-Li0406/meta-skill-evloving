---
name: Kagi Research Suite
description: Complete suite for Web Search, Content Summarization, and Deep Research using Kagi API.
---

# Kagi Research Suite

This skill provides a set of tools to query information, summarize content, and conduct deep research using Kagi's FastGPT and Universal Summarizer.

> [!WARNING]
> **Cost Alert**: All tools below consume Kagi API credits. You must append `--confirm` to execute them.

## Prerequisites
- `KAGI_API_KEY` must be set in `.env`.
- `@dotenvx/dotenvx` must be installed.

## Tools & Usage

### 1. FastGPT (Smart Search)
Get an AI-synthesized answer with references.
```bash
node .agent/skills/kagi-search/scripts/fastgpt.cjs "query" --confirm
```

### 2. Universal Summarizer
Summarize a specific URL (article, video, etc.).
```bash
node .agent/skills/kagi-search/scripts/summarize.cjs --url "https://..." --confirm
```

### 3. Deep Research
Conduct a comprehensive "Deep Dive". This can be expensive (1 FastGPT + N Summaries).
1. Uses FastGPT to get a high-level answer and sources.
2. Recursively summarizes the top sources (controlled by `--depth`).
3. Aggregates everything into a Markdown report.

```bash
node .agent/skills/kagi-search/scripts/research.cjs "Topic Name" --depth 5 --confirm
```

## Workflows
- **"Kagi <query>"**: Run `fastgpt.cjs`.
- **"Kagi <url>"**: Run `summarize.cjs`.
- **"Deep Research <topic>"**: Run `research.cjs`.

## Free Options
*Currently, all reliable API endpoints (v0/FastGPT) require credits. The `search.cjs` script attempting to use the Standard Search API is currently restricted (Beta/401).*
