# Figma to Code - Learnings

This file contains accumulated insights, patterns, and lessons learned.
It is automatically updated by the `/learn` skill and loaded when this skill is invoked.

---

## Patterns

### Website Content Layer - Image Object Handling (Jan 2026)

When building Next.js websites that fetch content from SphereOS CMS, the content layer (`src/lib/content/index.ts`) MUST handle image objects from the inline editor.

**The Problem:**
- Inline editor saves images as objects: `{id, url, src, alt, filename}`
- Frontends typically expect plain URL strings: `"https://cdn.example.com/image.jpg"`
- Without proper handling, components receive objects instead of strings and images don't display

**The Solution:**
Add an `isImageObject()` helper and update `transformImageUrls()` to extract URLs:

```typescript
/**
 * Check if an object is an image object from the CMS inline editor.
 * Image objects have url/src and typically id, alt, filename.
 */
function isImageObject(obj: unknown): obj is { url?: string; src?: string } {
  if (typeof obj !== 'object' || obj === null) return false;
  const o = obj as Record<string, unknown>;
  // Must have url or src, and should have typical image fields
  return (typeof o.url === 'string' || typeof o.src === 'string') &&
    (o.id !== undefined || o.filename !== undefined || o.alt !== undefined);
}

/**
 * Transform image data for frontend consumption.
 * - Extracts URL strings from image objects saved by the inline editor
 * - Transforms /images/ paths to CDN URLs (if applicable)
 * - Recursively processes objects and arrays
 */
function transformImageUrls<T>(data: T): T {
  if (data === null || data === undefined) return data;

  if (typeof data === 'string') {
    // Transform /images/... paths to CDN URLs if needed
    if (data.startsWith('/images/')) {
      return data.replace('/images/', `${CDN_BASE_URL}/`) as T;
    }
    return data;
  }

  if (Array.isArray(data)) {
    return data.map(item => transformImageUrls(item)) as T;
  }

  if (typeof data === 'object') {
    // Check if this is an image object - extract URL directly
    if (isImageObject(data)) {
      const imageUrl = (data as { url?: string; src?: string }).url ||
                       (data as { url?: string; src?: string }).src || '';
      return imageUrl as T;
    }

    const result: Record<string, unknown> = {};
    for (const [key, value] of Object.entries(data as Record<string, unknown>)) {
      result[key] = transformImageUrls(value);
    }
    return result as T;
  }

  return data;
}
```

**Usage in getPageContent():**
```typescript
export async function getPageContent<T>(slug: string): Promise<T> {
  const { data } = await client.query(...);
  return transformImageUrls(data?.contentEntryBySlug?.data) as T;
}
```

**Key Points:**
- Always apply `transformImageUrls()` to CMS data before returning to components
- The function is recursive - it handles nested objects and arrays
- Image objects are detected by presence of `url`/`src` AND typical fields like `id`, `filename`, or `alt`
- This pattern is essential for inline editor compatibility

### Individual MEDIA Fields for Image Arrays (Jan 2026)

**CRITICAL:** Never use `type: 'json'` for image collections (galleries, Instagram feeds, etc.).

**The Problem:**
Using JSON arrays for images bypasses the CMS media library:
```typescript
// ❌ WRONG - Creates JSON blob editor, no media picker
{ slug: 'galleryImages', name: 'Gallery', type: 'json' }
// Stores: [{src: '...', alt: '...'}, ...]
```

This causes:
1. CMS admin shows raw JSON textarea instead of image pickers
2. Users can't browse/select from media library
3. No image previews
4. Inline editor shows JSON editor instead of image picker
5. URLs aren't validated

**The Solution:**
Use individual MEDIA fields for each image slot:
```typescript
// ✅ CORRECT - Each image gets its own media picker
{ slug: 'galleryImage1', name: 'Gallery Image 1', type: 'media' },
{ slug: 'galleryImage1Alt', name: 'Gallery Image 1 Alt', type: 'text' },
{ slug: 'galleryImage2', name: 'Gallery Image 2', type: 'media' },
{ slug: 'galleryImage2Alt', name: 'Gallery Image 2 Alt', type: 'text' },
// ... continue for max needed (typically 4-8)
```

