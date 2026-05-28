# Phase 8: Page Content Extraction & CMS Population

**FOR EACH PAGE (in order):**

## Step A: Extract ALL Text from Figma

- Use Figma MCP to get every text element
- Copy EXACTLY as shown — no rewording

## Step B: Map Images to CDN URLs

Use `/docs/image-manifest.json` to get CDN URLs for each image.

## Step C: Create CMS Entry

> **CRITICAL: Use FLAT data structure!**
> All sections must be at the TOP LEVEL of the data object.
> Do NOT nest content inside a `data` property - this breaks inline editing.

✅ **Correct (flat):** `entry.data.hero.title`
❌ **Wrong (nested):** `entry.data.data.hero.title`

> **IMPORTANT:** The example shows the PATTERN.
> Page names, sections, and fields depend on YOUR Figma.
> Do NOT assume specific sections exist.

```typescript
// Use actual page slug from YOUR Figma
await createOrUpdateEntry('page-content', '[your-page-slug]', {
  // Meta fields at top level
  title: '[Page Title]',
  metaTitle: '[Brand Name] | [Page Title]',
  metaDescription: '[Description from Figma]',

  // ALL sections at top level (NOT nested inside "data")
  sectionName: {
    heading: '[Exact heading from Figma]',
    paragraph: '[Exact paragraph from Figma]',
    buttonText: '[Button text if present]',
    buttonHref: '[Link destination]',
    imageSrc: '[CDN URL]',
  },

  // For arrays (team, FAQ, products, etc.):
  arraySection: [
    {
      field1: '[Value from Figma]',
      field2: '[Value from Figma]',
    },
    // ... all items
  ],

  // Add sections ONLY for what exists in Figma
});
```

## Repeat for ALL Pages

For each page in your Figma file:
1. Extract text from Figma MCP
2. Map images to CDN URLs
3. Create CMS entry
4. Verify entry was created

## Create Collection Entries (If Applicable)

Create entries for collections ONLY if they exist in Figma:

```typescript
// FAQ items
// await createOrUpdateEntry('faq-item', 'faq-1', { question: '...', answer: '...' });

// Team members
// await createOrUpdateEntry('team-member', 'john-doe', { name: '...', title: '...' });
```

## Documentation

Update `/docs/cms-entries.md` with all page entries:

```markdown
## Page Entries
| Content Type | Entry Slug | Page |
|--------------|------------|------|
| page-content | home | Homepage |
| page-content | about | About page |
```

## Git Commit

```bash
git commit -m "feat: All page content populated in CMS"
```

## Checkpoint

```bash
osascript -e 'display notification "Phase 8: Page content populated" with title "Claude Code" sound name "Ping"'
```

**Next:** Proceed to [PHASE-9-PAGES.md](PHASE-9-PAGES.md)
