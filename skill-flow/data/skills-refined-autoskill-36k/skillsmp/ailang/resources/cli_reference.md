# AILANG CLI Reference

## Core Commands

### `ailang run`
Run an AILANG program.

```bash
ailang run [flags] <file.ail>
```

**Flags (must come BEFORE filename!):**
| Flag | Description |
|------|-------------|
| `--caps <list>` | Enable capabilities: IO, FS, Net, Clock |
| `--entry <name>` | Entrypoint function (default: main) |
| `--args-json <json>` | JSON arguments to pass to entrypoint |
| `--trace` | Enable execution tracing |
| `--print` | Print return value (default: true) |
| `--no-print` | Suppress output (exit code only) |
| `--relax-modules` | Allow module path mismatch |

**Examples:**
```bash
# Basic run with IO
ailang run --caps IO --entry main hello.ail

# Multiple capabilities
ailang run --caps IO,FS,Net --entry main server.ail

# Pass arguments
ailang run --caps IO --entry main --args-json '{"name":"Alice"}' greet.ail

# Trace execution
ailang run --trace --caps IO --entry main debug.ail
```

### `ailang repl`
Start interactive REPL.

```bash
ailang repl
```

**REPL Commands:**
| Command | Description |
|---------|-------------|
| `:help` | Show help |
| `:type <expr>` | Show type of expression |
| `:quit` | Exit REPL |
| `:load <file>` | Load file into REPL |
| `:reset` | Clear REPL state |

### `ailang check`
Type-check without running.

```bash
ailang check <file.ail>
```

### `ailang watch`
Watch for changes and auto-reload.

```bash
ailang watch <file.ail>
```

### `ailang prompt`
Display teaching prompt for AI code generation.

```bash
ailang prompt                    # Current version
ailang prompt --version v0.3.24  # Specific version
ailang prompt --list             # List all versions
```

### `ailang examples` (v0.6.2+)
Search and view working code examples.

```bash
# Search examples (flags BEFORE query!)
ailang examples search "pattern matching"
ailang examples search --limit 5 "recursion"
ailang examples search --json "fold"

# List examples
ailang examples list                    # All 97 working examples
ailang examples list --tags adt         # Filter by tag
ailang examples list --status all       # Include broken

# View specific example
ailang examples show adt_option         # Show with metadata
ailang examples show adt_option --run   # Show and execute
ailang examples show fold --expected    # Show expected output only

# List available tags
ailang examples tags
```

**Search scoring:**
| Match Type | Score | Description |
|------------|-------|-------------|
| Tag match | 1.0 | Query matches a tag exactly |
| Description match | 0.95 | Query found in description |
| Content match | 0.80 | Query found in .ail file |
| Partial match | 0.60-0.70 | Some query words found |

## Development Tools

### `ailang builtins`
Manage builtin functions.

```bash
ailang builtins list             # List all builtins
ailang builtins list --by-module # Group by module
ailang builtins check-migration  # Check for issues
```

### `ailang doctor`
Diagnostic tools.

```bash
ailang doctor builtins  # Validate builtin registry
```

### `ailang test`
Run test suite.

```bash
ailang test
```

### `ailang iface`
Output module interface (JSON).

```bash
ailang iface <module>
```

## Eval Tools (AI Benchmarking)

### `ailang eval-suite`
Run AI code generation benchmarks.

```bash
ailang eval-suite                          # Dev models (fast)
ailang eval-suite --full                   # All models
ailang eval-suite --models gpt5,claude-sonnet-4-5
ailang eval-suite --skip-existing          # Resume interrupted run
```

### `ailang eval-report`
Generate benchmark reports.

```bash
ailang eval-report <results-dir> <version> --format=json
ailang eval-report <results-dir> <version> --format=markdown
```

### `ailang eval-compare`
Compare two baseline results.

```bash
ailang eval-compare <baseline1-dir> <baseline2-dir>
```

## Server (Collaboration Hub)

### `ailang serve`
Start the Collaboration Hub server.

```bash
ailang serve                    # Default port 1957
ailang serve --port 8080        # Custom port
ailang serve --db /tmp/test.db  # Custom database
```

## Messages (Cross-Agent Communication)

### `ailang messages`
Manage agent-to-agent messages.

```bash
ailang messages list             # All messages
ailang messages list --unread    # Unread only
ailang messages read <id>        # Read message
ailang messages ack <id>         # Mark as read
ailang messages send <inbox> "message" --title "Title"
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `AILANG_RELAX_MODULES` | Set to `1` to relax module path matching |
| `DEBUG_STRICT` | Set to `1` for strict error handling |
| `DEBUG_PARSER` | Set to `1` for parser tracing |
| `DEBUG_MONO_VERBOSE` | Set to `1` for monomorphization tracing |
