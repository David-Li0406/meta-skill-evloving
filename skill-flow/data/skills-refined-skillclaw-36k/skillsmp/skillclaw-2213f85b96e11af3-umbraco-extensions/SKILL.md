---
name: umbraco-extensions
description: Use this skill when implementing various extension components in the Umbraco backoffice, such as sections, menus, modals, and elements, based on official documentation.
---

# Umbraco Extensions

## What is it?
Umbraco extensions are customizable components that enhance the functionality of the Umbraco backoffice. This includes sections, menus, menu items, modals, and Umbraco elements, each serving specific purposes for navigation, content management, and user interaction.

## Documentation
Always fetch the latest docs before implementing:

- **Sections**: [Sections Documentation](https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types/sections/section)
- **Menus**: [Menus Documentation](https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types/menu)
- **Menu Items**: [Menu Items Documentation](https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types/menu-item)
- **Modals**: [Modals Documentation](https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types/modals)
- **Umbraco Elements**: [Umbraco Element Documentation](https://docs.umbraco.com/umbraco-cms/customizing/foundation/umbraco-element)

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above.
2. **Ask questions** - Determine the purpose of the extension. What will it contain? What user interactions are needed?
3. **Generate files** - Create the necessary manifests and components based on the latest documentation.
4. **Explain** - Show what was created and how to configure or use the extensions.

## Minimal Examples

### Section Manifest (umbraco-package.json)
```json
{
  "type": "section",
  "alias": "My.Section",
  "name": "My Section"
}
```

### Menu Item Manifest (manifest.ts)
```typescript
export const manifests = [
  {
    type: "menuItem",
    kind: "link",
    alias: "My.MenuItem",
    name: "My Menu Item",
    weight: 100,
    meta: {
      menus: ["My.Menu"],
      label: "My Item",
      icon: "icon-document",
      href: "/my-link"
    }
  }
];
```

### Custom Modal Example
```typescript
import { html, customElement } from '@umbraco-cms/backoffice/external/lit';
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';

@customElement('my-modal')
export class MyModal extends UmbLitElement {
  render() {
    return html`
      <div class="modal">
        <h3>My Custom Modal</h3>
        <p>Content goes here.</p>
      </div>
    `;
  }
}
```

### Using UmbElementMixin
```typescript
import { customElement } from '@umbraco-cms/backoffice/external/lit';
import { UmbElementMixin } from '@umbraco-cms/backoffice/element-api';

@customElement('my-element')
export class MyElement extends UmbElementMixin(HTMLElement) {
  constructor() {
    super();
    this.consumeContext(MY_CONTEXT, (context) => {
      console.log('Context consumed:', context);
    });
  }
}
```