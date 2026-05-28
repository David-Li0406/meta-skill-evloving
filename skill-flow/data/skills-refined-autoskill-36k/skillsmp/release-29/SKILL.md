---
name: release
description: Bumps version and creates git tag for release
disable-model-invocation: true
argument-hint: "[version-number]"
---

# Version Management

Version is stored in `recent_state_summarizer/__init__.py` as `__version__` and referenced by `pyproject.toml` using setuptools dynamic versioning.

## Bumping Version

Follow these steps to bump the version:

```bash
# 1. Edit version in recent_state_summarizer/__init__.py
# 2. Commit and tag
git add recent_state_summarizer/__init__.py
git commit -m "chore: Bump up X.Y.Z"
git tag vX.Y.Z
git push origin main --tags
```

## Instructions

**Prerequisites:**
- This must be executed on the `main` branch
- All feature branches should be merged into `main` before running this command
- Check current branch with `git branch --show-current` before proceeding

If the user provided a version number (e.g., `/release 0.1.0`), use that. Otherwise:
1. Read the current version from `recent_state_summarizer/__init__.py`
2. Parse the version number (format: MAJOR.MINOR.PATCH)
3. Increment the PATCH number by 1
4. Use the new version (e.g., `0.0.9` → `0.0.10`)

Execute the steps above, replacing X.Y.Z with the specified or auto-incremented version.

After creating the commit and tag, use AskUserQuestion to ask whether to push to remote:
- Question: "リモートにプッシュしますか？"
- Option 1: "今すぐプッシュする" → Execute `git push origin main --tags`
- Option 2: "後でやる" → Skip push and remind the user they can run `git push origin main --tags` manually later
