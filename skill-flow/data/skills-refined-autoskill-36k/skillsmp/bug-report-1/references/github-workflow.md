# GitHub Workflow Reference

## Creating Issues

### Using `gh` CLI

List existing issues:
```bash
gh issue list
```

Create a new issue:
```bash
gh issue create --title "Bug: ..." --body "Description..."
```

The command will output the issue URL and number (e.g., `#123`).

### Issue Title Format

Use format: `Bug: [Component] - [Brief description]`

Examples:
- `Bug: Calculator - Negative input not handled correctly`
- `Bug: Config Loader - YAML variant merging missing fields`
- `Bug: API endpoint - Returns incorrect tax breakdown`

### Issue Body Format

Include key sections:

```
## Description
Brief explanation of the bug.

## Reproduction Steps
1. ...
2. ...
3. ...

## Expected Behavior
What should happen.

## Actual Behavior
What actually happens.

## Additional Context
- Environment details if relevant
- Related issues if applicable
```

## Committing with Issue Reference

Use the issue number in commit message:

```bash
git commit -m "fix: [description] (fixes #123)"
```

The `fixes #123` syntax automatically closes the issue when commit is merged.

Other keywords:
- `closes #123`
- `resolves #123`
- `ref #123` (just references, doesn't close)

Example full commit:
```bash
git commit -m "fix: validate gross_annual before calculation (fixes #123)

The calculation engine was not validating positive values. Added
validation at the API boundary to reject negative gross income."
```

## Verifying Issue Creation

```bash
# Check the issue was created
gh issue view <number>

# View issue in browser
gh issue view <number> --web
```

## Linking Issues in Commits

If issue already created, reference it in commit:

```bash
git commit -m "fix: handle null values gracefully

This fixes the issue described in #123 where undefined inputs
were causing the calculator to crash."
```

The `#123` format will be recognized as a reference.
