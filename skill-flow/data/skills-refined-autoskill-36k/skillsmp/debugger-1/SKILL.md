---
name: debugger
description: Debugging strategy and constraints for ikigai
---

# Debugger

Debugging strategy for ikigai - a TUI app with special constraints.

## Critical Constraint

**ikigai requires `/dev/tty`** - it cannot run in subshells or pipes.

```
Error: Failed to open /dev/tty [src/terminal.c:29]
```

This means:
- `./ikigai` in a Bash tool **will fail**
- You cannot capture stdout/stderr directly
- All builds (debug, release, sanitize) have this constraint

## Build Modes

| Build | `assert()` | Crash behavior |
|-------|------------|----------------|
| `debug` (default) | Active | `SIGABRT` |
| `release` (`-DNDEBUG`) | Compiled out | Segfault/corruption |
| `sanitize` | Active | `SIGABRT` + sanitizer report |

## Decision Tree

```
Bug to investigate?
├── Can reproduce in unit test?
│   └── YES → Run test with sanitizers/valgrind
├── Crash on startup?
│   └── Use core dump analysis
├── Runtime crash/hang?
│   └── Use gdbserver
├── Memory issue?
│   └── valgrind or sanitizers on tests
└── Need trace output?
    └── Add DEBUG_LOG calls
```

## What NOT To Do

- Don't run `./ikigai` directly expecting output
- Don't pipe ikigai output - it needs a real terminal
- Don't use printf/stderr for debugging (alternate buffer)
