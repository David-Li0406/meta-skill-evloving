# Media Assets

## Upload Media

Upload a file as base64-encoded data.

```graphql
mutation UploadMedia($input: UploadMediaInput!) {
  uploadMedia(input: $input) {
    id
    filename
    mimeType
    size
    width
    height
    alt
    createdAt
    variants {
      original
      thumbnail
      medium
      large
    }
  }
}
```

**Variables:**
```json
{
  "input": {
    "organizationId": "org_abc123",
    "propertyId": null,
    "filename": "hero-image.jpg",
    "mimeType": "image/jpeg",
    "alt": "Hotel hero image",
    "base64Data": "/9j/4AAQSkZJRgABAQEASABIAAD/4QBMRXhpZgAATU0AKgAAAA..."
  }
}
```

## Query Media Assets

```graphql
query GetMediaAssets($filter: MediaFilterInput!, $pagination: PaginationInput) {
  mediaAssets(filter: $filter, pagination: $pagination) {
    items {
      id
      filename
      mimeType
      size
      width
      height
      alt
      variants { original thumbnail medium large }
      property { id name }
    }
    pagination { total skip take hasMore }
  }
}
```

**Variables (All images):**
```json
{
  "filter": {
    "organizationId": "org_abc123",
    "mimeTypePrefix": "image/"
  },
  "pagination": { "skip": 0, "take": 20 }
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

**Variables (Property-specific):**
```json
{
  "filter": {
    "organizationId": "org_abc123",
    "propertyId": "prop_xyz789"
  }
}
```

## MIME Type Prefixes

- `image/` - Images (JPEG, PNG, GIF, WebP, SVG)
- `video/` - Videos
- `audio/` - Audio files
- `text/` - Text files
- `application/` - Documents (PDF, etc.)
- `font/` - Font files

## Query by ID

```graphql
query GetMediaAsset($id: ID!) {
  mediaAsset(id: $id) {
    id
    filename
    mimeType
    size
    width
    height
    alt
    variants { original thumbnail medium large }
    organization { id name }
    property { id name }
  }
}
```

## Update Metadata

```graphql
mutation UpdateMediaAsset($id: ID!, $input: UpdateMediaInput!) {
  updateMediaAsset(id: $id, input: $input) {
    id
    filename
    alt
    updatedAt
  }
}
```

**Variables:**
```json
{
  "id": "media_abc123",
  "input": {
    "filename": "hero-background.jpg",
    "alt": "Panoramic view of the hotel pool"
  }
}
```

## Delete Media

```graphql
mutation DeleteMediaAsset($id: ID!) {
  deleteMediaAsset(id: $id)
}
```
