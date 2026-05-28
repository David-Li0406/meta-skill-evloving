---
name: stimulus-controller
description: Generate Stimulus controllers with Turbo integration for interactive UI. Use when user needs interactivity, client-side logic, form handling, or says "add interaction", "make it interactive", "create stimulus controller", "handle click/submit/toggle".
---

# Stimulus Controller Generator

Generate Stimulus controllers with Turbo Drive/Frame integration for modern Rails interactions.

## Quick Start

```
Task Progress (copy and check off):
- [ ] 1. Identify interaction needed
- [ ] 2. Choose controller pattern
- [ ] 3. Generate controller file
- [ ] 4. Add data attributes to HTML
- [ ] 5. Test interaction
- [ ] 6. Add Turbo if needed
```

## Project Setup

**Import Map** (config/importmap.rb):
```ruby
pin "application"
pin "@hotwired/stimulus", to: "stimulus.min.js"
pin "@hotwired/turbo-rails", to: "turbo.min.js"
pin "@hotwired/stimulus-loading", to: "stimulus-loading.js"
```

**Controller Location**:
```
app/javascript/controllers/
├── application.js
├── hello_controller.js
├── modal_controller.js
└── tab_controller.js
```

## Basic Controller Template

```javascript
// app/javascript/controllers/example_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["output", "input"]
  static values = {
    url: String,
    count: { type: Number, default: 0 }
  }
  static classes = ["active", "hidden"]

  connect() {
    console.log("Controller connected")
  }

  disconnect() {
    console.log("Controller disconnected")
  }

  // Action method
  handleClick(event) {
    event.preventDefault()
    console.log("Clicked!")
  }
}
```

**HTML Usage**:
```erb
<div data-controller="example"
     data-example-url-value="<%= posts_path %>"
     data-example-count-value="0">

  <input data-example-target="input" type="text">
  <div data-example-target="output"></div>

  <button data-action="click->example#handleClick">
    Click me
  </button>
</div>
```

## Common Patterns

- **Modal**: [reference/modal-controller.md](reference/modal-controller.md)
- **Tab**: [reference/tab-controller.md](reference/tab-controller.md)
- **Form**: [reference/form-controller.md](reference/form-controller.md)
- **Toggle**: [reference/toggle-controller.md](reference/toggle-controller.md)
- **Dropdown**: [reference/dropdown-controller.md](reference/dropdown-controller.md)

## Data Attributes

### Controller
```erb
<div data-controller="modal">
```

**Multiple Controllers**:
```erb
<div data-controller="modal dropdown">
```

### Action
```erb
<button data-action="click->modal#open">Open</button>
```

**Shorthand** (click is default for buttons):
```erb
<button data-action="modal#open">Open</button>
```

**Multiple Actions**:
```erb
<button data-action="click->modal#open mouseenter->tooltip#show">
```

### Target
```erb
<div data-modal-target="dialog"></div>
```

**Access in Controller**:
```javascript
this.dialogTarget  // First target
this.dialogTargets // All targets
this.hasDialogTarget // Boolean
```

### Value
```erb
<div data-modal-url-value="<%= modal_path %>">
```

**Access in Controller**:
```javascript
this.urlValue // Get value
this.urlValue = "new-url" // Set value
```

**Value Change Callback**:
```javascript
urlValueChanged(value, previousValue) {
  console.log(`URL changed from ${previousValue} to ${value}`)
}
```

### Class
```erb
<div data-modal-active-class="bg-primary"
     data-modal-hidden-class="hidden">
```

**Access in Controller**:
```javascript
element.classList.add(this.activeClass)
element.classList.remove(this.hiddenClass)
```

## Turbo Integration

### Turbo Frame
```erb
<%= turbo_frame_tag "modal" do %>
  <!-- Content loaded/replaced here -->
<% end %>
```

**Load Frame**:
```javascript
// Controller
loadContent(event) {
  event.preventDefault()
  const frame = document.getElementById("modal")
  frame.src = this.urlValue
}
```

### Turbo Stream
```javascript
// Append content
fetch(url, {
  method: "POST",
  headers: {
    "Accept": "text/vnd.turbo-stream.html"
  }
})
```

**Stream Response** (controller):
```ruby
def create
  @post = Post.new(post_params)

  respond_to do |format|
    if @post.save
      format.turbo_stream {
        render turbo_stream: turbo_stream.prepend("posts", partial: "posts/post", locals: { post: @post })
      }
    end
  end
end
```

## Lifecycle Callbacks

```javascript
connect() {
  // Called when controller connects to DOM
  console.log("Connected")
}

disconnect() {
  // Called when controller disconnects from DOM
  console.log("Disconnected")
}

targetConnected(target, name) {
  // Called when target connects
  console.log(`${name} target connected`)
}

targetDisconnected(target, name) {
  // Called when target disconnects
}

valueChanged(value, previousValue) {
  // Called when value changes
}
```

## Event Handling

**Click**:
```erb
<button data-action="click->controller#method">
```

**Submit**:
```erb
<form data-action="submit->form#submit">
```

**Input**:
```erb
<input data-action="input->search#filter">
```

**Change**:
```erb
<select data-action="change->filter#update">
```

**Custom Events**:
```javascript
// Dispatch
this.dispatch("success", { detail: { id: 123 } })

// Listen
<div data-action="controller:success@window->listener#handleSuccess">
```

## Best Practices

1. **Keep Controllers Small**: One responsibility per controller
2. **Use Targets**: Don't use querySelector
3. **Clean Up**: Remove event listeners in disconnect()
4. **Values for Data**: Use values, not dataset
5. **Turbo-Aware**: Check `event.detail.fetchResponse` for Turbo events

## Common Use Cases

### Toggle (Show/Hide)
```javascript
toggle(event) {
  event.preventDefault()
  this.targetElement.classList.toggle(this.hiddenClass)
}
```

### Form Validation
```javascript
validate(event) {
  const input = event.target
  if (input.value.length < 5) {
    input.classList.add("border-destructive")
    event.preventDefault()
  }
}
```

### Auto-Save
```javascript
static debounces = ["save"]

save() {
  fetch(this.urlValue, {
    method: "PATCH",
    body: new FormData(this.formTarget)
  })
}
```

## Debugging

```javascript
connect() {
  console.log("Controller:", this.identifier)
  console.log("Element:", this.element)
  console.log("Targets:", this.targets)
  console.log("Values:", this.values)
}
```

**Check Controller Connected**:
```javascript
// In browser console
document.querySelector('[data-controller="modal"]').controller
```

## After Generation

```bash
# No build step needed (importmap)
# Just reload browser

# Check in browser console
> $("[data-controller='modal']").controller
```

## Examples

- [Modal Controller](examples/modal_controller.js)
- [Tab Controller](examples/tab_controller.js)
- [Dropdown Controller](examples/dropdown_controller.js)

## Checklist

- [ ] Controller file created
- [ ] data-controller added to HTML
- [ ] data-action for events
- [ ] data-targets defined
- [ ] data-values if needed
- [ ] Clean up in disconnect()
- [ ] Tested in browser
- [ ] Works with Turbo navigation
