# Phase 6: Global Content Extraction & CMS Population

Extract ALL global content from Figma and populate the CMS.
No content should be hardcoded in components.

> **IMPORTANT:** Extract ONLY what exists in YOUR Figma designs.
> Do not invent content or assume fields exist.

## Step 1: Extract Navigation Content

Use Navigation Figma frames to extract ONLY what appears:

```typescript
// PATTERN - extract fields that exist in YOUR navigation
const navigationContent = {
  menuLinks: [
    // { label: '[exact text from Figma]', href: '[destination]' },
  ],
  // Include ONLY if present in your Figma:
  // ctaButtonText: '[button text]',
  // ctaButtonUrl: '[button link]',
};

await createOrUpdateEntry('site-navigation', 'global-navigation', navigationContent);
```

## Step 2: Extract Footer Content

Use Footer Figma frames:

```typescript
// PATTERN - extract fields that exist in YOUR footer
const footerContent = {
  // footerLinks: [...],  // only if present
  // copyrightText: '...', // only if present
  // newsletterTitle: '...', // only if newsletter exists
};

await createOrUpdateEntry('site-footer', 'global-footer', footerContent);
```

## Step 3: Extract Site Settings

```typescript
// PATTERN - extract what appears across your designs
const siteSettings = {
  logoUrl: '[CDN URL for logo]',
  logoAlt: '[Brand name]',
  // address: '[only if appears]',
  // phone: '[only if appears]',
};

await createOrUpdateEntry('site-settings', 'global-settings', siteSettings);
```

## Step 4: Additional Global Content

Create entries ONLY for content that exists in Figma:
- Social media section (if present)
- Testimonials (if global)
- Partner logos (if present)

## Step 5: Error Page Content

**Create ONLY if 404 page exists in Figma:**

```typescript
// const errorPageContent = {
//   title: '[Title from Figma]',
//   message: '[Message from Figma]',
//   buttonText: '[Button text from Figma]',
// };
// await createOrUpdateEntry('error-page', '404', errorPageContent);
```

## Step 6: Verify All Global Content

```typescript
const nav = await getNavigation();
const footer = await getFooterContent();
const settings = await getSiteSettings();

console.log('✓ Navigation:', nav.menuLinks.length, 'links');
console.log('✓ Footer created');
console.log('✓ Site Settings:', settings.logoUrl);
```

## Documentation

Create `/docs/cms-entries.md` listing all created entries:

```markdown
# CMS Entries

## Global Entries
| Content Type | Entry Slug | Purpose |
|--------------|------------|---------|
| site-settings | global-settings | Logo, contact info |
| site-navigation | global-navigation | Menu links |
| site-footer | global-footer | Footer content |
```

## Git Commit

```bash
git commit -m "feat: Global content extracted and populated"
```

## Checkpoint

```bash
osascript -e 'display notification "Phase 6: Global content populated" with title "Claude Code" sound name "Ping"'
```

**Next:** Proceed to [PHASE-7-COMPONENTS.md](PHASE-7-COMPONENTS.md)
