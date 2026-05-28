---
name: code-stats
description: Analyze codebase statistics with tokei (line counts by language) and difft (semantic AST-aware diffs). Use for project composition, refactoring scope, codebase metrics.
triggers: code statistics, line count, language breakdown, semantic diff, tokei, difft, codebase metrics, project size
---

# Code Statistics

Rapid codebase analysis using two complementary tools.

## Tools

### tokei - Language Statistics

Line-count statistics across programming languages:
- File count per language
- Total lines, code lines, comments, blank lines
- Supports 150+ languages

**Usage:**
```bash
tokei                                    # Full project stats
tokei --type=TypeScript,JavaScript       # Filter by language
tokei --exclude="vendor/*"               # Exclude patterns
tokei -o json                            # JSON output for automation
```

### difft - Semantic Diffs

AST-aware diffing that understands code structure:
- Ignores formatting changes
- Recognizes code moves and refactoring
- Shows meaningful changes, not line shuffles

**Usage:**
```bash
difft file1.go file2.go                  # Compare two files
GIT_EXTERNAL_DIFF=difft git diff         # Git integration
GIT_EXTERNAL_DIFF=difft git show HEAD    # Show last commit
GIT_EXTERNAL_DIFF=difft git log -p       # Log with semantic diffs
```

## Workflow

1. **Quick snapshot**: `tokei` for project composition
2. **Deep analysis**: `tokei -o json | jq` for automation
3. **Review changes**: `GIT_EXTERNAL_DIFF=difft git diff` for meaningful diffs

## MUST DO

- Use `tokei` before estimating project scope
- Use `difft` for refactoring reviews
- Filter output when only specific languages matter

## MUST NOT

- Rely on raw line counts for complexity estimates
- Ignore comment ratios in health assessments

## Advanced Features

- **tokei advanced**: See `references/tokei-advanced.md` for filtering, automation, CI patterns
- **difft advanced**: See `references/difft-advanced.md` for git integration, display modes, config
