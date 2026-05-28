# CMS Field Definitions Guide

This document defines the rules and best practices for creating CMS content types and field definitions. Following these rules ensures the CMS admin UI is user-friendly (individual form fields instead of JSON blobs) and data is properly structured.

---

## Critical Rule: Image Collections

> **NEVER use `type: 'json'` for image arrays.**
>
> This is the most common mistake. JSON fields bypass the media library picker entirely.

### Why This Matters

When you use JSON for images:
```typescript
// ❌ WRONG
{ slug: 'galleryImages', name: 'Gallery Images', type: 'json' }
// Stores: [{src: '...', alt: '...'}, {src: '...', alt: '...'}]
```

**Problems:**
1. CMS admin shows a raw JSON textarea - no image picker
2. Users can't browse or select from the media library
3. No image previews in the admin
4. No CDN URL validation
5. Inline editor shows a JSON editor instead of image picker
6. Users can paste any URL, including broken or external ones

### The Correct Pattern

Use **individual MEDIA fields** for each image slot:

```typescript
// ✅ CORRECT - Each image gets its own media picker
{ slug: 'galleryImage1', name: 'Gallery Image 1', type: 'media' },
{ slug: 'galleryImage1Alt', name: 'Gallery Image 1 Alt', type: 'text' },
{ slug: 'galleryImage2', name: 'Gallery Image 2', type: 'media' },
{ slug: 'galleryImage2Alt', name: 'Gallery Image 2 Alt', type: 'text' },
{ slug: 'galleryImage3', name: 'Gallery Image 3', type: 'media' },
{ slug: 'galleryImage3Alt', name: 'Gallery Image 3 Alt', type: 'text' },
// ... continue for maximum needed (typically 4-8)
```

**Benefits:**
1. Each image has its own media picker with library browser
2. Image previews in the CMS admin
3. CDN URLs are validated
4. Inline editor shows proper image picker UI
5. Better accessibility with individual alt text fields

### When JSON IS Appropriate

JSON is fine for **non-media arrays**:

```typescript
// ✅ OK - These are text/link data, not images
{ slug: 'menuLinks', name: 'Menu Links', type: 'json' },     // [{label, url}]
{ slug: 'socialLinks', name: 'Social Links', type: 'json' }, // [{platform, url}]
{ slug: 'businessHours', name: 'Hours', type: 'json' },      // [{days, open, close}]
{ slug: 'menuItems', name: 'Menu Items', type: 'json' },     // [{name, price, description}]
{ slug: 'sections', name: 'Page Sections', type: 'json' },   // [{type, slug}] references
```

### Quick Decision Guide

| Data Type | Use This |
|-----------|----------|
| Single image | `type: 'media'` |
| Image gallery (3-8 images) | Individual `media` fields: `image1`, `image2`, etc. |
| Navigation links | `type: 'json'` |
| Social media links | `type: 'json'` |
| Menu items (text only) | `type: 'json'` |
| Business hours | `type: 'json'` |
| Section references | `type: 'json'` |

---

## Core Principles

### 1. Content Types Before Entries

**Always create content types with proper field definitions BEFORE creating content entries.**

```
Order of operations:
1. Create content type (e.g., "page-content")
2. Create field definitions for that type
3. Create content entries

If you create entries before field definitions, the CMS admin will show a single JSON blob editor instead of individual form fields.
```

### 2. Flat Field Structure

**Field slugs must be flat (single level) — no dot notation or nesting.**

```typescript
// ✅ CORRECT: Flat field slugs
{ slug: 'heroTitle', name: 'Hero Title', type: 'text' }
{ slug: 'heroVideoUrl', name: 'Hero Video', type: 'media' }
{ slug: 'aboutBody', name: 'About Body', type: 'richText' }

// ❌ WRONG: Nested/dot notation slugs (won't work)
{ slug: 'hero.title', name: 'Hero Title', type: 'text' }
{ slug: 'hero.videoUrl', name: 'Hero Video', type: 'media' }
```

### 3. Naming Convention

**Use camelCase for field slugs with section prefix:**

