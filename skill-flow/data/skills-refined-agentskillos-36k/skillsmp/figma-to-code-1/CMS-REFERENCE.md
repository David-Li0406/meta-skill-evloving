# CMS Content Type Reference

> **NOTE:** Create content types ONLY for what exists in YOUR Figma designs.

## Global Content Types

| Content Type | Slug | Entry Slug | Purpose |
|--------------|------|------------|---------|
| Site Settings | `site-settings` | `global-settings` | Logo, contact info |
| Navigation | `site-navigation` | `global-navigation` | Menu links, CTA |
| Footer | `site-footer` | `global-footer` | Footer content |

## Page Content Type

| Content Type | Slug | Entry Slug | Purpose |
|--------------|------|------------|---------|
| Page Content | `page-content` | Use page slug (e.g., `home`, `about`) | All page content |

## Collection Content Types (Create If Needed)

| Content Type | Slug | When to Create |
|--------------|------|----------------|
| FAQ Item | `faq-item` | FAQ section in Figma |
| Team Member | `team-member` | Team section in Figma |
| Product | `product` | Product listings in Figma |
| Testimonial | `testimonial` | Testimonials in Figma |
| Blog Post | `blog-post` | Blog in Figma |

## Content Type Field Types

| Type | Use For |
|------|---------|
| `string` | Short text, titles |
| `text` | Long text, paragraphs |
| `json` | Arrays, objects |
| `number` | Prices, quantities |
| `boolean` | Toggles, flags |
| `date` | Dates, times |
| `media` | Images, files |

## Example Content Type Definition

```typescript
await createOrUpdateContentType('site-settings', 'Site Settings', [
  { slug: 'logoUrl', name: 'Logo URL', type: 'string', required: true },
  { slug: 'logoAlt', name: 'Logo Alt', type: 'string', required: true },
  { slug: 'address', name: 'Address', type: 'string' },
  { slug: 'phone', name: 'Phone', type: 'string' },
  { slug: 'email', name: 'Email', type: 'string' },
  { slug: 'socialLinks', name: 'Social Links', type: 'json' },
]);
```

## Example Page Content Structure

```json
{
  "metaTitle": "Brand | Page Title",
  "metaDescription": "Page description",
  "data": {
    "hero": {
      "title": "Hero Title",
      "subtitle": "Hero subtitle",
      "buttonText": "CTA Text",
      "buttonHref": "/contact",
      "imageSrc": "https://cdn.example.com/hero.webp"
    },
    "sections": [
      {
        "heading": "Section Heading",
        "content": "Section content"
      }
    ]
  }
}
```
