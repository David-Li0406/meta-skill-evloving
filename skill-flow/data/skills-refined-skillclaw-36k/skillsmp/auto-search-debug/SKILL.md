---
name: auto-search-debug
description: Proactive self-healing debugging using Antigravity Manager's Search & Reader MCPs.
---

# Auto-Search Debugging (Self-Healing Loop)

This skill enables the agent to proactively resolve errors by leveraging the Antigravity Manager's built-in MCP tools.

## Core Protocol

1. **Trigger**: When a "Critical" or "Fatal" error is detected in the logs (e.g., Python stack trace, Node.js exception).
2. **Search**: Use `search_web` to find the error message on StackOverflow, GitHub Issues, or official documentation.
3. **Read**: Use `read_url_content` to extract the fix or implementation example from the search results.
4. **Apply**: Propose or implement the fix directly in the code.

## Verification

- Run a broken script (e.g., missing dependency).
- Observe the agent triggering the search loop.
- Confirm the fix is proposed based on real-world documentation.
