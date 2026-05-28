# Collection Generation Process

Technical details about how CMS collections are generated in Wix CLI apps, including the `getDataExtensionAndCollectionsFiles` function and collection operation merging.

## Overview

The `getDataExtensionAndCollectionsFiles` function is responsible for generating the `src/data/extensions.ts` file that contains all CMS collection definitions. It handles merging existing collections with new collection operations and generates the final file structure.

## Function Signature

```typescript
getDataExtensionAndCollectionsFiles(
  collectionOperations: CollectionOperation[],
  existingCollections: Collection[] = []
): FilesType
```

### Parameters

- **`collectionOperations`**: Array of collection operations (INSERT, UPDATE, DELETE) to apply
- **`existingCollections`**: Array of existing collections (used in iteration flows)

### Returns

Array of file operations (typically one file: `src/data/extensions.ts`)

## Generation Flow

### Step 1: Merge Collections

The function first merges existing collections with new operations using `applyCollectionOperations`:

```typescript
const mergedCollections = applyCollectionOperations(
  existingCollections,
  collectionOperations
);
```

### Step 2: Handle Empty Collections

If no collections remain after merging, return a DELETE operation:

```typescript
if (!mergedCollections?.length) {
  return [
    {
      operation: ExtensionGenerationOperation.DELETE,
      path: DATA_EXTENSION_PATH, // "src/data/extensions.ts"
    },
  ];
}
```

This ensures the file is deleted when all collections are removed.

### Step 3: Build Collection Data

Each collection is prepared with the required `schemaUrl` field:

```typescript
const collectionsData = mergedCollections.map((collection) => {
  return {
    schemaUrl: "https://www.wix.com/", // Legacy field, will be removed
    ...collection,
  };
});
```

### Step 4: Generate Extension Object

The extension object is created with:

- **`compId`**: Random UUID generated for each generation
- **`compName`**: Always `"data-extension"`
- **`compType`**: Always `"DATA_COMPONENT"`
- **`compData.dataComponent.collections`**: Array of all collections

```typescript
const objStr = naturalJsonStringify({
  compId: "{{GENERATE_UUID}}", // Replace with a static UUID v4 string
  compName: "data-extension",
  compType: "DATA_COMPONENT",
  compData: {
    dataComponent: {
      collections: collectionsData,
    },
  },
});
```

### Step 5: Generate Code

The final TypeScript code is generated as a template string:

```typescript
const generatedCode = `
import { extensions } from '@wix/astro/builders';

export const dataExtension = extensions.genericExtension(${objStr});
`;
```

### Step 6: Return File Operation

The function returns a file operation with INSERT operation:

```typescript
return [
  {
    operation: ExtensionGenerationOperation.INSERT,
    path: "src/data/extensions.ts",
    content: generatedCode,
  },
];
```

## Collection Operations

Collections support three operation types:

### INSERT

Creates a new collection or replaces an existing one.

```typescript
{
  operation: ExtensionGenerationOperation.INSERT,
  data: {
    idSuffix: "products",
    displayName: "Products",
    fields: [...],
    dataPermissions: {...}
  }
}
```

**Behavior:** Sets the collection in the map, replacing any existing collection with the same `idSuffix`.

### UPDATE

Modifies an existing collection.

```typescript
{
  operation: ExtensionGenerationOperation.UPDATE,
  data: {
    idSuffix: "products",
    fields: [...], // New or updated fields
  }
}
```

**Behavior:**

- If collection exists: Merges new data with existing collection
- If collection doesn't exist: Treats update as insert (creates new collection)

### DELETE

Removes a collection.

```typescript
{
  operation: ExtensionGenerationOperation.DELETE,
  data: {
    idSuffix: "products"
  }
}
```

**Behavior:** Removes the collection from the map. If all collections are deleted, the entire file is deleted.

## Operation Merging Logic

The `applyCollectionOperations` function merges operations using a Map:

```typescript
export const applyCollectionOperations = (
  existingCollections: Collection[],
  operations: CollectionOperation[]
): Collection[] => {
  const collectionsMap = new Map<string, Collection>();

  // 1. Add all existing collections to the map
  existingCollections.forEach((collection) => {
    if (collection.idSuffix) {
      collectionsMap.set(collection.idSuffix, collection);
    }
  });

  // 2. Apply operations to modify the map
  operations?.forEach((operation) => {
    const collectionId = operation.data.idSuffix;
    if (!collectionId) return;

    switch (operation.operation) {
      case ExtensionGenerationOperation.INSERT:
        collectionsMap.set(collectionId, operation.data);
        break;
      case ExtensionGenerationOperation.UPDATE: {
        const existing = collectionsMap.get(collectionId);
        if (existing) {
          collectionsMap.set(collectionId, { ...existing, ...operation.data });
        } else {
          // If collection doesn't exist, treat update as insert
          collectionsMap.set(collectionId, operation.data);
        }
        break;
      }
      case ExtensionGenerationOperation.DELETE:
        collectionsMap.delete(collectionId);
        break;
    }
  });

  return Array.from(collectionsMap.values());
};
```

