---
name: preview-markdown
description: Open a markdown file in Marked for preview. Use when asked to preview markdown or "open in Marked".
---

# Preview Markdown

Open a markdown file in Marked for preview.

## Triggers

- `/preview <file-path>` - explicit invocation
- Natural language: "open in Marked", "preview in Marked", "show me in Marked"

## Instructions

When the user asks to preview a markdown file in Marked (either via `/preview` or natural language like "open the file in Marked"), run:

```bash
open -a "Marked" "<file-path>"
```

If the file path is relative, resolve it against the current working directory.

If no file path is provided and you just edited a markdown file, use that file.
