# Storing Content

Store reusable content—writing or code—into the content bank for future use.

## Workflow

1. **Identify** content suitable for reuse (user-selected or detected)
2. **Classify** as writing or code
3. **Propose** 1–3 topic options and wait for user confirmation
4. **Categorize** as idea, snippet, or outline
5. **Append** entry to the appropriate file with full metadata
6. **Update** `topics.md` if adding a new topic

> Note: Auto-initialization runs before any operation if the content bank doesn't exist (see SKILL.md).

## Entry Format

### Writing Content

```markdown
### {Title}
- **Type**: writing
- **Source**: {draft file path or "original"}
- **Why useful**: {one sentence on reuse value}
- **Tags**: {comma-separated keywords}
- **Content**:
  > {the actual text}
```

### Code Content

```markdown
### {Title}
- **Type**: code
- **Language**: {programming language}
- **Source**: {file path or "legacy"}
- **Why useful**: {one sentence on reuse value}
- **Tags**: {comma-separated keywords}
- **Content**:
  ```{language}
  {the actual code}
  ```
```

## Topic Inference

When banking content:
1. Analyze the content to infer likely topics
2. Propose 1–3 topic options to the user
3. Allow override or creation of a new topic
4. Use kebab-case for topic folder names (e.g., `developer-productivity`, `error-handling`)

Always confirm before banking—never auto-bank without user approval.
