# Phase 5: CMS Content Type Setup

Create content types based on **Figma component patterns**, not individual pages.

> **CRITICAL INSIGHT:** Content Types should map to reusable Figma components.
> Pages then reference these component entries, enabling reuse across the site.

> **IMPORTANT:** See [CMS-FIELD-DEFINITIONS.md](CMS-FIELD-DEFINITIONS.md) for detailed rules on field definitions, naming conventions, and handling arrays.

---

## Critical Rule: Image Collections

> **NEVER use `type: 'json'` for image arrays.**
>
> JSON fields display as raw JSON editors in the CMS admin, bypassing the media library picker.
> This breaks the user experience and prevents CDN validation.

### The Problem with JSON Image Arrays

```typescript
// ❌ WRONG - Creates a JSON blob editor, no media picker
{ slug: 'galleryImages', name: 'Gallery Images', type: 'json' }
// Stores: [{src: '...', alt: '...'}, {src: '...', alt: '...'}]
```

**Issues:**
1. CMS admin shows raw JSON textarea instead of image pickers
2. Users can't use the media library to select images
3. No image preview in the admin
4. No CDN URL validation
5. Inline editor can't show media picker for these fields

### The Correct Pattern: Individual MEDIA Fields

```typescript
// ✅ CORRECT - Each image gets a proper media picker
{ slug: 'galleryImage1', name: 'Gallery Image 1', type: 'media' },
{ slug: 'galleryImage1Alt', name: 'Gallery Image 1 Alt', type: 'text' },
{ slug: 'galleryImage2', name: 'Gallery Image 2', type: 'media' },
{ slug: 'galleryImage2Alt', name: 'Gallery Image 2 Alt', type: 'text' },
{ slug: 'galleryImage3', name: 'Gallery Image 3', type: 'media' },
{ slug: 'galleryImage3Alt', name: 'Gallery Image 3 Alt', type: 'text' },
// ... up to the maximum needed (typically 4-8)
```

**Benefits:**
1. Each image has its own media picker in CMS admin
2. Users can browse and select from media library
3. Image previews in the admin
4. CDN URLs are validated
5. Inline editor shows proper image picker UI

### When JSON Arrays ARE Appropriate

JSON is fine for **non-media arrays** like:
- Navigation links: `[{label, url, isExternal}]`
- Social links: `[{platform, url, ariaLabel}]`
- Business hours: `[{days, open, close}]`
- Menu items (text-only): `[{name, description, price}]`

---

## The Three-Tier Content Model

### Why Component-Based?

| Approach | Problem |
|----------|---------|
| One CT per page | Duplicates fields, can't share content between pages |
| One CT for everything | Too generic, hard to validate |
| **Component-based** | Reusable, validates well, maps to Figma design |

### The Tier System

```
┌─────────────────────────────────────────────────────────────────┐
│                     TIER 1: GLOBAL (3 CTs)                      │
│  site-settings  │  navigation  │  footer                        │
│  (1 entry each - site-wide configuration)                       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                   TIER 2: COMPONENTS (varies)                   │
│  hero-section  │  content-section  │  gallery  │  faq-item      │
│  (N entries each - reusable building blocks from Figma)         │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     TIER 3: PAGES (1 CT)                        │
│  page                                                           │
│  (N entries - references component entries above)               │
└─────────────────────────────────────────────────────────────────┘
```

---

## Step 1: Analyze Figma Components

Before creating content types, analyze your Figma file's Components page.

**Look for:**
1. **Hero variants** — How many hero styles exist? (split-screen, full-screen, gallery, etc.)
2. **Section patterns** — What reusable section layouts appear? (half-screen, centered text, etc.)
3. **Card types** — What card components exist? (event cards, team members, awards, etc.)
4. **Global components** — Navigation, footer, menu overlay
5. **Image galleries** — Count max images per gallery to determine field count

**Document in `/project-config/content-model.md`:**

