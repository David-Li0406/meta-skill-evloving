---
name: perplexity-search
description: Use this skill for AI-powered web search, research, and reasoning via Perplexity.
---

# Perplexity AI Search

Web search with AI-powered answers, deep research, and chain-of-thought reasoning.

## When to Use

- Direct web search for ranked results (no AI synthesis)
- AI-synthesized research with citations
- Chain-of-thought reasoning for complex decisions
- Deep comprehensive research on topics

## Models (2025)

| Model | Purpose |
|-------|---------|
| `sonar` | Lightweight search with grounding |
| `sonar-pro` | Advanced search for complex queries |
| `sonar-reasoning-pro` | Chain of thought reasoning |
| `sonar-deep-research` | Expert-level exhaustive research |

## Usage

### Quick question (AI answer)
```bash
uv run python scripts/perplexity_search.py \
    --ask "<your_question>"
```

### Direct web search (ranked results, no AI)
```bash
uv run python scripts/perplexity_search.py \
    --search "<your_search_query>" \
    --max-results <number_of_results> \
    --recency <time_filter>
```

### AI-synthesized research
```bash
uv run python scripts/perplexity_search.py \
    --research "<your_research_topic>"
```

### Chain-of-thought reasoning
```bash
uv run python scripts/perplexity_search.py \
    --reason "<your_decision_query>"
```

### Deep comprehensive research
```bash
uv run python scripts/perplexity_search.py \
    --deep "<your_deep_research_topic>"
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| `--ask` | Quick question with AI answer (sonar) |
| `--search` | Direct web search - ranked results without AI synthesis |
| `--research` | AI-synthesized research (sonar-pro) |
| `--reason` | Chain-of-thought reasoning (sonar-reasoning-pro) |
| `--deep` | Deep comprehensive research (sonar-deep-research) |

### Search-specific options
| Parameter | Description |
|-----------|-------------|
| `--max-results N` | Number of results (1-20, default: 10) |
| `--recency` | Filter: `day`, `week`, `month`, `year` |
| `--domains` | Limit to specific domains |

## Mode Selection Guide

| Need | Use | Why |
|------|-----|-----|
| Quick fact | `--ask` | Fast, lightweight |
| Find sources | `--search` | Raw results, no AI overhead |
| Synthesized answer | `--research` | AI combines multiple sources |
| Complex decision | `--reason` | Chain-of-thought analysis |
| Comprehensive report | `--deep` | Exhaustive multi-source research |

## Examples

```bash
# Find recent sources on a topic
uv run python scripts/perplexity_search.py \
    --search "<your_topic>" \
    --recency <time_filter> --max-results <number_of_results>

# Get AI synthesis
uv run python scripts/perplexity_search.py \
    --research "<your_research_topic>"

# Make a decision
uv run python scripts/perplexity_search.py \
    --reason "<your_decision_query>"

# Deep dive
uv run python scripts/perplexity_search.py \
    --deep "<your_deep_research_topic>"
```

## API Key Required

Requires `PERPLEXITY_API_KEY` in environment or `~/.claude/.env`.