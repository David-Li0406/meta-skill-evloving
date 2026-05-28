# Accessibility Stimulus Controllers

## Roving Tabindex Controller

For composite widgets (tabs, menus, toolbars) where only one item should be in the tab sequence:

```javascript
// app/javascript/controllers/roving_tabindex_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["item"]

  connect() {
    this.currentIndex = 0
    this.updateTabindex()
  }

  next(event) {
    event.preventDefault()
    this.currentIndex = (this.currentIndex + 1) % this.itemTargets.length
    this.focusCurrent()
  }

  previous(event) {
    event.preventDefault()
    this.currentIndex = (this.currentIndex - 1 + this.itemTargets.length) % this.itemTargets.length
    this.focusCurrent()
  }

  updateTabindex() {
    this.itemTargets.forEach((item, index) => {
      item.setAttribute("tabindex", index === this.currentIndex ? "0" : "-1")
    })
  }

  focusCurrent() {
    this.updateTabindex()
    this.itemTargets[this.currentIndex].focus()
  }
}
```

**Usage:**
```erb
<div role="tablist"
     data-controller="roving-tabindex"
     data-action="keydown.right->roving-tabindex#next keydown.left->roving-tabindex#previous">
  <button role="tab" data-roving-tabindex-target="item" tabindex="0">Tab 1</button>
  <button role="tab" data-roving-tabindex-target="item" tabindex="-1">Tab 2</button>
  <button role="tab" data-roving-tabindex-target="item" tabindex="-1">Tab 3</button>
</div>
```

---

## Focus Trap Controller

For modal dialogs to trap keyboard focus within the dialog:

```javascript
// app/javascript/controllers/focus_trap_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["container"]

  connect() {
    this.focusableElements = this.containerTarget.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    )
    this.firstFocusable = this.focusableElements[0]
    this.lastFocusable = this.focusableElements[this.focusableElements.length - 1]

    // Store previous focus to restore later
    this.previousFocus = document.activeElement

    // Focus first element in trap
    this.firstFocusable?.focus()
  }

  disconnect() {
    // Restore focus when trap is removed
    this.previousFocus?.focus()
  }

  trapFocus(event) {
    if (event.key !== "Tab") return

    if (event.shiftKey) {
      // Shift+Tab from first element goes to last
      if (document.activeElement === this.firstFocusable) {
        event.preventDefault()
        this.lastFocusable.focus()
      }
    } else {
      // Tab from last element goes to first
      if (document.activeElement === this.lastFocusable) {
        event.preventDefault()
        this.firstFocusable.focus()
      }
    }
  }
}
```

**Usage:**
```erb
<div data-controller="focus-trap"
     data-focus-trap-target="container"
     data-action="keydown->focus-trap#trapFocus">
  <button>First focusable</button>
  <input type="text">
  <button>Last focusable</button>
</div>
```

---

## Modal Controller

Complete accessible modal with focus management:

```javascript
// app/javascript/controllers/modal_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["dialog", "trigger"]

  connect() {
    this.previousFocus = null
  }

  open() {
    this.previousFocus = document.activeElement
    this.dialogTarget.hidden = false
    this.dialogTarget.setAttribute("aria-hidden", "false")

    // Focus first focusable element
    const firstFocusable = this.dialogTarget.querySelector(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    )
    firstFocusable?.focus()
  }

  close() {
    this.dialogTarget.hidden = true
    this.dialogTarget.setAttribute("aria-hidden", "true")

    // Return focus to trigger
    this.previousFocus?.focus()
  }

  closeOnEscape(event) {
    if (event.key === "Escape") {
      this.close()
    }
  }

  closeOnBackdrop(event) {
    if (event.target === this.dialogTarget) {
      this.close()
    }
  }
}
```
