---
name: umbraco-customization
description: Use this skill when you want to implement custom themes and icons in the Umbraco backoffice.
---

# Umbraco Customization

## What is it?
This skill allows you to customize the visual appearance of the Umbraco backoffice by implementing themes and custom icons. You can create themes to change colors and typography, as well as register custom icons for use throughout the interface.

## Documentation
Always fetch the latest docs before implementing:

- **Themes**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types/themes
- **Icons**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types/icons
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Extension Registry**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above.
2. **Ask questions** - What colors or icons are needed? Are SVG sources available?
3. **Generate files** - Create manifest files, CSS for themes, and icon files based on the latest docs.
4. **Explain** - Show what was created and how to test the themes and icons.

## Minimal Examples

### Theme Manifest (manifests.ts)
```typescript
import type { ManifestTheme } from '@umbraco-cms/backoffice/extension-registry';

export const manifests: Array<ManifestTheme> = [
  {
    type: 'theme',
    alias: 'My.Theme.Dark',
    name: 'My Dark Theme',
    css: () => import('./dark-theme.css?inline'),
  },
];
```

### Theme CSS File (dark-theme.css)
```css
:root {
  /* Background colors */
  --uui-color-surface: #1e1e1e;
  --uui-color-text: #d4d4d4;
  /* Additional color variables... */
}
```

### Icon Manifest (umbraco-package.json)
```json
{
  "name": "My Icons Package",
  "extensions": [
    {
      "type": "icons",
      "alias": "My.Icons",
      "name": "My Custom Icons",
      "js": "/App_Plugins/MyPackage/icons.js"
    }
  ]
}
```

### Icons Registry (icons.ts)
```typescript
export default [
  {
    name: 'my-custom-icon',
    path: () => import('./icons/my-custom-icon.js'),
  },
  // Additional icons...
];
```

### Icon File (icons/my-custom-icon.ts)
```typescript
export default `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
  <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
</svg>`;
```

### Using Custom Icons
```typescript
// In any extension manifest
const manifest = {
  type: 'headerApp',
  kind: 'button',
  alias: 'My.HeaderApp',
  name: 'My App',
  meta: {
    label: 'My App',
    icon: 'my-custom-icon',  // Use your custom icon
  },
};
```

### In HTML Templates
```html
<umb-icon name="my-custom-icon"></umb-icon>
```

That's it! Always fetch fresh docs.