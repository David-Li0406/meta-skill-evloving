# Obsidian Markdown Reference

## Relevant Obsidian Syntax for Meeting Notes

This reference covers Obsidian-specific markdown syntax used in meeting notes.

### Internal Links (Wikilinks)

**Basic wikilink syntax:**
```markdown
[[Page Name]]                    # Link to another note
[[Page Name|Display Text]]       # Link with custom display text
[[Folder/Page Name]]            # Link to note in subfolder
```

**For meeting attendees, use the formal-to-casual link format:**
```markdown
[[Last, First|First Last]]
```

**Examples:**
- `[[Tronkowski, Kevin|Kevin Tronkowski]]` → Links to "Tronkowski, Kevin.md", displays as "Kevin Tronkowski"
- `[[Pahwa, Kashish|Kashish Pahwa]]` → Links to "Pahwa, Kashish.md", displays as "Kashish Pahwa"

**Why this format?**
- **File name**: `Last, First.md` - Handles duplicate first names, sorts alphabetically
- **Display name**: `First Last` - Natural reading in meeting notes
- **Link syntax**: `[[filename|display text]]`

### Images and Embeds

**Embedding images:**
```markdown
![[image.png]]                   # Embed local image
![[SCR-20260108-abcd.png]]      # Screenshot reference
```

**Note:** In meeting processing workflow, image references are removed after extracting attendees.

### Frontmatter (YAML metadata)

**Meeting note metadata:**
```yaml
---
when: 2026-01-08
tags:
  - meeting
---
```

### Lists

**Attendee lists with counts:**
```markdown
## In Meeting (5)
- [[Person, Name|Name Person]]
- [[Another, Person|Person Another]]

## Invited/Other Participants (3)
- [[Smith, John|John Smith]]
```

### Text Formatting

```markdown
**bold text**                    # Bold
*italic text*                    # Italic
***bold and italic***            # Both
~~strikethrough~~                # Strikethrough
`inline code`                    # Inline code
```

### Headings

```markdown
# H1 Heading                     # Top level
## H2 Heading                    # Section
### H3 Heading                   # Subsection
```

**Meeting note structure:**
- `# Attendees` - Top level
- `## In Meeting (X)` - Section with count
- `# Subject` - Top level
- `# Notes` - Top level
- `## Meeting Purpose` - Section
- `### Topic Area` - Subsection
- `## Transcript` - Section

### Code Blocks

```markdown
```bash
command here
` ` `

```python
code here
` ` `
```

(Note: backticks shown with spaces for display; remove spaces in actual use)

### Blockquotes

```markdown
> This is a blockquote
> Multiple lines
```

### Horizontal Rules

```markdown
---
***
___
```

### Tables

```markdown
| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
| Cell 3   | Cell 4   |
```

## Meeting Note Best Practices

### Attendee Section
- Use `## In Meeting (X)` and `## Invited/Other Participants (Y)` with counts
- Link all attendees using `[[Last, First|First Last]]` format
- Remove screenshot references after extracting attendees

### Transcript Section
- Use `## Transcript` (not `# Transcript`)
- Format speakers as: `**[[Last, First|First Last]]** timestamp`
- Include blank line between speakers
- No images or metadata in cleaned transcript

### Notes Section
- Use structured headings: `## Meeting Purpose`, `### Topic Area`
- Use bullet points with bold keywords for scanability
- Link to People profiles when mentioning team members

### Links and References
- Always use proper wikilink syntax for internal references
- External links: `[Display Text](https://url)`
- Jira tickets: Include both title reference and clickable link
