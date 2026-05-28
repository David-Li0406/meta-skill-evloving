# mc-quick.sh Usage Specification

Ultra-simple wrapper script for meatycapture request-log capture. Reduces ~20 lines of JSON to a single command line with 6 arguments.

**Script Location**: `.claude/skills/meatycapture-capture/scripts/mc-quick.sh`

---

## When to Use mc-quick.sh vs Direct CLI

| Scenario | Tool | Rationale |
|----------|------|-----------|
| Single capture during development | `mc-quick.sh` | Fastest - no JSON construction |
| AI agent capturing findings | `mc-quick.sh` | Token-efficient - single command |
| Batch capture (3+ items) | Direct CLI | Script handles one item at a time |
| Complex notes with formatting | Direct CLI | Script notes are plain strings |
| Appending to existing docs | Direct CLI | Script creates new entries only |
| Custom fields (context) | Direct CLI | Script uses predefined field set |

**Rule of thumb**: Use `mc-quick.sh` for quick single captures; use direct CLI for complex scenarios.

---

## Installation

The script requires `meatycapture` CLI to be in PATH. No additional dependencies.

### Verify Installation

```bash
# Check meatycapture is available
which meatycapture

# Check script is executable
ls -la .claude/skills/meatycapture-capture/scripts/mc-quick.sh

# Make executable if needed
chmod +x .claude/skills/meatycapture-capture/scripts/mc-quick.sh
```

### Add to PATH (Optional)

For convenience, add script to PATH or create alias:

```bash
# Option 1: Alias in shell config
alias mc-quick='.claude/skills/meatycapture-capture/scripts/mc-quick.sh'

# Option 2: Symlink to user bin
ln -s $(pwd)/.claude/skills/meatycapture-capture/scripts/mc-quick.sh ~/bin/mc-quick
```

---

## Command Syntax

```
mc-quick.sh TYPE DOMAIN SUBDOMAIN "Title" "Problem" "Goal" [additional notes...]
```

### Positional Arguments

| Position | Argument | Required | Description |
|----------|----------|----------|-------------|
| 1 | TYPE | Yes | Item type: `enhancement`, `bug`, `idea`, `task`, `question` |
| 2 | DOMAIN | Yes | Primary domain(s) - comma-separated for multiple |
| 3 | SUBDOMAIN | Yes | Subdomain/component(s) - comma-separated for multiple |
| 4 | TITLE | Yes | Short descriptive title |
| 5 | PROBLEM | Yes | Description of the problem or current state |
| 6 | GOAL | Yes | Description of desired outcome |
| 7+ | [notes...] | No | Additional notes (each becomes separate note) |

### Environment Variables

Configure defaults to reduce repetitive arguments:

| Variable | Default | Description |
|----------|---------|-------------|
| `MC_PROJECT` | `skillmeat` | Project name for the capture |
| `MC_PRIORITY` | `medium` | Priority level |
| `MC_STATUS` | `triage` | Initial status |

```bash
# Set for session
export MC_PROJECT="my-project"
export MC_PRIORITY="high"

# Or inline for single command
MC_PROJECT=my-project MC_PRIORITY=high mc-quick.sh ...
```

---

## Examples

### Basic Enhancement

```bash
mc-quick.sh enhancement web deployments \
  "Implement Remove button" \
  "Button shows not implemented error" \
  "Full removal with filesystem toggle option"
```

### High-Priority Bug

```bash
MC_PRIORITY=high mc-quick.sh bug api validation \
  "Fix auth timeout" \
  "Sessions expire after 5 minutes" \
  "Extend session TTL to 24 hours"
```

### Multiple Domains

```bash
mc-quick.sh enhancement "web,cli" "deployments,sync" \
  "Unified deployment status" \
  "Web and CLI show different statuses" \
  "Single source of truth for deployment state"
```

### With Additional Notes

```bash
mc-quick.sh idea core analytics \
  "Usage analytics dashboard" \
  "No visibility into feature usage" \
  "Dashboard showing usage metrics" \
  "Include daily/weekly/monthly views" \
  "Track most-used artifacts" \
  "Consider privacy implications"
```

### Quick Idea Capture

