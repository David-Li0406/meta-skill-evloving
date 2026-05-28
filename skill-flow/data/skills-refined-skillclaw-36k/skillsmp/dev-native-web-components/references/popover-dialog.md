# Popover & Dialog Reference

> Use native `popover` and `<dialog>` for all overlays. Never build custom modals.

---

## Decision Tree

```
User must respond?
├── YES → <dialog> (modal)
└── NO → Does it auto-dismiss?
    ├── YES → popover="auto" (menu, tooltip)
    └── NO → popover="manual" (toast)
```

---

## Popover API

### Auto Popover (Default)

```html
<button popovertarget="menu">Open Menu</button>
<nav id="menu" popover>
  <a href="/home">Home</a>
  <a href="/about">About</a>
</nav>
```

Closes when:

- Clicking outside
- Pressing Escape
- Opening another auto popover

### Manual Popover

```html
<div id="toast" popover="manual">
  Saved successfully!
  <button popovertarget="toast" popovertargetaction="hide">×</button>
</div>

<script>
  function showToast() {
    document.getElementById("toast").showPopover();
    setTimeout(() => toast.hidePopover(), 3000);
  }
</script>
```

### Popover Actions

```html
<button popovertarget="popup" popovertargetaction="toggle">Toggle</button>
<button popovertarget="popup" popovertargetaction="show">Show</button>
<button popovertarget="popup" popovertargetaction="hide">Hide</button>
```

---

## Dialog Element

### Modal Dialog

```html
<dialog id="modal">
  <h2>Confirm Action</h2>
  <p>Are you sure?</p>
  <form method="dialog">
    <button value="cancel">Cancel</button>
    <button value="confirm">Confirm</button>
  </form>
</dialog>

<button onclick="modal.showModal()">Open Modal</button>

<script>
  modal.addEventListener("close", () => {
    console.log("Return value:", modal.returnValue);
  });
</script>
```

### Non-Modal Dialog

```html
<dialog id="panel">
  <h2>Side Panel</h2>
</dialog>

<button onclick="panel.show()">Open Panel</button>
```

---

## Styling Popovers

```css
[popover] {
  margin: 0;
  padding: 1rem;
  border: 1px solid var(--border);
  border-radius: 0.5rem;
  box-shadow: 0 4px 16px #0002;

  /* Entry/exit animation */
  opacity: 0;
  transform: translateY(-0.5rem);
  transition: opacity 0.2s, transform 0.2s, display 0.2s allow-discrete;
}

[popover]:popover-open {
  opacity: 1;
  transform: translateY(0);
}

@starting-style {
  [popover]:popover-open {
    opacity: 0;
    transform: translateY(-0.5rem);
  }
}

/* Backdrop for popovers */
[popover]::backdrop {
  background: transparent;
}
```

---

## Styling Dialogs

```css
dialog {
  padding: 0;
  border: none;
  border-radius: 0.75rem;
  box-shadow: 0 8px 32px #0003;
  max-width: min(90vw, 30rem);

  &::backdrop {
    background: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(4px);
  }

  /* Animation */
  opacity: 0;
  transform: scale(0.95);
  transition: opacity 0.2s, transform 0.2s, display 0.2s allow-discrete;
}

dialog[open] {
  opacity: 1;
  transform: scale(1);
}

@starting-style {
  dialog[open] {
    opacity: 0;
    transform: scale(0.95);
  }
}
```

---

## Nested Popovers

```html
<button popovertarget="menu">Menu</button>
<nav id="menu" popover>
  <button popovertarget="submenu">More ▸</button>
  <div id="submenu" popover>Submenu items</div>
</nav>
```

---

<!-- NOTE: The following features are NOT Baseline (limited status) and have been removed:
- Anchor positioning with popover
- popover="hint" (Chrome 133+ only)
- dialog.requestClose() (Chrome 132+ only)
-->

---

## Comparison Table

| Feature                 | Popover auto | Popover manual | Dialog      |
| ----------------------- | ------------ | -------------- | ----------- |
| Blocks interaction      | No           | No             | Yes (modal) |
| Closes on Escape        | Yes          | No             | Yes         |
| Closes on outside click | Yes          | No             | No          |
| Has ::backdrop          | No           | No             | Yes         |
| Top layer               | Yes          | Yes            | Yes         |
| Focus trap              | No           | No             | Yes         |

---

## Accessibility

```html
<!-- Popover menu with ARIA -->
<button popovertarget="menu" aria-haspopup="menu" aria-expanded="false">
  Menu
</button>

<nav id="menu" popover role="menu">
  <a href="/" role="menuitem">Home</a>
</nav>

<script>
  menu.addEventListener("toggle", (e) => {
    button.setAttribute("aria-expanded", e.newState === "open");
  });
</script>
```

---

## Checklist

- [ ] Use `popover` for tooltips, menus, dropdowns
- [ ] Use `<dialog>` for modals requiring response
- [ ] Add `@starting-style` for entry animations
- [ ] Include ARIA attributes for accessibility
- [ ] Handle `toggle` event for state sync

_Reference: [web.dev/popover-api](https://web.dev/blog/popover-api)_