```
Pattern: {sectionName}{FieldName}

Examples:
- heroTitle, heroSubtitle, heroVideoUrl, heroPosterUrl
- aboutHeading, aboutBody, aboutCtaText, aboutCtaUrl
- contactEmail, contactPhone, contactAddress
- footerCopyright, footerLinks
- galleryImage1, galleryImage1Alt, galleryImage2, galleryImage2Alt
```

---

## Field Types Reference

| Type | CMS Admin UI | Use For |
|------|--------------|---------|
| `text` | Single-line text input | Titles, labels, short text, alt text |
| `richText` | Rich text editor (Tiptap) | Paragraphs, formatted content |
| `number` | Number input | Counts, sort orders, prices |
| `boolean` | Toggle switch | Flags, visibility toggles |
| `media` | Media picker (file upload) | **ALL images**, videos, documents |
| `json` | JSON editor | Link arrays, structured text data (NOT images) |
| `reference` | Content entry selector | Links to other entries |

### When to Use Each Type

**`text`** - Short strings (< 255 chars)
```typescript
{ slug: 'heroTitle', name: 'Hero Title', type: 'text', required: true }
{ slug: 'buttonLabel', name: 'Button Label', type: 'text' }
{ slug: 'imageAlt', name: 'Image Alt Text', type: 'text' }  // For accessibility
```

**`richText`** - Formatted paragraphs, HTML content
```typescript
{ slug: 'aboutBody', name: 'About Body', type: 'richText' }
{ slug: 'faqAnswer', name: 'Answer', type: 'richText' }
```

**`media`** - Images, videos, files (ALWAYS use for images)
```typescript
{ slug: 'heroImage', name: 'Hero Image', type: 'media' }
{ slug: 'heroImageAlt', name: 'Hero Image Alt', type: 'text' }
{ slug: 'teamMemberPhoto', name: 'Photo', type: 'media' }
{ slug: 'teamMemberPhotoAlt', name: 'Photo Alt', type: 'text' }
```

**`json`** - Arrays of text/link data (NEVER for images)
```typescript
// ✅ OK - Non-image arrays
{ slug: 'navigationLinks', name: 'Navigation Links', type: 'json' }
{ slug: 'socialMediaLinks', name: 'Social Links', type: 'json' }
{ slug: 'businessHours', name: 'Business Hours', type: 'json' }

// ❌ WRONG - Image arrays
{ slug: 'galleryImages', name: 'Gallery', type: 'json' }  // NO!
```

**`reference`** - Links to other content entries
```typescript
{ slug: 'authorId', name: 'Author', type: 'reference' }
```

---

## Handling Image Collections

### Pattern: Individual MEDIA Fields

For galleries, carousels, or any image collection, use numbered individual fields:

```typescript
// Gallery with up to 6 images
await createContentType('gallery', 'Gallery', [
  { slug: 'name', name: 'Gallery Name', type: 'text', required: true },

  // Individual image fields
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
]);
```

### Frontend: Building Arrays from Individual Fields

Your content layer transforms individual fields back into arrays for components:

```typescript
// src/lib/content/index.ts

/**
 * Extract URL from MEDIA field (handles string and array formats)
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

// Usage:
const galleryImages = buildImageArray(data, 'image', 6);
// Returns: [{src: '...', alt: '...'}, {src: '...', alt: '...'}]
```

---

## Handling Non-Image Arrays

### JSON for Link/Text Arrays

JSON is appropriate for arrays of structured text data:

```typescript
// Navigation links
{ slug: 'menuLinks', name: 'Menu Links', type: 'json' }
// Format: [{label: 'About', url: '/about', isExternal: false}]

// Social media
{ slug: 'socialLinks', name: 'Social Links', type: 'json' }
// Format: [{platform: 'instagram', url: 'https://...', ariaLabel: 'Follow us'}]

// Business hours
{ slug: 'hours', name: 'Business Hours', type: 'json' }
// Format: [{days: 'Mon-Fri', open: '9am', close: '5pm'}]

// Menu items (text only)
{ slug: 'menuItems', name: 'Menu Items', type: 'json' }
// Format: [{name: 'Burger', description: '...', price: '$12'}]
```

### Reference Pattern for Complex Collections

For items that need individual editing (FAQ, team members, events):

