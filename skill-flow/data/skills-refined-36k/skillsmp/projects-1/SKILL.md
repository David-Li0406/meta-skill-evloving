---
name: projects
description: This skill should be used when managing portfolio projects - adding new projects, editing existing ones, or removing projects. It provides an interactive workflow starting with listing existing projects.
---

# Projects

## Overview

Manage project pages for the portfolio website. Projects are MDX files in `src/content/projects/` that are automatically discovered and displayed on the `/projects` page.

## Workflow

### Step 1: List Existing Projects

Run the script to get a compact summary of all projects:

```bash
python3 .claude/skills/projects/scripts/read_projects.py list
```

This outputs a token-efficient summary. Other commands:

```bash
python3 .claude/skills/projects/scripts/read_projects.py json          # Full JSON data
python3 .claude/skills/projects/scripts/read_projects.py detail <slug> # Single project details
python3 .claude/skills/projects/scripts/read_projects.py slugs         # Just slug names
```

### Step 2: Present Options

Use the `AskUserQuestion` tool to ask the user what they want to do with selectable options:

- **Add** - Create a new project
- **Edit** - Modify an existing project
- **Delete** - Remove a project

---

## Add Project

1. Gather project information:
   - Title, description, tags, featured status, content

2. Generate slug from title:
   - Lowercase, replace spaces with hyphens, remove special characters

3. Create MDX file at `src/content/projects/{slug}.mdx`:
   - YAML frontmatter (see `references/frontmatter-schema.md`)
   - Content body with h2/h3 headings for TOC

---

## Edit Project

1. Ask which project to edit (by number or slug from script output)

2. Read the existing MDX file

3. Ask what to modify:
   - Frontmatter fields (title, description, tags, etc.)
   - Content body

4. Apply changes and save the file

5. Optionally update the slug (rename file) if title changed significantly

---

## Delete Project

1. Ask which project to delete (by number or slug)

2. Confirm deletion with the user

3. Remove the MDX file from `src/content/projects/`

---

## Content Guidelines

- Use `## Heading` (h2) and `### Subheading` (h3) for table of contents
- Include code examples with syntax highlighting
- Keep content focused and well-organized

## Resources

### scripts/

- `read_projects.py` - Parses MDX files and outputs compact summary

### references/

- `frontmatter-schema.md` - Complete frontmatter schema with required/optional fields
