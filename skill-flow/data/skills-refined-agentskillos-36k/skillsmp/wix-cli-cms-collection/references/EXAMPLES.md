# Collection Examples

Real-world examples of CMS collections for Wix CLI apps, showing the complete `src/data/extensions.ts` structure.

## Example 1: Simple Collection with Initial Data

Complete example of a collection with basic fields and initial seed data.

**File:** `src/data/extensions.ts`

```typescript
import { extensions } from "@wix/astro/builders";

export const dataExtension = extensions.genericExtension({
  compId: "{{GENERATE_UUID}}",
  compName: "data-extension",
  compType: "DATA_COMPONENT",
  compData: {
    dataComponent: {
      collections: [
        {
          schemaUrl: "https://www.wix.com/",
          idSuffix: "additional-fees",
          displayName: "Additional Fees",
          displayField: "title",
          fields: [
            {
              key: "title",
              displayName: "Fee Title",
              type: "TEXT",
            },
            {
              key: "amount",
              displayName: "Fee Amount",
              type: "NUMBER",
            },
          ],
          dataPermissions: {
            itemRead: "ANYONE",
            itemInsert: "PRIVILEGED",
            itemUpdate: "PRIVILEGED",
            itemRemove: "PRIVILEGED",
          },
          initialData: [
            {
              title: "Handling Fee",
              amount: 5,
            },
            {
              title: "Gift Wrapping",
              amount: 3.5,
            },
          ],
        },
      ],
    },
  },
});
```

**Key Points:**

- Single collection with basic TEXT and NUMBER fields
- Includes `initialData` with seed records
- Uses Wix CLI default permissions (read: ANYONE, write: PRIVILEGED)
- `displayField` set to 'title' for display purposes

## Example 2: Collection with Multiple Field Types

Collection demonstrating various field types including boolean and descriptions.

**File:** `src/data/extensions.ts`

```typescript
import { extensions } from "@wix/astro/builders";

export const dataExtension = extensions.genericExtension({
  compId: "{{GENERATE_UUID}}",
  compName: "data-extension",
  compType: "DATA_COMPONENT",
  compData: {
    dataComponent: {
      collections: [
        {
          schemaUrl: "https://www.wix.com/",
          idSuffix: "additional-fees",
          displayName: "Additional Fees Configuration",
          displayField: "feeTitle",
          fields: [
            {
              key: "feeTitle",
              displayName: "Fee Title",
              type: "TEXT",
            },
            {
              key: "feeAmount",
              displayName: "Fee Amount",
              type: "NUMBER",
            },
            {
              key: "feeType",
              displayName: "Fee Type",
              description: "Type of fee (e.g., flat rate, percentage)",
              type: "TEXT",
            },
            {
              key: "isActive",
              displayName: "Is Active",
              description: "Whether the fee is currently enabled",
              type: "BOOLEAN",
            },
          ],
          dataPermissions: {
            itemRead: "ANYONE",
            itemInsert: "ANYONE",
            itemUpdate: "ANYONE",
            itemRemove: "ANYONE",
          },
          initialData: [
            {
              feeTitle: "Handling Fee",
              feeAmount: 5,
              feeType: "flat",
              isActive: true,
            },
            {
              feeTitle: "Fragile Item Surcharge",
              feeAmount: 10,
              feeType: "flat",
              isActive: true,
            },
          ],
        },
      ],
    },
  },
});
```

**Key Points:**

- Multiple field types: TEXT, NUMBER, BOOLEAN
- Field descriptions for documentation
- All permissions set to ANYONE (less restrictive pattern)
- Initial data matches all field types correctly

## Example 3: Collection with Reference Field

Collection demonstrating a REFERENCE field linking to another collection.

**Collection Definition:**

