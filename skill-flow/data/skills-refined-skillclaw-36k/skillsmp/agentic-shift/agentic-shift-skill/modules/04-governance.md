# Module 4: Governance (Optional)

## Learning Objectives

By the end of this module, learners will:
- Understand the value of automated quality gates
- Install pre-commit hooks for basic security checks
- Know how to extend hooks for their team's needs

> **Note**: This module is optional. Start with Modules 1-3 first. Add governance once your team is comfortable with the core workflow.

## Why Git Hooks?

Git hooks catch issues before they reach code review:

```
Commit → Pre-commit hook (fast) → Push → Pre-push hook (thorough) → Remote
```

**Benefits:**
- Catch secrets before they're committed
- Enforce consistent standards
- Reduce code review burden

## Quick Start: Pre-Commit Hook

### Step 1: Copy the Template

```bash
# From your project root
cp path/to/agentic-shift-skill/templates/pre-commit.template .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

### Step 2: Test It

Create a file with a fake secret:
```bash
echo 'API_KEY = "sk-test1234567890"' > test-secret.js
git add test-secret.js
git commit -m "test"  # Should be blocked!
```

### Step 3: Clean Up

```bash
git reset HEAD test-secret.js
rm test-secret.js
```

## What the Hooks Check

### Pre-Commit (Fast)
- Hardcoded secrets and API keys
- Common credential patterns
- Large files

### Pre-Push (Thorough, Optional)
- OWASP security patterns
- Code style issues
- Requires Claude CLI

## Team-Wide Deployment

### Option 1: Committed Hooks

```bash
# Store hooks in repo
mkdir .githooks
cp .git/hooks/pre-commit .githooks/
git add .githooks/

# Team members run once:
git config core.hooksPath .githooks
```

### Option 2: Use Existing Tools

- **JavaScript**: [husky](https://typicode.github.io/husky/)
- **Python**: [pre-commit](https://pre-commit.com/)

## Customization

Edit the hook templates to match your team's needs:
- Add/remove secret patterns
- Adjust severity levels
- Add project-specific checks

## Checkpoint

Module 4 is complete when:
- [ ] Pre-commit hook is installed and working
- [ ] You've verified it catches a test violation

## Next

Final module: **Module 5: Skill Creation** - capture your team's patterns as reusable skills.

Type "next" or run `/onboard-skills` to continue.
