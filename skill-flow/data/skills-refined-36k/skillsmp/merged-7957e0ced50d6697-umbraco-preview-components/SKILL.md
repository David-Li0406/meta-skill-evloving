---
name: umbraco-preview-components
description: Use this skill when implementing custom preview components for content and file uploads in the Umbraco backoffice.
---

# Umbraco Preview Components

## What is it?
Umbraco Preview Components allow you to create custom items in the preview window menu and file upload previews in the Umbraco backoffice. These components enhance the content editing experience by providing additional functionalities such as device simulation, accessibility checks, SEO analysis, and visual representations of uploaded files based on their MIME types.

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
2. **Ask questions** - What preview functionality or MIME types? What UI?
3. **Generate files** - Create manifest + element based on latest docs.
4. **Explain** - Show what was created and how to test.

## Minimal Examples

### Preview App Manifest (manifests.ts)
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

### Preview App Element Implementation (my-preview-app.element.ts)
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
    // Apply your preview functionality
    this.#applyPreviewMode(this._isActive);
  }

  #applyPreviewMode(active: boolean) {
    // Access the preview iframe or apply styles
    const previewFrame = document.querySelector('iframe.preview-frame');
    if (previewFrame && active) {
      // Apply custom preview mode
    }
  }
}

export default MyPreviewAppElement;
```

### File Upload Preview Element Implementation (my-file-preview.element.ts)
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
    if (this._previewUrl) {
      URL.revokeObjectURL(this._previewUrl);
    }
  }

  override render() {
    if (!this.file) return html``;

    return html`
      <div class="preview-container">
        <uui-icon name="icon-document"></uui-icon>
        <span>${this.file.name}</span>
      </div>
    `;
  }
}

export default MyFilePreviewElement;
```

## Interface References

```typescript
interface ManifestPreviewAppProvider extends ManifestElement {
  type: 'previewApp';
}

interface ManifestFileUploadPreview extends ManifestElement<UmbFileUploadPreviewElement> {
  type: 'fileUploadPreview';
  forMimeTypes: string | Array<string>; // e.g., 'image/*', ['image/png', 'image/jpeg']
}

interface UmbFileUploadPreviewElement {
  file?: File;
}
```

## Best Practices

- Keep the UI compact as it appears in a menu.
- Provide clear enable/disable states.
- Consider the preview context and available iframe.
- Use appropriate icons for quick recognition.

That's it! Always fetch fresh docs, keep examples minimal, and generate complete working code.