```typescript
// 1. Create the item content type
await createContentType('faq-item', 'FAQ Item', [
  { slug: 'question', name: 'Question', type: 'text', required: true },
  { slug: 'answer', name: 'Answer', type: 'richText', required: true },
  { slug: 'category', name: 'Category', type: 'text' },
  { slug: 'sortOrder', name: 'Sort Order', type: 'number' },
]);

// 2. Create individual entries for each FAQ
// 3. Query all FAQ items and filter/sort in frontend
```

---

## Content Type Patterns

### Page Content Type

For pages with multiple sections, use flat field names:

```typescript
await createContentType('page-content', 'Page Content', [
  // Meta fields
  { slug: 'metaTitle', name: 'Meta Title', type: 'text' },
  { slug: 'metaDescription', name: 'Meta Description', type: 'text' },

  // Hero section - individual media fields
  { slug: 'heroTitle', name: 'Hero Title', type: 'text' },
  { slug: 'heroSubtitle', name: 'Hero Subtitle', type: 'text' },
  { slug: 'heroImage', name: 'Hero Image', type: 'media' },
  { slug: 'heroImageAlt', name: 'Hero Image Alt', type: 'text' },

  // About section
  { slug: 'aboutHeading', name: 'About Heading', type: 'text' },
  { slug: 'aboutBody', name: 'About Body', type: 'richText' },
  { slug: 'aboutImage', name: 'About Image', type: 'media' },
  { slug: 'aboutImageAlt', name: 'About Image Alt', type: 'text' },
  { slug: 'aboutCtaText', name: 'About CTA Text', type: 'text' },
  { slug: 'aboutCtaUrl', name: 'About CTA URL', type: 'text' },

  // Gallery - individual media fields (NOT JSON)
  { slug: 'galleryImage1', name: 'Gallery Image 1', type: 'media' },
  { slug: 'galleryImage1Alt', name: 'Gallery Image 1 Alt', type: 'text' },
  { slug: 'galleryImage2', name: 'Gallery Image 2', type: 'media' },
  { slug: 'galleryImage2Alt', name: 'Gallery Image 2 Alt', type: 'text' },
  { slug: 'galleryImage3', name: 'Gallery Image 3', type: 'media' },
  { slug: 'galleryImage3Alt', name: 'Gallery Image 3 Alt', type: 'text' },

  // Links stay as JSON (not images)
  { slug: 'navLinks', name: 'Navigation Links', type: 'json' },
]);
```

### Collection Content Types

For repeatable items (FAQ, team members, menu items):

```typescript
// FAQ Item
await createContentType('faq-item', 'FAQ Item', [
  { slug: 'question', name: 'Question', type: 'text', required: true },
  { slug: 'answer', name: 'Answer', type: 'richText', required: true },
  { slug: 'sortOrder', name: 'Sort Order', type: 'number' },
]);

// Team Member
await createContentType('team-member', 'Team Member', [
  { slug: 'name', name: 'Name', type: 'text', required: true },
  { slug: 'title', name: 'Job Title', type: 'text' },
  { slug: 'bio', name: 'Biography', type: 'richText' },
  { slug: 'photo', name: 'Photo', type: 'media' },
  { slug: 'photoAlt', name: 'Photo Alt', type: 'text' },
  { slug: 'sortOrder', name: 'Sort Order', type: 'number' },
]);
```

### Global Content Types

For site-wide content (settings, navigation, footer):

```typescript
// Site Settings
await createContentType('site-settings', 'Site Settings', [
  { slug: 'siteName', name: 'Site Name', type: 'text' },
  { slug: 'siteDescription', name: 'Site Description', type: 'text' },
  { slug: 'logo', name: 'Logo', type: 'media' },
  { slug: 'logoAlt', name: 'Logo Alt Text', type: 'text' },
]);

// Site Navigation
await createContentType('site-navigation', 'Site Navigation', [
  { slug: 'menuLinks', name: 'Menu Links', type: 'json' },  // OK - links not images
  { slug: 'ctaText', name: 'CTA Button Text', type: 'text' },
  { slug: 'ctaUrl', name: 'CTA Button URL', type: 'text' },
]);

// Site Footer
await createContentType('site-footer', 'Site Footer', [
  { slug: 'copyrightText', name: 'Copyright Text', type: 'text' },
  { slug: 'footerLinks', name: 'Footer Links', type: 'json' },  // OK - links not images
  { slug: 'socialLinks', name: 'Social Links', type: 'json' },   // OK - links not images
  { slug: 'footerLogo', name: 'Footer Logo', type: 'media' },
  { slug: 'footerLogoAlt', name: 'Footer Logo Alt', type: 'text' },
]);
```

