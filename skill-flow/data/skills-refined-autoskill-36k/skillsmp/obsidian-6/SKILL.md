---
name: obsidian
description: Save a document to the Obsidian vault. Use when the user asks to save notes, summaries, or documents to Obsidian or "Notater".
---

# Obsidian

Save AI-generated documents to the Obsidian vault at `~/Notater/Øystein/`.

## Instructions

1. **Determine filename**
   - Ask the user for a filename if not obvious from context
   - Use descriptive names in Norwegian
   - Use `.md` extension

2. **Format the document**
   - Add YAML frontmatter with tags
   - Include `#ai-generert` and `#bleikøya` tags
   - Add creation date
   - Keep the content in markdown format

3. **Write the file**
   - Save to `/Users/gunderwonder/Notater/Øystein/`
   - Use the Write tool

4. **Confirm to user**
   - Show the full path where the file was saved

## Template

```markdown
---
tags:
  - ai-generert
  - bleikøya
date: YYYY-MM-DD
---

# Title

Content here...
```

## Example

If the user says "lagre dette i Obsidian" after generating a summary:

```markdown
---
tags:
  - ai-generert
  - bleikøya
date: 2025-12-27
---

# Sammendrag av styremøte

Her er innholdet...
```

Saved to: `~/Notater/Øystein/Sammendrag av styremøte.md`
