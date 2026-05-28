---
name: morph-apply
description: Use this skill for fast file editing via the Morph Apply API, especially when dealing with large files where reading the entire content would be inefficient.
---

# Morph Fast Apply

Fast, AI-powered file editing using the Morph Apply API. Edit files without reading them first. Processes at 10,500 tokens/sec with 98% accuracy.

## When to Use

- Fast file edits without reading the entire file first
- Batch edits to a file (multiple changes in one operation)
- When you know what to change but the file is large
- Large files where reading would consume too many tokens

## Key Pattern: Code Markers

Use `// ... existing code ...` (or language-appropriate comments) to mark where edits go:

```python
# ... existing code ...
try:
    result = process()
except Exception as e:
    log.error(e)
# ... existing code ...
```

The API intelligently places your edit in the right location.

## Usage

### Add error handling
```bash
uv run python -m runtime.harness scripts/morph_apply.py \
    --file "src/auth.py" \
    --instruction "Add error handling to login function" \
    --code_edit "# ... existing code ...
try:
    user = authenticate(credentials)
except AuthError as e:
    log.error(f'Auth failed: {e}')
    raise
# ... existing code ..."
```

### Add logging
```bash
uv run python -m runtime.harness scripts/morph_apply.py \
    --file "src/api.py" \
    --instruction "Add debug logging" \
    --code_edit "# ... existing code ...
logger.debug(f'Processing request: {request.id}')
# ... existing code ..."
```

### TypeScript example
```bash
uv run python -m runtime.harness scripts/morph_apply.py \
    --file "src/types.ts" \
    --instruction "Add user validation" \
    --code_edit "// ... existing code ...
if (!user) throw new Error('User not found');
if (!user.isActive) throw new Error('User inactive');
// ... existing code ..."
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| `--file` | File path to edit (required) |
| `--instruction` | Human description of the change (required) |
| `--code_edit` | Code snippet with markers showing where to place edit (required) |

## vs Claude's Edit Tool

| Tool | Best For |
|------|----------|
| **morph-apply** | Fast edits, don't need to read file first, large files, batch edits |
| **Claude Edit** | Small precise edits when the file is already in context |

**Use morph-apply when:**
- The file is not in context and reading it would be expensive
- The file is very large (>500 lines)
- Making multiple related edits at once
- You know the context of the changes needed