---
name: time-helper
description: Use this skill when the user asks for the current time or timezone information.
---

## When to use
- User asks questions related to current time, such as "现在几点", "当前时间", "时区", "UTC 时间", or "本地时间".

## Procedure
1) Call `get_time` tool with empty parameters.
2) Use the tool result (`utc`, `local`, `timezone`) to answer.

## Output requirements
- Always include local time and timezone.
- If the user explicitly asks for UTC, include UTC as well.