# The 12 Factors of CLI Design

Deep dive on each principle from [12-Factor CLI Apps](https://medium.com/@jdxcode/12-factor-cli-apps-dd3c227a0e46).

## 1. Great Help is Essential

Help is the primary way users discover functionality. Without a UI, help must be exceptional.

### Requirements

All of these must show help:
```bash
hawkop                      # List commands
hawkop --help               # Full help
hawkop -h                   # Full help
hawkop <cmd> --help         # Command help
hawkop <cmd> -h             # Command help
```

### Help Content

Every command's help should include:
- **Description** - What the command does
- **Arguments** - Each arg with description
- **Flags** - Each flag with description and default
- **Examples** - Most important! Common usage patterns

### Shell Completion

Completion is another form of help. Users discover flags and values by pressing TAB.

---

## 2. Prefer Flags to Args

Flags are self-documenting; positional arguments require memorization.

### The Rule

| Positional Args | Recommendation |
|-----------------|----------------|
| 1 type | OK |
| 2 types | Suspect - consider flags |
| 3+ types | Always use flags |

### Example

```bash
# BAD: Which is source, which is destination?
hawkop fork app1 app2

# GOOD: Crystal clear
hawkop fork --from app1 --to app2
```

### Exception

Variable-length same-type args are fine:
```bash
hawkop delete id1 id2 id3  # All IDs, same type
```

---

## 3. What Version Am I On?

Users need version info for debugging and support requests.

### Requirements

All of these should work:
```bash
hawkop version    # Multi-command CLIs
hawkop --version  # Standard
hawkop -V         # Short form
```

### Include Debug Info

```
hawkop 0.3.0 (darwin-arm64)
API: https://api.stackhawk.com
Config: ~/.config/hawkop/config.yaml
```

### User-Agent

Send version in API requests for server-side debugging:
```
User-Agent: hawkop/0.3.0 darwin-arm64
```

---

## 4. Mind the Streams

Proper stream usage enables composability.

### The Rule

| Stream | Purpose | Example |
|--------|---------|---------|
| stdout | Data output | Tables, JSON, results |
| stderr | Messaging | Progress, warnings, errors |

### Why It Matters

```bash
hawkop scan list > scans.json  # JSON to file
# Progress bar still visible on stderr!
```

### Implementation

```rust
println!("{}", data);      // stdout - data
eprintln!("Loading...");   // stderr - message
```

---

## 5. Handle Things Going Wrong

Errors happen frequently. Make them helpful.

### Great Error Structure

1. **Error code/type** - For programmatic handling
2. **Error title** - Human-readable summary
3. **Description** - What happened (optional)
4. **How to fix** - Actionable guidance
5. **URL** - More information (optional)

### Example

```
Error: EPERM - Invalid permissions on output.json
Cannot write to output.json, file does not have write permissions.
Fix with: chmod +w output.json
Docs: https://docs.example.com/errors#eperm
```

### Debug Mode

For unexpected errors, support `--debug` or `DEBUG=1` for full traces.

---

## 6. Be Fancy!

Modern CLIs should look good, but degrade gracefully.

### Use Thoughtfully

- **Colors** - Highlight important information
- **Spinners** - Operations >1 second
- **Progress bars** - Known-length operations
- **Box drawing** - Structure complex output

### Respect the Environment

| Condition | Action |
|-----------|--------|
| `NO_COLOR` set | Disable colors |
| `TERM=dumb` | Disable colors |
| `--no-color` | Disable colors |
| stdout not TTY | Plain output |

---

## 7. Prompt If You Can

Interactive prompts improve UX when appropriate.

### Guidelines

- Prompt when stdin is TTY and info is missing
- **Never require prompts** - flags must override
- Use confirmation for dangerous actions

### Pattern

```rust
let value = match flag_value {
    Some(v) => v,
    None if stdin.is_terminal() => prompt_user()?,
    None => return Err("--flag required in non-interactive mode"),
};
```

---

## 8. Use Tables

Tables are the primary data display format.

### Rules

| Rule | Reason |
|------|--------|
| No borders | Breaks parsing, adds noise |
| One row = one entry | Enables `wc -l`, `grep` |
| Headers by default | Identifies columns |
| Truncate to width | Prevents wrapping |

### Supported Flags

- `--columns COL1,COL2` - Select columns
- `--no-headers` - Hide headers
- `--no-truncate` - Full content
- `--sort COL` - Sort by column

---

## 9. Be Speedy

Startup time affects user perception.

### Benchmarks

| Time | Perception |
|------|------------|
| <100ms | Very fast |
| 100-500ms | **Target this** |
| 500ms-2s | Usable |
| 2s+ | Frustrating |

### For Slow Operations

- Show spinner immediately
- Progress bar for known length
- Stream results as they arrive

---

## 10. Encourage Contributions

Open source benefits from community.

### Checklist

- Open source with clear license
- README with quick start
- CONTRIBUTING.md with:
  - Local development setup
  - Test instructions
  - Code style guide
- CODE_OF_CONDUCT.md
- Issue and PR templates

---

## 11. Be Clear About Subcommands

HawkOp is a multi-command CLI.

### Empty Invocation

Show help, not default action:
```bash
$ hawkop
HawkOp - CLI for StackHawk

Commands:
  init    Initialize configuration
  scan    View and manage scans
  ...
```

### Hierarchy

```bash
hawkop scan list      # List scans
hawkop scan get       # Get details
```

### Avoid Ambiguity

Don't use argument names that could be subcommands:
```bash
# Problematic if "help" could be a valid resource name
hawkop resource help  # Subcommand or argument?
```

---

## 12. Follow XDG Spec

Store files in standard locations.

### Locations

| Type | Path |
|------|------|
| Config | `~/.config/hawkop/` |
| Data | `~/.local/share/hawkop/` |
| Cache | `~/.cache/hawkop/` |

### Environment Variables

Respect overrides:
- `XDG_CONFIG_HOME`
- `XDG_DATA_HOME`
- `XDG_CACHE_HOME`


---

## Quick Reference Card

| # | Factor | One-Line Rule |
|---|--------|---------------|
| 1 | Help | `-h`/`--help` everywhere with examples |
| 2 | Flags | 1 arg type OK, 2+ use flags |
| 3 | Version | `--version`, `-V`, `version` |
| 4 | Streams | stdout=data, stderr=messages |
| 5 | Errors | What + why + how to fix |
| 6 | Fancy | Colors yes, but degrade gracefully |
| 7 | Prompts | Interactive OK, flags override |
| 8 | Tables | No borders, one row per entry |
| 9 | Speed | <500ms startup, show progress |
| 10 | Open | License, docs, welcoming |
| 11 | Subcommands | Clear hierarchy, help on empty |
| 12 | XDG | Standard config locations |