```bash
mc-quick.sh idea dx tooling \
  "Auto-generate schema validation" \
  "Manually writing validation is error-prone" \
  "Generate validation from TypeScript types"
```

### Different Project

```bash
MC_PROJECT=other-project mc-quick.sh bug cli commands \
  "Help text shows wrong examples" \
  "Examples use deprecated syntax" \
  "Update help text with current syntax"
```

---

## Output

### Success

```
✓ Capture successful
```

The command also outputs the JSON response from meatycapture (to stdout):
```json
{
  "success": true,
  "doc_id": "REQ-20260111-skillmeat",
  "doc_path": "/path/to/REQ-20260111-skillmeat.md",
  "items_created": [
    {
      "item_id": "REQ-20260111-skillmeat-01",
      "title": "Implement Remove button"
    }
  ]
}
```

### Validation Errors

```bash
# Missing arguments
❌ Error: Minimum 6 arguments required

# Invalid type
❌ Error: TYPE must be one of: enhancement bug idea task question
```

### Capture Failure

```
❌ Capture failed
```

Check meatycapture logs for details.

---

## How It Works

1. **Parse Arguments**: Validates TYPE and extracts positional args
2. **Build Tags**: Auto-generates tags from comma-separated domain/subdomain values
3. **Build Notes**: Creates notes array from Problem, Goal, and additional args
4. **Construct JSON**: Wraps in proper `{ project, items: [...] }` structure
5. **Temp File**: Writes JSON to temp file (workaround for stdin bug)
6. **Call CLI**: Runs `meatycapture log create <tempfile> --json`
7. **Cleanup**: Removes temp file on exit (via trap)

### Auto-Generated Tags

Domain and subdomain values become tags automatically:

```bash
mc-quick.sh enhancement web "deployments,modal" "Title" "Problem" "Goal"
```

Generates tags: `["web", "deployments", "modal"]`

### Notes Structure

Problem and Goal are automatically prefixed:

```bash
mc-quick.sh idea cli automation "Title" \
  "Current process is manual" \
  "Automate the workflow" \
  "Additional implementation detail"
```

Generates notes:
```json
[
  "Problem: Current process is manual",
  "Goal: Automate the workflow",
  "Additional implementation detail"
]
```

---

## Integration with AI Agents

### Token Efficiency

Using `mc-quick.sh` reduces token usage compared to constructing JSON:

| Approach | Approximate Tokens |
|----------|-------------------|
| Full JSON construction | ~200-300 tokens |
| mc-quick.sh command | ~50-80 tokens |

### Example Agent Usage

```bash
# AI agent can capture findings with single command
mc-quick.sh bug web "components,forms" \
  "Form validation fires on initial load" \
  "Validation errors show before user input" \
  "Only validate on blur or submit"
```

### Batch Pattern for Agents

For multiple captures, run sequentially:

```bash
mc-quick.sh bug api auth "Token refresh fails" "..." "..."
mc-quick.sh enhancement web ui "Add loading states" "..." "..."
mc-quick.sh idea dx testing "E2E test generator" "..." "..."
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `meatycapture: command not found` | CLI not in PATH | Install meatycapture or check PATH |
| `Permission denied` | Script not executable | `chmod +x scripts/mc-quick.sh` |
| `Capture failed` | Invalid JSON or API error | Check meatycapture CLI directly |
| Wrong project | MC_PROJECT not set | Set `MC_PROJECT=your-project` |
| Tags not appearing | Empty domain/subdomain | Provide at least one value each |

### Debug Mode

To see the generated JSON before capture:

```bash
# Edit script temporarily or add debug output
# The JSON is written to a temp file - check with:
cat /tmp/tmp.XXXXXX  # Replace with actual temp file
```

---

## Limitations

- **Single item only**: Use direct CLI for batch capture
- **No context field**: Script doesn't support context parameter
- **No append mode**: Always creates new entries
- **Simple notes**: No structured note objects (only plain strings)
- **Fixed structure**: Problem/Goal format enforced

For advanced scenarios, use `meatycapture log create` directly with full JSON control.

---

## Related Documentation

- `../SKILL.md` - Skill overview and quick reference
- `../workflows/capturing.md` - Full capture workflow documentation
- `../references/field-options.md` - Complete field catalog
- `../templates/` - JSON templates for direct CLI usage