### Merging Behavior

1. **Start with existing collections**: All existing collections are added to a Map keyed by `idSuffix`
2. **Apply operations in order**: Each operation modifies the Map
3. **INSERT**: Replaces collection (or creates new)
4. **UPDATE**: Merges with existing (or creates if missing)
5. **DELETE**: Removes collection
6. **Return final state**: All remaining collections are returned as an array

## App Namespace Scoping

Collections are automatically scoped with the app namespace to prevent conflicts.

### Adding Namespace

The `addAppNamespaceToCollectionId` function prefixes collection IDs:

```typescript
export const addAppNamespaceToCollectionId = (
  collections: CollectionOperation[],
  appNamespace: string
): CollectionOperation[] => {
  return (
    collections?.map((collection) => {
      const newIdSuffix = path.join(
        appNamespace,
        collection?.data?.idSuffix ?? "no-collection-id"
      );

      if (collection.operation === ExtensionGenerationOperation.DELETE) {
        return {
          operation: ExtensionGenerationOperation.DELETE,
          data: {
            idSuffix: newIdSuffix,
          },
        };
      }

      return {
        ...collection,
        data: {
          ...collection.data,
          idSuffix: newIdSuffix,
        },
      };
    }) || []
  );
};
```

### Example

**Input:**

- `idSuffix`: `"products"`
- `appNamespace`: `"my-app"`

**Output:**

- `idSuffix`: `"my-app/products"`

This scoping happens before collections are passed to `getDataExtensionAndCollectionsFiles`.

## File Path

The generated file is always at:

```typescript
export const DATA_EXTENSION_PATH = path.join("src", "data", "extensions.ts");
// Result: "src/data/extensions.ts"
```

## Constants

The generation uses these constants:

```typescript
export const CMS_BUILDER = "genericExtension";
export const CMS_COMP_TYPE = "DATA_COMPONENT";
export const CMS_COMP_NAME = "data-extension";
export const ASTRO_BUILDERS_IMPORT = "@wix/astro/builders";
```

## Initial Generation vs Iteration

### Initial Generation

- `existingCollections`: Empty array `[]`
- All operations are INSERT
- Creates new `src/data/extensions.ts` file

### Iteration

- `existingCollections`: Array of current collections from previous generation
- Operations can be INSERT, UPDATE, or DELETE
- Modifies existing `src/data/extensions.ts` file

## Example: Complete Flow

### Input

**Existing Collections:**

```json
[
  {
    "idSuffix": "products",
    "displayName": "Products",
    "fields": [{ "key": "name", "type": "TEXT" }]
  }
]
```

**Operations:**

```json
[
  {
    "operation": "UPDATE",
    "data": {
      "idSuffix": "products",
      "fields": [
        { "key": "name", "type": "TEXT" },
        { "key": "price", "type": "NUMBER" }
      ]
    }
  },
  {
    "operation": "INSERT",
    "data": {
      "idSuffix": "categories",
      "displayName": "Categories",
      "fields": [{ "key": "name", "type": "TEXT" }]
    }
  }
]
```

### Processing

1. **Merge**: Start with existing `products` collection
2. **UPDATE products**: Merge new fields (adds `price`)
3. **INSERT categories**: Add new collection
4. **Result**: Two collections (`products` with both fields, `categories`)

### Output

**File:** `src/data/extensions.ts`

```typescript
import { extensions } from '@wix/astro/builders';

export const dataExtension = extensions.genericExtension({
  compId: "{{GENERATE_UUID}}",
  compName: "data-extension",
  compType: "DATA_COMPONENT",
  compData: {
    dataComponent: {
      collections: [
        {
          schemaUrl: "https://www.wix.com/",
          idSuffix: "products",
          displayName: "Products",
          fields: [
            { key: "name", type: "TEXT" },
            { key: "price", type: "NUMBER" }
          ],
          dataPermissions: {...}
        },
        {
          schemaUrl: "https://www.wix.com/",
          idSuffix: "categories",
          displayName: "Categories",
          fields: [
            { key: "name", type: "TEXT" }
          ],
          dataPermissions: {...}
        }
      ]
    }
  }
});
```

## Key Takeaways

1. **Single file**: All collections are in one file (`src/data/extensions.ts`)
2. **Operations merge**: INSERT/UPDATE/DELETE operations are applied to existing collections
3. **Empty handling**: If all collections are deleted, the file is deleted
4. **UUID requirement**: The `compId` must be a unique, static UUID v4 string (do not use `randomUUID()`)
5. **Namespace scoping**: Collection IDs are automatically scoped with app namespace
6. **Legacy field**: `schemaUrl` is added but will be removed in future
