# Web Components Guide

## Documentation with Custom Elements Manifest

Document components with JSDoc for automatic manifest generation:

```javascript
/**
 * A button component with loading state.
 *
 * @summary Interactive button with loading indicator.
 * @tag action-button
 *
 * @attr {string} variant - Button style: "primary" | "secondary"
 * @attr {boolean} loading - Shows loading spinner
 * @attr {boolean} disabled - Disables interaction
 *
 * @slot - Button label content
 * @slot icon - Optional icon slot
 *
 * @cssprop {<color>} [--button-bg=#0066cc] - Background color
 * @cssprop {<color>} [--button-text=#ffffff] - Text color
 *
 * @csspart button - The button element
 *
 * @fires {CustomEvent} action-click - Fired on button click
 */
class ActionButton extends HTMLElement { }
```

See [custom-elements/MANIFEST.md](../custom-elements/MANIFEST.md) for full documentation.

---

## Lifecycle Callbacks

### constructor()

Called when element is created:

```javascript
constructor() {
    super();  // MUST call super() first
    this.attachShadow({ mode: 'open' });
}
```

### connectedCallback()

Called when element is added to DOM:

```javascript
connectedCallback() {
    this.render();

    // Add document-level event listeners
    this.boundHandler = this.handleEvent.bind(this);
    document.addEventListener('external-event', this.boundHandler);

    // Set up MutationObserver for lang changes
    this.langObserver = new MutationObserver(() => this.render());

    this.langObserver.observe(document.documentElement, {
        attributes: true,
        attributeFilter: ['lang']
    });

    // Observe ancestor lang attributes
    let ancestor = this.parentElement;
    while (ancestor) {
        if (ancestor.hasAttribute('lang')) {
            this.langObserver.observe(ancestor, {
                attributes: true,
                attributeFilter: ['lang']
            });
        }
        ancestor = ancestor.parentElement;
    }
}
```

### disconnectedCallback()

Called when element is removed - MUST clean up:

```javascript
disconnectedCallback() {
    // Remove event listeners
    document.removeEventListener('external-event', this.boundHandler);

    // Disconnect observers
    this.langObserver?.disconnect();
}
```

### attributeChangedCallback()

Called when observed attributes change:

```javascript
static get observedAttributes() {
    return ['lang', 'value', 'disabled'];
}

attributeChangedCallback(name, oldValue, newValue) {
    if (oldValue !== newValue) {
        switch (name) {
            case 'lang':
                this.render();
                break;
            case 'value':
                this.handleValueChange(newValue);
                break;
            case 'disabled':
                this.updateDisabledState(newValue !== null);
                break;
        }
    }
}
```

## Shadow DOM

Always use open mode for debugging:

```javascript
constructor() {
    super();
    this.attachShadow({ mode: 'open' });
}
```

### Querying Shadow DOM

```javascript
// Query within shadow root
const button = this.shadowRoot.querySelector('button');
const inputs = this.shadowRoot.querySelectorAll('input');

// Store references after render
render() {
    this.shadowRoot.innerHTML = `...`;
    this.input = this.shadowRoot.querySelector('input');
    this.button = this.shadowRoot.querySelector('button');
}
```

## Template Pattern

Templates are pure functions that receive translations:

```javascript
// my-component-template.js
export const template = (t) => `
    <div class="container">
        <h2>${t.title}</h2>
        <button type="button">${t.submit}</button>
    </div>
`;
```

With multiple parameters:

```javascript
export const template = ({ title, items, showFooter }) => `
    <article>
        <h2>${title}</h2>
        <ul>
            ${items.map((item) => `<li>${item}</li>`).join('')}
        </ul>
        ${showFooter ? '<footer>Footer content</footer>' : ''}
    </article>
`;
```

## Styles Pattern

Export CSS as a string:

```javascript
// my-component-styles.js
export const styles = `
    :host {
        display: block;
        margin: var(--size-3);
    }

    :host([hidden]) {
        display: none;
    }

    .container {
        padding: var(--size-2);
        background: var(--surface-1);
        border-radius: var(--radius-2);
    }

    button {
        background: var(--brand);
        color: var(--text-on-brand);
        border: none;
        padding: var(--size-2) var(--size-3);
        border-radius: var(--radius-2);
        cursor: pointer;
    }

    button:focus {
        outline: 2px solid var(--brand);
        outline-offset: 2px;
    }
`;
```

Use Open Props custom properties for consistency.

## Observed Attributes

Always include 'lang' for i18n support:

```javascript
static get observedAttributes() {
    return ['lang', 'value', 'disabled', 'required'];
}
```

## Custom Element Registration

```javascript
// At end of file
customElements.define('my-component', MyComponent);

// Named export for testing
export { MyComponent };
```