```markdown
# Content Model Plan

## Figma Components Found
- hero-option-1 (split-screen, full-screen variants)
- hero-option-2 (standard hero)
- section-half-screen (image + text, alternating)
- gallery (6-image grid) → Need 6 individual image fields
- instagram-feed (4 images) → Need 4 individual image fields
- faq-accordion (question/answer)
- navigation (desktop/mobile)
- footer

## Proposed Content Types
[Map each component to a content type]
```

---

## Step 2: Create Tier 1 Content Types (Global)

These have exactly **one entry** each.

### Site Settings

```typescript
await createOrUpdateContentType('site-settings', 'Site Settings', [
  // Basic info
  { slug: 'siteName', name: 'Site Name', type: 'text', required: true },
  { slug: 'siteDescription', name: 'Site Description', type: 'text' },

  // Logos (individual MEDIA fields)
  { slug: 'logoUrl', name: 'Primary Logo', type: 'media', required: true },
  { slug: 'logoAlt', name: 'Logo Alt Text', type: 'text', required: true },
  { slug: 'logoAltUrl', name: 'Alternative Logo (Footer)', type: 'media' },
  { slug: 'logoAltAlt', name: 'Alt Logo Alt Text', type: 'text' },

  // Contact
  { slug: 'phone', name: 'Phone Number', type: 'text' },
  { slug: 'email', name: 'Email Address', type: 'text' },
  { slug: 'address', name: 'Full Address', type: 'json' }, // {street, city, state, zip} - OK for structured text

  // Social & External (JSON OK - these are links, not images)
  { slug: 'socialLinks', name: 'Social Links', type: 'json' }, // [{platform, url, ariaLabel}]
  { slug: 'instagramHandle', name: 'Instagram Handle', type: 'text' },
  { slug: 'reservationUrl', name: 'Reservation URL', type: 'text' },

  // Hours (JSON OK - structured text data)
  { slug: 'hours', name: 'Business Hours', type: 'json' }, // [{days, open, close}]
]);
```

### Navigation

```typescript
await createOrUpdateContentType('navigation', 'Navigation', [
  // JSON OK for link arrays (text data, not images)
  { slug: 'menuLinks', name: 'Menu Links', type: 'json', required: true },
  // Format: [{label, url, isExternal?, ariaLabel?}]

  { slug: 'ctaText', name: 'CTA Button Text', type: 'text' },
  { slug: 'ctaUrl', name: 'CTA Button URL', type: 'text' },
  { slug: 'ctaAriaLabel', name: 'CTA ARIA Label', type: 'text' },

  // Background image if applicable
  { slug: 'backgroundImage', name: 'Menu Background Image', type: 'media' },
  { slug: 'backgroundImageAlt', name: 'Background Image Alt', type: 'text' },
]);
```

### Footer

```typescript
await createOrUpdateContentType('footer', 'Footer', [
  // Column content - JSON OK for link arrays
  { slug: 'column1Title', name: 'Column 1 Title', type: 'text' },
  { slug: 'column1Links', name: 'Column 1 Links', type: 'json' }, // [{label, url}]
  { slug: 'column2Title', name: 'Column 2 Title', type: 'text' },
  { slug: 'column2Links', name: 'Column 2 Links', type: 'json' },
  { slug: 'column3Title', name: 'Column 3 Title', type: 'text' },
  { slug: 'column3Links', name: 'Column 3 Links', type: 'json' },

  // Newsletter (if present)
  { slug: 'newsletterHeading', name: 'Newsletter Heading', type: 'text' },
  { slug: 'newsletterPlaceholder', name: 'Newsletter Placeholder', type: 'text' },

  // Legal
  { slug: 'copyrightText', name: 'Copyright Text', type: 'text' },
  { slug: 'legalLinks', name: 'Legal Links', type: 'json' }, // [{label, url}]

  // Footer logos (individual MEDIA fields, NOT JSON array)
  { slug: 'footerLogo', name: 'Footer Logo', type: 'media' },
  { slug: 'footerLogoAlt', name: 'Footer Logo Alt', type: 'text' },
  { slug: 'wordmark', name: 'Wordmark Image', type: 'media' },
  { slug: 'wordmarkAlt', name: 'Wordmark Alt', type: 'text' },
]);
```

