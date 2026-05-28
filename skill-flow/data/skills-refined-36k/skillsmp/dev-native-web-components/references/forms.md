# Forms in Shadow DOM Reference

> Native form integration with Declarative Shadow DOM components.

---

## The Challenge

Form elements inside Shadow DOM don't participate in form submission by default. The form can't "see" inputs inside shadow roots.

**Solution**: Use one of these patterns:

1. Keep form elements in light DOM (slot them)
2. Use Form-Associated Custom Elements (`ElementInternals`)

---

## Pattern 1: Slotted Form Elements (Recommended)

Keep form elements in light DOM and slot them into Shadow DOM for styling.

```html
<form-field>
  <template shadowrootmode="open">
    <style>
      :host {
        display: grid;
        gap: 0.25rem;
      }
      
      ::slotted(label) {
        font-weight: 500;
        font-size: 0.875rem;
      }
      
      ::slotted(input),
      ::slotted(textarea),
      ::slotted(select) {
        padding: 0.5rem 0.75rem;
        border: 1px solid var(--border);
        border-radius: 0.375rem;
        font: inherit;
        field-sizing: content; /* 2024 Baseline */
      }
      
      ::slotted(input:focus),
      ::slotted(textarea:focus),
      ::slotted(select:focus) {
        outline: 2px solid var(--accent);
        outline-offset: 2px;
      }
      
      /* Validation states using :has() */
      :host(:has(input:invalid:not(:placeholder-shown))) {
        --field-border: var(--error);
      }
      
      .error {
        color: var(--error);
        font-size: 0.75rem;
        display: none;
      }
      
      :host(:has(input:invalid:not(:placeholder-shown))) .error {
        display: block;
      }
    </style>
    
    <slot name="label"></slot>
    <slot name="input"></slot>
    <p class="error"><slot name="error">This field is invalid</slot></p>
    <slot name="hint"></slot>
  </template>
  
  <!-- Light DOM: participates in form -->
  <label slot="label" for="email">Email</label>
  <input slot="input" type="email" id="email" name="email" 
         placeholder="you@example.com" required>
  <span slot="error">Please enter a valid email address</span>
</form-field>
```

### Complete Form Example

```html
<form action="/api/contact" method="POST">
  <form-field>
    <template shadowrootmode="open">
      <!-- Styles from above -->
    </template>
    <label slot="label" for="name">Name</label>
    <input slot="input" type="text" id="name" name="name" required>
  </form-field>
  
  <form-field>
    <template shadowrootmode="open">
      <!-- Styles from above -->
    </template>
    <label slot="label" for="email">Email</label>
    <input slot="input" type="email" id="email" name="email" required>
  </form-field>
  
  <form-field>
    <template shadowrootmode="open">
      <!-- Styles from above -->
    </template>
    <label slot="label" for="message">Message</label>
    <textarea slot="input" id="message" name="message" rows="4" required></textarea>
  </form-field>
  
  <button type="submit">Send</button>
</form>
```

---

## Pattern 2: @scope for Light DOM Forms

Use `@scope` (Baseline 2025) for styling without Shadow DOM.

```html
<div class="form-field">
  <label for="username">Username</label>
  <input type="text" id="username" name="username" required>
  <p class="error">Username is required</p>
</div>

<style>
@scope (.form-field) {
  :scope {
    display: grid;
    gap: 0.25rem;
  }
  
  label {
    font-weight: 500;
    font-size: 0.875rem;
  }
  
  input, textarea, select {
    padding: 0.5rem 0.75rem;
    border: 1px solid var(--border);
    border-radius: 0.375rem;
    font: inherit;
  }
  
  input:focus {
    outline: 2px solid var(--accent);
    outline-offset: 2px;
  }
  
  .error {
    color: var(--error);
    font-size: 0.75rem;
    display: none;
  }
  
  :scope:has(input:invalid:not(:placeholder-shown)) .error {
    display: block;
  }
}
</style>
```

