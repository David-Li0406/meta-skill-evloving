---
name: time-helper
description: Use this skill when a user asks for the current time or timezone information.
---

# Skill body

## When to use
- User asks questions related to time, such as "What time is it now?" or "What is the current timezone?"

## Procedure
1) Call the `get_time` tool with empty parameters.
2) Use the tool result to gather `local`, `utc`, and `timezone` information.
3) Respond with the local time and timezone. If the user explicitly requests UTC, include that as well.