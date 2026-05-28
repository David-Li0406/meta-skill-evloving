---
name: browser-debugging
description: Use this skill when you need to systematically test UI functionality, validate design fidelity, monitor console output, and track network requests in a browser environment.
---

# Browser Debugging

This Skill provides comprehensive browser-based UI testing, visual analysis, and debugging capabilities using Chrome DevTools or Claude-in-Chrome Extension MCP tools, along with optional external vision models via Claudish.

## When to Use This Skill

Claude and agents (developer, reviewer, tester, UI developer) should invoke this Skill when:

- **Validating Own Work**: After implementing UI features, agents should verify their work in a real browser.
- **Design Fidelity Checks**: Comparing implementation screenshots against design references.
- **Visual Regression Testing**: Detecting layout shifts, styling issues, or visual bugs.
- **Console Error Investigation**: User reports console errors or warnings.
- **Form/Interaction Testing**: Verifying user interactions work correctly.
- **Pre-Commit Verification**: Before committing or deploying code.
- **Bug Reproduction**: User describes UI bugs that need investigation.

## Prerequisites

### Required: Chrome DevTools MCP or Claude-in-Chrome Extension

This skill requires either Chrome DevTools MCP or Claude-in-Chrome Extension MCP. Check availability and install if needed:

```bash
# Check if Chrome DevTools is available
mcp__chrome-devtools__list_pages 2>/dev/null && echo "Available" || echo "Not available"

# Install via claudeup (recommended)
npm install -g claudeup@latest
claudeup mcp add chrome-devtools
```

### Optional: External Vision Models (via OpenRouter)

For advanced visual analysis, use external vision-language models via Claudish:

```bash
# Check OpenRouter API key
[[ -n "${OPENROUTER_API_KEY}" ]] && echo "OpenRouter configured" || echo "Not configured"

# Install claudish
npm install -g claudish
```

---

## Visual Analysis Models (Recommended)

For best visual analysis of UI screenshots, use these models via Claudish:

### Tier 1: Best Quality (Recommended for Design Validation)

| Model | Strengths | Cost | Best For |
|-------|-----------|------|----------|
| **qwen/qwen3-vl-32b-instruct** | Best OCR, spatial reasoning, GUI automation, 32+ languages | ~$0.06/1M input | Design fidelity, OCR, element detection |
| **google/gemini-2.5-flash** | Fast, excellent performance for visual tasks | TBD | General visual analysis |