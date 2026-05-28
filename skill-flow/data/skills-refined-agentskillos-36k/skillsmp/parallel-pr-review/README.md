# Parallel PR Review

A Claude Code skill that runs two independent code review methodologies in parallel, validates the findings, and produces an aggregated summary.

## Why Use This?

- **Multiple perspectives** catch more issues than a single review
- **Validation phase** filters out false positives
- **Aggregated summary** shows agreement between reviewers
- **No auto-posting** - you control what gets posted to the PR

## Quick Start

```bash
# Review current PR
claude "Run parallel-pr-review"

# Review specific PR
claude "Run parallel-pr-review --pr 123"

# Review with higher confidence threshold
claude "Run parallel-pr-review --pr 123 --confidence 80"
```

## Prerequisites

Install the required plugins:

```
/plugins install code-review from claude-plugins-official
/plugins install pr-review-toolkit from claude-plugins-official
```

## How It Works

```
┌────────────────────────────────────────────────────────────────┐
│  Phase 0: Validate required skills exist                       │
└────────────────────────────────────────────────────────────────┘
                              ↓
┌────────────────────────────────────────────────────────────────┐
│  Phase 1: Run reviews in PARALLEL                              │
│  ┌─────────────────────┐     ┌─────────────────────┐           │
│  │ code-review:        │     │ pr-review-toolkit:  │           │
│  │ code-review         │     │ review-pr           │           │
│  └─────────────────────┘     └─────────────────────┘           │
└────────────────────────────────────────────────────────────────┘
                              ↓
┌────────────────────────────────────────────────────────────────┐
│  Phase 2: Validate findings in PARALLEL                        │
│  ┌─────────────────────┐     ┌─────────────────────┐           │
│  │ Validator 1         │     │ Validator 2         │           │
│  │ (filter false +)    │     │ (filter false +)    │           │
│  └─────────────────────┘     └─────────────────────┘           │
└────────────────────────────────────────────────────────────────┘
                              ↓
┌────────────────────────────────────────────────────────────────┐
│  Phase 3: Aggregate & deduplicate into final summary           │
└────────────────────────────────────────────────────────────────┘
                              ↓
┌────────────────────────────────────────────────────────────────┐
│  Post-review: Action menu (view, fix, create issues, etc.)     │
└────────────────────────────────────────────────────────────────┘
```

## Output Files

All results are saved to `.reviews/<timestamp>/`:

| File | Description |
|------|-------------|
| `review-code-review.md` | Raw findings from code-review skill |
| `review-pr-toolkit.md` | Raw findings from pr-review-toolkit skill |
| `validated-code-review.md` | Filtered findings (false positives removed) |
| `validated-pr-toolkit.md` | Filtered findings (false positives removed) |
| `pr-review-summary.md` | **Final aggregated report** |

## Options

### Input Options

| Option | Description |
|--------|-------------|
| `--pr <number>` | Review a specific PR |
| `--branch <name>` | Review branch changes vs main |
| `--files <paths>` | Review specific files only |
| `--full-context` | Review entire files, not just diff |

### Configuration

| Option | Default | Description |
|--------|---------|-------------|
| `--output-dir` | `./.reviews/` | Where to save results |
| `--confidence` | `70` | Minimum confidence to include (0-100) |
| `--skip-validation` | `false` | Skip Phase 2 for faster results |
| `--only <skill>` | both | Run only `code-review` or `pr-toolkit` |

## Examples

```bash
# Basic - auto-detects PR from current branch
claude "Run parallel-pr-review"

# Specific PR with custom output location
claude "Run parallel-pr-review --pr 456 --output-dir ./reviews"

# Higher confidence threshold (fewer but more certain issues)
claude "Run parallel-pr-review --confidence 85"

# Quick review - skip validation phase
claude "Run parallel-pr-review --skip-validation"

# Only run one reviewer
claude "Run parallel-pr-review --only code-review"

# Review specific files
claude "Run parallel-pr-review --files src/auth.ts src/login.ts"
```

## Understanding the Summary

The final `pr-review-summary.md` includes:

### Issue Categories

- **Critical Issues** - Must fix before merging
- **Important Issues** - Should fix
- **Suggestions** - Nice to have improvements

### Source Column

| Value | Meaning |
|-------|---------|
| `both` | Found by both reviewers (high confidence) |
| `code-review` | Only found by code-review skill |
| `pr-toolkit` | Only found by pr-review-toolkit skill |

### Agreement Analysis

Shows how much the two reviewers agreed:
- High agreement = high confidence in findings
- Issues found by both reviewers are more likely real

## Post-Review Actions

After the review completes, you'll see an action menu:

1. **View** - Open the summary
2. **Fix** - Generate fix suggestions for critical issues
3. **Issues** - Create GitHub issues for tracking
4. **Comment** - Post summary to PR (requires your approval)
5. **Rerun** - Re-run on specific files
6. **Done** - Exit

## FAQ

**Q: Will this post comments to my PR automatically?**
A: No. All output goes to markdown files. You decide what to post.

**Q: How long does it take?**
A: Depends on PR size. Phases 1 and 2 run in parallel, so it's faster than running sequentially.

**Q: Can I run just one reviewer?**
A: Yes, use `--only code-review` or `--only pr-toolkit`.

**Q: What if one reviewer fails?**
A: The skill continues with available results and warns you.

**Q: How do I adjust sensitivity?**
A: Use `--confidence`. Higher values (80-90) = fewer but more certain issues. Lower values (50-60) = more issues but more false positives.

## Files

```
~/.claude/skills/parallel-pr-review/
├── SKILL.md   # Instructions for Claude (technical)
└── README.md  # This file (human documentation)
```
