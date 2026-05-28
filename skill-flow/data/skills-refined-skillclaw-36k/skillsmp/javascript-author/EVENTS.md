# Event Handling Guide

## Dispatching Custom Events

Always use CustomEvent with bubbles and composed:

```javascript
this.dispatchEvent(new CustomEvent('component-update', {
    detail: {
        value: newValue,
        previousValue: oldValue,
        source: 'user-interaction',
    },
    bubbles: true,    // Propagates up DOM tree
    composed: true,   // Crosses Shadow DOM boundary
}));
```

## Event Naming Convention

Use kebab-case, prefixed with component name:

| Pattern | Example |
|---------|---------|
| `{component}-{action}` | `color-picker-change` |
| `{component}-{noun}` | `msg-box-update` |
| General events | `debug-log`, `theme-change` |

## Debug Logging Pattern

Create a reusable logDebug method:

```javascript
/**
 * @private
 * Dispatches debug log event for external logging systems
 * @param {string} type - Event type (render, connect, error, etc.)
 * @param {string} message - Human-readable message
 * @param {Object} [data] - Optional data payload
 */
logDebug(type, message, data = null) {
    this.dispatchEvent(new CustomEvent('debug-log', {
        bubbles: true,
        composed: true,
        detail: {
            source: this.tagName.toLowerCase(),
            type,
            message,
            data,
            timestamp: Date.now(),
        },
    }));
}

// Usage examples
this.logDebug('render', 'Component rendered', { lang: this.lang });
this.logDebug('connected', 'Component connected to DOM');
this.logDebug('value-change', 'Value updated', { from: oldValue, to: newValue });
this.logDebug('error', 'Validation failed', { field: 'email', reason: 'invalid format' });
```

## Listening to Events

### Document-Level Events

For cross-component communication:

```javascript
connectedCallback() {
    // Store bound reference for cleanup
    this.boundHandler = this.handleExternalEvent.bind(this);
    document.addEventListener('theme-change', this.boundHandler);
}

disconnectedCallback() {
    document.removeEventListener('theme-change', this.boundHandler);
}

handleExternalEvent(event) {
    const { theme } = event.detail;
    this.updateTheme(theme);
}
```

### Shadow DOM Internal Events

For component-internal events:

```javascript
render() {
    this.shadowRoot.innerHTML = `...`;

    // Add listeners after render
    this.shadowRoot.querySelector('button')
        .addEventListener('click', (e) => this.handleClick(e));

    this.shadowRoot.querySelector('input')
        .addEventListener('input', (e) => this.handleInput(e));
}
```

### Event Delegation

For dynamic content:

```javascript
connectedCallback() {
    this.render();

    // Single listener on container
    this.shadowRoot.querySelector('.list')
        .addEventListener('click', (e) => {
            const item = e.target.closest('.list-item');
            if (item) {
                this.handleItemClick(item.dataset.id);
            }
        });
}
```

## Media Query Events

For system preference changes:

```javascript
constructor() {
    super();
    this.attachShadow({ mode: 'open' });

    // Set up media query listener
    this.darkModeQuery = window.matchMedia('(prefers-color-scheme: dark)');
    this.boundMediaHandler = this.handleDarkModeChange.bind(this);
}

connectedCallback() {
    this.darkModeQuery.addEventListener('change', this.boundMediaHandler);
    // Apply initial state
    this.handleDarkModeChange(this.darkModeQuery);
}

disconnectedCallback() {
    this.darkModeQuery.removeEventListener('change', this.boundMediaHandler);
}

handleDarkModeChange(event) {
    const isDark = event.matches;
    this.setAttribute('data-theme', isDark ? 'dark' : 'light');
}
```

## Event Detail Best Practices

Include sufficient context:

```javascript
// Good - contextual detail
this.dispatchEvent(new CustomEvent('form-submit', {
    detail: {
        formData: Object.fromEntries(new FormData(form)),
        submitTime: Date.now(),
        isValid: form.checkValidity(),
    },
    bubbles: true,
    composed: true,
}));

// Bad - minimal detail
this.dispatchEvent(new CustomEvent('submit', {
    detail: { data: formData },
}));
```

## Preventing Default and Stopping Propagation

```javascript
handleClick(event) {
    event.preventDefault();      // Prevent default action (e.g., form submit)
    event.stopPropagation();    // Stop bubbling (use sparingly)

    // Process click
}
```

## Input Event Handling

Debounce for performance:

```javascript
constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this.debounceTimer = null;
}

handleInput(event) {
    clearTimeout(this.debounceTimer);
    this.debounceTimer = setTimeout(() => {
        this.processInput(event.target.value);
    }, 300);
}

disconnectedCallback() {
    clearTimeout(this.debounceTimer);
}
```

## Keyboard Events

```javascript
handleKeydown(event) {
    switch (event.key) {
        case 'Enter':
        case ' ':
            event.preventDefault();
            this.activate();
            break;
        case 'Escape':
            this.close();
            break;
        case 'ArrowDown':
            event.preventDefault();
            this.focusNext();
            break;
        case 'ArrowUp':
            event.preventDefault();
            this.focusPrevious();
            break;
    }
}
```
