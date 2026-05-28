# SphereOS CMS API - Learnings

This file contains accumulated insights, patterns, and lessons learned.
It is automatically updated by the `/learn` skill and loaded when this skill is invoked.

---

## Patterns

### Inline Editor Image Data Format (Jan 2026)

The inline editor saves image fields as objects, not plain URL strings:

```json
{
  "hero": {
    "imageUrl": {
      "id": "abc123",
      "url": "https://cdn.example.com/images/hero.jpg",
      "src": "https://cdn.example.com/images/hero.jpg",
      "alt": "Hero background",
      "filename": "hero.jpg"
    }
  }
}
```

**Key Fields:**
- `id` - Media asset ID from CMS
- `url` - CDN URL (primary)
- `src` - CDN URL (fallback, same as url)
- `alt` - Alt text for accessibility
- `filename` - Original filename

**Frontend Implications:**
Websites must transform these objects to plain URL strings before rendering. See `figma-to-code` skill for the `transformImageUrls()` pattern.

### Backend normalizeFieldPath for Nested Data (Jan 2026)

The `inline-editor.service.ts` has a `normalizeFieldPath()` method that auto-detects flat vs nested data structures:

- **Flat:** `{ hero: { title: "..." } }` → path `hero.title`
- **Nested:** `{ data: { hero: { title: "..." } } }` → path auto-adjusted to `data.hero.title`

This allows the inline editor to work with legacy databases that have nested `data.data` structures without requiring database migrations.

---

## Gotchas

<!-- Common mistakes and edge cases to avoid -->

### Inline Editor Image Field - String URL Spread Bug (Fixed Jan 2026)
When the inline editor stores image URLs as strings (common for nested fields like `whyBeckons.cards[0].imageUrl`), selecting a new image from the media picker could corrupt the data. The bug: `JSON.parse()` returns the raw string, and spreading it (`{...stringUrl}`) creates an object with numeric keys like `{"0":"h","1":"t","2":"t",...}`. The save appears to succeed but the data is corrupted. **Fix applied in `public/inline-editor.js`** - always check `typeof currentValue === 'object'` before spreading.

### Images Display in Editor But Not on Website (Jan 2026)
**Symptom:** Inline editor shows updated image, but website still shows old image (or no image) after refresh.

**Cause:** The inline editor saves images as objects `{id, url, src, alt, filename}`, but the frontend expects plain URL strings.

**Solution:** The website's content layer (`src/lib/content/index.ts`) must include a `transformImageUrls()` function that recursively extracts URL strings from image objects. See `figma-to-code` skill LEARNINGS.md for the complete pattern.

### Nested Data Structure Breaks Inline Editing (Jan 2026)
**Symptom:** Inline editor shows empty fields or fails to save properly.

**Cause:** Some databases store content with double-nesting: `{ data: { data: { hero: {...} } } }`. The editor expects flat: `{ data: { hero: {...} } }`.

**Backend Fix:** The `inline-editor.service.ts` now has `normalizeFieldPath()` that auto-detects and handles both structures. No database migration required.

**Prevention:** When creating new content entries, always use FLAT structure with sections at the top level of the `data` object.

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

## CMS

<!-- CMS-specific behaviors and quirks -->

---

## Tooling

<!-- Build, dev, and tooling insights -->

---

## Debug

<!-- Debugging tips and solutions -->

---
