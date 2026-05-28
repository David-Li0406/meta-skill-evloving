---
name: umbraco-backoffice-extensions
description: Use this skill when implementing various types of extensions in the Umbraco backoffice, such as property editors, collection actions, entity actions, and views.
---

# Umbraco Backoffice Extensions

## What is it?
This skill encompasses the implementation of various extension types in the Umbraco backoffice, including property editor schemas, collection actions, entity actions, and collection views. These extensions enhance the functionality and user experience of the Umbraco CMS.

## Documentation
Always fetch the latest docs before implementing:

- **Main docs**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Extension Registry**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above.
2. **Ask questions** - Determine the type of extension needed (property editor, collection action, entity action, or collection view) and the specific requirements.
3. **Generate files** - Create the necessary manifest and implementation files based on the latest documentation.
4. **Explain** - Show what was created and how to test the implementation.

## Types of Extensions

### Property Editor Schema
- **Purpose**: Defines server-side metadata and configuration for property editors.
- **When to Create**: Use built-in schemas when possible; create custom schemas for specialized data handling.

### Collection Action
- **Purpose**: Adds buttons in a collection's toolbar for actions on the collection as a whole.
- **Examples**: "Create New" buttons, export functionality.

### Entity Create Option Action
- **Purpose**: Provides customizable options when creating entities, allowing users to choose different creation methods.
- **Use Case**: Extensibility for adding creation options to workflows.

### Collection View
- **Purpose**: Defines how data is displayed within a collection, allowing for custom visual representations.
- **Examples**: Tables, grids, cards, or any custom layout.

### Entity Actions
- **Purpose**: Perform actions on specific items in Umbraco, appearing in context menus.
- **Examples**: Actions that manipulate document property permissions or integrate with user permission controls.

## Minimal Examples

### Property Editor Schema Example
```csharp
// C# schema class example
public class MyCustomSchema : PropertyEditor
{
    // Implementation details...
}
```

### Collection Action Example
```typescript
import type { ManifestCollectionAction } from '@umbraco-cms/backoffice/extension-registry';

const manifest: ManifestCollectionAction = {
  type: 'collectionAction',
  alias: 'My.CollectionAction.Create',
  name: 'Create Item Action',
  api: () => import('./create-action.js'),
  meta: {
    label: 'Create New',
  },
};
```

### Entity Create Option Action Example
```typescript
import type { ManifestEntityCreateOptionAction } from '@umbraco-cms/backoffice/extension-registry';

const manifest: ManifestEntityCreateOptionAction = {
  type: 'entityCreateOptionAction',
  alias: 'My.EntityCreateOptionAction',
  name: 'My Create Option',
  weight: 100,
  api: () => import('./my-create-option-action.js'),
  forEntityTypes: ['user'],
  meta: {
    icon: 'icon-add',
    label: 'Create with Template',
  },
};
```

### Collection View Example
```typescript
import type { ManifestCollectionView } from '@umbraco-cms/backoffice/extension-registry';

const manifest: ManifestCollectionView = {
  type: 'collectionView',
  alias: 'My.CollectionView.Cards',
  name: 'Card View',
  element: () => import('./card-view.element.js'),
  meta: {
    label: 'Cards',
    icon: 'icon-grid',
  },
};
```

### Entity Action Example
```typescript
import type { ManifestEntityAction } from '@umbraco-cms/backoffice/extension-registry';

const manifest: ManifestEntityAction = {
  type: 'entityAction',
  alias: 'My.EntityAction',
  name: 'My Entity Action',
  weight: 10,
  api: MyEntityAction,
  forEntityTypes: ['document'],
  meta: {
    icon: 'icon-alarm-clock',
  },
};
```