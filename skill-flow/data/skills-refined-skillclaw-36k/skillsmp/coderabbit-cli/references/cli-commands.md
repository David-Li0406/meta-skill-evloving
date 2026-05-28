# CodeRabbit CLI Command Reference

Complete reference for CodeRabbit CLI commands used in AI agent workflows.

## Review Commands

### Basic Review

```bash
# Review all uncommitted changes
coderabbit review

# Review with plain text output (detailed feedback)
coderabbit review --plain

# Review with prompt-only output (token-efficient)
coderabbit review --prompt-only
```

### File-Specific Review

```bash
# Review specific files
coderabbit review --files path/to/file1.ts path/to/file2.tsx

# Review files matching pattern
coderabbit review --files "apps/**/*.tsx"
```

### Review Options

```bash
# Review staged changes only
git add .
coderabbit review

# Review with custom base branch
coderabbit review --base main

# Review with custom context
coderabbit review --context "Implementing feature X"
```

## Authentication

```bash
# Login to CodeRabbit
coderabbit auth login

# Check authentication status
coderabbit auth status

# Logout
coderabbit auth logout
```

## Configuration

CodeRabbit reads configuration from `.coderabbit.yaml` in the repository root.

### Example Configuration

```yaml
# .coderabbit.yaml
language: "en-US"

reviews:
  # Suppress auto-generated review status comments
  review_status: false
  
  # Configure pre-merge checks
  pre_merge_checks:
    # Disable docstring coverage for TypeScript repos
    docstrings:
      mode: "off"
    
    # Configure other checks
    # security:
    #   mode: "on"
    #   threshold: "high"
```

### Configuration Options

- `language`: Review language (default: "en-US")
- `reviews.review_status`: Show/hide review status comments
- `reviews.pre_merge_checks`: Configure pre-merge quality gates
  - `docstrings`: Docstring coverage checks
  - `security`: Security vulnerability checks
  - `complexity`: Code complexity checks

See [CodeRabbit Configuration Docs](https://docs.coderabbit.ai/configuration) for complete options.

## Output Formats

### Plain Text (`--plain`)

Detailed feedback with:
- File-by-file review comments
- Line-specific suggestions
- Code examples
- Explanation of issues

Best for: Active development, comprehensive feedback

### Prompt-Only (`--prompt-only`)

Token-efficient summary with:
- High-level feedback summary
- Key issues only
- Actionable suggestions

Best for: Token-constrained environments, quick checks

## Common Workflows

### Pre-Commit Review

```bash
# Stage changes
git add .

# Run review
coderabbit review --plain

# Fix issues, then commit
git commit -m "feat: implement feature"
```

### Iterative Improvement Loop

```bash
# Initial review
coderabbit review --plain

# Make fixes based on feedback
# ... edit files ...

# Re-review to validate
coderabbit review --plain
```

### Focused File Review

```bash
# Review only changed files in specific directory
coderabbit review --files apps/ralph-monitoring/app/routes/**/*.tsx
```

## Error Handling

### Common Issues

**Not authenticated:**
```bash
coderabbit auth login
```

**No changes to review:**
```bash
# Stage or make changes first
git add .
# or make code changes
```

**Repository not found:**
```bash
# Ensure you're in a git repository
git status
```

## Integration Examples

### With Git Hooks

Add to `.git/hooks/pre-commit`:
```bash
#!/bin/bash
coderabbit review --prompt-only || exit 1
```

### With CI/CD

```yaml
# .github/workflows/review.yml
- name: CodeRabbit Review
  run: coderabbit review --plain
```

## See Also

- [CodeRabbit CLI Documentation](https://docs.coderabbit.ai/cli)
- [CodeRabbit Configuration](https://docs.coderabbit.ai/configuration)
- [CodeRabbit Review Guidelines](https://docs.coderabbit.ai/reviews)