---

## Pattern 3: Form-Associated Custom Elements

For complex components that need to act as form controls.

> **Note**: This requires JavaScript. See `minimal-javascript.md` (coming soon) for implementation patterns.

### ElementInternals API Summary

| Method | Description |

|--------|-------------|
| `setFormValue(value)` | Set the value submitted with the form |
| `setValidity(flags, message, anchor)` | Set validation state |
| `reportValidity()` | Show validation message |
| `checkValidity()` | Check validity without UI |
| `form` | Reference to parent form |
| `labels` | Associated label elements |

_Reference: [MDN ElementInternals](https://developer.mozilla.org/en-US/docs/Web/API/ElementInternals)_

---

## Native Validation with DSD

Use native constraint validation with slotted inputs.

```html
<validated-input>
  <template shadowrootmode="open">
    <style>
      :host {
        display: grid;
        gap: 0.25rem;
      }
      
      /* Valid state */
      :host(:has(input:valid:not(:placeholder-shown))) {
        --icon: "✓";
        --icon-color: var(--success);
      }
      
      /* Invalid state */
      :host(:has(input:invalid:not(:placeholder-shown))) {
        --icon: "✗";
        --icon-color: var(--error);
      }
      
      .input-wrapper {
        position: relative;
      }
      
      .input-wrapper::after {
        content: var(--icon, "");
        position: absolute;
        right: 0.75rem;
        top: 50%;
        transform: translateY(-50%);
        color: var(--icon-color);
      }
      
      ::slotted(input) {
        width: 100%;
        padding: 0.5rem 2rem 0.5rem 0.75rem;
        border: 1px solid var(--border);
        border-radius: 0.375rem;
      }
    </style>
    
    <slot name="label"></slot>
    <div class="input-wrapper">
      <slot name="input"></slot>
    </div>
  </template>
  
  <label slot="label" for="url">Website URL</label>
  <input slot="input" type="url" id="url" name="url" 
         placeholder="https://example.com" required>
</validated-input>
```

---

## Auto-Growing Inputs (field-sizing)

Use `field-sizing: content` (Baseline 2024) for auto-growing textareas.

```css
::slotted(textarea) {
  field-sizing: content;
  min-height: 4rem;
  max-height: 20rem;
}
```

```html
<form-field>
  <template shadowrootmode="open">
    <style>
      ::slotted(textarea) {
        field-sizing: content;
        min-height: 4rem;
        max-height: 20rem;
        resize: vertical;
      }
    </style>
    <slot name="label"></slot>
    <slot name="input"></slot>
  </template>
  
  <label slot="label" for="bio">Bio</label>
  <textarea slot="input" id="bio" name="bio" 
            placeholder="Tell us about yourself..."></textarea>
</form-field>
```

---

## Validation Pattern Summary

| Pattern | Use Case | JS Required |

|---------|----------|-------------|
| `:has(input:invalid)` | Visual feedback in Shadow DOM | No |
| Slotted inputs | Full form participation | No |
| `@scope` styling | Light DOM forms | No |
| `ElementInternals` | Custom form controls | Yes (see `minimal-javascript.md`) |

---

## Checklist

- [ ] Keep form elements in light DOM when possible
- [ ] Use slots to project inputs into Shadow DOM
- [ ] Style validation states with `:has()` and `:invalid`
- [ ] Use `field-sizing: content` for auto-grow
- [ ] Use `ElementInternals` only for custom controls
- [ ] Associate labels with inputs correctly (id/for)
- [ ] Provide error messages for invalid states

---

_References:_

- [MDN ElementInternals](https://developer.mozilla.org/en-US/docs/Web/API/ElementInternals)
- [web.dev Learn Forms](https://web.dev/learn/forms/)
- [Chrome field-sizing](https://developer.chrome.com/docs/css-ui/css-field-sizing)
