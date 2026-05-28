# Organizations

## Create Organization

```graphql
mutation CreateOrganization($input: CreateOrganizationInput!) {
  createOrganization(input: $input) {
    id
    slug
    name
    settings
    createdAt
  }
}
```

**Variables:**
```json
{
  "input": {
    "name": "Luxury Hotels International",
    "slug": "luxury-hotels-intl",
    "settings": {
      "timezone": "America/New_York",
      "defaultLanguage": "en",
      "defaultCurrency": "USD",
      "brandColors": {
        "primary": "#1a365d",
        "secondary": "#2d3748"
      }
    }
  }
}
```

## Query All Organizations

```graphql
query GetOrganizations {
  organizations {
    id
    slug
    name
    settings
    properties { id name slug }
  }
}
```

## Query by ID

```graphql
query GetOrganization($id: ID!) {
  organization(id: $id) {
    id
    slug
    name
    settings
    properties { id name slug settings }
  }
}
```

## Query by Slug

```graphql
query GetOrganizationBySlug($slug: String!) {
  organizationBySlug(slug: $slug) {
    id
    slug
    name
    settings
    properties { id name slug }
  }
}
```

## Update Organization

```graphql
mutation UpdateOrganization($input: UpdateOrganizationInput!) {
  updateOrganization(input: $input) {
    id
    slug
    name
    settings
    updatedAt
  }
}
```

**Variables:**
```json
{
  "input": {
    "id": "org_abc123",
    "name": "Luxury Hotels International Group",
    "settings": { "timezone": "America/Los_Angeles" }
  }
}
```

## Delete Organization

Cascades to all properties.

```graphql
mutation DeleteOrganization($id: ID!) {
  deleteOrganization(id: $id)
}
```
