# Field Types Reference

Complete documentation of all field types supported in Wix CMS collections for Wix CLI apps.

## Basic Types

### TEXT

Single-line text field.

**Use cases:** Names, titles, email addresses, short descriptions, slugs

**Example:**

```json
{
  "key": "productName",
  "displayName": "Product Name",
  "type": "TEXT"
}
```

**Constraints:**

- Field keys must be lowerCamelCase and ASCII
- No length limit specified

### NUMBER

Decimal number field.

**Use cases:** Prices, quantities, ratings, measurements, counts

**Example:**

```json
{
  "key": "price",
  "displayName": "Price",
  "type": "NUMBER"
}
```

**Constraints:**

- Supports decimal values
- No explicit min/max limits

### BOOLEAN

True/false field.

**Use cases:** Toggles, flags, active/inactive status, feature toggles

**Example:**

```json
{
  "key": "isActive",
  "displayName": "Is Active",
  "type": "BOOLEAN"
}
```

### DATE

Date only (without time).

**Use cases:** Birthdays, event dates, deadlines, anniversaries

**Example:**

```json
{
  "key": "eventDate",
  "displayName": "Event Date",
  "type": "DATE"
}
```

**Format:** ISO 8601 date string (YYYY-MM-DD)

### DATETIME

Date with time.

**Use cases:** Timestamps, event start times, creation dates, deadlines with time

**Example:**

```json
{
  "key": "createdAt",
  "displayName": "Created At",
  "type": "DATETIME"
}
```

**Format:** ISO 8601 datetime string

### TIME

Time only (without date).

**Use cases:** Schedules, opening hours, time-based events

**Example:**

```json
{
  "key": "openingTime",
  "displayName": "Opening Time",
  "type": "TIME"
}
```

## Media Types

### IMAGE

Single image file.

**Use cases:** Thumbnails, profile pictures, featured images, product images

**Example:**

```json
{
  "key": "featuredImage",
  "displayName": "Featured Image",
  "type": "IMAGE"
}
```

### VIDEO

Video file.

**Use cases:** Video content, tutorials, media galleries

**Example:**

```json
{
  "key": "introVideo",
  "displayName": "Intro Video",
  "type": "VIDEO"
}
```

### AUDIO

Audio file.

**Use cases:** Podcasts, music, sound effects, voice recordings

**Example:**

```json
{
  "key": "podcastEpisode",
  "displayName": "Podcast Episode",
  "type": "AUDIO"
}
```

### DOCUMENT

File attachment (PDF, Word, etc.).

**Use cases:** PDFs, documents, downloadable files

**Example:**

```json
{
  "key": "contract",
  "displayName": "Contract Document",
  "type": "DOCUMENT"
}
```

### MEDIA_GALLERY

Multiple media files (images, videos, etc.).

**Use cases:** Product galleries, photo albums, media collections

**Example:**

```json
{
  "key": "productImages",
  "displayName": "Product Images",
  "type": "MEDIA_GALLERY"
}
```

## Rich Content Types

### RICH_TEXT

Formatted HTML text.

**Use cases:** Blog content, descriptions with formatting, articles

**Example:**

```json
{
  "key": "articleContent",
  "displayName": "Article Content",
  "type": "RICH_TEXT"
}
```

### RICH_CONTENT

Rich content with embedded media and formatting.

**Use cases:** Complex content with embedded media, rich blog posts

**Example:**

```json
{
  "key": "blogPost",
  "displayName": "Blog Post",
  "type": "RICH_CONTENT"
}
```

## Array Types

### ARRAY

Array of values (generic).

**Use cases:** Flexible arrays of mixed types

**Example:**

```json
{
  "key": "metadata",
  "displayName": "Metadata",
  "type": "ARRAY"
}
```

### ARRAY_STRING

Array of strings.

**Use cases:** Tags, categories list, string arrays

**Example:**

```json
{
  "key": "tags",
  "displayName": "Tags",
  "type": "ARRAY_STRING"
}
```

### ARRAY_DOCUMENT

Array of document references.

**Use cases:** Multiple file attachments, document collections

**Example:**

```json
{
  "key": "attachments",
  "displayName": "Attachments",
  "type": "ARRAY_DOCUMENT"
}
```

## Reference Types

### REFERENCE

Link to one item in another collection.