---

## Entry Data Structure

### Flat Data for Flat Fields

When you have individual field definitions, entry data should match:

```typescript
await createEntry('page-content', 'home', {
  // Meta
  metaTitle: 'Welcome to Our Site',
  metaDescription: 'Discover amazing experiences...',

  // Hero section (flat, not nested)
  heroTitle: 'Welcome',
  heroSubtitle: 'Discover the extraordinary',
  heroImage: 'https://cdn.example.com/hero.jpg',  // Single URL
  heroImageAlt: 'Beautiful landscape view',

  // Gallery (individual fields, NOT array)
  galleryImage1: 'https://cdn.example.com/gallery-1.jpg',
  galleryImage1Alt: 'Gallery image 1 description',
  galleryImage2: 'https://cdn.example.com/gallery-2.jpg',
  galleryImage2Alt: 'Gallery image 2 description',
  galleryImage3: 'https://cdn.example.com/gallery-3.jpg',
  galleryImage3Alt: 'Gallery image 3 description',

  // Links as JSON (OK - not images)
  navLinks: [
    { label: 'About', url: '/about' },
    { label: 'Contact', url: '/contact' },
  ],
});
```

---

## Frontend Transformation

### Why Transform?

Components often expect nested data structures for organization:

```typescript
// Component expects:
interface HeroProps {
  hero: {
    title: string;
    subtitle: string;
    image: { src: string; alt: string };
  };
}
```

But CMS stores flat:

```typescript
// CMS returns:
{
  heroTitle: 'Welcome',
  heroSubtitle: 'Discover',
  heroImage: 'https://...',
  heroImageAlt: 'Description',
}
```

### Transformation Layer Pattern

Create a content layer that transforms flat CMS data to nested component props:

```typescript
// src/lib/content/index.ts

function transformPageData(flat: FlatPageData): NestedPageData {
  return {
    hero: {
      title: flat.heroTitle,
      subtitle: flat.heroSubtitle,
      image: {
        src: extractMediaUrl(flat.heroImage) || '',
        alt: flat.heroImageAlt || '',
      },
    },
    gallery: buildImageArray(flat, 'galleryImage', 6),
    about: {
      heading: flat.aboutHeading,
      body: flat.aboutBody,
    },
  };
}
```

---

## Migration Checklist

When converting existing JSON blobs to proper field definitions:

1. **Analyze Current Structure**
   - List all fields in the JSON blob
   - Identify image arrays (need individual MEDIA fields)
   - Identify text arrays (can stay as JSON)
   - Note required fields

2. **Create Field Definitions**
   - Flatten nested objects to `sectionFieldName` format
   - Convert image arrays to individual MEDIA fields
   - Keep text/link arrays as JSON fields
   - Set appropriate field types

3. **Transform Entry Data**
   - Convert nested to flat structure
   - Split image arrays into individual fields
   - Preserve all values
   - Test in CMS admin

4. **Update Frontend**
   - Add `buildImageArray()` helper function
   - Update transformation layer to build arrays from individual fields
   - Test rendering

5. **Verify**
   - CMS admin shows individual form fields
   - Media picker works for all image fields
   - Editing and saving works
   - Frontend renders correctly

---

## Version History

**v1.1.0** (January 2026)
- Added critical rule: NEVER use JSON for image arrays
- Added individual MEDIA field pattern for galleries
- Added `buildImageArray()` frontend helper pattern
- Updated all examples to use individual MEDIA fields

**v1.0.0** (January 2026)
- Initial field definitions guide
- Flat field structure rules
- Collection patterns (JSON vs references)
- Frontend transformation patterns
