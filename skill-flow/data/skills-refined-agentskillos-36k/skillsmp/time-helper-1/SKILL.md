---
name: time-helper
description: Provide accurate current time by calling get_time tool.
allowed-tools:
  - get_time
---

## When to use
- User asks about current time / timezone.

## Procedure
1) Call `get_time`.
2) Answer with local time + timezone (and UTC if asked).

