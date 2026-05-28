---
name: wordpress-publisher
description: Publishes content to WordPress via REST API. Handles post creation, ACF field population, featured images, categories, tags, and SEO meta. Supports scheduling and draft modes. Use when content is finalized and ready for WordPress deployment.
---

# WordPress Publisher

Veröffentlicht fertige Artikel auf WordPress via REST API.

## Quick Start

```
Input: HTML Content + Meta-Daten + Media Assets
Output: WordPress Post (Draft/Published) + Post ID + URL
```

## Workflow

1. **Content vorbereiten** → HTML, Meta, Featured Image
2. **Media hochladen** → Bilder → Media Library
3. **Post erstellen** → Draft oder Published
4. **ACF Fields setzen** → Custom Fields befüllen
5. **Taxonomien zuweisen** → Kategorien, Tags
6. **SEO Meta setzen** → Yoast/RankMath Felder
7. **Verifizieren** → Post-URL prüfen

## API Endpoints

### Base URL

```
${WORDPRESS_URL}/wp-json/wp/v2/
```

### Authentication

```typescript
// Basic Auth Header
const auth = Buffer.from(`${username}:${appPassword}`).toString('base64');

headers: {
  'Authorization': `Basic ${auth}`,
  'Content-Type': 'application/json'
}
```

### Key Endpoints

| Endpoint | Method | Beschreibung |
|----------|--------|--------------|
| `/posts` | POST | Post erstellen |
| `/posts/{id}` | PUT | Post aktualisieren |
| `/media` | POST | Media hochladen |
| `/categories` | GET/POST | Kategorien |
| `/tags` | GET/POST | Tags |

## Post-Erstellung

### Request Body

```json
{
  "title": "Artikel-Titel",
  "content": "<article>HTML Content...</article>",
  "excerpt": "Kurzbeschreibung für Listings",
  "status": "draft",
  "slug": "artikel-slug",
  "date": "2024-01-15T10:00:00",
  "featured_media": 123,
  "categories": [1, 5],
  "tags": [10, 15, 20],
  "meta": {
    "_yoast_wpseo_title": "SEO Title",
    "_yoast_wpseo_metadesc": "SEO Description"
  },
  "acf": {
    "custom_field_1": "value",
    "custom_field_2": "value"
  }
}
```

### Status-Optionen

| Status | Beschreibung |
|--------|--------------|
| `publish` | Sofort veröffentlichen |
| `draft` | Als Entwurf speichern |
| `pending` | Zur Prüfung |
| `future` | Geplant (mit date) |
| `private` | Privat |

## Media-Upload

### Bild hochladen

```typescript
const uploadMedia = async (imageBuffer: Buffer, filename: string) => {
  const formData = new FormData();
  formData.append('file', imageBuffer, filename);

  const response = await fetch(`${WP_URL}/wp-json/wp/v2/media`, {
    method: 'POST',
    headers: {
      'Authorization': `Basic ${auth}`,
      'Content-Disposition': `attachment; filename="${filename}"`
    },
    body: formData
  });

  return response.json(); // { id: 123, source_url: "..." }
};
```

### Featured Image setzen

```typescript
await updatePost(postId, {
  featured_media: mediaId
});
```

## ACF Integration

### Custom Fields lesen/schreiben

```typescript
// POST mit ACF-Feldern
const postData = {
  title: "...",
  content: "...",
  acf: {
    hero_image: mediaId,
    author_bio: "Autor-Beschreibung",
    reading_time: "12 min",
    content_type: "pillar",
    related_articles: [101, 102, 103]
  }
};
```

### Typische ACF-Felder

| Feldname | Typ | Beschreibung |
|----------|-----|--------------|
| `hero_image` | Image | Hero-Bild |
| `author_bio` | Text | Autor-Info |
| `reading_time` | Text | Lesezeit |
| `table_of_contents` | WYSIWYG | Inhaltsverzeichnis |
| `schema_markup` | Textarea | JSON-LD Schema |
| `related_articles` | Relationship | Verwandte Artikel |

## SEO Meta (Yoast/RankMath)

### Yoast SEO

```typescript
meta: {
  '_yoast_wpseo_title': 'SEO Title | Brand',
  '_yoast_wpseo_metadesc': 'Meta Description...',
  '_yoast_wpseo_focuskw': 'primary keyword',
  '_yoast_wpseo_canonical': 'https://example.com/page',
  '_yoast_wpseo_opengraph-title': 'OG Title',
  '_yoast_wpseo_opengraph-description': 'OG Description',
  '_yoast_wpseo_twitter-title': 'Twitter Title',
  '_yoast_wpseo_twitter-description': 'Twitter Description'
}
```

