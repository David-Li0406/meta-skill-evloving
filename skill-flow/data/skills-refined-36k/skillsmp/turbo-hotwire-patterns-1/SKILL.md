---
name: "Turbo & Hotwire Patterns"
description: "Complete guide to Hotwire implementation including Turbo Drive, Turbo Frames, Turbo Streams, and Stimulus controllers in Rails applications. Use when: (1) Implementing partial page updates, (2) Adding real-time features, (3) Creating Turbo Frames and Streams, (4) Writing Stimulus controllers, (5) Debugging Turbo-related issues. Trigger keywords: Turbo, Stimulus, Hotwire, real-time, SPA, live updates, ActionCable, broadcasts, turbo_stream, turbo_frame"
version: 1.1.0
---

# Turbo & Hotwire Patterns

## Hotwire Decision Tree

```
What do I need?
│
├─ Full page navigation without reload?
│   └─ Turbo Drive (automatic, no config needed)
│
├─ Update part of page on interaction?
│   └─ Turbo Frames
│       └─ Wrap section in turbo_frame_tag
│
├─ Real-time updates from server?
│   └─ Turbo Streams + ActionCable
│       └─ Model broadcasts + turbo_stream_from
│
├─ Multiple DOM changes on form submit?
│   └─ Turbo Stream responses
│       └─ respond_to format.turbo_stream
│
├─ JavaScript behavior (click, input, etc)?
│   └─ Stimulus controller
│       └─ data-controller + data-action
│
└─ Communication between controllers?
    └─ Stimulus Outlets
        └─ static outlets + data-*-outlet
```

---

## NEVER Do This

**NEVER** forget matching frame IDs:
```erb
<%# WRONG - IDs don't match, frame won't update %>
<%= turbo_frame_tag "tasks" do %>
  <%= link_to "Edit", edit_task_path(@task) %>
<% end %>

<%# edit.html.erb - different ID %>
<%= turbo_frame_tag "task_edit" do %>
  <%= render "form" %>
<% end %>

<%# RIGHT - IDs match %>
<%= turbo_frame_tag dom_id(@task) do %>
  <%= link_to "Edit", edit_task_path(@task) %>
<% end %>

<%# edit.html.erb - same ID %>
<%= turbo_frame_tag dom_id(@task) do %>
  <%= render "form" %>
<% end %>
```

**NEVER** return HTML for form errors (return 422):
```ruby
# WRONG - 200 status doesn't show errors properly
format.turbo_stream {
  render turbo_stream: turbo_stream.replace("form", partial: "form")
}

# RIGHT - 422 status for validation errors
format.turbo_stream {
  render turbo_stream: turbo_stream.replace("form", partial: "form"),
         status: :unprocessable_entity
}
```

**NEVER** use target without checking existence:
```javascript
// WRONG - crashes if target missing
search() {
  this.resultsTarget.innerHTML = html
}

// RIGHT - check first
search() {
  if (this.hasResultsTarget) {
    this.resultsTarget.innerHTML = html
  }
}
```

**NEVER** forget cleanup in disconnect:
```javascript
// WRONG - memory leak
connect() {
  this.timer = setInterval(() => this.refresh(), 1000)
}

// RIGHT - clean up
connect() {
  this.timer = setInterval(() => this.refresh(), 1000)
}

disconnect() {
  clearInterval(this.timer)
}
```

**NEVER** skip ARIA for dynamic content:
```erb
<%# WRONG - screen readers miss updates %>
<div id="tasks">
  <%= render @tasks %>
</div>

<%# RIGHT - announce updates %>
<div id="tasks" aria-live="polite">
  <%= render @tasks %>
</div>
```

---

## Hotwire Stack Overview

```
Hotwire
├── Turbo
│   ├── Turbo Drive      — Full page navigation without reload
│   ├── Turbo Frames     — Partial page updates
│   └── Turbo Streams    — Real-time updates over WebSocket/HTTP
│
└── Stimulus             — Lightweight JavaScript controllers
```

**External References:**
- Turbo: https://turbo.hotwired.dev/
- Stimulus: https://stimulus.hotwired.dev/