```json
{
  "idSuffix": "products",
  "displayName": "Products",
  "fields": [
    {
      "key": "name",
      "displayName": "Product Name",
      "type": "TEXT"
    },
    {
      "key": "category",
      "displayName": "Category",
      "type": "REFERENCE",
      "referenceOptions": {
        "referencedCollectionId": "categories"
      }
    }
  ],
  "dataPermissions": {
    "itemRead": "ANYONE",
    "itemInsert": "PRIVILEGED",
    "itemUpdate": "PRIVILEGED",
    "itemRemove": "PRIVILEGED"
  }
}
```

**Key Points:**

- REFERENCE field links to another collection (`categories`)
- `referencedCollectionId` uses the `idSuffix` of the referenced collection
- Both collections must be defined in the same plan
- Reference is between custom collections (not Wix business entities)

## Example 4: Collection with Multi-Reference Field

Collection demonstrating a MULTI_REFERENCE field for many-to-many relationships.

**Collection Definition:**

```json
{
  "idSuffix": "products",
  "displayName": "Products",
  "fields": [
    {
      "key": "name",
      "displayName": "Product Name",
      "type": "TEXT"
    },
    {
      "key": "tags",
      "displayName": "Tags",
      "type": "MULTI_REFERENCE",
      "multiReferenceOptions": {
        "referencedCollectionId": "tags"
      }
    }
  ],
  "dataPermissions": {
    "itemRead": "ANYONE",
    "itemInsert": "PRIVILEGED",
    "itemUpdate": "PRIVILEGED",
    "itemRemove": "PRIVILEGED"
  }
}
```

**Key Points:**

- MULTI_REFERENCE allows linking to multiple items
- Useful for many-to-many relationships (products → tags)
- Same constraints as REFERENCE (only between custom collections)

## Example 5: Multiple Collections with Relationships

Complete example showing multiple collections with relationships between them.

**File:** `src/data/extensions.ts`

```typescript
import { extensions } from "@wix/astro/builders";

export const dataExtension = extensions.genericExtension({
  compId: "{{GENERATE_UUID}}",
  compName: "data-extension",
  compType: "DATA_COMPONENT",
  compData: {
    dataComponent: {
      collections: [
        {
          schemaUrl: "https://www.wix.com/",
          idSuffix: "categories",
          displayName: "Categories",
          displayField: "name",
          fields: [
            {
              key: "name",
              displayName: "Category Name",
              type: "TEXT",
            },
            {
              key: "description",
              displayName: "Description",
              type: "TEXT",
            },
          ],
          dataPermissions: {
            itemRead: "ANYONE",
            itemInsert: "PRIVILEGED",
            itemUpdate: "PRIVILEGED",
            itemRemove: "PRIVILEGED",
          },
        },
        {
          schemaUrl: "https://www.wix.com/",
          idSuffix: "products",
          displayName: "Products",
          displayField: "name",
          fields: [
            {
              key: "name",
              displayName: "Product Name",
              type: "TEXT",
            },
            {
              key: "price",
              displayName: "Price",
              type: "NUMBER",
            },
            {
              key: "category",
              displayName: "Category",
              type: "REFERENCE",
              referenceOptions: {
                referencedCollectionId: "categories",
              },
            },
          ],
          dataPermissions: {
            itemRead: "ANYONE",
            itemInsert: "PRIVILEGED",
            itemUpdate: "PRIVILEGED",
            itemRemove: "PRIVILEGED",
          },
        },
      ],
    },
  },
});
```

**Key Points:**

- Multiple collections defined in the same file
- `products` collection references `categories` collection
- Both collections use the same permission pattern
- All collections are in the `collections` array

## Example 6: Collection with Initial Data (Complex)

Collection with multiple field types and initial data demonstrating proper type matching.

**Collection Definition:**

```json
{
  "idSuffix": "products",
  "displayName": "Products",
  "fields": [
    {
      "key": "name",
      "displayName": "Name",
      "type": "TEXT"
    },
    {
      "key": "price",
      "displayName": "Price",
      "type": "NUMBER"
    },
    {
      "key": "isActive",
      "displayName": "Is Active",
      "type": "BOOLEAN"
    }
  ],
  "dataPermissions": {
    "itemRead": "ANYONE",
    "itemInsert": "PRIVILEGED",
    "itemUpdate": "PRIVILEGED",
    "itemRemove": "PRIVILEGED"
  },
  "initialData": [
    {
      "name": "Sample Product 1",
      "price": 29.99,
      "isActive": true
    },
    {
      "name": "Sample Product 2",
      "price": 49.99,
      "isActive": false
    }
  ]
}
```

