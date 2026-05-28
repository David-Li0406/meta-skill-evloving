---
name: terminal
description: |
  Interactive terminal session management using tmux. Use when TTY or stdin is required for interactive commands (vim, top, less, ssh, etc.). Provides persistent sessions that maintain state across multiple interactions. Use the Bash tool for simple non-interactive commands; use this skill only when interactivity is needed.
---

# Terminal

Provides interactive terminal sessions for executing commands that require TTY or stdin.

## Key Features

- Send keystrokes to a tmux session and capture output
- Persistent sessions maintain state (environment variables, working directory)
- Multiple sessions can be managed independently
- Special key support (Enter, Escape, Up, Down, C-c, etc.)

## Usage

Run `scripts/terminal.sh` with the following commands:

### Execute: Send keys and capture output

```bash
scripts/terminal.sh execute [options] [keys...]
```

**Options:**
- `--session NAME` - Session name (auto-generated if omitted, reuses last session)
- `--read-wait MS` - Wait time before capturing output (default: 1000)
- `--key-delay MS` - Delay between keystrokes (default: 0)
- `--literal` - Send keys literally without parsing special keys
- `--raw-output` - Preserve escape sequences (ANSI colors, formatting) in output
- `--width N` - Terminal width for new sessions
- `--height N` - Terminal height for new sessions

**Keys:** Pass keys as separate arguments. Special keys are automatically recognized:
- Control keys: `C-c`, `C-d`, `C-z`, `C-u`, etc.
- Function keys: `F1`-`F12`
- Navigation: `Up`, `Down`, `Left`, `Right`, `Home`, `End`, `PageUp`, `PageDown`
- Other: `Enter`, `Escape`, `Tab`, `BSpace` (backspace), `DC` (delete)

### Close: Terminate a session

```bash
scripts/terminal.sh close --session NAME
```

### Cleanup: Terminate all sessions

```bash
scripts/terminal.sh cleanup
```

## Examples

**Run a command:**
```bash
scripts/terminal.sh execute 'echo hello world' Enter
```

**Start an interactive program:**
```bash
scripts/terminal.sh execute 'top' Enter --read-wait 2000
```

**Send keys to exit (press q):**
```bash
scripts/terminal.sh execute q
```

**Edit a file with vim:**
```bash
scripts/terminal.sh execute 'vim file.txt' Enter --read-wait 1000
```

**Navigate vim and save:**
```bash
scripts/terminal.sh execute ':wq' Enter
```

**Cancel a running command:**
```bash
scripts/terminal.sh execute C-c
```

**Use a named session:**
```bash
scripts/terminal.sh execute --session dev 'cd /project && npm start' Enter
scripts/terminal.sh execute --session dev  # Check output later
scripts/terminal.sh close --session dev
```

**Capture colored output:**
```bash
scripts/terminal.sh execute --raw-output 'ls --color=always' Enter
scripts/terminal.sh execute --raw-output 'grep --color=always pattern file.txt' Enter
```

## Best Practices

- Use empty keys to check current terminal state: `scripts/terminal.sh execute`
- End commands with `Enter` to execute them
- Use `--literal` for text containing special key names
- Use `--read-wait` with longer values for slow commands
- Use `C-c` to interrupt running processes
