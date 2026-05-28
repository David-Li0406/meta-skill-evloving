# Common Stimulus Controller Patterns

## Lifecycle Methods

```javascript
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  // Called when controller connects to DOM
  connect() {
    console.log("Connected!")
  }

  // Called when controller disconnects from DOM
  disconnect() {
    // Clean up: remove listeners, cancel timers, etc.
  }

  // Called when target connects
  nameTargetConnected(element) {
    console.log("Name target added:", element)
  }

  // Called when target disconnects
  nameTargetDisconnected(element) {
    console.log("Name target removed:", element)
  }
}
```

## Form Handling

### Form Submission with Loading State

```javascript
// app/javascript/controllers/form_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["submit", "spinner"]
  static classes = ["loading"]

  submit() {
    this.submitTarget.disabled = true
    this.submitTarget.classList.add(this.loadingClass)
    if (this.hasSpinnerTarget) {
      this.spinnerTarget.classList.remove("hidden")
    }
  }

  // Called when Turbo completes
  reset() {
    this.submitTarget.disabled = false
    this.submitTarget.classList.remove(this.loadingClass)
    if (this.hasSpinnerTarget) {
      this.spinnerTarget.classList.add("hidden")
    }
  }
}
```

```erb
<%= form_with model: @article,
      data: {
        controller: "form",
        action: "turbo:submit-start->form#submit turbo:submit-end->form#reset",
        form_loading_class: "opacity-50"
      } do |f| %>
  <!-- fields -->
  <button type="submit" data-form-target="submit">
    Save
    <span data-form-target="spinner" class="hidden">
      <%= image_tag "spinner.svg" %>
    </span>
  </button>
<% end %>
```

### Client-Side Validation

```javascript
// app/javascript/controllers/validation_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["input", "error"]
  static values = {
    rules: Object  // { required: true, minLength: 3, pattern: "email" }
  }

  validate(event) {
    const input = event.target
    const errors = this.getErrors(input)

    if (errors.length > 0) {
      this.showError(input, errors[0])
    } else {
      this.clearError(input)
    }
  }

  submit(event) {
    let valid = true

    this.inputTargets.forEach(input => {
      const errors = this.getErrors(input)
      if (errors.length > 0) {
        this.showError(input, errors[0])
        valid = false
      }
    })

    if (!valid) {
      event.preventDefault()
    }
  }

  getErrors(input) {
    const errors = []
    const value = input.value.trim()
    const rules = JSON.parse(input.dataset.validationRules || "{}")

    if (rules.required && !value) {
      errors.push("This field is required")
    }
    if (rules.minLength && value.length < rules.minLength) {
      errors.push(`Minimum ${rules.minLength} characters`)
    }
    if (rules.pattern === "email" && value && !this.isValidEmail(value)) {
      errors.push("Invalid email format")
    }

    return errors
  }

  showError(input, message) {
    input.classList.add("border-red-500")
    const errorEl = input.nextElementSibling
    if (errorEl?.classList.contains("error-message")) {
      errorEl.textContent = message
      errorEl.classList.remove("hidden")
    }
  }

  clearError(input) {
    input.classList.remove("border-red-500")
    const errorEl = input.nextElementSibling
    if (errorEl?.classList.contains("error-message")) {
      errorEl.classList.add("hidden")
    }
  }

  isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
  }
}
```

## UI Components

### Dropdown/Menu

```javascript
// app/javascript/controllers/dropdown_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["menu"]
  static classes = ["open"]

  connect() {
    this.boundClose = this.closeOnClickOutside.bind(this)
  }

  toggle() {
    if (this.menuTarget.classList.contains(this.openClass)) {
      this.close()
    } else {
      this.open()
    }
  }

  open() {
    this.menuTarget.classList.add(this.openClass)
    document.addEventListener("click", this.boundClose)
  }

  close() {
    this.menuTarget.classList.remove(this.openClass)
    document.removeEventListener("click", this.boundClose)
  }

  closeOnClickOutside(event) {
    if (!this.element.contains(event.target)) {
      this.close()
    }
  }

  disconnect() {
    document.removeEventListener("click", this.boundClose)
  }
}
```

### Tabs

