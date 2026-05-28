---
name: uloop-clear-console
description: Use this skill when you need to clear Unity console logs before running tests, starting a fresh debugging session, or cleaning up log output for better readability.
---

# uloop clear-console

Clear Unity console logs.

## Usage

```bash
uloop clear-console [--add-confirmation-message]
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--add-confirmation-message` | boolean | `false` | Add confirmation message after clearing |

## Examples

```bash
# Clear console
uloop clear-console

# Clear with confirmation
uloop clear-console --add-confirmation-message
```

## Output

Returns JSON confirming the console was cleared.