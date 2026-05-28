---
name: opensrc
description: Fetch npm package source code for implementation analysis. Use when types/docs aren't enough and you need to understand HOW a library works internally.
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---

# opensrc

Fetch npm package source code locally when you need to understand implementation details.

## When to Use

- Debugging unexpected library behavior
- Understanding internal patterns before extending a library
- Types/docs are insufficient

## Commands

```bash
# Fetch package(s)
npx opensrc <package>
npx opensrc ai zod @anthropic-ai/sdk

# Check what's fetched
cat opensrc/sources.json

# Clean up when done
rm -rf opensrc/<package>
```

## Exploration Pattern

```bash
# 1. Fetch
npx opensrc ai

# 2. Check structure (many are monorepos)
ls opensrc/ai/packages/

# 3. Find what you need
grep -r "functionName" opensrc/ai/src/

# 4. Read the implementation
# (use Read tool)

# 5. Clean up
rm -rf opensrc/ai
```

## Tips

- **Check `sources.json` first** - don't re-fetch what's already there
- **Target specific files** - don't read entire packages
- **Monorepos**: Check `packages/` directory for subpackages
- **Clean up** - source code takes disk space, remove when done

## Common Packages

| Package | Structure |
|---------|-----------|
| `ai` | Monorepo: `packages/anthropic/`, `packages/openai/`, etc. |
| `@anthropic-ai/sdk` | Single package: `src/` |
| `zod` | Single package: `src/types/` |
