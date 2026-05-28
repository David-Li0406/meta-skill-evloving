---
name: research
description: Use this skill when starting research on any topic, when stuck in research, or when unsure if research is complete. It helps diagnose research quality and guides systematic query expansion.
---

# Research Skill

Tool-assisted research with Tavily integration. Transforms basic questions into comprehensive search strategies using AI-optimized web search.

## Setup

This skill includes a bundled Tavily CLI script.

### Requirements

1. **Deno** - Install from https://deno.land
2. **Tavily API Key** - Get one at https://tavily.com (free tier available)

### Configuration

Set your API key:
```bash
export TAVILY_API_KEY="your-key-here"
```

Create an alias for convenience (add to your shell profile):
```bash
# Adjust path to where this skill is installed
alias tavily='deno run --allow-net --allow-env /path/to/skills/research/scripts/tavily-cli.ts'
```

Or run directly:
```bash
deno run --allow-net --allow-env ./scripts/tavily-cli.ts "your query"
```

Commands below use `tavily` assuming the alias is configured.

---

## Quick Reference

### Common Commands

```bash
# Basic search
tavily "your query"

# With AI answer summary
tavily "your query" --answer

# Deep search with more results
tavily "your query" --depth advanced --results 10 --answer

# News/recent content
tavily "your query" --topic news --time week

# Exclude familiar sources to find new perspectives
tavily "your query" --exclude wikipedia.org,reddit.com
```

### Phase Summary

| Phase | Type | Purpose |
|-------|------|---------|
| 0 | Manual | Analyze topic, set scope |
| 1 | Tavily | Discover expert terminology |
| 2 | Tavily | Foundational search |
| 3 | Tavily | Counter-perspectives |
| 4 | Manual | Synthesize findings |

### Scope → Tavily Depth

| Decision Stakes | Tavily Settings |
|-----------------|-----------------|
| Low, reversible | `--depth basic --results 3` |
| Moderate | `--depth basic --results 5 --answer` |
| High, irreversible | `--depth advanced --results 10 --answer` |

---

## Phase 0: Analysis

**Goal**: Structure topic before searching. Prevents unfocused searches and scope mismatch.

### Scope Calibration

Before searching, assess stakes:

| Decision Type | Confidence Needed | Research Depth |
|---------------|-------------------|----------------|
| Reversible, low-stakes | 60-70% | Quick scan (minutes) |
| Reversible, moderate | 75-85% | Working knowledge |
| Irreversible, moderate | 85-95% | In-depth analysis |
| Irreversible, high-stakes | 95%+ | Comprehensive understanding |