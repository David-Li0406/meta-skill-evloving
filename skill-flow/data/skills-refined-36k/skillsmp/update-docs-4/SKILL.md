---
name: update-docs
description: Updates project documentation. Use when adding pages, updating content, restructuring navigation, or maintaining the documentation site.
allowed-tools: Read, Glob, Grep, Write, Edit
---

# Updating Project Documentation

## Documentation Location

Documentation is typically located in a `docs/` folder within the project or in a separate documentation repository.

## Workflow

### 1. Understand what exists

List all documentation pages and check current structure.

### 2. Create or update pages

**Page frontmatter format (for MDX/Markdown):**
```mdx
---
title: 'Page Title'
description: 'Brief description for SEO and previews'
---
```

### 3. Update navigation

If using a documentation framework (Mintlify, Docusaurus, etc.), update the navigation configuration.

### 4. Validate changes

Test documentation locally if a dev server is available.

### 5. Present summary to user

After completing the documentation updates, present a summary to the user that includes:
- List of files created or modified
- Navigation changes made
- Any new pages added and their location
- Suggested next steps (e.g., review locally, deploy)

## Best Practices

- Keep pages focused on a single topic
- Include practical examples where helpful
- Use consistent heading hierarchy (one H1 via title, then H2+)
- Add new pages to navigation
- Test locally before finalizing

## File Naming

- Use lowercase with hyphens: `my-new-page.md`
- Place in appropriate folder structure
- Match the path in navigation configuration

## Creating New Pages

1. Create the `.md` or `.mdx` file with frontmatter
2. Add content
3. Update navigation to include the new page
4. Test locally
