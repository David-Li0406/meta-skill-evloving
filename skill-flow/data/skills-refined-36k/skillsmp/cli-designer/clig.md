# CLI Guidelines (clig.dev Reference)

Local reference for [clig.dev](https://clig.dev) principles. Use this for quick lookup during CLI design.

---

## Philosophy

### Core Principles

| Principle | Meaning |
|-----------|---------|
| **Human-First** | Design for humans primarily, machines secondarily |
| **Composability** | Work with other tools via stdin/stdout/stderr, exit codes |
| **Consistency** | Follow established terminal conventions |
| **Discoverability** | Users learn through exploration, not memorization |
| **Empathy** | Make users feel supported; exceed expectations |
| **Robustness** | Handle unexpected input gracefully |

### Conversational Interaction

CLI use is a dialogue: try command → receive feedback → adjust. Good design acknowledges this with suggestions, clarifications, and confirmations.

---

## The Basics (Non-Negotiable)

### Exit Codes

```bash
0   = success
1+  = failure (map specific failures to specific codes)
```

Scripts depend on exit codes to determine outcomes.

### Output Routing

| Stream | Purpose | Example |
|--------|---------|---------|
| stdout | Data output | JSON, tables, results |
| stderr | Messages | Progress, warnings, errors |

This separation keeps piped output clean.

### Argument Parsing

Use established libraries:

| Language | Library |
|----------|---------|
| Rust | clap |
| Go | Cobra |
| Python | Click |
| Node | oclif |
| Java | picocli |

---

## Help Documentation

### Help Must Work Everywhere

```bash
hawkop --help           # Full help
hawkop -h               # Full help
hawkop <cmd> --help     # Command help
hawkop help <cmd>       # Alternative (Git-style)
```

### Help Content Strategy

1. **Lead with examples** - users reference these most
2. **Most common flags first** - don't bury useful options
3. **Include actual output** - shows what to expect
4. **Link to web docs** - for detailed explanations
5. **Suggest next commands** - guide exploration

### On Missing Arguments

Show brief help including:
- What the program does
- 1-2 example invocations
- Common flags
- Instructions to use `--help` for full details

### Error Suggestions

When users mistype commands, suggest corrections but **don't execute them automatically**:
```
Did you mean 'hawkop scan list'?
```

---

## Output Formatting

### Human-Readable First

Detect terminal presence via TTY check. Format for humans when interactive, plain when piped.

### Machine-Readable Support

| Flag | Output |
|------|--------|
| `--json` | Structured JSON |
| `--plain` | One record per line, no colors |

### Success Output

- **Display what changed** - UNIX silence can seem broken
- **Keep messages brief** - don't overwhelm
- **Support `-q`/`--quiet`** - for scripts

### State Visibility

Make current state easily accessible (like `git status`). Inform users and suggest next actions.

### Color Guidelines

Enable color when:
- Output is an interactive TTY
- `NO_COLOR` is not set
- `TERM` is not `dumb`
- `--no-color` was not passed

Use color to **highlight critical information**, not everything.

### Progress Indication

- Display for operations >1 second
- Use animated spinners (shows program is alive)
- Show progress bars for known-length operations
- Display estimated time remaining when possible
- Disable animations when output isn't a TTY

---

## Error Handling

### Human-Centered Errors

Catch expected errors and rewrite for humans:

```
# BAD
EPERM: operation not permitted

# GOOD
Can't write to output.json. Try running 'chmod +w output.json'.
```

### Visual Hierarchy

Place most important information **last** (where eyes linger).

### Debug Information

For unexpected errors:
1. Provide debug logs/traceback
2. Include submission instructions
3. Consider writing debug logs to files

### Bug Report Pathway

Generate pre-populated bug report URLs with context when possible.

---

## Arguments and Flags

### Prefer Flags to Arguments

Flags clarify intent and enable future changes:

```bash
# BAD: Which is source, which is dest?
hawkop copy app1 app2

# GOOD: Crystal clear
hawkop copy --from app1 --to app2
```

### Full-Length Versions Required

Always provide both forms:
```bash
-h, --help    # Both required
```

Long forms for descriptive scripts; short forms for interactive speed.

### Standard Flag Names

| Flag | Purpose |
|------|---------|
| `-a, --all` | Include everything |
| `-d, --debug` | Enable debug output |
| `-f, --force` | Force, suppress prompts |
| `-h, --help` | Help (exclusively) |
| `--json` | JSON output |
| `-n, --dry-run` | Preview without executing |
| `--no-input` | Disable all prompts |
| `-o, --output` | Output file path |
| `-q, --quiet` | Reduce verbosity |
| `-v, --verbose` | Increase verbosity |
| `--version` | Version information |

### Sensible Defaults

Make defaults correct for **most users**. Most won't find or remember flags.

### Confirmation for Dangerous Operations

| Severity | Action |
|----------|--------|
| Mild | Optional confirmation |
| Moderate | Prompt + offer `--dry-run` |
| Severe | Require typed confirmation or `--confirm="name"` |

### Never Accept Secrets via Flags

Flags leak to `ps` output and shell history. Use:
- `--password-file` for file-based secrets
- stdin for piped secrets

---

## Interactivity

### TTY Detection

Use prompts only when stdin is an interactive terminal. Piped/scripted contexts should fail with clear flag requirements.

### `--no-input` Flag

Explicit opt-out of all prompts. When set and input needed, fail with instructions on passing info via flags.

### User Escape Routes

- Always respect Ctrl-C (INT signal)
- Exit immediately when Ctrl-C pressed
- Document escape sequences for wrapper programs

---

## Subcommands

### Consistency Rules

- Same flag names for same purposes across subcommands
- Consistent output formatting
- Consistent noun-verb or verb-noun ordering

### Avoid Ambiguity

Don't have "update" and "upgrade" as separate commands - use different terminology.

### No Catch-All Subcommands

Don't allow omitting frequently-used subcommands (prevents adding new commands).

### No Ambiguous Abbreviations

Disallow `i` for `install` - can't add future commands starting with `i`.

---

## Robustness

### Response Time

Output something within **100ms**. Network requests should print before executing.

### Progress for Long Operations

Static progress bars that freeze make programs appear crashed. Keep them moving.

### Timeouts

All network operations need configurable timeouts with reasonable defaults.

### Crash-Only Software

Defer cleanup or perform it on next run. Enables immediate exit on interruption.

### Anticipate Misuse

Users will:
- Wrap in scripts
- Run on poor connections
- Launch multiple instances
- Use in untested environments

Design defensively.

---

## Configuration

### Hierarchy (highest to lowest)

1. Command-line flags
2. Environment variables
3. Project-level config (`.env`)
4. User-level config
5. System-wide config

### XDG Base Directory Spec

Follow XDG to consolidate config files:

| Type | Path |
|------|------|
| Config | `~/.config/<app>/` |
| Data | `~/.local/share/<app>/` |
| Cache | `~/.cache/<app>/` |

Respect `XDG_CONFIG_HOME`, `XDG_DATA_HOME`, `XDG_CACHE_HOME` overrides.

---

## Environment Variables

### Respect Standard Variables

| Variable | Purpose |
|----------|---------|
| `NO_COLOR` | Disable colors |
| `FORCE_COLOR` | Enable colors despite detection |
| `DEBUG` | Verbose output |
| `EDITOR` | For file editing prompts |
| `HTTP_PROXY` | Network routing |
| `PAGER` | Output pagination |

### Never Store Secrets in Environment Variables

Environment variables leak through:
- Export to child processes
- Shell substitutions in process state
- Docker inspect
- systemctl show

Use credential files, pipes, or secret management services.

---

## Signals

### Ctrl-C Handling

1. Exit immediately when Ctrl-C pressed
2. Announce exit before starting cleanup
3. Implement timeouts on cleanup
4. Second Ctrl-C skips remaining cleanup

---

## Naming

| Rule | Example |
|------|---------|
| Simple, memorable | `fig` not `fast-intelligent-generator` |
| Unique | Check existing commands |
| Lowercase only | `hawkop` not `HawkOp` |
| Dashes if needed | `my-tool` |
| Typable | Consider ergonomics |

---

## Quick Reference Card

| Category | Key Rule |
|----------|----------|
| Exit codes | 0 = success, non-zero = failure |
| Streams | stdout = data, stderr = messages |
| Help | `-h`/`--help` everywhere with examples |
| Errors | What + why + how to fix |
| Flags | Prefer over positional args |
| Defaults | Correct for most users |
| Colors | Respect `NO_COLOR`, `TERM=dumb` |
| Progress | Show for >1 second operations |
| Timeouts | Always have them |
| Config | Follow XDG spec |
| Secrets | Never in flags or env vars |

---

## Further Reading

- [clig.dev](https://clig.dev) - Original source
- [12-Factor CLI Apps](https://medium.com/@jdxcode/12-factor-cli-apps-dd3c227a0e46) - See `12-factors.md`
- [XDG Base Directory Spec](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html)
- [POSIX Utility Conventions](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html)
