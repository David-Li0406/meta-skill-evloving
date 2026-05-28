# Common Hotwire Patterns Reference

## Infinite Scroll

```erb
<%# View %>
<div data-controller="infinite-scroll"
     data-infinite-scroll-url-value="<%= tasks_path %>"
     data-infinite-scroll-page-value="1">

  <div id="tasks" data-infinite-scroll-target="container">
    <%= render @tasks %>
  </div>

  <div data-infinite-scroll-target="loading" class="hidden">
    Loading...
  </div>
</div>
```

```javascript
// app/javascript/controllers/infinite_scroll_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["container", "loading"]
  static values = { url: String, page: Number }

  connect() {
    this.observer = new IntersectionObserver(
      entries => this.handleIntersect(entries),
      { threshold: 0.1 }
    )
    this.observer.observe(this.loadingTarget)
  }

  handleIntersect(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        this.loadMore()
      }
    })
  }

  async loadMore() {
    this.loadingTarget.classList.remove("hidden")

    const response = await fetch(
      `${this.urlValue}?page=${this.pageValue + 1}`,
      { headers: { "Accept": "text/vnd.turbo-stream.html" } }
    )

    if (response.ok) {
      this.pageValue++
      const html = await response.text()
      Turbo.renderStreamMessage(html)
    }

    this.loadingTarget.classList.add("hidden")
  }

  disconnect() {
    this.observer.disconnect()
  }
}
```

---

## Auto-Submit Form

```erb
<%= form_with url: search_path,
              method: :get,
              data: {
                controller: "auto-submit",
                turbo_frame: "results"
              } do |f| %>

  <%= f.text_field :q,
                   data: {
                     action: "input->auto-submit#submit",
                     auto_submit_target: "input"
                   } %>
<% end %>

<%= turbo_frame_tag "results" do %>
  <%= render @results %>
<% end %>
```

```javascript
// app/javascript/controllers/auto_submit_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["input"]

  submit() {
    clearTimeout(this.timeout)
    this.timeout = setTimeout(() => {
      this.element.requestSubmit()
    }, 300)
  }
}
```

---

## Flash Messages with Turbo

```erb
<%# app/views/layouts/_flash.html.erb %>
<div id="flash">
  <% flash.each do |type, message| %>
    <div class="flash flash-<%= type %>"
         data-controller="flash"
         data-flash-timeout-value="5000">
      <%= message %>
      <button data-action="click->flash#dismiss">x</button>
    </div>
  <% end %>
</div>
```

```javascript
// app/javascript/controllers/flash_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static values = { timeout: { type: Number, default: 5000 } }

  connect() {
    this.timer = setTimeout(() => this.dismiss(), this.timeoutValue)
  }

  dismiss() {
    this.element.remove()
  }

  disconnect() {
    clearTimeout(this.timer)
  }
}
```

---

## Client-Side Form Validation

```erb
<%= form_with model: @task,
              data: {
                controller: "form-validation",
                action: "turbo:submit-end->form-validation#handleResponse"
              } do |f| %>

  <%= f.text_field :title,
                   required: true,
                   minlength: 5,
                   data: {
                     form_validation_target: "field",
                     action: "blur->form-validation#validateField"
                   } %>
  <span data-form-validation-target="error" class="hidden text-red-500"></span>

  <%= f.submit "Save",
               data: { form_validation_target: "submit" } %>
<% end %>
```

```javascript
// app/javascript/controllers/form_validation_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["field", "error", "submit"]

  validateField(event) {
    const field = event.target
    const error = field.parentElement.querySelector('[data-form-validation-target="error"]')

    if (!field.validity.valid) {
      error.textContent = field.validationMessage
      error.classList.remove("hidden")
      field.classList.add("border-red-500")
    } else {
      error.classList.add("hidden")
      field.classList.remove("border-red-500")
    }
  }

  handleResponse(event) {
    const { success, fetchResponse } = event.detail

    if (!success && fetchResponse.response.status === 422) {
      // Server returned validation errors
      this.disableSubmit(false)
    }
  }

  disableSubmit(disabled) {
    this.submitTarget.disabled = disabled
  }
}
```

---

## Stimulus Components Integration

```javascript
// Using stimulus-components library
import { Application } from "@hotwired/stimulus"
import Dropdown from "@stimulus-components/dropdown"
import Notification from "@stimulus-components/notification"
import Popover from "@stimulus-components/popover"

const application = Application.start()
application.register("dropdown", Dropdown)
application.register("notification", Notification)
application.register("popover", Popover)
```

```erb
<!-- Dropdown component -->
<div data-controller="dropdown">
  <button data-action="dropdown#toggle">Menu</button>
  <div data-dropdown-target="menu">
    <a href="/profile">Profile</a>
    <a href="/settings">Settings</a>
  </div>
</div>

<!-- Notification component -->
<div data-controller="notification"
     data-notification-delay-value="5000"
     data-notification-remove-after-value="true">
  <p>Your task was created successfully!</p>
  <button data-action="notification#hide">x</button>
</div>

<!-- Popover component -->
<div data-controller="popover"
     data-popover-translate-x="-50%"
     data-popover-translate-y="8">
  <button data-action="popover#toggle">Show Info</button>
  <div data-popover-target="card" class="hidden">
    Popover content
  </div>
</div>
```
