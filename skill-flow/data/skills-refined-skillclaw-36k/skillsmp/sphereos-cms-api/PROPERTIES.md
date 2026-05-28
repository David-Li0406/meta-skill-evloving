# Properties

## Create Property

```graphql
mutation CreateProperty($input: CreatePropertyInput!) {
  createProperty(input: $input) {
    id
    slug
    name
    settings
    createdAt
    organization { id name }
  }
}
```

**Variables:**
```json
{
  "input": {
    "organizationId": "org_abc123",
    "name": "The Ritz - Paris",
    "slug": "ritz-paris",
    "settings": {
      "timezone": "Europe/Paris",
      "defaultLanguage": "fr",
      "address": {
        "street": "15 Place Vendome",
        "city": "Paris",
        "postalCode": "75001",
        "country": "France"
      },
      "coordinates": { "lat": 48.8682, "lng": 2.3292 }
    }
  }
}
```

## Query by Organization

```graphql
query GetPropertiesByOrganization($organizationId: ID!) {
  propertiesByOrganization(organizationId: $organizationId) {
    id
    slug
    name
    settings
  }
}
```

## Query by ID

```graphql
query GetProperty($id: ID!) {
  property(id: $id) {
    id
    slug
    name
    settings
    organization { id name slug }
  }
}
```

## Query by Slugs

```graphql
query GetPropertyBySlug($organizationSlug: String!, $propertySlug: String!) {
  propertyBySlug(organizationSlug: $organizationSlug, propertySlug: $propertySlug) {
    id
    slug
    name
    settings
    organization { id name }
  }
}
```

**Variables:**
```json
{
  "organizationSlug": "luxury-hotels-intl",
  "propertySlug": "ritz-paris"
}
```

## Update Property

```graphql
mutation UpdateProperty($input: UpdatePropertyInput!) {
  updateProperty(input: $input) {
    id
    slug
    name
    settings
    updatedAt
  }
}
```

## Delete Property

```graphql
mutation DeleteProperty($id: ID!) {
  deleteProperty(id: $id)
}
```
