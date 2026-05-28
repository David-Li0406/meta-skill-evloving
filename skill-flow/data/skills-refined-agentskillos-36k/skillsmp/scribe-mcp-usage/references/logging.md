# Logging Discipline

Every `append_entry` must include a reasoning block:
```json
{"reasoning": {"why": "...", "what": "...", "how": "..."}}
```

Log after each meaningful step (every 2-3 edits or ~5 minutes) and after investigations, decisions, tests, errors, and completions.
