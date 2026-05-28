---
name: update-docs
description: Updates Video Story Agent documentation using Mintlify. Use when adding pages, updating content, restructuring navigation, or maintaining the documentation site.
allowed-tools: Read, Glob, Grep, Write, Edit, Bash(mint:*)
---

# Updating Video Story Agent Documentation

## Documentation Location

The documentation is in a **separate repository**:
- **Path**: `/Users/roelandhofkens/Projects/Ai/video-story-creator-docs/`
- **Config**: `docs.json` - navigation, theme, colors, metadata
- **Pages**: `.mdx` files in root and subdirectories
- **Assets**: `/images/`, `/logo/`

Always work in the docs directory when updating documentation.

## Current Navigation Structure

```
Documentation tab:
├── Get Started (introduction, quickstart)
└── Concepts (overview, organizations, projects, assets, scenes, workflow)

Guides tab:
└── Guides (creating-first-project, uploading-assets, generating-narrative, generating-videos, brand-kit-setup)
```

## Workflow

### 1. Understand what exists
```bash
# List all documentation pages
find /Users/roelandhofkens/Projects/Ai/video-story-creator-docs -name "*.mdx" -o -name "*.md" | grep -v node_modules

# Check current navigation
cat /Users/roelandhofkens/Projects/Ai/video-story-creator-docs/docs.json | jq '.navigation'
```

### 2. Create or update pages

**Page frontmatter format:**
```mdx
---
title: 'Page Title'
description: 'Brief description for SEO and previews'
---
```

**Common components:**
- `<CardGroup cols={2}>` - Grid of cards
- `<Card title="" icon="" href="">` - Navigation card
- `<Steps>` / `<Step title="">` - Step-by-step instructions
- `<Tip>`, `<Note>`, `<Warning>` - Callout boxes
- `<Accordion>` / `<AccordionGroup>` - Collapsible content

### 3. Update navigation in docs.json

Navigation structure:
```json
{
  "navigation": {
    "tabs": [
      {
        "tab": "Tab Name",
        "groups": [
          {
            "group": "Group Name",
            "pages": ["page-path", "folder/page-path"]
          }
        ]
      }
    ]
  }
}
```

### 4. Validate changes
```bash
# Run local dev server (from docs directory)
cd /Users/roelandhofkens/Projects/Ai/video-story-creator-docs && mint dev
```

### 5. Present summary to user

After completing the documentation updates, present a summary to the user that includes:
- List of files created or modified
- Navigation changes made to `docs.json`
- Any new pages added and their location in the navigation
- Suggested next steps (e.g., review locally with `mint dev`, deploy)

## Screenshots (Optional)

If the user requests screenshots of the application for documentation:

1. Read `SCREENSHOT_CAPTURE.md` for detailed instructions
2. Use Playwright MCP to capture screenshots from **localhost only**
3. Save screenshots to `/Users/roelandhofkens/Projects/Ai/video-story-creator-docs/images/screenshots/`
4. Reference them in MDX files using `<img src="/images/screenshots/..." />`

**Important:** Only capture screenshots when explicitly requested by the user.

## Best Practices

- Use "Video Story Agent" (not "Video Story Creator") throughout
- Keep pages focused on a single topic
- Include practical examples and screenshots where helpful
- Use consistent heading hierarchy (one H1 via title, then H2+)
- Add new pages to `docs.json` navigation
- Test with `mint dev` before finalizing

## File Naming

- Use lowercase with hyphens: `my-new-page.mdx`
- Place in appropriate folder: `concepts/`, `guides/`
- Match the path in `docs.json` navigation

## Creating New Pages

1. Create the `.mdx` file with frontmatter
2. Add content using Mintlify components
3. Update `docs.json` to include in navigation
4. Test locally with `mint dev`
