---
name: internet-search
description:
  Search the internet using Gemini CLI when web search tools are unavailable or
  when user requests Gemini specifically.
---

# Internet Search

When web search tools unavailable, delegate to `gemini` CLI:

```bash
gemini -p "Research [query]. Provide summary and relevant source links. Don't make any file changes."
```

- Use ≥60s timeout (web searches can be slow)
- Always request source links for fact-checking