```javascript
// app/javascript/controllers/tabs_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["tab", "panel"]
  static classes = ["activeTab", "activePanel"]
  static values = { index: { type: Number, default: 0 } }

  connect() {
    this.showTab(this.indexValue)
  }

  select(event) {
    const index = this.tabTargets.indexOf(event.currentTarget)
    this.indexValue = index
  }

  indexValueChanged() {
    this.showTab(this.indexValue)
  }

  showTab(index) {
    this.tabTargets.forEach((tab, i) => {
      tab.classList.toggle(this.activeTabClass, i === index)
      tab.setAttribute("aria-selected", i === index)
    })

    this.panelTargets.forEach((panel, i) => {
      panel.classList.toggle(this.activePanelClass, i === index)
      panel.hidden = i !== index
    })
  }
}
```

### Toast Notifications

```javascript
// app/javascript/controllers/toast_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static values = {
    duration: { type: Number, default: 5000 },
    dismissable: { type: Boolean, default: true }
  }

  connect() {
    if (this.durationValue > 0) {
      this.timeout = setTimeout(() => this.dismiss(), this.durationValue)
    }
  }

  dismiss() {
    this.element.classList.add("opacity-0", "translate-x-full")
    setTimeout(() => this.element.remove(), 300)
  }

  disconnect() {
    clearTimeout(this.timeout)
  }
}
```

## Data Fetching

### Autocomplete

```javascript
// app/javascript/controllers/autocomplete_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["input", "results"]
  static values = { url: String }

  search() {
    clearTimeout(this.timeout)
    this.timeout = setTimeout(() => this.fetchResults(), 300)
  }

  async fetchResults() {
    const query = this.inputTarget.value
    if (query.length < 2) {
      this.resultsTarget.innerHTML = ""
      return
    }

    const response = await fetch(`${this.urlValue}?q=${encodeURIComponent(query)}`)
    this.resultsTarget.innerHTML = await response.text()
  }

  select(event) {
    this.inputTarget.value = event.currentTarget.dataset.value
    this.resultsTarget.innerHTML = ""
  }

  closeOnClickOutside(event) {
    if (!this.element.contains(event.target)) {
      this.resultsTarget.innerHTML = ""
    }
  }
}
```

### Polling

```javascript
// app/javascript/controllers/poll_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static values = {
    url: String,
    interval: { type: Number, default: 5000 }
  }

  connect() {
    this.poll()
  }

  poll() {
    this.interval = setInterval(async () => {
      const response = await fetch(this.urlValue)
      if (response.ok) {
        this.element.innerHTML = await response.text()
      }
    }, this.intervalValue)
  }

  disconnect() {
    clearInterval(this.interval)
  }
}
```

## Turbo Integration

### Handling Turbo Events

```javascript
// app/javascript/controllers/turbo_form_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  // Before form submits
  beforeSubmit(event) {
    // Validate, show loading, etc.
  }

  // After successful submission
  afterSubmit(event) {
    if (event.detail.success) {
      this.element.reset()
    }
  }

  // Stream rendered
  streamRendered(event) {
    // React to turbo stream updates
  }
}
```

```erb
<%= form_with model: @comment,
      data: {
        controller: "turbo-form",
        action: "turbo:before-fetch-request->turbo-form#beforeSubmit turbo:submit-end->turbo-form#afterSubmit"
      } do |f| %>
<% end %>
```

### Preventing Turbo Navigation

```javascript
// app/javascript/controllers/unsaved_changes_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static values = { dirty: { type: Boolean, default: false } }

  markDirty() {
    this.dirtyValue = true
  }

  markClean() {
    this.dirtyValue = false
  }

  confirmNavigation(event) {
    if (this.dirtyValue) {
      if (!confirm("You have unsaved changes. Leave anyway?")) {
        event.preventDefault()
      }
    }
  }

  connect() {
    document.addEventListener("turbo:before-visit", this.confirmNavigation.bind(this))
  }

  disconnect() {
    document.removeEventListener("turbo:before-visit", this.confirmNavigation.bind(this))
  }
}
```

## Best Practices

### Keep Controllers Focused
Each controller should handle one concern. Combine using multiple controllers on an element.

### Use Values for Configuration
Pass configuration through data attributes, not hardcoded values.

### Clean Up in disconnect()
Always clean up timers, event listeners, and subscriptions.

### Leverage Targets
Use targets for DOM queries instead of querySelector.

### Use Classes for Styling
Define CSS classes in data attributes for flexibility.
