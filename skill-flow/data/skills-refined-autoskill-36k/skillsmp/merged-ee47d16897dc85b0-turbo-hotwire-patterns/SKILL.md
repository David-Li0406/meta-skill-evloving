---
name: turbo-hotwire-patterns
description: Use this skill when implementing Hotwire features in Rails applications, including Turbo Drive, Turbo Frames, Turbo Streams, and Stimulus controllers for real-time updates and partial page rendering.
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

## Core Principles

- **HTML over the wire**: Hotwire sends HTML from the server, not JSON. JavaScript enhances server-rendered HTML rather than replacing it.
- **Progressive enhancement**: Works without JavaScript, enhanced with it.
- **Server-first**: Business logic stays on the server.
- **Minimal JavaScript**: Just enough JS to make HTML interactive.

## Turbo Drive

Automatically converts links/forms to AJAX. Disable when needed:

```erb
<%# Skip Turbo Drive for this link %>
<%= link_to "External", "https://example.com", data: { turbo: false } %>

<%# Skip for form %>
<%= form_with model: @user, data: { turbo: false } do |f| %>
```

## Turbo Frames

Use for partial page updates without full refreshes.

```erb
<%= turbo_frame_tag "user_profile" do %>
  <%= render @user %>
<% end %>

<%# Link that updates only the frame %>
<%= link_to "Edit", edit_user_path(@user), data: { turbo_frame: "user_profile" } %>
```

### Common Patterns

| Pattern | Usage |
|---------|-------|
| Basic frame | `turbo_frame_tag "id"` |
| Model frame | `turbo_frame_tag dom_id(@task)` |
| Target other | `data: { turbo_frame: "other_id" }` |
| Break out | `data: { turbo_frame: "_top" }` |
| Lazy load | `src: path, loading: :lazy` |

## Turbo Streams

Use for real-time updates from server.

```ruby
# Controller
respond_to do |format|
  format.turbo_stream
  format.html { redirect_to @post }
end
```

### Stream Actions

| Action | Result |
|--------|--------|
| `append` | Add to end of container |
| `prepend` | Add to start of container |
| `replace` | Replace entire element |
| `update` | Replace element's contents |
| `remove` | Delete element |
| `before/after` | Insert adjacent |

## Stimulus Controllers

### Guidelines
- Keep controllers simple and focused.
- Make controllers generic when possible, specific only when needed.
- **Never** have controllers communicate with each other.

### Basic Controller Example

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

## Debugging

### Common Issues

1. **Frame not updating**: Check frame IDs match between source and target.
2. **Streams not working**: Verify `turbo_stream_from` subscription.
3. **Actions not firing**: Check data-action syntax and controller registration.
4. **Morphing issues**: Use `data-turbo-permanent` for persistent elements.
5. **Focus loss**: Implement focus management in Stimulus controllers.
6. **Screen reader issues**: Add proper ARIA attributes and live regions.

## References

Detailed patterns and examples in `references/`:
- `turbo-frames.md` - Frame patterns, lazy loading, navigation
- `turbo-streams.md` - Stream actions, broadcasts, form validation
- `stimulus-controllers.md` - Targets, values, actions, classes, outlets
- `common-patterns.md` - Infinite scroll, auto-submit, flash messages
- `accessibility.md` - ARIA, keyboard navigation, focus management
- `testing.md` - System tests, Stimulus controller tests
- `turbo8-native.md` - Turbo 8 morphing, native apps