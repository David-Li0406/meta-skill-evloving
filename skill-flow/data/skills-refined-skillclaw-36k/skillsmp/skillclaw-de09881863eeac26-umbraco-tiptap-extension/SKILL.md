---
name: umbraco-tiptap-extension
description: Use this skill when you want to implement Tiptap extensions, including toolbar and statusbar components, for the Umbraco rich text editor using official documentation.
---

# Umbraco Tiptap Extension

## What is it?
A Tiptap Extension adds functionality to Umbraco's Rich Text Editor (which is built on Tiptap). Extensions can add new node types, marks, or other editor capabilities, as well as components to the toolbar or status bar.

## Documentation
Always fetch the latest docs before implementing:

- **Extension Types**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types
- **Rich Text Editor**: https://docs.umbraco.com/umbraco-cms/fundamentals/backoffice/property-editors/built-in-umbraco-property-editors/rich-text-editor
- **Tiptap Docs**: https://tiptap.dev/docs/editor/extensions/overview
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation

## Related Skills

- **Tiptap Toolbar Extension**: For adding toolbar buttons and controls.
- **Tiptap Statusbar Extension**: For adding statusbar elements.

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above.
2. **Ask questions** - What functionality is needed? Is it a node, mark, toolbar button, or statusbar element?
3. **Generate files** - Create manifest and API class based on the latest docs.
4. **Explain** - Show what was created and how to test.

## Minimal Examples

### Manifest (manifests.ts)
```typescript
import type { ManifestTiptapExtension } from '@umbraco-cms/backoffice/extension-registry';

const manifest: ManifestTiptapExtension = {
  type: 'tiptapExtension',
  alias: 'My.TiptapExtension.Highlight',
  name: 'Highlight Extension',
  api: () => import('./highlight.tiptap-api.js'),
  meta: {
    icon: 'icon-marker',
    label: 'Highlight',
    group: 'formatting',
  },
};

export const manifests = [manifest];
```

### Statusbar Element (word-count.statusbar-element.ts)
```typescript
import { html, css, customElement, state } from '@umbraco-cms/backoffice/external/lit';
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';

@customElement('word-count-statusbar')
export class WordCountStatusbar extends UmbLitElement {
  @state() wordCount = 0;

  // Logic to update word count
  // ...
}
```

### Button Kind Manifest (manifests.ts)
```typescript
import type { ManifestTiptapToolbarExtensionButtonKind } from '@umbraco-cms/backoffice/extension-registry';

const manifest: ManifestTiptapToolbarExtensionButtonKind = {
  type: 'tiptapToolbarExtension',
  kind: 'button',
  alias: 'My.TiptapToolbar.Bold',
  name: 'Bold Toolbar Button',
  api: () => import('./bold.tiptap-toolbar-api.js'),
  forExtensions: ['Umb.Tiptap.Bold'],
  meta: {
    alias: 'bold',
    icon: 'icon-bold',
    label: 'Bold',
  },
};

export const manifests = [manifest];
```