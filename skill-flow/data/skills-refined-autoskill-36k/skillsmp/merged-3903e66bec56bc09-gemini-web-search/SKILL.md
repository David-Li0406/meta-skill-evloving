---
name: gemini-web-search
description: Use this skill to perform web searches using the Google Gemini CLI for current information, documentation, or recent events.
---

# Gemini Web Search Skill

## Overview

This skill enables web search using the Google Gemini CLI. Use it when you need:

- Latest information not in training data
- Current documentation or API references
- Recent news or events
- Up-to-date web data

## Prerequisites

Ensure the Gemini CLI is installed and authenticated. Run the check script first:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/check-gemini.sh
```

## Usage

### Basic Web Search

To perform a web search, use the following command:

```bash
gemini "Use web search to find current information about: <search query>"
```

### Examples

```bash
# Search for latest features
gemini "Use web search to find current information about: Claude Code latest features 2026"

# Look up current API documentation
gemini "Use web search to find current information about: OpenAI API rate limits 2026"

# Research recent news
gemini "Use web search to find current information about: AI regulation updates January 2026"
```

## Workflow

1. **Check Prerequisites**
   - Verify Gemini CLI installation
   - Ensure authentication is complete

2. **Execute Search**
   - Run the `gemini` command with the query
   - Wait for results (60s timeout)

3. **Process Results**
   - Summarize key findings
   - Note relevant sources
   - Highlight latest information

## Error Handling

| Error | Solution |
|-------|----------|
| Gemini CLI not found | Install via `npm install -g @google/gemini-cli` |
| Authentication failed | Run `gemini` to complete OAuth |
| Timeout | Retry with a more specific query |

## Notes

- Uses `gemini-2.5-flash-lite` model by default (stable, good rate limits)
- Override with `GEMINI_MODEL` environment variable
- 60-second timeout to prevent hanging
- Results are returned to the forked context to avoid main context pollution
- The explicit prefix "Use web search to find current information about:" ensures a web search is performed rather than relying solely on training data.