**Frontend Pattern - Building Arrays from Individual Fields:**
```typescript
function extractMediaUrl(field: unknown): string | null {
  if (Array.isArray(field) && field.length > 0 && typeof field[0] === 'string') {
    return field[0];
  }
  if (typeof field === 'string' && field.length > 0) {
    return field;
  }
  return null;
}

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
const gallery = buildImageArray(data, 'galleryImage', 6);
const instagram = buildImageArray(data, 'instagramImage', 4);
```

**JSON is OK for non-image arrays:**
- Navigation links: `[{label, url}]`
- Social links: `[{platform, url}]`
- Menu items: `[{name, price}]`
- Business hours: `[{days, open, close}]`

---

## Gotchas

<!-- Common mistakes and edge cases to avoid -->

### Inline Editor Image Field - String URL Spread Bug (Fixed Jan 2026)
When the inline editor stores image URLs as strings (common for nested fields like `whyBeckons.cards[0].imageUrl`), selecting a new image from the media picker could corrupt the data. The bug: `JSON.parse()` returns the raw string, and spreading it (`{...stringUrl}`) creates an object with numeric keys like `{"0":"h","1":"t","2":"t",...}`. The save appears to succeed but the data is corrupted. **Fix applied in `public/inline-editor.js`** - always check `typeof currentValue === 'object'` before spreading.

### Website Content Layer Must Handle Image Objects (Jan 2026)
The inline editor saves images as objects `{id, url, src, alt, filename}`, but frontends typically expect plain URL strings. Without a `transformImageUrls()` function that extracts URLs from image objects, images won't display after inline editing. See the **Patterns** section above for the complete solution.

### isImageObject() Too Aggressive - Breaks {src, alt} Arrays (Jan 2026)
**Problem:** The `isImageObject()` check was too aggressive and matched simple `{src, alt}` objects from legacy JSON arrays (like Instagram images stored as `[{src: '...', alt: '...'}]`). This caused the `transformImageUrls()` function to convert the entire object to just a URL string, breaking components that expected the full `{src, alt}` structure.

**Bad check:**
```typescript
// ❌ This matches {src, alt} from arrays AND inline editor objects
return (typeof o.url === 'string' || typeof o.src === 'string') &&
  (o.id !== undefined || o.filename !== undefined || o.alt !== undefined);
```

**Fixed check:**
```typescript
// ✅ Only match actual inline editor image objects (have id OR filename)
return (typeof o.url === 'string' || typeof o.src === 'string') &&
  (o.id !== undefined || o.filename !== undefined);
// Note: Removed `|| o.alt !== undefined` - alt alone doesn't indicate inline editor object
```

**Key insight:** Inline editor image objects always have `id` or `filename` fields. Simple `{src, alt}` pairs from JSON arrays only have those two fields. Don't match on `alt` alone.

### Nested Data Structure Breaks Inline Editing (Jan 2026)
Some early CMS implementations stored content with an extra `data` wrapper: `{ data: { data: { hero: {...} } } }`. This breaks inline editing because the editor looks for paths like `data.hero.title`, not `data.data.hero.title`. The backend `inline-editor.service.ts` now has `normalizeFieldPath()` to auto-detect and handle both flat and nested structures, but new sites should always use flat structures: `{ data: { hero: {...} } }`.

---

## Preferences

<!-- Client/team preferences and conventions -->

---

## Architecture

<!-- Structural decisions and organization -->

---

## Performance

<!-- Optimization insights -->

---

## Styling

<!-- Design and CSS related learnings -->

---

## CMS

<!-- CMS-specific behaviors and quirks -->

---

## Tooling

<!-- Build, dev, and tooling insights -->

---

## Debug

<!-- Debugging tips and solutions -->

---
