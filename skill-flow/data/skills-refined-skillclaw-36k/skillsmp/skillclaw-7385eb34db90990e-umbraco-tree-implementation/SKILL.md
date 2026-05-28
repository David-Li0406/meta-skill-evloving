---
name: umbraco-tree-implementation
description: Use this skill when you need to implement tree structures in the Umbraco backoffice, including custom tree items and their associated behaviors.
---

# Umbraco Tree Implementation

## What is it?
This skill covers the implementation of tree structures in the Umbraco backoffice, including the creation of custom tree items and their behaviors. Trees are hierarchical structures that display organized content and require a data source for fetching items.

## Documentation
Always fetch the latest docs before implementing:

- **Main docs**: [Umbraco Tree Documentation](https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types/tree)
- **Foundation**: [Umbraco Foundation](https://docs.umbraco.com/umbraco-cms/customizing/foundation)
- **Extension Registry**: [Umbraco Extension Registry](https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry)

## When to Use Custom Tree Item Contexts
Most tree items use `kind: 'default'` and do not require a custom context. Create a custom context for:

- **Custom icon logic** - Dynamic icons based on item state
- **Custom labels or badges** - Additional visual information
- **Special rendering** - Unique behavior for specific entity types
- **Additional item behaviors** - Click handlers, drag-and-drop, etc.

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above.
2. **Ask questions** - Determine entity types and custom rendering needs.
3. **Generate files** - Create the necessary manifest and optional element/context.
4. **Explain** - Show what was created and how to test.

## File Structure
Modern trees typically use 2-3 files:
```
my-tree/
├── manifest.ts          # Registers repository and tree
├── tree.repository.ts   # Repository + inline data source
└── types.ts             # Type definitions (optional)
```

## Minimal Examples

### Basic Manifest (manifests.ts)
```typescript
export const manifests: Array<UmbExtensionManifest> = [
  {
    type: 'treeItem',
    kind: 'default',
    alias: 'My.TreeItem',
    name: 'My Tree Item',
    forEntityTypes: ['my-entity-type'],
  },
];
```

### Custom Tree Item with Context
```typescript
import { MY_ENTITY_TYPE, MY_ROOT_ENTITY_TYPE } from '../entity.js';

export const manifests: Array<UmbExtensionManifest> = [
  {
    type: 'treeItem',
    kind: 'custom',
    alias: 'My.CustomTreeItem',
    name: 'My Custom Tree Item',
    forEntityTypes: [MY_ENTITY_TYPE],
  },
];
```

## CRITICAL: Tree + Workspace Integration
- **Tree items REQUIRE workspaces** - Clicking a tree item navigates to a workspace for that entity type. Ensure a workspace is registered for the `entityType`.
- **Workspaces must be `kind: 'routable'`** - For proper navigation and selection state, use `kind: 'routable'` workspaces.
- **Entity types link trees to workspaces** - The `entityType` in your tree item data must match the `entityType` in your workspace manifest.

## Related Foundation Skills
- **Repository Pattern**: When implementing tree data sources, repositories, data fetching, or CRUD operations.
- **Context API**: When accessing tree context.
- **Workspace**: For integrating tree items with workspaces.