### RankMath

```typescript
meta: {
  'rank_math_title': 'SEO Title | Brand',
  'rank_math_description': 'Meta Description...',
  'rank_math_focus_keyword': 'primary keyword',
  'rank_math_canonical_url': 'https://example.com/page',
  'rank_math_facebook_title': 'OG Title',
  'rank_math_twitter_title': 'Twitter Title'
}
```

## Taxonomien

### Kategorien zuweisen

```typescript
// Kategorie-ID finden
const categories = await fetch(`${WP_URL}/wp-json/wp/v2/categories?search=Marketing`);

// Post mit Kategorien erstellen
const postData = {
  // ...
  categories: [5, 12] // Kategorie-IDs
};
```

### Neue Kategorie erstellen

```typescript
const newCategory = await fetch(`${WP_URL}/wp-json/wp/v2/categories`, {
  method: 'POST',
  body: JSON.stringify({
    name: 'Neue Kategorie',
    slug: 'neue-kategorie',
    parent: 5 // Optional: Parent-Kategorie
  })
});
```

### Tags zuweisen

```typescript
// Tag-IDs finden oder erstellen
const tag = await fetch(`${WP_URL}/wp-json/wp/v2/tags?search=SEO`);

// Post mit Tags erstellen
const postData = {
  // ...
  tags: [10, 15, 20] // Tag-IDs
};
```

## Scheduling

### Geplante Veröffentlichung

```typescript
const postData = {
  title: "...",
  content: "...",
  status: "future",
  date: "2024-02-01T09:00:00", // UTC oder mit Timezone
  date_gmt: "2024-02-01T08:00:00" // Explizit GMT
};
```

### Zeitzone beachten

```typescript
// WordPress Timezone-Setting prüfen
const settings = await fetch(`${WP_URL}/wp-json/wp/v2/settings`);
// settings.timezone_string

// Datum entsprechend anpassen
const publishDate = new Date('2024-02-01T10:00:00');
const gmtDate = publishDate.toISOString();
```

## Error Handling

### Häufige Fehler

| Code | Bedeutung | Lösung |
|------|-----------|--------|
| 401 | Nicht autorisiert | App Password prüfen |
| 403 | Keine Berechtigung | User-Rechte prüfen |
| 404 | Nicht gefunden | Endpoint/ID prüfen |
| 400 | Bad Request | Request Body prüfen |
| 500 | Server Error | WP Logs prüfen |

### Error Response

```typescript
try {
  const response = await fetch(url, options);

  if (!response.ok) {
    const error = await response.json();
    console.error('WP Error:', error.code, error.message);
    throw new Error(`WordPress API Error: ${error.message}`);
  }

  return response.json();
} catch (error) {
  // Retry-Logik oder Fallback
}
```

## Output Format

```json
{
  "success": true,
  "post": {
    "id": 12345,
    "title": "Artikel-Titel",
    "slug": "artikel-slug",
    "status": "publish",
    "url": "https://example.com/artikel-slug",
    "date": "2024-01-15T10:00:00",
    "featured_image": {
      "id": 123,
      "url": "https://example.com/wp-content/uploads/..."
    },
    "categories": ["Marketing", "Content"],
    "tags": ["SEO", "Strategy"]
  },
  "seo": {
    "title": "SEO Title | Brand",
    "description": "Meta description...",
    "canonical": "https://example.com/artikel-slug"
  }
}
```

## Integration mit Convex

### Post-Referenz speichern

```typescript
// Nach WordPress-Publish
await ctx.db.patch(articleId, {
  wordpressPostId: wpPost.id,
  wordpressUrl: wpPost.url,
  publishedAt: new Date().toISOString(),
  status: 'published'
});
```

### Sync-Status tracken

```typescript
// Convex Schema
export const articles = defineTable({
  // ...
  wordpressPostId: v.optional(v.number()),
  wordpressUrl: v.optional(v.string()),
  wordpressSyncedAt: v.optional(v.string()),
  wordpressSyncStatus: v.union(
    v.literal('pending'),
    v.literal('synced'),
    v.literal('error')
  )
});
```

## Checkliste

### Vor dem Publish
- [ ] Content HTML validiert?
- [ ] Featured Image hochgeladen?
- [ ] Kategorien zugewiesen?
- [ ] Tags gesetzt?
- [ ] SEO Meta ausgefüllt?
- [ ] ACF Fields befüllt?
- [ ] Slug geprüft?

### Nach dem Publish
- [ ] Post-URL erreichbar?
- [ ] Featured Image sichtbar?
- [ ] Internal Links funktionieren?
- [ ] Schema Markup valide?
- [ ] Mobile Darstellung OK?
