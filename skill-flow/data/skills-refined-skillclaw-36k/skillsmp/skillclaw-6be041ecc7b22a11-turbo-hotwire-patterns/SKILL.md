---
name: turbo-hotwire-patterns
description: Use this skill when implementing real-time updates, partial page rendering, or JavaScript behaviors in Rails views with Hotwire, Turbo, and Stimulus.
---

# Turbo & Hotwire Patterns

This skill provides comprehensive guidance for implementing Hotwire (Turbo + Stimulus) in Ruby on Rails applications.

## When to Use This Skill

- Implementing partial page updates
- Adding real-time features
- Creating Turbo Frames and Streams
- Writing Stimulus controllers
- Debugging Turbo-related issues

## Core Philosophy

**HTML over the wire**: Hotwire sends HTML from the server, not JSON. JavaScript enhances server-rendered HTML rather than replacing it.

- **Progressive enhancement**: Works without JavaScript, enhanced with it
- **Server-first**: Business logic stays on the server
- **Minimal JavaScript**: Just enough JS to make HTML interactive

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

## Common Patterns

### Stimulus Controller Basics

```javascript
// app/javascript/controllers/toggle_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["content"]
  static classes = ["hidden"]
  static values = { open: { type: Boolean, default: false } }

  toggle() {
    this.openValue = !this.openValue
  }

  openValueChanged() {
    this.contentTarget.classList.toggle(this.hiddenClass, !this.openValue)
  }
}
```

```erb
<div data-controller="toggle" data-toggle-hidden-class="hidden">
  <button data-action="toggle#toggle">Toggle</button>
  <div data-toggle-target="content">Content here</div>
</div>
```

### Turbo Frame Basics

```erb
<%= turbo_frame_tag "tasks_list" do %>
  <% @tasks.each do |task| %>
    <%= render task %>
  <% end %>
  
  <%= link_to "Load more", tasks_path(page: @next_page) %>
<% end %>
```

### Turbo Streams

Use for real-time updates from the server.

```ruby
# Controller
respond_to do |format|
  format.turbo_stream
  format.html { redirect_to @post }
end
```

```erb
<%# app/views/posts/create.turbo_stream.erb %>
<%= turbo_stream.prepend "posts", @post %>
<%= turbo_stream.update "post_count", Post.count %>
```

## Best Practices

- **NEVER** forget matching frame IDs to ensure updates work correctly.
- **NEVER** return HTML for form errors; use a 422 status for validation errors.
- **NEVER** use targets without checking their existence to avoid crashes.
- **NEVER** forget cleanup in the disconnect method of Stimulus controllers.

## External References

- **Turbo**: [Turbo Documentation](https://turbo.hotwired.dev/)
- **Stimulus**: [Stimulus Documentation](https://stimulus.hotwired.dev/)