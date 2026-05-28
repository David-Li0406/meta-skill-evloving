# Hotwire Accessibility Reference

## ARIA Live Regions

```erb
<!-- Announce dynamic updates to screen readers -->
<div id="tasks" aria-live="polite" aria-atomic="false">
  <%= render @tasks %>
</div>

<div id="flash"
     role="status"
     aria-live="assertive"
     aria-atomic="true">
  <!-- Flash messages announced immediately -->
</div>
```

---

## Keyboard Navigation

```javascript
// app/javascript/controllers/keyboard_nav_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["item"]

  connect() {
    this.currentIndex = 0
    this.itemTargets[this.currentIndex]?.focus()
  }

  next(event) {
    if (event.key === "ArrowDown") {
      event.preventDefault()
      this.currentIndex = Math.min(this.currentIndex + 1, this.itemTargets.length - 1)
      this.itemTargets[this.currentIndex].focus()
    }
  }

  previous(event) {
    if (event.key === "ArrowUp") {
      event.preventDefault()
      this.currentIndex = Math.max(this.currentIndex - 1, 0)
      this.itemTargets[this.currentIndex].focus()
    }
  }

  select(event) {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault()
      event.target.click()
    }
  }
}
```

```erb
<div data-controller="keyboard-nav"
     tabindex="0"
     data-action="keydown->keyboard-nav#next keydown->keyboard-nav#previous">

  <% @items.each do |item| %>
    <div data-keyboard-nav-target="item"
         tabindex="0"
         role="button"
         aria-label="<%= item.title %>"
         data-action="keydown->keyboard-nav#select">
      <%= item.title %>
    </div>
  <% end %>
</div>
```

---

## Focus Management

```javascript
// app/javascript/controllers/modal_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["dialog", "closeButton"]

  open() {
    this.previousFocus = document.activeElement
    this.dialogTarget.showModal()
    this.closeButtonTarget.focus()

    // Trap focus within modal
    this.dialogTarget.addEventListener("keydown", this.trapFocus.bind(this))
  }

  close() {
    this.dialogTarget.close()
    this.previousFocus?.focus()
  }

  trapFocus(event) {
    if (event.key === "Tab") {
      const focusableElements = this.dialogTarget.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      )
      const firstElement = focusableElements[0]
      const lastElement = focusableElements[focusableElements.length - 1]

      if (event.shiftKey && document.activeElement === firstElement) {
        lastElement.focus()
        event.preventDefault()
      } else if (!event.shiftKey && document.activeElement === lastElement) {
        firstElement.focus()
        event.preventDefault()
      }
    }
  }
}
```

---

## Feature Detection

```javascript
// app/javascript/controllers/progressive_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  connect() {
    // Check for required features
    if ('IntersectionObserver' in window) {
      this.enableLazyLoading()
    }

    if ('fetch' in window) {
      this.enableAjaxFeatures()
    }
  }

  enableLazyLoading() {
    // Use IntersectionObserver for lazy loading
  }

  enableAjaxFeatures() {
    // Enable AJAX-dependent features
  }
}
```

---

## Network Error Handling

```javascript
// app/javascript/application.js
document.addEventListener("turbo:fetch-request-error", (event) => {
  const { detail: { fetchResponse } } = event

  if (!fetchResponse || fetchResponse.response.status >= 500) {
    // Show offline/error UI
    document.getElementById("error-banner").classList.remove("hidden")
  }
})

document.addEventListener("turbo:frame-missing", (event) => {
  // Handle missing frame gracefully
  const frame = event.target
  frame.innerHTML = `
    <div class="alert alert-warning">
      Content could not be loaded. <a href="${frame.src}">Try again</a>
    </div>
  `
  event.preventDefault()
})
```
