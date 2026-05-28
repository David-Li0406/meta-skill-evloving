# Daily Journal Format

## Location

Daily notes are stored at: `~/Documents/2026/Journal/Daily/YYYY-MM-DD.md`

Example: `2026-01-10.md` for January 10th, 2026

## Daily Note Structure

```yaml
---
tags:
  - daily
hit study goal:
---

- Activity 1
- Activity 2
- ...
```

## Adding a Study Entry

Append a bullet point summarizing the study session, including flashcards added:

```
- Studied [[Reference filename]] - [topic summary], added N cards on [topics]
```

Examples:
- `- Studied [[SICP-Abelson-2007.pdf]] - Chapter 1.2, added 4 cards on recursion and iteration`
- `- Studied [[LISP-McCarthy-1960.pdf]] - S-expressions, added 6 cards on car/cdr and list structure`
- `- Studied [[recursion-notes.md]] - tail recursion (no cards added)`

Use Obsidian wiki-links (`[[filename]]`) to link to the reference material.

## Entry Components

1. **Reference** - Wiki-link to the studied material
2. **Topic** - Chapter, section, or main subject
3. **Card count** - How many flashcards were accepted (if any)
4. **Card topics** - Brief list of what the cards cover

If no flashcards were added, note that: `(no cards added)` or `(review only)`

## If Daily Note Doesn't Exist

Create a new file with the template:

```yaml
---
tags:
  - daily
hit study goal:
---

- Studied [[Reference filename]] - [topic], added N cards on [topics]
```

## Tips

- Keep entries brief - one line per study session
- Use wiki-links to References for easy navigation
- Include chapter/section if applicable
- Round card count (no need to be exact)
- Group card topics briefly (e.g., "recursion and special forms" not listing each card)