---

## Step 3: Create Tier 2 Content Types (Components)

These map to Figma components and can have **multiple entries**.

### Hero Section

```typescript
await createOrUpdateContentType('hero-section', 'Hero Section', [
  // Variant selection based on Figma hero types
  { slug: 'variant', name: 'Hero Variant', type: 'text', required: true },
  // Options: 'split-screen', 'full-screen', 'gallery', 'text-only'

  // Content fields
  { slug: 'headline', name: 'Headline', type: 'text' },
  { slug: 'subtitle', name: 'Subtitle', type: 'text' },
  { slug: 'bodyText', name: 'Body Text', type: 'richText' },

  // Primary media (individual fields)
  { slug: 'backgroundImage', name: 'Background Image', type: 'media' },
  { slug: 'backgroundImageAlt', name: 'Background Image Alt', type: 'text' },
  { slug: 'backgroundVideo', name: 'Background Video URL', type: 'text' },

  // Split-screen variant images
  { slug: 'leftImage', name: 'Left Image', type: 'media' },
  { slug: 'leftImageAlt', name: 'Left Image Alt', type: 'text' },
  { slug: 'rightImage', name: 'Right Image', type: 'media' },
  { slug: 'rightImageAlt', name: 'Right Image Alt', type: 'text' },

  // Gallery variant images (individual MEDIA fields, NOT JSON)
  { slug: 'galleryImage1', name: 'Gallery Image 1', type: 'media' },
  { slug: 'galleryImage1Alt', name: 'Gallery Image 1 Alt', type: 'text' },
  { slug: 'galleryImage2', name: 'Gallery Image 2', type: 'media' },
  { slug: 'galleryImage2Alt', name: 'Gallery Image 2 Alt', type: 'text' },
  { slug: 'galleryImage3', name: 'Gallery Image 3', type: 'media' },
  { slug: 'galleryImage3Alt', name: 'Gallery Image 3 Alt', type: 'text' },
  { slug: 'galleryImage4', name: 'Gallery Image 4', type: 'media' },
  { slug: 'galleryImage4Alt', name: 'Gallery Image 4 Alt', type: 'text' },
  { slug: 'galleryImage5', name: 'Gallery Image 5', type: 'media' },
  { slug: 'galleryImage5Alt', name: 'Gallery Image 5 Alt', type: 'text' },
  { slug: 'galleryImage6', name: 'Gallery Image 6', type: 'media' },
  { slug: 'galleryImage6Alt', name: 'Gallery Image 6 Alt', type: 'text' },

  // Logo/wordmark
  { slug: 'logoImage', name: 'Logo/Wordmark', type: 'media' },
  { slug: 'logoImageAlt', name: 'Logo Alt', type: 'text' },

  // CTA
  { slug: 'ctaText', name: 'CTA Button Text', type: 'text' },
  { slug: 'ctaUrl', name: 'CTA Button URL', type: 'text' },
  { slug: 'ctaAriaLabel', name: 'CTA ARIA Label', type: 'text' },

  // Layout
  { slug: 'textAlignment', name: 'Text Alignment', type: 'text' }, // left, center, right
  { slug: 'overlayOpacity', name: 'Overlay Opacity', type: 'number' },
]);
```

### Content Section

For half-screen sections, text blocks, etc.:

