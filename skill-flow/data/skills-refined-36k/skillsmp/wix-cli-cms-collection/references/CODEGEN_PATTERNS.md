# Wix CLI-Specific Patterns and Constraints

Additional patterns, constraints, and best practices for CMS collections in Wix CLI apps.

**Main constraints:** See [SKILL.md](../SKILL.md#wix-cli-specific-constraints) for embedded script parameters vs collections and site widget settings vs collections.

## Configuration vs Data Collections

### Configuration Collections

**Configuration collections are for:**

- Static or hardcoded behaviors
- Reference data that rarely changes
- Default settings that need to be stored

**Guidelines:**

- At most create one minimal read-only configuration collection only when strictly necessary
- Prefer embedded script parameters or widget panels for configuration
- Only use collections for configuration when it's multi-record relational data

### Data Collections

**Data collections are for:**

- Business entities (products, orders, customers)
- User-generated content (reviews, comments, submissions)
- Transactional data (events, logs, history)
- Multi-record relational data

**Guidelines:**

- Create collections for persistent data that accumulates over time
- Use collections for data that needs to be queried, filtered, or related to other data

## Reference Field Constraints

**Main constraints:** See [SKILL.md](../SKILL.md#relationships) for the critical constraints on REFERENCE and MULTI_REFERENCE fields.

### Example: Correct Reference Usage

**CORRECT:**

```json
{
  "collections": [
    {
      "idSuffix": "blog-posts",
      "fields": [
        {
          "key": "author",
          "type": "REFERENCE",
          "referenceOptions": {
            "referencedCollectionId": "authors"
          }
        }
      ]
    },
    {
      "idSuffix": "authors",
      "fields": [...]
    }
  ]
}
```

Both collections are defined in the same plan, so the reference is valid.

### Example: Incorrect Reference Usage

**WRONG:**

```json
{
  "key": "product",
  "type": "REFERENCE",
  "referenceOptions": {
    "referencedCollectionId": "Products"
  }
}
```

"Products" is a Wix business entity, not a custom collection. Use the Wix Stores API instead.

## App Namespace Scoping

### Collection ID Scoping

Collections are automatically scoped with the app namespace:

- Collection `idSuffix`: `"products"`
- App namespace: `"my-app"`
- Final collection ID: `"my-app/products"`

This prevents conflicts between collections from different apps.

### Reference Collection IDs

When referencing collections, use the `idSuffix` (not the full scoped ID):

```json
{
  "key": "category",
  "type": "REFERENCE",
  "referenceOptions": {
    "referencedCollectionId": "categories" // Use idSuffix, not "my-app/categories"
  }
}
```

The system automatically resolves the scoped ID.

## When to Create Collections

### Create Collections When:

1. **Blueprint explicitly requests persistent data**
2. **Business entities need to be stored** (products, orders, inventory)
3. **User-generated content** (reviews, comments, submissions)
4. **Multi-record relational data** that is NOT configuration
5. **Event logs** (if explicitly requested for analytics/tracking)

### Do NOT Create Collections When:

1. **Blueprint doesn't request persistent data**
2. **Embedded script configuration** → use embedded script parameters
3. **Site widget configuration** → use widget settings panel
4. **Static/hardcoded behaviors** → code it, don't store it
5. **Single configuration values** → use parameters or settings
6. **Audit/transaction/log collections** (unless explicitly requested)

## Initial Data Guidelines

### When to Include Initial Data

**Include `initialData` when:**

- Blueprint mentions example items, sample data, or default configurations
- Collection represents configuration or reference data that needs default values
- Blueprint describes a demo or example use case that requires sample records

### When NOT to Include Initial Data

**Do NOT include `initialData` when:**

- Collection is for user-generated content that starts empty
- Blueprint doesn't mention any example or default data
- Collection is for transactional/log data that accumulates over time

### Initial Data Compliance

**Each item in `initialData` MUST strictly comply with the collection schema:**

- Use exact field keys defined in the schema (lowerCamelCase)
- Match field types exactly (TEXT → string, NUMBER → number, BOOLEAN → boolean)
- DATE/DATETIME → ISO 8601 string
- For REFERENCE fields: provide valid reference ID of `idSuffix` of the referenced collection
- For required fields: always provide values
- For optional fields: may omit if not needed for the example

**Example:**

```json
{
  "idSuffix": "handling-fees",
  "fields": [
    { "key": "title", "type": "TEXT" },
    { "key": "amount", "type": "NUMBER" }
  ],
  "initialData": [
    {
      "title": "Handling Fee",
      "amount": 5
    },
    {
      "title": "Gift Wrapping",
      "amount": 3.5
    }
  ]
}
```

## Field Naming Conventions

### Field Keys

- **Format:** `lowerCamelCase`
- **Characters:** ASCII only
- **Examples:** `productName`, `isActive`, `createdAt`

### Collection IDs (idSuffix)

- **Format:** `lower-kebab-case` or `lower_underscore`
- **Avoid:** Spaces, uppercase, special characters
- **Examples:** `product-categories`, `blog_posts`, `handling-fees`

### Display Names

- **Format:** Human-readable, can contain spaces
- **Examples:** `"Product Name"`, `"Is Active"`, `"Created At"`

## Common Anti-Patterns to Avoid

### ❌ Don't Create Aggregated Fields

**WRONG:**

```json
{
  "key": "averageRating",
  "type": "NUMBER"
}
```

If you have individual `rating` fields, calculate the average dynamically. Don't store aggregated values.

### ❌ Don't Duplicate Configuration

**WRONG:**

- Embedded script parameters: `{ headline: "...", color: "..." }`
- CMS collection: `popup-configurations` with same data

**CORRECT:**

- Only embedded script parameters

### ❌ Don't Create Collections for Single Values

**WRONG:**

```json
{
  "idSuffix": "app-settings",
  "fields": [{ "key": "theme", "type": "TEXT" }]
}
```

For single configuration values, use embedded script parameters or widget settings.

### ✅ Do Create Collections for Multi-Record Data

**CORRECT:**

```json
{
  "idSuffix": "product-categories",
  "fields": [
    { "key": "name", "type": "TEXT" },
    { "key": "description", "type": "TEXT" }
  ]
}
```

Multiple categories that need to be managed → use a collection.
