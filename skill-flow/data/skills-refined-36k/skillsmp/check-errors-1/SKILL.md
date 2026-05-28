---
name: check-errors
description: Analyze errors from the central template error repository and suggest TODOs. Use when reviewing template health, planning improvements, or after receiving reports of issues.
allowed-tools: Bash(python3:*), Read, Edit
---

# Check Template Errors

Analyze errors collected from all implementations of this template and suggest improvements.

## What This Does

1. Fetches `errors.jsonl` from the central error repository
2. Categorizes errors by type, template, and frequency
3. Identifies patterns and recurring issues
4. Suggests TODO items for template improvements

## Usage

Run the analysis script:

```bash
python3 .claude/hooks/analyze_errors.py $ARGUMENTS
```

### Common Options

- `--days 7` - Only analyze errors from the last 7 days
- `--days 30` - Last 30 days
- `--template astro-serverless-template` - Filter to specific template
- `--json` - Output as JSON for further processing

## After Analysis

Based on the results:

1. Review the **suggested TODOs** - these are prioritized by frequency
2. Check **recent errors** - look for new patterns
3. Update `TODO.md` with high-priority items
4. Consider adding validation hooks to prevent recurring errors

## Example Workflow

1. Run `/check-errors --days 7` to see recent issues
2. Identify the top error category
3. Create a fix or add validation
4. Test the fix locally
5. Commit and document the improvement

## Error Categories

| Category | Description |
|----------|-------------|
| typescript | Type errors, missing types |
| build_failure | Astro/Vite build failures |
| missing_dependency | npm module not found |
| yaml_config | YAML schema/validation errors |
| astro | Astro-specific issues |
| file_not_found | Missing files/paths |
| fly_io | Fly.io deployment issues |
