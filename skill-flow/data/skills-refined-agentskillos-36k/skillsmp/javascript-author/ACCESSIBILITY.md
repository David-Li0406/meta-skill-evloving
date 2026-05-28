# Accessibility in JavaScript

## Focus Management

### After Dynamic Content Updates

```javascript
// After removing content, move focus appropriately
handleDelete(item) {
    const nextItem = item.nextElementSibling || item.previousElementSibling;
    item.remove();

    if (nextItem) {
        nextItem.focus();
    } else {
        this.shadowRoot.querySelector('.empty-message')?.focus();
    }
}

// After adding content, focus the new element
handleAdd() {
    const newItem = this.createItem();
    this.container.appendChild(newItem);
    newItem.focus();
}
```

### Modal/Dialog Focus Trapping

```javascript
openModal() {
    this.previousFocus = document.activeElement;
    this.modal.hidden = false;

    // Focus first focusable element
    const firstFocusable = this.modal.querySelector(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    firstFocusable?.focus();

    // Trap focus
    this.modal.addEventListener('keydown', this.handleModalKeydown.bind(this));
}

closeModal() {
    this.modal.hidden = true;
    this.previousFocus?.focus();
}

handleModalKeydown(event) {
    if (event.key === 'Escape') {
        this.closeModal();
        return;
    }

    if (event.key !== 'Tab') return;

    const focusables = this.modal.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    const first = focusables[0];
    const last = focusables[focusables.length - 1];

    if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
    }
}
```

## Keyboard Navigation

Support full keyboard interaction:

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
        case 'Home':
            event.preventDefault();
            this.focusFirst();
            break;
        case 'End':
            event.preventDefault();
            this.focusLast();
            break;
    }
}

focusNext() {
    const items = [...this.shadowRoot.querySelectorAll('[role="option"]')];
    const current = this.shadowRoot.activeElement;
    const index = items.indexOf(current);
    const next = items[index + 1] || items[0];
    next.focus();
}
```

## ARIA Attributes

Update ARIA states dynamically:

```javascript
// Toggle expanded state
toggleExpanded() {
    const expanded = this.getAttribute('aria-expanded') === 'true';
    this.setAttribute('aria-expanded', String(!expanded));
    this.panel.hidden = expanded;
}

// Update selected state in a listbox
selectItem(item) {
    // Remove selection from all
    this.items.forEach((i) => i.setAttribute('aria-selected', 'false'));
    // Select current
    item.setAttribute('aria-selected', 'true');
    // Update aria-activedescendant
    this.listbox.setAttribute('aria-activedescendant', item.id);
}

// Update busy state during loading
async loadData() {
    this.setAttribute('aria-busy', 'true');
    try {
        await this.fetchData();
    } finally {
        this.setAttribute('aria-busy', 'false');
    }
}
```

## Live Regions

Announce changes to screen readers:

```html
<!-- In template -->
<div role="status" aria-live="polite" class="sr-only"></div>
```

```javascript
announceChange(message) {
    const announcer = this.shadowRoot.querySelector('[role="status"]');
    // Clear first to ensure re-announcement
    announcer.textContent = '';
    requestAnimationFrame(() => {
        announcer.textContent = message;
    });
}

// Usage
this.announceChange('Item added to cart');
this.announceChange(`${count} results found`);
this.announceChange('Form submitted successfully');
```

Screen reader only CSS:

```css
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}
```

## Reduced Motion

Respect user preference:

```javascript
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

animateElement(element) {
    if (prefersReducedMotion.matches) {
        // Instant change, no animation
        element.style.opacity = '1';
    } else {
        // Animate
        element.animate(
            [{ opacity: 0 }, { opacity: 1 }],
            { duration: 300, easing: 'ease-out' }
        );
    }
}
```

In CSS:

```css
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}
```

## Form Validation

Announce validation errors:

```javascript
handleInvalid(input) {
    const error = input.validationMessage;

    input.setAttribute('aria-invalid', 'true');
    input.setAttribute('aria-describedby', `${input.id}-error`);

    // Show error message
    const errorEl = this.shadowRoot.querySelector(`#${input.id}-error`);
    errorEl.textContent = error;

    // Announce to screen reader
    this.announceChange(error);
}

handleValid(input) {
    input.removeAttribute('aria-invalid');
    input.removeAttribute('aria-describedby');

    const errorEl = this.shadowRoot.querySelector(`#${input.id}-error`);
    errorEl.textContent = '';
}
```

## Template Accessibility

Ensure templates include proper attributes:

```javascript
export const template = (t) => `
    <button type="button"
            aria-label="${t.toggleLabel}"
            aria-expanded="false"
            aria-controls="panel">
        <span aria-hidden="true">${t.icon}</span>
        ${t.buttonText}
    </button>

    <div id="panel"
         role="region"
         aria-labelledby="panel-title"
         hidden>
        <h2 id="panel-title">${t.panelTitle}</h2>
        <div role="status" aria-live="polite" class="sr-only"></div>
    </div>
`;
```

## Image Accessibility

Handle decorative vs informative images:

```javascript
// Decorative - hide from screen readers
`<span class="icon" aria-hidden="true">${iconSvg}</span>`

// Informative - provide alt text
`<img src="${src}" alt="${alt}" />`

// Icon buttons need labels
`<button type="button" aria-label="${t.deleteLabel}">
    <span aria-hidden="true">${deleteIcon}</span>
</button>`
```

## Color and Contrast

Never rely on color alone:

```javascript
// Bad - color only
`<span class="${isError ? 'red' : 'green'}">${message}</span>`

// Good - color plus text/icon
`<span class="${isError ? 'error' : 'success'}">
    <span aria-hidden="true">${isError ? '!' : '✓'}</span>
    ${message}
</span>`
```