**Use cases:** One-to-one or many-to-one relationships

**Example:**

```json
{
  "key": "author",
  "displayName": "Author",
  "type": "REFERENCE",
  "referenceOptions": {
    "referencedCollectionId": "authors"
  }
}
```

**CRITICAL CONSTRAINTS:**

- **ONLY use REFERENCE fields when linking between custom CMS collections defined within this app**
- The `referencedCollectionId` MUST be the `idSuffix` of another collection you are creating in the same plan
- **NEVER use REFERENCE fields to link to Wix business entities** (Products, Orders, Contacts, Members, etc.)
- Only for relationships between your custom collections

### MULTI_REFERENCE

Link to many items in another collection.

**Use cases:** Many-to-many relationships, tags, categories

**Example:**

```json
{
  "key": "categories",
  "displayName": "Categories",
  "type": "MULTI_REFERENCE",
  "multiReferenceOptions": {
    "referencedCollectionId": "categories"
  }
}
```

**CRITICAL CONSTRAINTS:**

- Same constraints as REFERENCE
- **ONLY between custom CMS collections in your app**
- **NEVER to Wix business entities**

## Special Types

### URL

URL validation field.

**Use cases:** Links, external URLs, website addresses

**Example:**

```json
{
  "key": "websiteUrl",
  "displayName": "Website URL",
  "type": "URL"
}
```

### ADDRESS

Structured address field.

**Use cases:** Physical addresses, locations, shipping addresses

**Example:**

```json
{
  "key": "shippingAddress",
  "displayName": "Shipping Address",
  "type": "ADDRESS"
}
```

### PAGE_LINK

Link to a Wix page.

**Use cases:** Internal navigation, page references

**Example:**

```json
{
  "key": "landingPage",
  "displayName": "Landing Page",
  "type": "PAGE_LINK"
}
```

### LANGUAGE

Language code field.

**Use cases:** Multi-language content, language selection

**Example:**

```json
{
  "key": "contentLanguage",
  "displayName": "Content Language",
  "type": "LANGUAGE"
}
```

### OBJECT

JSON object field (flexible structure).

**Use cases:** Flexible data structures, metadata, custom objects

**CRITICAL:** When using `type: "OBJECT"`, you **MUST** include the `objectOptions` property, even if it's an empty object.

**Example:**

```json
{
  "key": "customData",
  "displayName": "Custom Data",
  "type": "OBJECT",
  "objectOptions": {
    "fields": [
      {
        "key": "string",
        "displayName": "A random string",
        "type": "TEXT"
      }
    ]
  }
}
```

**Minimum required format:**

```json
{
  "key": "triggerRules",
  "displayName": "Trigger Rules",
  "type": "OBJECT",
  "objectOptions": {}
}
```

**Note:** The `objectOptions` property is required by the Wix API validation. Use an empty object `{}` if you don't need to define a specific schema structure.

### ANY

Any type (most flexible).

**Use cases:** Truly flexible fields where type is unknown

**Example:**

```json
{
  "key": "flexibleField",
  "displayName": "Flexible Field",
  "type": "ANY"
}
```

## Field Properties

All field types support these optional properties:

- `key` (required): Field identifier in lowerCamelCase
- `displayName` (required): Human-readable label
- `type` (required): One of the field types above
- `description` (optional): Help text or documentation
- `required` (optional): Whether the field must have a value
- `unique` (optional): Whether values must be unique across items

## Field Naming Conventions

- **Field keys:** Must be `lowerCamelCase` and ASCII only
- **Display names:** Human-readable, can contain spaces and special characters
- **Collection IDs:** Use `lower-kebab-case` or `lower_underscore` (e.g., `product-categories` or `product_categories`)

## Complete Field Types List

All supported field types (in alphabetical order):

1. ADDRESS
2. ANY
3. ARRAY
4. ARRAY_DOCUMENT
5. ARRAY_STRING
6. AUDIO
7. BOOLEAN
8. DATE
9. DATETIME
10. DOCUMENT
11. IMAGE
12. LANGUAGE
13. MEDIA_GALLERY
14. MULTI_REFERENCE
15. NUMBER
16. OBJECT
17. PAGE_LINK
18. REFERENCE
19. RICH_CONTENT
20. RICH_TEXT
21. TEXT
22. TIME
23. URL
24. VIDEO
