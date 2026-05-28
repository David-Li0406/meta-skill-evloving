---
name: ship
description: Quick commit and push workflow. Ship changes to remote with zero friction.
disable-model-invocation: true
allowed-tools: Bash
---

# /ship - Quick Commit & Push

Ship changes to remote. Zero-friction git workflow.

## Usage

```
/ship              # Ship current repo
/ship --dry        # Show what would be shipped (no commit)
```

## Workflow

### 1. Check Status
```bash
git status --short
```

### 2. If Changes Exist
```bash
# Stage all
git add -A

# Commit with auto-generated message
git commit -m "$(cat <<'EOF'
<type>: <summary>

Generated with Atlas Configurator

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"

# Push
git push origin main
```

### 3. Output Summary
Show results in formatted summary.

## Commit Type Detection

| Files Changed | Type |
|---------------|------|
| `*.md` in docs/ | `docs:` |
| `*.ts`, `*.js` | `feat:` or `fix:` |
| Config files | `chore:` |

## Safety Rules

1. **Never force push**
2. **Skip sensitive files** - `.env*`, `credentials*`, `secrets*`
3. **Warn on large commits** - If >50 files, ask confirmation
4. **Pre-commit hooks respected**
