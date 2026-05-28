# Mintlify Reference

## docs.json Schema

```json
{
  "$schema": "https://mintlify.com/schema.json",
  "name": "Site Name",
  "theme": "mint|maple|palm|willow|linden|almond|aspen",
  "logo": {
    "dark": "/logo/dark.svg",
    "light": "/logo/light.svg"
  },
  "favicon": "/favicon.svg",
  "colors": {
    "primary": "#hex",
    "light": "#hex",
    "dark": "#hex"
  },
  "navigation": {
    "tabs": [...]
  }
}
```

## Available Themes

- `mint` - Classic green
- `maple` - Warm red/orange
- `palm` - Tropical green
- `willow` - Soft green
- `linden` - Yellow/gold
- `almond` - Warm brown
- `aspen` - Cool blue/gray

## MDX Components

### Cards
```mdx
<CardGroup cols={2}>
  <Card title="Title" icon="icon-name" href="/path">
    Description text
  </Card>
</CardGroup>
```

### Steps
```mdx
<Steps>
  <Step title="Step 1">
    Content for step 1
  </Step>
  <Step title="Step 2">
    Content for step 2
  </Step>
</Steps>
```

### Callouts
```mdx
<Note>Informational note</Note>
<Tip>Helpful tip</Tip>
<Warning>Warning message</Warning>
<Info>Additional info</Info>
```

### Accordions
```mdx
<AccordionGroup>
  <Accordion title="Question 1">
    Answer 1
  </Accordion>
  <Accordion title="Question 2">
    Answer 2
  </Accordion>
</AccordionGroup>
```

### Tabs
```mdx
<Tabs>
  <Tab title="Tab 1">
    Content 1
  </Tab>
  <Tab title="Tab 2">
    Content 2
  </Tab>
</Tabs>
```

### Code Blocks
```mdx
```javascript
const example = "code";
```
```

With title:
```mdx
```javascript title="example.js"
const example = "code";
```
```

### Images
```mdx
<img src="/images/example.png" alt="Description" />

<!-- Or with dark mode variant -->
<img className="block dark:hidden" src="/images/light.png" alt="Light" />
<img className="hidden dark:block" src="/images/dark.png" alt="Dark" />
```

## Frontmatter Options

```yaml
---
title: 'Page Title'           # Required
description: 'Description'    # For SEO
icon: 'icon-name'            # Optional icon
---
```

## Icons

Mintlify uses Font Awesome icons. Common ones:
- `rocket` - Getting started
- `book` - Documentation
- `code` - API/Code
- `gear` - Settings
- `palette` - Customization
- `film` - Video
- `sparkles` - AI/Magic
- `folder-open` - Projects
- `images` - Assets
- `wand-magic-sparkles` - AI workflow

## CLI Commands

```bash
# Start dev server
mint dev

# Build for production
mint build

# Deploy (if configured)
mint deploy
```
