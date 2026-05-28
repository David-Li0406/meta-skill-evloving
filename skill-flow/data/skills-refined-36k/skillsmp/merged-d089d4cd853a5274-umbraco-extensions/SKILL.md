---
name: umbraco-extensions
description: Use this skill when implementing various extension types in the Umbraco backoffice, including sections, menus, and modals.
---

# Umbraco Extensions

## Overview
This skill covers the implementation of various extension types in the Umbraco backoffice, including sections, menus, and modals. Each extension type enhances the user interface and functionality, allowing for organized navigation and interaction.

## Documentation
Always fetch the latest docs before implementing:

- **Sections**: [Sections Documentation](https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types/sections/section)
- **Menus**: [Menus Documentation](https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types/menu)
- **Modals**: [Modals Documentation](https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types/modals)
- **Foundation**: [Foundation Documentation](https://docs.umbraco.com/umbraco-cms/customizing/foundation)
- **Extension Registry**: [Extension Registry](https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry)

## Workflow
1. **Fetch docs** - Use WebFetch on the URLs above.
2. **Ask questions** - Determine the purpose of the extension (e.g., what will the section/menu/modal contain?).
3. **Generate files** - Create the necessary manifest and configuration files based on the latest docs.
4. **Explain** - Show what was created and how to configure permissions or test the implementation.

## Sections
### What is it?
Sections are top-level navigation items in the Umbraco backoffice that provide a home for custom content and functionality.

### Key Properties
- **type**: Always `"section"`
- **alias**: Unique identifier for the section
- **name**: Display name in backoffice
- **meta.label**: Label shown in navigation
- **meta.pathname**: URL route for the section

### Example
```json
{
  "type": "section",
  "alias": "My.Section",
  "name": "My Section",
  "meta": {
    "label": "My Section",
    "pathname": "my-section"
  }
}
```

## Menus
### What is it?
Menus are extension components that display throughout the Umbraco backoffice interface, enabling organized navigation and action grouping.

### Key Properties
- **type**: `"menu"` for menu container, `"menuItem"` for items
- **alias**: Unique identifier
- **menus**: Array of menu aliases this item should appear in
- **weight**: Controls ordering (higher = later in list)

### Example
```json
{
  "type": "menu",
  "alias": "My.Menu",
  "name": "My Menu"
}
```

## Modals
### What is it?
A modal is a popup layer that darkens the surroundings and is used to configure and present dialogs and sidebars within the Umbraco backoffice.

### Key Properties
- **type**: `"modal"`
- **alias**: Unique identifier
- **element**: The component to render in the modal

### Example
```typescript
export const manifests = [
  {
    type: 'modal',
    alias: 'My.Modal',
    name: 'My Modal',
    element: () => import('./modal.element.js'),
  },
];
```

## Built-in Extensions
- **Sections**: Content, Media, Settings, Packages, Users, Members
- **Menus**: Help, Content, Media, Settings

That's it! Always fetch fresh docs, keep examples minimal, and generate complete working code.