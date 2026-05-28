# JSON Schema Notes (Concise)

## Exit codes

- `0` success
- `2` invalid usage
- `10` Streaks app not found
- `11` Shortcuts CLI missing or failed
- `12` Streaks shortcut missing
- `13` action execution failed

Errors are printed to stderr as JSON in agent mode, e.g.:

```json
{"error":"message","code":10,"error_code":"app_missing"}
```

## Action output envelope (agent mode)

Action results are wrapped in a stable envelope:

```json
{
  "ok": true,
  "timestamp": "RFC3339Nano",
  "action": {"id":"task-list"},
  "shortcut": {"name":"All Tasks"},
  "attempts": 1,
  "duration_ms": 12,
  "input": {"task":"Example"},
  "result": {"raw":"...","format":"text","shortcut":"All Tasks"}
}
```

For `--dry-run`, output is:

```json
{"dry_run":true,"shortcut":"Complete Example in Streaks","input":{"task":"Example"}}
```
