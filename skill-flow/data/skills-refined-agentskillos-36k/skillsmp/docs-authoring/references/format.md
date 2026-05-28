# File Format

## Supported Formats

| Format   | Extension | Use case                            |
| -------- | --------- | ----------------------------------- |
| Markdown | `.md`     | Simple content without components   |
| MDX      | `.mdx`    | Content with React/Astro components |
| Markdoc  | `.mdoc`   | Content with custom Markdoc tags    |

Prefer `.mdx` for new documentation as it supports the full component library.

## Frontmatter

Every documentation file needs YAML frontmatter:

```yaml
---
title: Page Title
description: Optional description for SEO and link previews
---
```

## Code Blocks

Use fenced code blocks with language identifiers:

```tql
from events
where severity > 3
select timestamp, message
```

Common language identifiers:

- `tql` - Tenzir Query Language
- `sh` - Shell commands
- `json` - JSON data
- `yaml` - YAML configuration

### Adjacent TQL Code Blocks

Adjacent TQL code blocks merge visually in the rendered docs. Use this to show
input/output pairs:

```tql
from {x: 1}
where x > 0
```

```tql
{x: 1}
```

The two blocks render as a single merged block, making it clear that the second
block is the output of the first.