---

## Turbo Drive

Automatically converts links/forms to AJAX. Disable when needed:

```erb
<%# Skip Turbo Drive for this link %>
<%= link_to "External", "https://example.com", data: { turbo: false } %>

<%# Skip for form %>
<%= form_with model: @user, data: { turbo: false } do |f| %>
```

---

## Turbo Frames Quick Reference

| Pattern | Usage |
|---------|-------|
| Basic frame | `turbo_frame_tag "id"` |
| Model frame | `turbo_frame_tag dom_id(@task)` |
| Target other | `data: { turbo_frame: "other_id" }` |
| Break out | `data: { turbo_frame: "_top" }` |
| Lazy load | `src: path, loading: :lazy` |

```erb
<%# Lazy loading example %>
<%= turbo_frame_tag "comments",
                    src: task_comments_path(@task),
                    loading: :lazy do %>
  <p>Loading comments...</p>
<% end %>
```

---

## Turbo Streams Quick Reference

| Action | Result |
|--------|--------|
| `append` | Add to end of container |
| `prepend` | Add to start of container |
| `replace` | Replace entire element |
| `update` | Replace element's contents |
| `remove` | Delete element |
| `before/after` | Insert adjacent |

```erb
<%# Stream response %>
<%= turbo_stream.prepend "tasks" do %>
  <%= render @task %>
<% end %>

<%= turbo_stream.remove dom_id(@deleted_task) %>
```

### Model Broadcasts

```ruby
class Task < ApplicationRecord
  after_create_commit -> { broadcast_prepend_to "tasks" }
  after_update_commit -> { broadcast_replace_to "tasks" }
  after_destroy_commit -> { broadcast_remove_to "tasks" }
end
```

```erb
<%# Subscribe in view %>
<%= turbo_stream_from "tasks" %>
<div id="tasks"><%= render @tasks %></div>
```

---

## Stimulus Quick Reference

| Feature | Declaration | HTML |
|---------|-------------|------|
| Targets | `static targets = ["input"]` | `data-search-target="input"` |
| Values | `static values = { delay: Number }` | `data-search-delay-value="300"` |
| Classes | `static classes = ["active"]` | `data-search-active-class="bg-blue"` |
| Actions | - | `data-action="click->search#submit"` |
| Outlets | `static outlets = ["form"]` | `data-search-form-outlet="#form"` |

### Basic Controller

```javascript
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["input", "results"]
  static values = { url: String }

  search() {
    fetch(`${this.urlValue}?q=${this.inputTarget.value}`)
      .then(r => r.text())
      .then(html => this.resultsTarget.innerHTML = html)
  }
}
```

```erb
<div data-controller="search"
     data-search-url-value="<%= search_path %>">
  <input data-search-target="input"
         data-action="input->search#search">
  <div data-search-target="results"></div>
</div>
```

---

## Action Modifiers

| Modifier | Effect |
|----------|--------|
| `:prevent` | `event.preventDefault()` |
| `:stop` | `event.stopPropagation()` |
| `.enter` | Only on Enter key |
| `.esc` | Only on Escape key |
| `.away` | Click outside element |

```erb
<form data-action="submit->form#save:prevent">
  <input data-action="keydown.enter->form#save:prevent">
</form>
```

---

## Debugging Checklist

| Issue | Check |
|-------|-------|
| Frame not updating | Frame IDs match? |
| Streams not working | `turbo_stream_from` subscription? |
| Actions not firing | data-action syntax correct? Controller registered? |
| Morphing issues | `data-turbo-permanent` on persistent elements? |

---

## References

Detailed patterns and examples in `references/`:
- `turbo-frames.md` - Frame patterns, lazy loading, navigation
- `turbo-streams.md` - Stream actions, broadcasts, form validation
- `stimulus-controllers.md` - Targets, values, actions, classes, outlets
- `common-patterns.md` - Infinite scroll, auto-submit, flash messages
- `accessibility.md` - ARIA, keyboard navigation, focus management
- `testing.md` - System tests, Stimulus controller tests
- `turbo8-native.md` - Turbo 8 morphing, native apps
