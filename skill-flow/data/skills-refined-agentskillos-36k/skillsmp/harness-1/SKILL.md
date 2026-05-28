---
name: harness
description: Operate the hn TUI at runtime via the agent harness
triggers:
  - test the tui
  - run the harness
  - interact with the tui
  - verify the ui
  - check the screen
---

# Agent Harness Skill

Operate the `hn` TUI as a black box: launch it, observe the screen, send keystrokes, and verify behavior.

## When to Use

- Verifying UI changes render correctly with real data
- Testing navigation flows (stories → comments → back)
- Checking that keybindings work as expected
- Validating error states and loading behavior

## Scripts

All scripts are in the `scripts/` directory. Run from the repo root.

### Start the Harness

```bash
./scripts/harness-start /tmp/hn-harness.sock
```

- Builds release binary if needed
- Spawns TUI in a PTY (80x24)
- Prints socket path on success
- Creates `${SOCKET}.pid` for tracking

### Send Commands

```bash
./scripts/harness-cmd <socket> '<json>'
```

Available commands:

| Command    | JSON               | Response                                                  |
|------------|--------------------|-----------------------------------------------------------|
| Get screen | `{"cmd":"screen"}` | `{"status":"screen","rows":24,"cols":80,"content":"..."}` |
| Quit       | `{"cmd":"quit"}`   | `{"status":"ok"}`                                         |

**Planned (not yet implemented):**

- `{"cmd":"keys","keys":"jjl"}` - send keystrokes
- `{"cmd":"ctrl","char":"c"}` - send control character
- `{"cmd":"wait","pattern":"comments","timeout_ms":3000}` - wait for text

### Stop the Harness

```bash
./scripts/harness-stop /tmp/hn-harness.sock
```

- Sends quit command
- Kills process by PID
- Removes socket and PID file
- Always succeeds (idempotent)

### Clean Up Orphaned Processes

```bash
./scripts/harness-cleanup
```

Run this if a previous session crashed or was interrupted. Kills all harness-related processes and removes socket files.

## Workflow

### Basic: Verify Screen Renders

```bash
# 1. Start harness
./scripts/harness-start /tmp/hn-harness.sock

# 2. Capture screen
SCREEN=$(./scripts/harness-cmd /tmp/hn-harness.sock '{"cmd":"screen"}')

# 3. Check content (using jq)
echo "$SCREEN" | jq -r '.content'

# 4. Stop harness
./scripts/harness-stop /tmp/hn-harness.sock
```

### Interpreting Screen Output

The `screen` command returns JSON with:

- `rows`: terminal height (24)
- `cols`: terminal width (80)
- `content`: plain text screen contents (newline-separated lines)

The content is the rendered TUI without ANSI escape codes. Example:

```
[0]Favs  [1]Top  [2]New  [3]Best  [4]Ask  [5]Show  [6]Jobs        loaded 5m ago
────────────────────────────────────────────────────────────────────────────────
▶ Story title here (domain.com)
  ▲ 123 | username | 45 comments | 2h ago
  Another story...
────────────────────────────────────────────────────────────────────────────────
 Top  1/30 | H/L:feeds  f:fav  ?:help  q:quit
```

Key elements to look for:

- **Feed tabs**: `[0]Favs  [1]Top  [2]New...` at top
- **Selected story**: marked with `▶`
- **Story metadata**: `▲ score | author | N comments | time`
- **Status bar**: feed name, position, keybindings at bottom
- **Separators**: `─` lines between sections

### Error Handling

If a command fails, the response will be:

```json
{
  "status": "error",
  "message": "description of error"
}
```

If the harness process dies, commands will fail with socket errors. Run `harness-cleanup` and start fresh.

## Important Notes

1. **Always stop the harness** when done. Use `harness-stop` or the session will leak processes.

2. **One harness at a time** per socket path. If you need multiple, use different socket paths.

3. **Screen content is live data**. The TUI fetches from the real HN API, so story titles and counts will vary.

4. **Release build is used** for speed. The TUI loads faster and renders more responsively.

5. **Dark theme is forced** via `--dark` flag to skip terminal detection (which would hang in PTY).

6. **Run commands in foreground without extended timeouts**. The scripts handle their own waiting internally (
   `harness-start` waits ~4s for initialization). Do not use `run_in_background` or set long timeouts—just run them
   normally and they'll complete quickly.

## Troubleshooting

### "socket not found"

The harness isn't running or hasn't started yet. Check if `harness-start` succeeded.

### Hanging commands

The harness may have crashed. Run `harness-cleanup` and try again.

### Empty screen content

Rare issue with PTY initialization. Stop, cleanup, and restart.

### "harness process died" on start

Build may have failed. Check cargo output. Ensure you're in the repo root.
