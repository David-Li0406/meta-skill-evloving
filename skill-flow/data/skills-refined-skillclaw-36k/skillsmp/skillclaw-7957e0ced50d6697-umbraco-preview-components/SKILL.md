---
name: umbraco-preview-components
description: Use this skill when implementing custom preview components in the Umbraco backoffice for various functionalities like file uploads and preview apps.
---

# Skill body

## What is it?
Umbraco Preview Components allow developers to create custom preview functionalities in the Umbraco backoffice. This includes adding preview app providers to the preview menu and rendering file upload previews for specific file types.

## Documentation
Always fetch the latest docs before implementing:

- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Extension Registry**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry
- **Umbraco Element**: https://docs.umbraco.com/umbraco-cms/customizing/foundation/umbraco-element

## Related Foundation Skills

- **Umbraco Element**: Base class for creating UI components
  - Reference skill: `umbraco-umbraco-element`

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above.
2. **Ask questions** - Determine the functionality needed for the preview (e.g., what MIME types for file uploads or what UI for preview apps).
3. **Generate files** - Create the necessary manifest and element files based on the latest documentation.
4. **Explain** - Show what was created and how to test the components.

## Minimal Examples

### Preview App Provider Manifest (manifests.ts)
```typescript
import type { ManifestPreviewAppProvider } from '@umbraco-cms/backoffice/extension-registry';

export const manifests: Array<ManifestPreviewAppProvider> = [
  {
    type: 'previewApp',
    alias: 'My.PreviewApp',
    name: 'My Preview App',
    element: () => import('./my-preview-app.element.js'),
  },
];
```

### File Upload Preview Manifest (manifests.ts)
```typescript
export const manifests: Array<UmbExtensionManifest> = [
  {
    type: 'fileUploadPreview',
    alias: 'My.FileUploadPreview.Custom',
    name: 'Custom File Upload Preview',
    weight: 100,
    element: () => import('./my-file-preview.element.js'),
    forMimeTypes: ['application/pdf', 'application/x-pdf'],
  },
];
```

### Element Implementation for Preview App (my-preview-app.element.ts)
```typescript
import { html, customElement, state } from '@umbraco-cms/backoffice/external/lit';
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';

@customElement('my-preview-app')
export class MyPreviewAppElement extends UmbLitElement {
  @state()
  private _isActive = false;

  override render() {
    return html`
      <uui-box headline="My Preview Tool">
        <p>Custom preview functionality</p>

        <uui-button
          look=${this._isActive ? 'primary' : 'default'}
          @click=${this.#toggle}
        >
          ${this._isActive ? 'Disable' : 'Enable'}
        </uui-button>
      </uui-box>
    `;
  }

  #toggle() {
    this._isActive = !this._isActive;
  }
}
```

### Element Implementation for File Upload Preview (my-file-preview.element.ts)
```typescript
import { html, customElement, property, state } from '@umbraco-cms/backoffice/external/lit';
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';
import type { UmbFileUploadPreviewElement } from '@umbraco-cms/backoffice/media';

@customElement('my-file-preview')
export class MyFilePreviewElement extends UmbLitElement implements UmbFileUploadPreviewElement {
  @property({ type: Object })
  file?: File;

  @state()
  private _previewUrl?: string;

  override updated(changedProperties: Map<string, unknown>) {
    if (changedProperties.has('file') && this.file) {
      this._previewUrl = URL.createObjectURL(this.file);
    }
  }

  override disconnectedCallback() {
    super.disconnectedCallback();
    // Clean up the object URL if necessary
    if (this._previewUrl) {
      URL.revokeObjectURL(this._previewUrl);
    }
  }
}