```typescript
await createOrUpdateContentType('content-section', 'Content Section', [
  // Variant based on Figma section patterns
  { slug: 'variant', name: 'Section Variant', type: 'text', required: true },
  // Options: 'half-screen-left', 'half-screen-right', 'text-centered', 'text-left'

  // Content
  { slug: 'heading', name: 'Heading', type: 'text' },
  { slug: 'subheading', name: 'Subheading', type: 'text' },
  { slug: 'bodyText', name: 'Body Text', type: 'richText' },

  // Image (single MEDIA field)
  { slug: 'image', name: 'Section Image', type: 'media' },
  { slug: 'imageAlt', name: 'Image Alt Text', type: 'text' },

  // CTA
  { slug: 'ctaText', name: 'CTA Text', type: 'text' },
  { slug: 'ctaUrl', name: 'CTA URL', type: 'text' },
  { slug: 'ctaAriaLabel', name: 'CTA ARIA Label', type: 'text' },

  // Style
  { slug: 'backgroundColor', name: 'Background Color', type: 'text' }, // light, dark, pink
]);
```

### Gallery

> **NOTE:** Use individual MEDIA fields, NOT a JSON array.

```typescript
await createOrUpdateContentType('gallery', 'Gallery', [
  { slug: 'name', name: 'Gallery Name', type: 'text', required: true },
  { slug: 'sectionLabel', name: 'Section ARIA Label', type: 'text' },

  // Individual image fields (adjust count based on Figma design)
  { slug: 'image1', name: 'Image 1', type: 'media' },
  { slug: 'image1Alt', name: 'Image 1 Alt', type: 'text', required: true },
  { slug: 'image2', name: 'Image 2', type: 'media' },
  { slug: 'image2Alt', name: 'Image 2 Alt', type: 'text', required: true },
  { slug: 'image3', name: 'Image 3', type: 'media' },
  { slug: 'image3Alt', name: 'Image 3 Alt', type: 'text', required: true },
  { slug: 'image4', name: 'Image 4', type: 'media' },
  { slug: 'image4Alt', name: 'Image 4 Alt', type: 'text' },
  { slug: 'image5', name: 'Image 5', type: 'media' },
  { slug: 'image5Alt', name: 'Image 5 Alt', type: 'text' },
  { slug: 'image6', name: 'Image 6', type: 'media' },
  { slug: 'image6Alt', name: 'Image 6 Alt', type: 'text' },
  { slug: 'image7', name: 'Image 7', type: 'media' },
  { slug: 'image7Alt', name: 'Image 7 Alt', type: 'text' },
  { slug: 'image8', name: 'Image 8', type: 'media' },
  { slug: 'image8Alt', name: 'Image 8 Alt', type: 'text' },
]);
```

### Instagram Feed

> **NOTE:** Use individual MEDIA fields for Instagram images.

```typescript
await createOrUpdateContentType('instagram-feed', 'Instagram Feed', [
  { slug: 'title', name: 'Section Title', type: 'text' },
  { slug: 'handle', name: 'Instagram Handle', type: 'text' },
  { slug: 'profileUrl', name: 'Profile URL', type: 'text' },
  { slug: 'sectionLabel', name: 'Section ARIA Label', type: 'text' },

  // Individual image fields (typically 4 for Instagram grids)
  { slug: 'image1', name: 'Image 1', type: 'media' },
  { slug: 'image1Alt', name: 'Image 1 Alt', type: 'text' },
  { slug: 'image2', name: 'Image 2', type: 'media' },
  { slug: 'image2Alt', name: 'Image 2 Alt', type: 'text' },
  { slug: 'image3', name: 'Image 3', type: 'media' },
  { slug: 'image3Alt', name: 'Image 3 Alt', type: 'text' },
  { slug: 'image4', name: 'Image 4', type: 'media' },
  { slug: 'image4Alt', name: 'Image 4 Alt', type: 'text' },
]);
```

### FAQ Item

```typescript
await createOrUpdateContentType('faq-item', 'FAQ Item', [
  { slug: 'question', name: 'Question', type: 'text', required: true },
  { slug: 'answer', name: 'Answer', type: 'richText', required: true },
  { slug: 'category', name: 'Category', type: 'text' }, // For filtering
  { slug: 'sortOrder', name: 'Sort Order', type: 'number' },
]);
```

### Additional Component Types (Create as needed)

