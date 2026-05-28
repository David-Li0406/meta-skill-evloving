---
name: commit
description: Runs tests (if source changed), commits all changes, and pushes. Use when ready to commit and push code.
allowed-tools: Bash(git:*), Bash(pytest:*)
---

# Commit and Push

When invoked, execute these steps automatically:

## 1. Check what changed
```bash
git status
git diff --stat
```

## 2. Run tests (only if source files changed)
- If `.py` files in `src/` changed: run `pytest`
- If only docs/markdown/config changed: skip tests
- If tests fail: STOP and report the failure

## 3. Analyze the diff
```bash
git diff
```

## 4. Craft commit message
Project style:
- Very short (3-8 words)
- Lowercase
- Action verbs: `add`, `fix`, `rename`, `extract`, `remove`, `update`
- No period at end
- Examples: `extract calculate_discount method`, `add test for premium discount`, `fmt`

## 5. Commit and push
```bash
git add -A
git commit -m "generated message"
git push
```

## Output
Report:
- ✅ Tests passed (or skipped)
- ✅ Committed: "message"
- ✅ Pushed

If tests fail:
- ❌ Tests failed: [test name and error]
- Do not commit or push
