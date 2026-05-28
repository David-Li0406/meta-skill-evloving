# Input Schema (User-Provided)

Collect the following fields from the user before creating a permanent note.

## Required

- `title` (string)
- `summary` (string, 1–2 lines)
- `domain` (enum): `work` | `learning`
- `kind` (enum): `hub` | `leaf` | `howto` | `principle` | `decision` | `glossary`

## Optional

- `topics` (list[string]) — keep <= 3 items, e.g. `backend`, `sql`, `aws`
- `status` (enum): `seed` | `draft` | `evergreen` | `deprecated` (default: `seed`)
- `related` (list[string]) — wiki links like `[[Some Note]]`
- `aliases` (list[string]) — alternative titles
- `content` (string) — body content or bullets to include
- `targetFolder` (enum): `00_inbox` | `10_hub` | `20_leaf` | `30_glossary` | `90_meta`

## Tag Encoding Rule

Write tags in frontmatter as strings without `#`, using these prefixes:

- domain: `d/work` or `d/learning`
- topics: `t/<topic>`
- kind: `k/<kind>`
- status: `s/<status>`

Example:

```yaml
tags: [d/work, t/sql, k/howto, s/draft]
```