**Event/Programming:**
```typescript
await createOrUpdateContentType('event', 'Event', [
  { slug: 'title', name: 'Title', type: 'text', required: true },
  { slug: 'date', name: 'Date', type: 'text', required: true },
  { slug: 'time', name: 'Time', type: 'text' },
  { slug: 'description', name: 'Description', type: 'richText' },
  { slug: 'image', name: 'Image', type: 'media' },
  { slug: 'imageAlt', name: 'Image Alt', type: 'text' },
  { slug: 'category', name: 'Category', type: 'text' },
  { slug: 'ticketUrl', name: 'Ticket URL', type: 'text' },
  { slug: 'isFeatured', name: 'Featured', type: 'boolean' },
]);
```

**Team Member:**
```typescript
await createOrUpdateContentType('team-member', 'Team Member', [
  { slug: 'name', name: 'Name', type: 'text', required: true },
  { slug: 'title', name: 'Job Title', type: 'text' },
  { slug: 'photo', name: 'Photo', type: 'media' },
  { slug: 'photoAlt', name: 'Photo Alt', type: 'text' },
  { slug: 'bio', name: 'Biography', type: 'richText' },
  { slug: 'sortOrder', name: 'Sort Order', type: 'number' },
]);
```

**Menu Category (for restaurants):**
```typescript
await createOrUpdateContentType('menu-category', 'Menu Category', [
  { slug: 'name', name: 'Category Name', type: 'text', required: true },
  { slug: 'availability', name: 'Availability', type: 'text' },
  // JSON OK here - menu items are text data, not images
  { slug: 'items', name: 'Menu Items', type: 'json', required: true },
  // Format: [{name, description, price, dietary?}]
  { slug: 'sortOrder', name: 'Sort Order', type: 'number' },
]);
```

**Award/Recognition:**
```typescript
await createOrUpdateContentType('award', 'Award', [
  { slug: 'name', name: 'Award Name', type: 'text', required: true },
  { slug: 'organization', name: 'Organization', type: 'text' },
  { slug: 'logo', name: 'Logo', type: 'media' },
  { slug: 'logoAlt', name: 'Logo Alt', type: 'text' },
  { slug: 'year', name: 'Year', type: 'text' },
  { slug: 'url', name: 'URL', type: 'text' },
]);
```

---

## Step 4: Create Tier 3 Content Type (Page)

A single flexible page type that references component entries.

```typescript
await createOrUpdateContentType('page', 'Page', [
  // Identity
  { slug: 'title', name: 'Page Title', type: 'text', required: true },
  { slug: 'slug', name: 'URL Slug', type: 'text', required: true },

  // SEO
  { slug: 'metaTitle', name: 'Meta Title', type: 'text' },
  { slug: 'metaDescription', name: 'Meta Description', type: 'text' },
  { slug: 'ogImage', name: 'Social Share Image', type: 'media' },
  { slug: 'ogImageAlt', name: 'OG Image Alt', type: 'text' },
  { slug: 'canonicalUrl', name: 'Canonical URL', type: 'text' },
  { slug: 'noIndex', name: 'Hide from Search Engines', type: 'boolean' },

  // Accessibility
  { slug: 'pageAnnouncement', name: 'Screen Reader Announcement', type: 'text' },

  // Hero reference
  { slug: 'heroSlug', name: 'Hero Section Slug', type: 'text' },
  // References a hero-section entry by slug

  // Sections (ordered array of references) - JSON OK for references
  { slug: 'sections', name: 'Page Sections', type: 'json' },
  // Format: [{type: 'content-section', slug: 'homepage-intro'}, ...]

  // Global section toggles
  { slug: 'showInstagram', name: 'Show Instagram Feed', type: 'boolean' },
  { slug: 'showFaq', name: 'Show FAQ Section', type: 'boolean' },
  { slug: 'faqCategory', name: 'FAQ Category Filter', type: 'text' },
]);
```

---

## Frontend: Building Arrays from Individual Fields

