---
name: sphereos-cms-api
description: SphereOS CMS GraphQL API reference. Use when making CMS API calls, creating content types, managing content entries, uploading media, or handling authentication. Complete query and mutation reference.
version: 1.0.0
author: SphereOS
license: MIT
tags: [GraphQL, CMS, Headless CMS, API, Content Management, Authentication]
dependencies: []
allowed-tools: Read, Bash, WebFetch
github-repo: gautam-lulla/claude-skills
skill-path: sos-api
---

## FIRST: Check for Updates

**Before proceeding, check if a newer version is available:**

1. Read local version from `~/.claude/skills/sos-api/SKILL.md` frontmatter
2. Fetch remote version: `https://raw.githubusercontent.com/gautam-lulla/claude-skills/main/sos-api/SKILL.md`
3. Compare the `version:` field in both

**If remote version > local version**, use AskUserQuestion:
- Question: "A newer version of sos-api is available. Current: [local] → Latest: [remote]. What would you like to do?"
- Options:
  1. "Update and continue (Recommended)"
  2. "Continue with current version"
  3. "View changelog"

**If user selects "Update and continue":**
- Fetch all .md files from `https://raw.githubusercontent.com/gautam-lulla/claude-skills/main/sos-api/`
- Save to `~/.claude/skills/sos-api/`
- Confirm: "Updated sos-api to version [X]. Proceeding..."

**If user selects "View changelog":**
- Fetch and display `https://raw.githubusercontent.com/gautam-lulla/claude-skills/main/sos-api/CHANGELOG.md`
- Then ask again

**If versions match**, proceed silently (no prompt).

---

# SphereOS CMS — GraphQL API Reference

Complete reference for all GraphQL queries and mutations available in the SphereOS Headless CMS.

## When to Use This Skill

**Use SphereOS CMS API when:**
- Authenticating with the CMS (login, tokens)
- Creating or managing organizations and properties
- Defining content types with field schemas
- Creating, updating, or querying content entries
- Uploading media assets (images, files)
- Managing users, roles, and permissions
- Handling API errors

**Key capabilities:**
- **Authentication**: JWT-based auth with refresh tokens
- **Content Types**: Define custom schemas with typed fields
- **Content Entries**: CRUD operations with slug-based lookups
- **Media Management**: Upload and query media assets
- **Multi-tenancy**: Organizations and properties support

## Base URL

- **Local Development:** `http://localhost:3001/graphql`
- **Production:** `https://backend-production-162b.up.railway.app/graphql`

## Authentication

All requests (except `login`) require a valid JWT access token:

```
Authorization: Bearer <access_token>
```

## Quick Reference

| Operation | Reference File |
|-----------|----------------|
| Login, Logout, Token Refresh | [AUTH.md](AUTH.md) |
| Organizations | [ORGANIZATIONS.md](ORGANIZATIONS.md) |
| Properties | [PROPERTIES.md](PROPERTIES.md) |
| Users & Roles | [USERS-ROLES.md](USERS-ROLES.md) |
| Content Types | [CONTENT-TYPES.md](CONTENT-TYPES.md) |
| Content Entries | [CONTENT-ENTRIES.md](CONTENT-ENTRIES.md) |
| Media Assets | [MEDIA.md](MEDIA.md) |
| Error Handling | [ERRORS.md](ERRORS.md) |

---

## Common Operations Quick Reference

### Authenticate

```graphql
mutation Login($input: LoginInput!) {
  login(input: $input) {
    accessToken
    refreshToken
    user { id email }
  }
}
```

### Get Content Entry by Slug

```graphql
query GetContentEntryBySlug($slug: String!, $contentTypeId: ID!, $organizationId: ID!) {
  contentEntryBySlug(slug: $slug, contentTypeId: $contentTypeId, organizationId: $organizationId) {
    id
    slug
    data
  }
}
```

### Create Content Entry

```graphql
mutation CreateContentEntry($input: CreateContentEntryInput!) {
  createContentEntry(input: $input) {
    id
    slug
    data
  }
}
```

### Update Content Entry

```graphql
mutation UpdateContentEntry($id: ID!, $input: UpdateContentEntryInput!) {
  updateContentEntry(id: $id, input: $input) {
    id
    slug
    data
    updatedAt
  }
}
```

### Create Content Type

```graphql
mutation CreateContentType($input: CreateContentTypeInput!) {
  createContentType(input: $input) {
    id
    slug
    name
    fields { slug name type required }
  }
}
```

---

## Global Content Entry Slugs

| Content Type | Recommended Slug | Purpose |
|--------------|------------------|---------|
| Site Settings | `global-settings` | Logo, contact info, social links |
| Navigation | `global-navigation` | Menu links, CTA buttons |
| Footer | `global-footer` | Footer links, newsletter, copyright |
| 404 Page | `404` | Error page content |

---

## Field Types

| Type | Description |
|------|-------------|
| `TEXT` | Single-line text |
| `RICH_TEXT` | HTML rich text |
| `NUMBER` | Numeric value |
| `BOOLEAN` | True/false |
| `DATE` | Date/datetime |
| `SELECT` | Single selection |
| `MEDIA` | Media reference |
| `REFERENCE` | Content reference |
| `JSON` | Arbitrary JSON |

---

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `BAD_REQUEST` | 400 | Invalid input |
| `UNAUTHENTICATED` | 401 | Missing/invalid token |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `CONFLICT` | 409 | Duplicate slug |

---

## Website Build Workflow

