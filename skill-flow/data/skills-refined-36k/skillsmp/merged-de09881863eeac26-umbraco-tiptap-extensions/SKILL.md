---
name: umbraco-tiptap-extensions
description: Use this skill to implement various Tiptap extensions, including statusbar and toolbar components, for the Umbraco rich text editor using official documentation.
---

# Umbraco Tiptap Extensions

## What is it?
Tiptap Extensions enhance Umbraco's Rich Text Editor by adding new functionalities such as custom nodes, marks, toolbar buttons, and statusbar elements. These extensions can provide visual components, editor capabilities, and additional formatting options.

## Documentation
Always fetch the latest docs before implementing:

- **Extension Types**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types
- **Rich Text Editor**: https://docs.umbraco.com/umbraco-cms/fundamentals/backoffice/property-editors/built-in-umbraco-property-editors/rich-text-editor
- **Tiptap Docs**: https://tiptap.dev/docs/editor/extensions/overview
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation

## Related Skills

- **Tiptap Toolbar Extension**: For adding toolbar buttons.
- **Tiptap Statusbar Extension**: For adding statusbar elements.

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above.
2. **Ask questions** - What functionality is needed? Node, Mark, or Extension? Custom styles?
3. **Generate files** - Create manifest + API class based on latest docs.
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

### Extension API (highlight.tiptap-api.ts)
```typescript
import { UmbTiptapExtensionApiBase } from '@umbraco-cms/backoffice/tiptap';
import type { UmbTiptapExtensionArgs } from '@umbraco-cms/backoffice/tiptap';
import Highlight from '@tiptap/extension-highlight';

export default class HighlightTiptapExtensionApi extends UmbTiptapExtensionApiBase {
  getTiptapExtensions(args?: UmbTiptapExtensionArgs) {
    return [
      Highlight.configure({
        multicolor: true,
      }),
    ];
  }
}
```

### Custom Node Extension
```typescript
import { UmbTiptapExtensionApiBase } from '@umbraco-cms/backoffice/tiptap';
import { Node } from '@tiptap/core';

export default class CalloutTiptapExtensionApi extends UmbTiptapExtensionApiBase {
  getTiptapExtensions() {
    const CalloutNode = Node.create({
      name: 'callout',
      group: 'block',
      content: 'block+',

      addAttributes() {
        return {
          type: {
            default: 'info',
          },
        };
      },

      parseHTML() {
        return [{ tag: 'div[data-callout]' }];
      },

      renderHTML({ HTMLAttributes }) {
        return ['div', { 'data-callout': '', ...HTMLAttributes }, 0];
      },
    });

    return [CalloutNode];
  }
}
```

### Toolbar Button Kind Manifest (manifests.ts)
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

### Statusbar Element Example
```typescript
import { html, css, customElement, state } from '@umbraco-cms/backoffice/external/lit';
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';
import { UMB_TIPTAP_RTE_CONTEXT } from '@umbraco-cms/backoffice/tiptap';

@customElement('my-word-count-statusbar')
export class WordCountStatusbarElement extends UmbLitElement {
  @state()
  private _wordCount = 0;

  @state()
  private _charCount = 0;

  constructor() {
    super();

    this.consumeContext(UMB_TIPTAP_RTE_CONTEXT, (context) => {
      this.observe(context.editor, (editor) => {
        if (editor) {
          editor.on('update', () => this.#updateCounts(editor));
          this.#updateCounts(editor);
        }
      });
    });
  }

  #updateCounts(editor: any) {
    const text = editor.getText();
    this._charCount = text.length;
    this._wordCount = text.trim() ? text.trim().split(/\s+/).length : 0;
  }

  render() {
    return html`
      <span class="count">Words: ${this._wordCount}</span>
      <span class="count">Characters: ${this._charCount}</span>
    `;
  }

  static styles = css`
    :host {
      display: flex;
      gap: var(--uui-size-space-4);
      font-size: var(--uui-type-small-size);
      color: var(--uui-color-text-alt);
    }

    .count {
      padding: 0 var(--uui-size-space-2);
    }
  `;
}

export default WordCountStatusbarElement;
```

## Meta Properties

| Property | Description |
|----------|-------------|
| `alias` | Unique identifier for the extension or toolbar item |
| `icon` | Icon shown in configuration UI |
| `label` | Display name |
| `group` | Group for organizing extensions |
| `description` | Optional description |

## Common Extension Groups

- `formatting` - Text formatting (bold, italic, etc.)
- `structure` - Structural elements (headings, lists, etc.)
- `media` - Media elements (images, embeds, etc.)
- `misc` - Other functionality

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.