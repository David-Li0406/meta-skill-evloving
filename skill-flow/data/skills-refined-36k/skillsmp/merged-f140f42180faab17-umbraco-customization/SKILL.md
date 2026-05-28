---
name: umbraco-customization
description: Use this skill when implementing custom themes and icons in the Umbraco backoffice.
---

# Umbraco Customization

## What is it?
This skill allows you to customize the visual appearance of the Umbraco backoffice by implementing themes and custom icons. Themes can change colors, typography, and other visual elements, while custom icons enhance the user interface with unique visual elements.

## Documentation
Always fetch the latest docs before implementing:

- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Extension Registry**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry
- **Themes**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types
- **Icons**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types/icons

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above.
2. **Ask questions** - What colors or icons are needed? Are SVG sources available?
3. **Generate files** - Create manifest, CSS, and icon files based on the latest docs.
4. **Explain** - Show what was created and how to test or use the themes and icons.

## Theme Implementation

### Minimal Examples

#### Manifest (manifests.ts)
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

#### CSS Theme File (dark-theme.css)
```css
:root {
  /* Background colors */
  --uui-color-surface: #1e1e1e;
  --uui-color-text: #d4d4d4;
  /* Additional color variables... */
}
```

## Icon Implementation

### Minimal Examples

#### Manifest (umbraco-package.json)
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

#### Icons Registry (icons.ts)
```typescript
export default [
  {
    name: 'my-custom-icon',
    path: () => import('./icons/my-custom-icon.js'),
  },
  // Additional icons...
];
```

#### Icon File (icons/my-custom-icon.ts)
```typescript
export default `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
  <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
</svg>`;
```

## Best Practices

- Test themes and icons with all UI components.
- Ensure sufficient contrast for accessibility.
- Use CSS custom properties for consistency in themes.
- Keep examples minimal and generate complete working code.

That's it! Always fetch fresh docs and follow the workflow for successful implementation.