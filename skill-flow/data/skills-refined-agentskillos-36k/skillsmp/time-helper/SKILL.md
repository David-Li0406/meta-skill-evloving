---
name: time-helper
description: Provide accurate current time by calling get_time tool.
allowed-tools:
  - get_time
---

## When to use
- User asks “现在几点/当前时间/时区/UTC 时间/本地时间” 等与时间相关的问题。

## Procedure
1) Call `get_time` tool with empty parameters.
2) Use the tool result (`utc`, `local`, `timezone`) to answer.

## Output requirements
- Always include local time and timezone.
- If user explicitly asks for UTC, include UTC too.