**Key Points:**

- Initial data matches field types exactly:
  - TEXT → string
  - NUMBER → number
  - BOOLEAN → boolean
- Field keys in initial data match schema keys (lowerCamelCase)
- Multiple seed records provided

## File Structure Notes

### Single File for All Collections

All collections are defined in a single file: `src/data/extensions.ts`

### File Format

```typescript
import { extensions } from "@wix/astro/builders";

export const dataExtension = extensions.genericExtension({
  compId: "{{GENERATE_UUID}}",
  compName: "data-extension",
  compType: "DATA_COMPONENT",
  compData: {
    dataComponent: {
      collections: [
        // All collections go here
      ],
    },
  },
});
```

### Required Properties

- `compId`: Unique static UUID v4 string (generate fresh, do not use randomUUID())
- `compName`: Always `'data-extension'`
- `compType`: Always `'DATA_COMPONENT'`
- `collections`: Array of collection definitions

### Collection Properties

Each collection must have:

- `schemaUrl`: `'https://www.wix.com/'` (legacy, will be removed)
- `idSuffix`: Collection identifier
- `displayName`: Human-readable name
- `fields`: Array of field definitions
- `dataPermissions`: Permission configuration

Optional properties:

- `displayField`: Field used for display
- `initialData`: Seed data array

## Common Patterns in Examples

### Default Permissions Pattern

```json
{
  "dataPermissions": {
    "itemRead": "ANYONE",
    "itemInsert": "PRIVILEGED",
    "itemUpdate": "PRIVILEGED",
    "itemRemove": "PRIVILEGED"
  }
}
```

Most common pattern in Wix CLI apps.

### Field Naming

- Field keys: `lowerCamelCase` (e.g., `feeTitle`, `isActive`)
- Collection IDs: `lower-kebab-case` (e.g., `additional-fees`)

### Initial Data Compliance

- All field types must match exactly
- Use correct data types (strings, numbers, booleans)
- Field keys must match schema exactly

## Example 7: Collection with OBJECT Field

Collection demonstrating an OBJECT type field for flexible JSON data.

**Collection Definition:**

```typescript
{
  idSuffix: "offers",
  displayName: "Offers",
  fields: [
    {
      key: "title",
      displayName: "Title",
      type: "TEXT"
    },
    {
      key: "triggerRules",
      displayName: "Trigger Rules",
      type: "OBJECT",
      objectOptions: {
        fields: [
                  {
                    key: 'url',
                    displayName: 'URL Condition',
                    type: 'TEXT'
                  },
                  {
                    key: 'scrollDepth',
                    displayName: 'Scroll Depth Percentage',
                    type: 'NUMBER'
                  },
                  {
                    key: 'dateStart',
                    displayName: 'Start Date',
                    type: 'DATE'
                  },
                  {
                    key: 'dateEnd',
                    displayName: 'End Date',
                    type: 'DATE'
                  },
                  {
                    key: 'timeStart',
                    displayName: 'Start Time',
                    type: 'TIME'
                  },
                  {
                    key: 'timeEnd',
                    displayName: 'End Time',
                    type: 'TIME'
                  }
                ]
      },
      description: 'Specific conditions for triggering the celebration',
    },
  ],
  dataPermissions: {
    itemRead: "ANYONE",
    itemInsert: "PRIVILEGED",
    itemUpdate: "PRIVILEGED",
    itemRemove: "PRIVILEGED"
  }
}
```

**Key Points:**

- **CRITICAL:** `objectOptions` is **required** when using `type: "OBJECT"`
- Use an empty object `{}` if you don't need schema validation
- The API will reject OBJECT fields without `objectOptions`
