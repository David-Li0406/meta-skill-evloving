**Skill**: [Code Hardcode Audit](../SKILL.md)

# Troubleshooting

## Tool Not Found Errors

### ruff not found

```
Error: ruff not found
```

**Fix**: Install Ruff globally with uv:

```bash
uv tool install ruff
```

### semgrep not found

```
Error: semgrep not found
```

**Fix**: Install Semgrep with Homebrew:

```bash
brew install semgrep
```

### npx not found

```
Error: npx not found
```

**Fix**: Install Node.js via mise:

```bash
mise install node
mise use --global node
```

## Semgrep Issues

### Rules file not found

```
Error: Semgrep rules not found: /path/to/assets/semgrep-hardcode-rules.yaml
```

**Cause**: Running script from wrong location or rules file missing.

**Fix**: Verify rules file exists:

```bash
/usr/bin/env bash << 'TROUBLESHOOTING_SCRIPT_EOF'
# Environment-agnostic path
PLUGIN_DIR="${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/plugins/marketplaces/cc-skills/plugins/itp}"
ls "$PLUGIN_DIR/skills/code-hardcode-audit/assets/semgrep-hardcode-rules.yaml"
TROUBLESHOOTING_SCRIPT_EOF
```

### Too many false positives

**Cause**: Default rules are broad for maximum detection.

**Fix**: Customize rules by editing `assets/semgrep-hardcode-rules.yaml`:

```yaml
# Add exclusions
patterns:
  - pattern: '"http://$..."'
  # Exclude test files
  - pattern-not-inside: |
      def test_$...():
          ...
```

### Semgrep timeout

```
Error: Semgrep timed out
```

**Cause**: Large codebase or complex rules.

**Fix**: Use `--exclude` to skip large directories:

```bash
uv run --script audit_hardcodes.py -- src/ --exclude "node_modules" --exclude ".venv"
```

## jscpd Issues

### jscpd timeout

```
Error: jscpd timed out after 5 minutes
```

**Cause**: Very large codebase.

**Fix**:

1. Exclude non-essential directories
2. Run jscpd separately on smaller directories

```bash
uv run --script run_jscpd.py -- src/core/
```

### No duplicates found (false negative)

**Cause**: Default threshold too high.

**Fix**: Lower detection threshold in jscpd config. Create `.jscpd.json`:

```json
{
  "threshold": 5,
  "minLines": 3,
  "minTokens": 25
}
```

### Node.js version mismatch

```
Error: jscpd requires Node.js >= 16
```

**Fix**: Update Node.js via mise:

```bash
mise install node
mise use --global node
```

## Ruff Issues

### No findings (false negative)

**Cause**: PLR2004 only detects magic numbers in **comparisons**.

```python
# NOT detected (assignments)
TIMEOUT = 30
port = 8123

# DETECTED (comparisons)
if timeout > 30:
if port == 8123:
```

**Fix**: Use Semgrep for broader detection of hardcoded values in assignments.

### Ruff version compatibility

```
Error: Unknown rule: PLR2004
```

**Cause**: Old Ruff version.

**Fix**: Update Ruff:

```bash
uv tool install --upgrade ruff
```

## General Issues

### Permission denied

```
Error: Permission denied: /path/to/file
```

**Fix**: Check file permissions or run with appropriate user:

```bash
chmod -R u+r /path/to/directory
```

### Out of memory

**Cause**: Very large codebase causing memory exhaustion.

**Fix**:

1. Use `--no-parallel` to run tools sequentially
2. Process directories individually

```bash
uv run --script audit_hardcodes.py -- src/ --no-parallel
```

### JSON parse error

```
Error: Error parsing output
```

**Cause**: Tool produced invalid JSON (often mixed with warnings).

**Fix**:

1. Check tool stderr for warnings
2. Run tool individually to isolate the issue

```bash
ruff check --select PLR2004 --output-format json src/ 2>&1
```

## Getting Help

1. Check tool-specific documentation:
   - [Ruff PLR2004](https://docs.astral.sh/ruff/rules/magic-value-comparison/)
   - [Semgrep Rules](https://semgrep.dev/docs/writing-rules/overview)
   - [jscpd GitHub](https://github.com/kucherenko/jscpd)

2. Report skill issues:
   - Check ADR-0047 for design decisions
   - Review the [code-hardcode-audit SKILL.md](../SKILL.md)
