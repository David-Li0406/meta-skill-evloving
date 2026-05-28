---
name: obsidian-vault
description: Manage the Obsidian vault at ~/dev/personal/obsidian/trobrock - create, edit, and organize personal notes, projects, and travel plans
---

# Obsidian Vault Management

This skill teaches goose how to effectively manage the Obsidian vault located at `~/dev/personal/obsidian/trobrock`.

## Vault Structure

```
~/dev/personal/obsidian/trobrock/
├── Personal Home.md      # Dashboard with goals and quick links
├── Projects/             # Side projects and business ideas
├── Travel/               # Trip planning and travel notes
├── Notes.md              # Scratch pad for quick notes and links
├── Quotes.md             # Inspirational quotes
├── Stuff I want.md       # Wishlist items
└── .obsidian/            # Obsidian config (don't modify)
```

## File Conventions

### Wiki Links
Always use Obsidian wiki-link syntax for internal links:
- `[[Page Name]]` - Link to a page
- `[[Page Name|Display Text]]` - Link with custom display text
- `[[Page Name#Heading]]` - Link to a specific section

### Frontmatter
Use YAML frontmatter at the top of notes for metadata. Always use `---` delimiters.

## Creating Notes by Type

### Projects (in `Projects/` folder)

```markdown
---
status: Idea | Active | Paused | Discontinued
tech_stack:
  - Rails
  - Ruby
  - Postgres
hosting:
  - Digitalocean
url: ""
---

# Project Name

Description and notes about the project.
```

**Status values:**
- `Idea` - Just a concept, not started
- `Active` - Currently being worked on
- `Paused` - On hold but may resume
- `Discontinued` - No longer being worked on

### Travel Plans (in `Travel/` folder)

```markdown
---
status: Planning | Booked | Done
purpose: Personal | Business
date_start: YYYY-MM-DD
date_end: YYYY-MM-DD
url: ""
---

# Trip Name

## Trip Overview
Brief description of the trip.

## To Do
- [ ] Task 1
- [ ] Task 2

## Flights
Flight details here.

## Accommodations
Hotel/lodging info.

## Itinerary
Day-by-day plans.
```

### Quick Notes (add to `Notes.md`)

For quick thoughts or links, append to `Notes.md` under the appropriate section:
- **"Jot down some text"** - Freeform notes and ideas
- **"Make a to-do list"** - Tasks
- **"Create sub-pages"** - Links to new detailed pages
- **"Embed links"** - External resources and bookmarks

### Standalone Pages

For new top-level notes, create in the root `~/dev/personal/obsidian/trobrock/` directory with a descriptive name.

## Editing Guidelines

1. **Preserve frontmatter** - When editing, always keep the YAML frontmatter intact
2. **Use Markdown** - Standard Markdown with Obsidian extensions (wiki links, callouts)
3. **Checkboxes** - Use `- [ ]` for incomplete and `- [x]` for complete tasks
4. **Tables** - Use Markdown tables for structured data
5. **Emoji** - Emoji are welcomed for visual organization (see Personal Home.md)

## Common Tasks

### Update Personal Home Dashboard
The `Personal Home.md` file contains yearly goals and quick links. Update goals and progress here.

### Add a New Project Idea
1. Create a new file in `Projects/` with the project name
2. Use the Project frontmatter template
3. Set status to `Idea`

### Plan a New Trip
1. Create a new file in `Travel/` with the trip name
2. Use the Travel frontmatter template  
3. Set status to `Planning`
4. Fill in dates, to-dos, and itinerary as known

### Add a Quick Bookmark/Link
1. Open `Notes.md`
2. Add under "Embed links" section: `- [[Link Title]]`
3. Create the linked page with the URL and notes

## Verification

After creating or editing notes:
- [ ] Frontmatter is valid YAML (no syntax errors)
- [ ] Wiki links use double brackets `[[]]`
- [ ] Dates are in YYYY-MM-DD format
- [ ] Files are in the correct folder (Projects/, Travel/, or root)
