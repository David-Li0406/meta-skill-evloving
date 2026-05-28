# CLI Design Checklist

Use this checklist when adding or reviewing CLI commands.

## Must Have (Blocking)

These items must pass before merging. Failures block the PR.

### Help & Documentation
- [ ] `-h` and `--help` display useful help text
- [ ] Help includes command description
- [ ] Help includes flag/argument descriptions
- [ ] Help includes usage examples in `after_help`

### Streams & Exit Codes
- [ ] Data output goes to stdout
- [ ] Progress, warnings, hints go to stderr
- [ ] Exit code 0 on success
- [ ] Exit code non-zero on failure

### Output Formats
- [ ] `--format json` produces valid JSON
- [ ] JSON output is parseable by `jq`
- [ ] Table output has no borders
- [ ] Each table row represents one entry

### Non-TTY Compatibility
- [ ] Works when stdout is piped: `hawkop cmd | head`
- [ ] Works when stderr is piped: `hawkop cmd 2>&1 | grep`
- [ ] No ANSI codes in output when not TTY
- [ ] No interactive prompts when stdin is not TTY

## Should Have (Important)

These significantly improve UX. Document exceptions if skipped.

### Error Messages
- [ ] Errors explain what went wrong
- [ ] Errors suggest how to fix the issue
- [ ] Errors reference relevant commands (e.g., "Run 'hawkop init'")
- [ ] API errors are translated to human-readable messages

### Color & Formatting
- [ ] Respects `NO_COLOR` environment variable
- [ ] Respects `TERM=dumb`
- [ ] Supports `--no-color` flag (if colors used)
- [ ] Colors degrade gracefully (info still visible without color)

### Navigation & Discovery
- [ ] Suggests next commands: `→ hawkop <next>`
- [ ] Shows "use --all for complete list" when paginated
- [ ] Empty results include helpful hint
- [ ] Invalid subcommand suggests closest match

### Pagination (for list commands)
- [ ] Supports `--limit` flag
- [ ] Supports `--page` flag
- [ ] Supports `--all` flag
- [ ] Shows pagination info in JSON meta

## Nice to Have (Polish)

These are enhancements. Add when time permits.

### Advanced Features
- [ ] Tab completion for dynamic values (IDs, names)
- [ ] `--quiet` / `-q` flag for minimal output
- [ ] `--verbose` / `-v` flag for detailed output
- [ ] Supports reading from stdin: `echo id | hawkop cmd -`

### Progress & Feedback
- [ ] Spinner for operations >1 second
- [ ] Progress bar for known-length operations
- [ ] Estimated time remaining for long operations
- [ ] Clear completion message

### Help Text Quality
- [ ] Examples show common use cases
- [ ] Examples show piping to other tools
- [ ] Flag descriptions include default values
- [ ] Related commands mentioned in help

## Arguments & Flags Review

### Positional Arguments
- [ ] Only ONE type of positional argument
- [ ] If 2+ types needed, use flags instead
- [ ] Variable-length args are same type (e.g., multiple IDs)
- [ ] Argument name is descriptive in help

### Flag Design
- [ ] Uses standard names where applicable:
  - `-f` / `--force` for destructive confirmation skip
  - `-q` / `--quiet` for minimal output
  - `-v` / `--verbose` for detailed output
  - `-n` / `--dry-run` for simulation
  - `-y` / `--yes` for auto-confirm
- [ ] Long flags are kebab-case: `--app-id` not `--appId`
- [ ] Boolean flags don't require values: `--all` not `--all=true`
- [ ] Environment variable fallbacks documented

### Global Flags
- [ ] `--org` works to override organization
- [ ] `--format` works (table/json)
- [ ] `--config` works to override config path
- [ ] `--debug` enables debug logging

## Review Output Template

When reviewing, provide this summary:

```markdown
## CLI Review: [command name]

### Must Have
| Item | Status | Notes |
|------|--------|-------|
| Help text | ✅ | Includes examples |
| Streams | ✅ | stdout/stderr correct |
| Exit codes | ⚠️ | Missing non-zero on API error |
| JSON output | ✅ | Valid, parseable |
| Non-TTY | ✅ | Tested with pipes |

### Should Have
- ✅ Actionable errors
- ⚠️ Missing navigation hints
- ✅ Color respects NO_COLOR

### Blocking Issues
1. Exit code should be non-zero when API returns error

### Recommendations
1. Add `→ hawkop scan get <id>` hint after list output
```
