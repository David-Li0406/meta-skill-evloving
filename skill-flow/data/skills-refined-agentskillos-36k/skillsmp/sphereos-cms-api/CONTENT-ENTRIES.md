# Content Entries

Content entries store actual content data based on content type schemas.

## IMPORTANT: Data Structure for Inline Editing

**The `data` field must use a FLAT structure.** Do NOT nest content inside a `data.data` object.

✅ **Correct (flat structure):**
```json
{
  "data": {
    "title": "Homepage",
    "hero": { "title": "Welcome" },
    "intro": { "heading": "About Us" }
  }
}
```

❌ **Wrong (nested structure - breaks inline editing):**
```json
{
  "data": {
    "title": "Homepage",
    "data": {
      "hero": { "title": "Welcome" },
      "intro": { "heading": "About Us" }
    }
  }
}
```

The inline editor looks for values at paths like `data.hero.title`. If you nest content inside `data.data`, the editor won't find the current values and fields will appear empty.

---

## Create Content Entry

```graphql
mutation CreateContentEntry($input: CreateContentEntryInput!) {
  createContentEntry(input: $input) {
    id
    slug
    data
    createdAt
    contentType { id slug name }
    organization { id name }
    property { id name }
  }
}
```

**Variables (Page Content):**
```json
{
  "input": {
    "organizationId": "org_abc123",
    "contentTypeId": "ct_page_content",
    "slug": "homepage",
    "data": {
      "title": "Homepage",
      "metaTitle": "Welcome to Our Hotel",
      "metaDescription": "Experience luxury at its finest.",
      "hero": {
        "title": "Welcome to Paradise",
        "subtitle": "Your dream vacation awaits",
        "backgroundImage": "https://cdn.example.com/hero.jpg",
        "buttonText": "Book Now",
        "buttonHref": "/reservations"
      },
      "intro": {
        "heading": "About Our Hotel",
        "paragraph": "Lorem ipsum dolor sit amet...",
        "buttonText": "Learn More",
        "buttonHref": "/about"
      }
    }
  }
}
```

**Variables (Global Navigation):**
```json
{
  "input": {
    "organizationId": "org_abc123",
    "contentTypeId": "ct_navigation",
    "slug": "global-navigation",
    "data": {
      "menuLinks": [
        { "label": "Home", "href": "/" },
        { "label": "About", "href": "/about" },
        { "label": "Rooms", "href": "/rooms" },
        { "label": "Contact", "href": "/contact" }
      ],
      "ctaButtonText": "Book Now",
      "ctaButtonUrl": "/reservations"
    }
  }
}
```

**Variables (Property-scoped):**
```json
{
  "input": {
    "organizationId": "org_abc123",
    "propertyId": "prop_xyz789",
    "contentTypeId": "ct_page_content",
    "slug": "homepage",
    "data": { "title": "Paris Hotel Homepage" }
  }
}
```

## Query Entries (Paginated & Filtered)

```graphql
query GetContentEntries($filter: ContentEntryFilterInput!) {
  contentEntries(filter: $filter) {
    items {
      id
      slug
      data
      createdAt
      updatedAt
      contentType { id slug name }
      property { id name }
    }
    pagination { total skip take hasMore }
  }
}
```

**Variables (By organization):**
```json
{
  "filter": {
    "organizationId": "org_abc123",
    "skip": 0,
    "take": 20
  }
}
```

**Variables (By content type):**
```json
{
  "filter": {
    "organizationId": "org_abc123",
    "contentTypeId": "ct_page_content",
    "skip": 0,
    "take": 20
  }
}
```

**Variables (Organization-level only):**
```json
{
  "filter": {
    "organizationId": "org_abc123",
    "orgLevelOnly": true
  }
}
```

## Query by ID

```graphql
query GetContentEntry($id: ID!) {
  contentEntry(id: $id) {
    id
    slug
    data
    contentType { id slug fields { slug name type required } }
    organization { id name }
    property { id name }
  }
}
```

## Query by Slug

```graphql
query GetContentEntryBySlug(
  $slug: String!
  $contentTypeId: ID!
  $organizationId: ID!
  $propertyId: ID
) {
  contentEntryBySlug(
    slug: $slug
    contentTypeId: $contentTypeId
    organizationId: $organizationId
    propertyId: $propertyId
  ) {
    id
    slug
    data
    contentType { id slug name }
  }
}
```

**Variables:**
```json
{
  "slug": "homepage",
  "contentTypeId": "ct_page_content",
  "organizationId": "org_abc123",
  "propertyId": null
}
```

## Update Entry

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

**Variables (Update data - merge mode, default):**
```json
{
  "id": "entry_abc123",
  "input": {
    "data": {
      "title": "Updated Homepage",
      "hero": {
        "title": "New Welcome Message"
      }
    }
  }
}
```

> **Note:** By default, data is **merged** with existing data (shallow merge at top level). Old fields are preserved unless explicitly overwritten.

**Variables (Update data - replace mode):**
```json
{
  "id": "entry_abc123",
  "input": {
    "replaceData": true,
    "data": {
      "title": "New Homepage",
      "hero": { "title": "Welcome" },
      "intro": { "heading": "About" }
    }
  }
}
```

> **Note:** With `replaceData: true`, the entire `data` field is **replaced**. All old fields are removed and only the new data is stored. Use this to clean up stale fields or restructure content.

**Variables (Update slug):**
```json
{
  "id": "entry_abc123",
  "input": { "slug": "home" }
}
```

## Delete Entry

```graphql
mutation DeleteContentEntry($id: ID!) {
  deleteContentEntry(id: $id)
}
```

## Global Entry Slugs

| Content Type | Slug | Purpose |
|--------------|------|---------|
| Site Settings | `global-settings` | Logo, contact, social |
| Navigation | `global-navigation` | Menu links, CTA |
| Footer | `global-footer` | Footer content |
| 404 Page | `404` | Error page |