1. **Authenticate** → `login` mutation
2. **Get organization** → `organizationBySlug` query
3. **Create content types** → `createContentType` mutation
4. **Create entries** → `createContentEntry` mutation
5. **Upload media** → `uploadMedia` mutation
6. **Fetch for rendering** → `contentEntryBySlug` query

For detailed examples, see the reference files linked above.

---

## Inline Editor Integration

To enable inline editing, create a client component that loads the script only when `?edit=true` is in the URL:

```tsx
// src/components/InlineEditorLoader.tsx
'use client';

import { useEffect } from 'react';
import { useSearchParams } from 'next/navigation';

export function InlineEditorLoader({ orgSlug }: { orgSlug: string }) {
  const searchParams = useSearchParams();
  const isEditMode = searchParams.get('edit') === 'true';

  useEffect(() => {
    if (!isEditMode) return;
    if (document.querySelector('script[data-cms-editor]')) return;

    const script = document.createElement('script');
    script.src = 'https://backend-production-162b.up.railway.app/inline-editor.js';
    script.dataset.cmsOrg = orgSlug;
    script.dataset.cmsApi = 'https://backend-production-162b.up.railway.app';
    script.dataset.cmsAdmin = 'https://sphereos.vercel.app';
    script.dataset.cmsEditor = 'true';
    script.defer = true;
    document.head.appendChild(script);
  }, [isEditMode, orgSlug]);

  return null;
}
```

Then in `layout.tsx`:
```tsx
<Suspense fallback={null}>
  <InlineEditorLoader orgSlug="your-org-slug" />
</Suspense>
```

**Required data attributes on editable elements:**

| Attribute | Required | Description |
|-----------|----------|-------------|
| `data-cms-entry` | Yes | Entry slug (e.g., `"homepage"`, `"global-footer"`) |
| `data-cms-field` | Yes | Dot-notation path (e.g., `"hero.title"`, `"links[0].label"`) |
| `data-cms-type` | Optional | Override type: `text`, `richtext`, `image`, `array` |

**IMPORTANT:** For image fields, always use `data-cms-type="image"`. Do NOT use `"url"` — that will show a text input instead of the image picker UI.

**Example:**
```html
<h1 data-cms-entry="homepage" data-cms-field="hero.title">Welcome</h1>
<img data-cms-entry="homepage" data-cms-field="hero.image" data-cms-type="image" src="..." />

<!-- For Next.js Image in a wrapper div -->
<div data-cms-entry="homepage" data-cms-field="hero.image" data-cms-type="image">
  <Image src={imageSrc} alt="" fill />
</div>
```

The inline editor requires authentication. Visit your site with `?edit=true` to trigger the login flow.

### Inline Editor Image Save Format

**IMPORTANT:** The inline editor saves images as objects, not plain URL strings:

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

**Frontend Requirement:** Your website's content layer MUST transform these image objects to plain URL strings before passing to components. Without this transformation, images will display in the editor but NOT on the live site after refresh.

See the `figma-to-code` skill LEARNINGS.md for the complete `transformImageUrls()` implementation pattern.

**Quick reference - content layer must include:**
```typescript
function isImageObject(obj: unknown): obj is { url?: string; src?: string } {
  if (typeof obj !== 'object' || obj === null) return false;
  const o = obj as Record<string, unknown>;
  return (typeof o.url === 'string' || typeof o.src === 'string') &&
    (o.id !== undefined || o.filename !== undefined || o.alt !== undefined);
}

function transformImageUrls<T>(data: T): T {
  // ... recursive function that extracts URLs from image objects
  // See figma-to-code LEARNINGS.md for full implementation
}
```

---

## Common Pitfalls to Avoid

❌ **Don't:**
- Forget to include the Authorization header on authenticated requests
- Use expired tokens without refreshing them first
- Create content entries without first creating the content type
- Use duplicate slugs within the same content type and organization
- Upload media without specifying the correct MIME type
- Assume field names — always check the content type schema
- **CRITICAL: Nest content inside a `data` property** — this breaks inline editing!
- Assume inline editor images are strings — they're objects with `{id, url, src, alt, filename}`
- Skip the `transformImageUrls()` function in your content layer — images won't display

✅ **Do:**
- Store and refresh JWT tokens before they expire
- Use `contentEntryBySlug` for public-facing lookups
- Create content types with clear, consistent field naming
- Use unique slugs that are URL-friendly (lowercase, hyphens)
- Handle errors by checking the `extensions.code` field
- Use the appropriate field type (TEXT, RICH_TEXT, MEDIA, etc.)
- **Use FLAT data structure** — all sections at top level of `data` object
- **Transform image objects to URLs** in your content layer before rendering
- Test inline editor saves by refreshing the page after saving

### Data Structure for Inline Editing

The inline editor looks for values at paths like `entry.data.hero.title`. If you nest content inside `data.data`, the editor won't find current values.

✅ **Correct:**
```json
{ "data": { "hero": { "title": "Welcome" }, "intro": { "heading": "About" } } }
```

❌ **Wrong:**
```json
{ "data": { "data": { "hero": { "title": "Welcome" } } } }
```

---

## Version History

**v1.1.0** (January 2026)
- Added inline editor image object format documentation
- Added `transformImageUrls()` pattern requirement for frontends
- Documented `normalizeFieldPath()` backend fix for nested data structures
- Updated pitfalls with image handling requirements

**v1.0.0** (January 2025)
- Initial skill release
- Complete GraphQL query/mutation reference
- Modular reference files for each domain
- Error handling documentation
