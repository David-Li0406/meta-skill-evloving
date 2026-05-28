# ARIA Patterns Guide

## Golden Rules of ARIA

1. **Don't use ARIA if you can use native HTML**
2. **Don't change native semantics** (unless necessary)
3. **All interactive ARIA controls must be keyboard accessible**
4. **Don't use `role="presentation"` or `aria-hidden="true"` on focusable elements**
5. **All interactive elements must have an accessible name**

## Common Patterns

### Buttons

```html
<!-- Native button (preferred) -->
<button type="button">Click me</button>

<!-- Custom button (when necessary) -->
<div role="button"
     tabindex="0"
     aria-pressed="false"
     onkeydown="handleKeyDown(event)"
     onclick="toggle()">
  Toggle Option
</div>

<!-- Icon button with accessible name -->
<button aria-label="Close dialog">
  <svg aria-hidden="true">...</svg>
</button>

<!-- Toggle button -->
<button aria-pressed="false" onclick="togglePress(this)">
  Bold
</button>
```

### Links vs Buttons

```html
<!-- Link: navigates to URL -->
<a href="/page">Go to page</a>

<!-- Button: performs action -->
<button onclick="doAction()">Save</button>

<!-- Common mistake: link that acts as button -->
<!-- Bad -->
<a href="#" onclick="doAction()">Save</a>

<!-- Good -->
<button onclick="doAction()">Save</button>
```

### Forms

```html
<!-- Basic labeled input -->
<label for="username">Username</label>
<input type="text" id="username" name="username">

<!-- Required field -->
<label for="email">
  Email <span aria-hidden="true">*</span>
</label>
<input type="email" id="email" required aria-required="true">

<!-- Input with description -->
<label for="password">Password</label>
<input type="password" id="password"
       aria-describedby="password-help password-error">
<div id="password-help">Must be at least 8 characters</div>
<div id="password-error" role="alert"></div>

<!-- Error state -->
<input type="email" id="email"
       aria-invalid="true"
       aria-describedby="email-error">
<div id="email-error" role="alert">
  Please enter a valid email address
</div>

<!-- Group of checkboxes -->
<fieldset>
  <legend>Notification preferences</legend>
  <label>
    <input type="checkbox" name="notify" value="email">
    Email notifications
  </label>
  <label>
    <input type="checkbox" name="notify" value="sms">
    SMS notifications
  </label>
</fieldset>
```

### Dialogs (Modals)

```html
<div role="dialog"
     aria-modal="true"
     aria-labelledby="dialog-title"
     aria-describedby="dialog-desc">
  <h2 id="dialog-title">Confirm Delete</h2>
  <p id="dialog-desc">Are you sure you want to delete this item?</p>
  <button>Cancel</button>
  <button>Delete</button>
</div>

<script>
// Focus management
function openDialog() {
  const dialog = document.querySelector('[role="dialog"]');
  const firstFocusable = dialog.querySelector('button, [tabindex="0"]');
  dialog.style.display = 'block';
  firstFocusable.focus();
  // Trap focus within dialog
}

function closeDialog() {
  // Return focus to trigger element
  triggerElement.focus();
}
</script>
```

### Navigation

```html
<!-- Primary navigation -->
<nav aria-label="Main">
  <ul>
    <li><a href="/" aria-current="page">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li><a href="/about">About</a></li>
  </ul>
</nav>

<!-- Secondary navigation -->
<nav aria-label="Footer">
  <ul>...</ul>
</nav>

<!-- Breadcrumb -->
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li><a href="/products/widgets" aria-current="page">Widgets</a></li>
  </ol>
</nav>
```

### Tabs

```html
<div class="tabs">
  <div role="tablist" aria-label="Account settings">
    <button role="tab"
            aria-selected="true"
            aria-controls="panel-1"
            id="tab-1"
            tabindex="0">
      Profile
    </button>
    <button role="tab"
            aria-selected="false"
            aria-controls="panel-2"
            id="tab-2"
            tabindex="-1">
      Security
    </button>
  </div>

  <div role="tabpanel"
       id="panel-1"
       aria-labelledby="tab-1"
       tabindex="0">
    Profile content...
  </div>

  <div role="tabpanel"
       id="panel-2"
       aria-labelledby="tab-2"
       tabindex="0"
       hidden>
    Security content...
  </div>
</div>

<script>
// Arrow key navigation between tabs
// Tab key moves to tab panel
// Home/End moves to first/last tab
</script>
```

### Accordions

```html
<div class="accordion">
  <h3>
    <button aria-expanded="true" aria-controls="section-1">
      Section 1
    </button>
  </h3>
  <div id="section-1">
    Section 1 content...
  </div>

  <h3>
    <button aria-expanded="false" aria-controls="section-2">
      Section 2
    </button>
  </h3>
  <div id="section-2" hidden>
    Section 2 content...
  </div>
</div>
```

### Menus (Dropdown)

```html
<div class="menu-container">
  <button aria-haspopup="true"
          aria-expanded="false"
          aria-controls="menu">
    Options
  </button>

  <ul id="menu" role="menu" hidden>
    <li role="menuitem" tabindex="-1">Edit</li>
    <li role="menuitem" tabindex="-1">Duplicate</li>
    <li role="separator"></li>
    <li role="menuitem" tabindex="-1">Delete</li>
  </ul>
</div>

<script>
// Arrow keys navigate menu items
// Escape closes menu
// Enter/Space activates item
// Focus returns to button on close
</script>
```

### Live Regions

```html
<!-- Polite announcement (waits for pause) -->
<div aria-live="polite">
  Your changes have been saved.
</div>

<!-- Assertive announcement (interrupts) -->
<div aria-live="assertive">
  Error: Form submission failed.
</div>

<!-- Alert (assertive + special semantics) -->
<div role="alert">
  Session expiring in 5 minutes.
</div>

<!-- Status (polite + special semantics) -->
<div role="status">
  3 search results found.
</div>

<!-- Log (polite, preserves history) -->
<div role="log" aria-live="polite">
  <p>User joined: Alice</p>
  <p>User joined: Bob</p>
</div>
```

### Loading States

```html
<!-- Loading indicator -->
<div role="status" aria-live="polite">
  <span aria-busy="true">Loading...</span>
</div>

<!-- Content being loaded -->
<section aria-busy="true" aria-describedby="loading-msg">
  <div id="loading-msg">Loading user data...</div>
</section>

<!-- After load complete -->
<section aria-busy="false">
  <!-- Content here -->
</section>
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| `<div onclick>` | Not keyboard accessible | Use `<button>` |
| ARIA on native element | Overrides semantics | Remove ARIA |
| Missing `aria-label` | No accessible name | Add label |
| `role="button"` without keyboard | Can't activate | Add keydown handler |
| `aria-hidden` on focusable | Confusing to AT | Remove or make unfocusable |
| Duplicate IDs | `aria-describedby` breaks | Use unique IDs |

## Testing

```javascript
// Check for accessible name
element.getAttribute('aria-label') ||
element.getAttribute('aria-labelledby') ||
element.textContent;

// Check for ARIA support
if (element.role && !element.matches('button, input, ...')) {
  // Ensure keyboard support
}
```
