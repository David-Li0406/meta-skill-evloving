---
name: history-chain
description: Maintain linked history entries in history.md. Use after any state change to record what changed and why.
---

# History Chain

## When to use this skill

- After every state.md modification
- Recording stage transitions
- Documenting contact updates
- Linking changes to source evidence

## Entry format

Each entry follows this structure:

```markdown
## {ISO Timestamp}

{Summary of what changed and why}

- **{Field}**: {Old Value} → {New Value}
- **Evidence**: [{source_file}]({relative_path})

---
```

## Example entry

```markdown
## 2025-01-15T14:30:00Z

Stage updated to Quote Pitched after presenting carrier options in call.

- **Stage**: Application Received → Quote Pitched
- **Evidence**: [call_150734](sources/calls/call_150734/raw.txt)

---
```

## Linking rules

1. **Newest first**: Prepend new entries after the `# Change History` header
2. **Evidence links**: Always link to the source that triggered the change
3. **Relative paths**: Use paths relative to account directory
4. **Separator**: End each entry with `---`

## See also

Reference `references/format-examples.md` for more entry examples.
