# Content Types

Content types define the schema for content entries.

## Create Content Type

```graphql
mutation CreateContentType($input: CreateContentTypeInput!) {
  createContentType(input: $input) {
    id
    slug
    name
    description
    icon
    isSystem
    createdAt
    fields {
      id
      slug
      name
      type
      required
      localized
      unique
      sortOrder
      description
      defaultValue
      validation
      uiConfig
    }
  }
}
```

**Variables:**
```json
{
  "input": {
    "organizationId": "org_abc123",
    "slug": "page-content",
    "name": "Page Content",
    "description": "Generic page content with flexible JSON data",
    "icon": "document",
    "fields": [
      {
        "slug": "title",
        "name": "Title",
        "type": "TEXT",
        "required": true,
        "sortOrder": 0,
        "validation": { "maxLength": 200 }
      },
      {
        "slug": "data",
        "name": "Page Data",
        "type": "JSON",
        "required": true,
        "sortOrder": 1
      },
      {
        "slug": "metaTitle",
        "name": "Meta Title",
        "type": "TEXT",
        "sortOrder": 2,
        "validation": { "maxLength": 60 }
      },
      {
        "slug": "metaDescription",
        "name": "Meta Description",
        "type": "TEXT",
        "sortOrder": 3,
        "validation": { "maxLength": 160 },
        "uiConfig": { "inputType": "textarea" }
      }
    ]
  }
}
```

## Query All Content Types

```graphql
query GetContentTypes($pagination: PaginationInput) {
  contentTypes(pagination: $pagination) {
    items {
      id
      slug
      name
      description
      icon
      isSystem
      entryCount
      fields { id slug name type required }
    }
    pagination { total skip take hasMore }
  }
}
```

## Query by Organization

```graphql
query GetContentTypesByOrganization($organizationId: ID!) {
  contentTypesByOrganization(organizationId: $organizationId) {
    id
    slug
    name
    entryCount
    fields { id slug name type required sortOrder }
  }
}
```

## Query by Slug

```graphql
query GetContentTypeBySlug($slug: String!, $organizationId: ID) {
  contentTypeBySlug(slug: $slug, organizationId: $organizationId) {
    id
    slug
    name
    description
    fields { id slug name type required sortOrder }
  }
}
```

## Update Content Type

```graphql
mutation UpdateContentType($input: UpdateContentTypeInput!) {
  updateContentType(input: $input) {
    id
    slug
    name
    description
    icon
    updatedAt
  }
}
```

## Add Fields

```graphql
mutation AddFieldsToContentType($input: AddFieldsInput!) {
  addFieldsToContentType(input: $input) {
    id
    fields { id slug name type sortOrder }
  }
}
```

**Variables:**
```json
{
  "input": {
    "contentTypeId": "ct_abc123",
    "fields": [
      {
        "slug": "publishedAt",
        "name": "Published At",
        "type": "DATE",
        "sortOrder": 10
      }
    ]
  }
}
```

## Update Fields

```graphql
mutation UpdateContentTypeFields($input: UpdateFieldsInput!) {
  updateContentTypeFields(input: $input) {
    id
    fields { id slug name type required sortOrder validation }
  }
}
```

## Remove Fields

```graphql
mutation RemoveFieldsFromContentType($input: RemoveFieldsInput!) {
  removeFieldsFromContentType(input: $input) {
    id
    fields { id slug name }
  }
}
```

## Delete Content Type

```graphql
mutation DeleteContentType($id: ID!) {
  deleteContentType(id: $id)
}
```

## Field Types

| Type | Description | Validation Options |
|------|-------------|-------------------|
| `TEXT` | Single-line text | `minLength`, `maxLength`, `pattern` |
| `RICH_TEXT` | HTML rich text | `maxLength` |
| `NUMBER` | Numeric value | `min`, `max`, `step` |
| `BOOLEAN` | True/false | - |
| `DATE` | Date/datetime | `minDate`, `maxDate` |
| `SELECT` | Single selection | `options: [{value, label}]` |
| `MEDIA` | Media reference | `allowedMimeTypes: string[]` |
| `REFERENCE` | Content reference | `referenceType: string` |
| `JSON` | Arbitrary JSON | `schema: JSONSchema` |
