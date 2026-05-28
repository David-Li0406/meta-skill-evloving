# Custom Elements Manifest

Generate a `custom-elements.json` manifest to document your web components for IDEs, Storybook, documentation tools, and framework integrations.

## Quick Setup

```bash
# Install the analyzer
npm i -D @custom-elements-manifest/analyzer

# Generate manifest
npx cem analyze

# Or add to package.json scripts
```

Add to `package.json`:

```json
{
  "scripts": {
    "manifest": "cem analyze",
    "manifest:watch": "cem analyze --watch"
  },
  "customElements": "custom-elements.json"
}
```

---

## Configuration

Create `custom-elements-manifest.config.mjs` in project root:

```javascript
export default {
  globs: ['src/components/**/*.js'],
  exclude: ['**/*.test.js', '**/*.spec.js'],
  outdir: '.',
  dev: false,
  watch: false,
  dependencies: false,
  packagejson: true
};
```

### Configuration Options

| Option | Type | Description |
|--------|------|-------------|
| `globs` | string[] | File patterns to analyze |
| `exclude` | string[] | Patterns to skip |
| `outdir` | string | Output directory for manifest |
| `dev` | boolean | Enable debug logging |
| `watch` | boolean | Watch mode for changes |
| `dependencies` | boolean | Include dependency manifests |
| `packagejson` | boolean | Add customElements to package.json |

---

## JSDoc Annotations

Document your components using these JSDoc tags:

### Element Metadata

```javascript
/**
 * A card component for displaying content.
 *
 * @summary Displays content in a bordered card layout.
 * @tag my-card
 * @tagname my-card
 */
class MyCard extends HTMLElement {
  // ...
}
```

### Attributes

```javascript
/**
 * @attr {string} variant - Visual style variant
 * @attr {boolean} disabled - Whether the card is disabled
 * @attribute {string} title - Card title text
 */
class MyCard extends HTMLElement {
  static get observedAttributes() {
    return ['variant', 'disabled', 'title'];
  }
}
```

### Properties

```javascript
class MyCard extends HTMLElement {
  /**
   * The card's heading text.
   * @type {string}
   * @default ''
   */
  heading = '';

  /**
   * Whether the card is expanded.
   * @type {boolean}
   * @default false
   */
  expanded = false;

  /**
   * Card data object.
   * @type {{ title: string, body: string }}
   */
  data;
}
```

### Events

```javascript
/**
 * @fires {CustomEvent} card-click - Fired when card is clicked
 * @fires {CustomEvent<{ id: string }>} card-select - Fired when card is selected
 * @event card-close Fired when card is closed
 */
class MyCard extends HTMLElement {
  handleClick() {
    this.dispatchEvent(new CustomEvent('card-click', {
      bubbles: true,
      composed: true
    }));
  }
}
```

### Slots

```javascript
/**
 * @slot - Default slot for card content
 * @slot header - Slot for card header content
 * @slot footer - Slot for card footer content
 * @slot actions - Slot for action buttons
 */
class MyCard extends HTMLElement {
  connectedCallback() {
    this.shadowRoot.innerHTML = `
      <header><slot name="header"></slot></header>
      <main><slot></slot></main>
      <footer><slot name="footer"></slot></footer>
    `;
  }
}
```

### CSS Custom Properties

```javascript
/**
 * @cssprop {<color>} --card-bg - Card background color
 * @cssprop {<length>} --card-padding - Card padding
 * @cssprop {<length>} [--card-radius=8px] - Card border radius
 * @cssproperty {<color>} --card-border - Card border color
 */
class MyCard extends HTMLElement {}
```

### CSS Parts

```javascript
/**
 * @csspart container - The card container
 * @csspart header - The card header section
 * @csspart content - The main content area
 * @part footer - The card footer section
 */
class MyCard extends HTMLElement {
  connectedCallback() {
    this.shadowRoot.innerHTML = `
      <div part="container">
        <header part="header"><slot name="header"></slot></header>
        <main part="content"><slot></slot></main>
        <footer part="footer"><slot name="footer"></slot></footer>
      </div>
    `;
  }
}
```

### Internal/Private Members

```javascript
class MyCard extends HTMLElement {
  /**
   * Internal state - excluded from manifest.
   * @internal
   */
  _internalState = {};

  /**
   * Ignored helper method.
   * @ignore
   */
  _helper() {}
}
```

---

## Complete Example

