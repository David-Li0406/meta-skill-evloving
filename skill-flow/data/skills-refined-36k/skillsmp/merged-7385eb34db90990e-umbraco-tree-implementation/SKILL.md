---
name: umbraco-tree-implementation
description: Use this skill when implementing tree structures and tree items in the Umbraco backoffice.
---

# Umbraco Tree Implementation

## What is it?
This skill covers the implementation of tree structures and tree items in the Umbraco backoffice. Trees represent hierarchical content, while tree items define how entities are rendered within these trees.

## Documentation
Always fetch the latest docs before implementing:

- **Main docs**: [Umbraco Tree Documentation](https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types/tree)
- **Foundation**: [Umbraco Foundation](https://docs.umbraco.com/umbraco-cms/customizing/foundation)
- **Extension Registry**: [Umbraco Extension Registry](https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry)

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above.
2. **Ask questions** - What data will the tree display? What repository will provide the data? Will tree items be clickable?
3. **Generate files** - Create minimal files based on the latest docs:
   - Create: `manifest.ts`, `tree.repository.ts` (with inline data source).
   - Avoid creating deprecated files.
4. **If clickable** - Create routable workspaces for each entity type.
5. **Explain** - Show what was created and how to test.

## Key Configuration Options

### Tree and Workspace Integration
- **Tree items require workspaces**: Ensure that clicking a tree item navigates to a workspace for that entity type.
- **Use `kind: 'routable'` for workspaces**: This is necessary for proper tree item selection state and navigation.

### Hide Tree Root
To show tree items at the root level, use `hideTreeRoot: true` on the **menuItem** manifest.

## Minimal Examples

### Tree Manifest
```typescript
export const manifests: UmbExtensionManifest[] = [
  {
    type: 'repository',
    alias: 'My.Tree.Repository',
    name: 'My Tree Repository',
    api: () => import('./tree.repository.js'),
  },
  {
    type: 'tree',
    kind: 'default',
    alias: 'My.Tree',
    name: 'My Tree',
    meta: {
      repositoryAlias: 'My.Tree.Repository',
    },
  },
  {
    type: 'treeItem',
    kind: 'default',
    alias: 'My.TreeItem',
    name: 'My Tree Item',
    forEntityTypes: ['my-entity'],
  },
  {
    type: 'menuItem',
    kind: 'tree',
    alias: 'My.MenuItem.Tree',
    meta: {
      treeAlias: 'My.Tree',
      menus: ['My.Menu'],
      hideTreeRoot: true,
    },
  },
];
```

### Repository with Inline Data Source
```typescript
import { UmbTreeRepositoryBase, UmbTreeServerDataSourceBase } from '@umbraco-cms/backoffice/tree';
import type { UmbControllerHost } from '@umbraco-cms/backoffice/controller-api';
import type { UmbApi } from '@umbraco-cms/backoffice/extension-api';

class MyTreeDataSource extends UmbTreeServerDataSourceBase<any, MyTreeItemModel> {
  constructor(host: UmbControllerHost) {
    super(host, {
      getRootItems: async () => {
        const items: MyTreeItemModel[] = [
          {
            unique: 'item-1',
            parent: { unique: null, entityType: 'my-root-entity' },
            entityType: 'my-entity',
            name: 'Item 1',
            hasChildren: false,
            isFolder: false,
            icon: 'icon-document',
          },
        ];
        return { data: { items, total: items.length } };
      },
      getChildrenOf: async () => ({ data: { items: [], total: 0 } }),
      getAncestorsOf: async () => ({ data: [] }),
      mapper: (item: any) => item,
    });
  }
}

export class MyTreeRepository extends UmbTreeRepositoryBase<MyTreeItemModel, MyTreeRootModel> implements UmbApi {
  constructor(host: UmbControllerHost) {
    super(host, MyTreeDataSource);
  }

  async requestTreeRoot() {
    const data: MyTreeRootModel = {
      unique: null,
      entityType: 'my-root-entity',
      name: 'My Tree',
      hasChildren: true,
      isFolder: true,
    };
    return { data };
  }
}

export { MyTreeRepository as api };
```

## Best Practices
- Use appropriate icons for different entity types.
- Keep tree items lightweight for performance.
- Always fetch fresh docs and keep examples minimal.

That's it! Follow these guidelines to implement trees and tree items effectively in Umbraco.