When your frontend needs to render a gallery or image grid, build the array from individual fields:

```typescript
// src/lib/content/index.ts

/**
 * Extract URL from MEDIA field (handles both string and array formats)
 */
function extractMediaUrl(field: unknown): string | null {
  if (Array.isArray(field) && field.length > 0 && typeof field[0] === 'string') {
    return field[0];
  }
  if (typeof field === 'string' && field.length > 0) {
    return field;
  }
  return null;
}

/**
 * Build image array from individual MEDIA fields
 */
function buildImageArray(
  data: Record<string, unknown>,
  prefix: string,
  count: number
): Array<{ src: string; alt: string }> {
  const images: Array<{ src: string; alt: string }> = [];

  for (let i = 1; i <= count; i++) {
    const url = extractMediaUrl(data[`${prefix}${i}`]);
    const alt = (data[`${prefix}${i}Alt`] as string) || `${prefix} ${i}`;

    if (url) {
      images.push({ src: url, alt });
    }
  }

  return images;
}

// Usage in getGalleryContent():
export async function getGalleryContent(slug: string) {
  const data = await fetchFromCMS('gallery', slug);

  return {
    name: data.name,
    images: buildImageArray(data, 'image', 8), // Build array from image1-image8
  };
}
```

---

## Content Type Naming Conventions

| Type | Slug Pattern | Example Entries |
|------|--------------|-----------------|
| Global | `site-{name}` or `{name}` | `global-settings`, `global-navigation` |
| Component | `{component-name}` | `hero-homepage`, `section-about-heritage` |
| Page | `page-{slug}` or just `{slug}` | `homepage`, `about`, `contact` |

---

## Key Rules Summary

### 1. Create Types BEFORE Entries
Always create content types first. Creating entries before types results in a JSON blob in the admin UI instead of form fields.

### 2. Use FLAT Field Slugs
```typescript
// ✅ CORRECT
{ slug: 'heroTitle', name: 'Hero Title', type: 'text' }

// ❌ WRONG
{ slug: 'hero.title', name: 'Hero Title', type: 'text' }
```

### 3. NEVER Use JSON for Image Arrays
```typescript
// ✅ CORRECT - Individual MEDIA fields
{ slug: 'image1', name: 'Image 1', type: 'media' },
{ slug: 'image1Alt', name: 'Image 1 Alt', type: 'text' },
{ slug: 'image2', name: 'Image 2', type: 'media' },
{ slug: 'image2Alt', name: 'Image 2 Alt', type: 'text' },

// ❌ WRONG - JSON array for images
{ slug: 'images', name: 'Images', type: 'json' }
```

### 4. JSON is OK for Non-Image Arrays
```typescript
// ✅ OK - Links, text data, structured objects
{ slug: 'menuLinks', name: 'Menu Links', type: 'json' },
{ slug: 'socialLinks', name: 'Social Links', type: 'json' },
{ slug: 'businessHours', name: 'Hours', type: 'json' },
{ slug: 'menuItems', name: 'Menu Items', type: 'json' },
```

### 5. Only Create What Exists in Figma
Don't blindly copy these examples. Create content types ONLY for components that appear in YOUR Figma design.

### 6. Component-Based Thinking
Ask: "Is this a reusable pattern in Figma?" If yes, it's probably a Tier 2 content type.

---

## Git Commit

```bash
git commit -m "feat: Component-based content types created

- Tier 1: Global types (site-settings, navigation, footer)
- Tier 2: Component types (hero-section, content-section, gallery, faq-item, etc.)
- Tier 3: Page type with section references
- Individual MEDIA fields for all image collections (no JSON arrays)
- Content model enables reuse across pages"
```

## Checkpoint

```bash
osascript -e 'display notification "Phase 5: Content types created" with title "Claude Code" sound name "Ping"'
```

**Next:** Proceed to [PHASE-6-GLOBAL-CONTENT.md](PHASE-6-GLOBAL-CONTENT.md)