```javascript
/**
 * A customizable card component for displaying content.
 *
 * @summary Flexible card layout with header, content, and footer slots.
 * @tag product-card
 *
 * @attr {string} variant - Visual variant: "default" | "outlined" | "elevated"
 * @attr {boolean} clickable - Makes the card interactive
 * @attr {string} href - Optional link URL
 *
 * @slot - Default slot for main content
 * @slot header - Card header content
 * @slot media - Image or media content
 * @slot actions - Action buttons
 *
 * @cssprop {<color>} [--card-bg=#ffffff] - Card background
 * @cssprop {<color>} [--card-border=#e0e0e0] - Border color
 * @cssprop {<length>} [--card-padding=1rem] - Content padding
 * @cssprop {<length>} [--card-radius=8px] - Border radius
 *
 * @csspart card - The card container element
 * @csspart header - Header section
 * @csspart content - Main content area
 * @csspart actions - Actions container
 *
 * @fires {CustomEvent} card-click - Emitted when card is clicked
 * @fires {CustomEvent<{ href: string }>} card-navigate - Emitted on navigation
 */
class ProductCard extends HTMLElement {
  static get observedAttributes() {
    return ['variant', 'clickable', 'href'];
  }

  /**
   * The card variant style.
   * @type {'default' | 'outlined' | 'elevated'}
   * @default 'default'
   */
  variant = 'default';

  /**
   * Whether the card responds to clicks.
   * @type {boolean}
   * @default false
   */
  clickable = false;

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  render() {
    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
          --_bg: var(--card-bg, #ffffff);
          --_border: var(--card-border, #e0e0e0);
          --_padding: var(--card-padding, 1rem);
          --_radius: var(--card-radius, 8px);
        }
        .card {
          background: var(--_bg);
          border: 1px solid var(--_border);
          border-radius: var(--_radius);
          overflow: hidden;
        }
        .content {
          padding: var(--_padding);
        }
      </style>
      <article class="card" part="card">
        <header part="header"><slot name="header"></slot></header>
        <slot name="media"></slot>
        <div class="content" part="content"><slot></slot></div>
        <footer part="actions"><slot name="actions"></slot></footer>
      </article>
    `;
  }
}

customElements.define('product-card', ProductCard);
export { ProductCard };
```

---

## Manifest Output

The analyzer generates `custom-elements.json`:

```json
{
  "schemaVersion": "2.1.0",
  "readme": "",
  "modules": [
    {
      "kind": "javascript-module",
      "path": "src/components/product-card.js",
      "declarations": [
        {
          "kind": "class",
          "name": "ProductCard",
          "customElement": true,
          "tagName": "product-card",
          "summary": "Flexible card layout with header, content, and footer slots.",
          "attributes": [
            {
              "name": "variant",
              "type": { "text": "string" },
              "description": "Visual variant: \"default\" | \"outlined\" | \"elevated\""
            }
          ],
          "slots": [
            {
              "name": "",
              "description": "Default slot for main content"
            },
            {
              "name": "header",
              "description": "Card header content"
            }
          ],
          "cssProperties": [
            {
              "name": "--card-bg",
              "default": "#ffffff",
              "description": "Card background"
            }
          ],
          "cssParts": [
            {
              "name": "card",
              "description": "The card container element"
            }
          ],
          "events": [
            {
              "name": "card-click",
              "type": { "text": "CustomEvent" },
              "description": "Emitted when card is clicked"
            }
          ]
        }
      ],
      "exports": [
        {
          "kind": "custom-element-definition",
          "name": "product-card",
          "declaration": { "name": "ProductCard" }
        }
      ]
    }
  ]
}
```

---

## Tool Integrations

### Storybook

Install addon:

```bash
npm i -D @storybook/addon-docs
```

Configure `.storybook/main.js`:

```javascript
export default {
  addons: ['@storybook/addon-docs'],
  docs: {
    autodocs: true
  }
};
```

Storybook reads `custom-elements.json` for automatic documentation.

### VS Code

Add to `.vscode/settings.json`:

```json
{
  "html.customData": ["./custom-elements.json"]
}
```

### JetBrains IDEs

WebStorm and IntelliJ automatically detect `custom-elements.json` for completion.

### API Viewer

Use with `api-viewer-element`:

```html
<api-viewer src="./custom-elements.json"></api-viewer>
```

---

## Syncing with elements.json

Keep `.claude/schemas/elements.json` (for HTML validation) in sync with your manifest:

```bash
# Generate manifest
npm run manifest

# Then update elements.json to match
```

Consider creating a script to sync both:

```javascript
// scripts/sync-elements.js
import { readFileSync, writeFileSync } from 'fs';

const manifest = JSON.parse(readFileSync('custom-elements.json', 'utf-8'));
const elements = JSON.parse(readFileSync('.claude/schemas/elements.json', 'utf-8'));

// Sync custom elements from manifest to elements.json
for (const module of manifest.modules) {
  for (const declaration of module.declarations || []) {
    if (declaration.customElement && declaration.tagName) {
      const tagName = declaration.tagName;

      if (!elements[tagName]) {
        elements[tagName] = {
          flow: true,
          permittedContent: ['@flow'],
          attributes: {}
        };
      }

      // Sync attributes
      for (const attr of declaration.attributes || []) {
        elements[tagName].attributes[attr.name] = {
          required: attr.required || false
        };
      }
    }
  }
}

writeFileSync('.claude/schemas/elements.json', JSON.stringify(elements, null, 2));
console.log('Synced elements.json with custom-elements.json');
```

---

## Checklist

When creating a new web component:

- [ ] Add JSDoc with `@tag` or `@tagname`
- [ ] Document `@attr` for each observed attribute
- [ ] Document `@slot` for each slot
- [ ] Document `@cssprop` for each CSS custom property
- [ ] Document `@csspart` for each shadow part
- [ ] Document `@fires` for each custom event
- [ ] Run `npm run manifest` to regenerate
- [ ] Update `.claude/schemas/elements.json` if needed for HTML validation

## Related Skills

- **javascript-author** - Write vanilla JavaScript for Web Components
- **data-attributes** - Using data-* attributes for state and variants
- **accessibility-checker** - Ensure WCAG2AA compliance
- **state-management** - Client-side state patterns for Web Components
