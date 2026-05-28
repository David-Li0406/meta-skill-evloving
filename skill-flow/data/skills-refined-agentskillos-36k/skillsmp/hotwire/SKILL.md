---
name: hotwire
description: This skill should be used when the user asks about "Hotwire", "Turbo", "Turbo Drive", "Turbo Frames", "Turbo Streams", "Stimulus", "Stimulus controllers", "Stimulus values", "Stimulus targets", "Stimulus actions", "import maps", "live updates", "partial page updates", "SPA-like behavior", "real-time updates", "turbo_frame_tag", "turbo_stream", "broadcast", or needs guidance on building modern Rails 7+ frontends without heavy JavaScript frameworks.
version: 1.1.0
---

# Hotwire for Rails 7+

Comprehensive guide to building modern, reactive web applications with Hotwire (Turbo + Stimulus) in Rails 7+.

## What is Hotwire?

Hotwire enables "fast, modern, progressively enhanced web applications without using much JavaScript." It sends HTML over the wire instead of JSON, keeping business logic on the server.

**Three components:**

1. **Turbo Drive** - Accelerates navigation by intercepting clicks and replacing `<body>`
2. **Turbo Frames** - Decompose pages into independently-updatable sections
3. **Turbo Streams** - Deliver live partial page updates via WebSocket, SSE, or HTTP
4. **Stimulus** - Modest JavaScript framework for behavior

## Turbo Drive

Turbo Drive intercepts link clicks and form submissions, fetching via `fetch` and replacing `<body>` while merging `<head>`. The window, document, and `<html>` persist across navigations.

### Disabling for Specific Elements

```erb
<%# Disable Turbo for external links or file downloads %>
<%= link_to "Download PDF", pdf_path, data: { turbo: false } %>

<%# Disable for forms that need full page reload %>
<%= form_with model: @export, data: { turbo: false } do |f| %>
```

### Progress Bar

```css
.turbo-progress-bar {
  background-color: #3b82f6;
  height: 3px;
}
```

## Turbo Frames

Frames wrap page segments in `<turbo-frame>` elements for scoped navigation. Only matching frames extract from server responses.

### Frame Attributes

| Attribute | Purpose |
|-----------|---------|
| `id` | Required. Unique identifier to match frames between requests |
| `src` | URL for eager-loading frame content on page load |
| `loading="lazy"` | Delay loading until frame becomes visible |
| `target` | Navigation scope: `_top` (full page), `_self`, or frame ID |
| `data-turbo-action` | Promote to browser history (`advance` or `replace`) |

### Basic Frame

```erb
<%# app/views/articles/show.html.erb %>
<h1><%= @article.title %></h1>

<%= turbo_frame_tag @article do %>
  <p><%= @article.body %></p>
  <%= link_to "Edit", edit_article_path(@article) %>
<% end %>

<%# app/views/articles/edit.html.erb %>
<%= turbo_frame_tag @article do %>
  <%= render "form", article: @article %>
<% end %>
```

### Lazy Loading

```erb
<%# Load content when frame becomes visible %>
<%= turbo_frame_tag "comments",
      src: article_comments_path(@article),
      loading: :lazy do %>
  <p>Loading comments...</p>
<% end %>
```

### Breaking Out of Frames

```erb
<%# Navigate entire page %>
<%= link_to "View Full", article_path(@article), data: { turbo_frame: "_top" } %>

<%# Target different frame %>
<%= link_to "Preview", preview_path(@article), data: { turbo_frame: "preview_panel" } %>
```

### Frame State Attributes

During navigation, frames receive `[aria-busy="true"]`. After completion, `[complete]` is set on the frame.

## Turbo Streams

Streams deliver DOM changes as `<turbo-stream>` elements specifying action and target.

### Stream Actions (9 total)

| Action | Description |
|--------|-------------|
| `append` | Add content to end of target |
| `prepend` | Add content to start of target |
| `replace` | Replace entire target element |
| `update` | Replace target's inner content only |
| `remove` | Delete target element |
| `before` | Insert before target element |
| `after` | Insert after target element |
| `morph` | Intelligently morph changes (variant of replace/update) |
| `refresh` | Refresh page or frame |

### HTTP Stream Response

```ruby
# app/controllers/comments_controller.rb
def create
  @comment = @article.comments.build(comment_params)

  if @comment.save
    respond_to do |format|
      format.turbo_stream  # Renders create.turbo_stream.erb
      format.html { redirect_to @article }
    end
  else
    render :new, status: :unprocessable_entity
  end
end
```

```erb
<%# app/views/comments/create.turbo_stream.erb %>
<%= turbo_stream.append "comments", @comment %>
<%= turbo_stream.update "comment_count", @article.comments.count %>
<%= turbo_stream.replace "new_comment", partial: "form", locals: { comment: Comment.new } %>
```

### Inline Stream Response

```ruby
def destroy
  @comment.destroy

  respond_to do |format|
    format.turbo_stream do
      render turbo_stream: [
        turbo_stream.remove(@comment),
        turbo_stream.update("comment_count", @article.comments.count)
      ]
    end
    format.html { redirect_to @article }
  end
end
```

### Broadcasting via WebSocket

```ruby
# app/models/comment.rb
class Comment < ApplicationRecord
  belongs_to :article

  after_create_commit -> {
    broadcast_append_to article, target: "comments"
  }

  after_destroy_commit -> {
    broadcast_remove_to article
  }
end
```

```erb
<%# Subscribe to broadcasts %>
<%= turbo_stream_from @article %>

<div id="comments">
  <%= render @article.comments %>
</div>
```

### WebSocket/SSE Source

```erb
<%# Persistent connection for real-time updates %>
<turbo-stream-source src="ws://example.com/updates"></turbo-stream-source>
```

## Stimulus

Stimulus is "a JavaScript framework with modest ambitions." It enhances server-rendered HTML using data attributes.

### Controller Structure

```javascript
// app/javascript/controllers/hello_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["name", "output"]
  static values = { greeting: { type: String, default: "Hello" } }
  static classes = ["active"]

  connect() {
    // Called when controller connects to DOM
  }

  disconnect() {
    // Called when controller disconnects - clean up here
  }

  greet() {
    this.outputTarget.textContent = `${this.greetingValue}, ${this.nameTarget.value}!`
  }
}
```

### Naming Conventions

| Context | Convention | Example |
|---------|------------|---------|
| Controller file | snake_case or kebab-case | `hello_controller.js`, `date-picker_controller.js` |
| Controller identifier | kebab-case in HTML | `data-controller="date-picker"` |
| Targets | camelCase | `static targets = ["firstName"]` |
| Values | camelCase | `static values = { itemCount: Number }` |
| Methods | camelCase | `submitForm()` |

### Targets

Define elements to reference within controller:

```javascript
static targets = ["query", "results", "errorMessage"]
```

**Generated properties:**

| Property | Purpose |
|----------|---------|
| `this.queryTarget` | First matching element (throws if missing) |
| `this.queryTargets` | Array of all matching elements |
| `this.hasQueryTarget` | Boolean existence check |

**Target callbacks:**

```javascript
queryTargetConnected(element) {
  // Called when target is added to DOM
}

queryTargetDisconnected(element) {
  // Called when target is removed from DOM
}
```

```erb
<div data-controller="search">
  <input data-search-target="query">
  <div data-search-target="results"></div>
</div>
```

### Values

Read/write typed data attributes:

```javascript
static values = {
  index: Number,           // data-controller-index-value
  url: String,             // data-controller-url-value
  active: Boolean,         // data-controller-active-value
  items: Array,            // data-controller-items-value (JSON)
  config: Object           // data-controller-config-value (JSON)
}
```

**Five supported types:** Array, Boolean, Number, Object, String

**Default values:**

```javascript
static values = {
  count: { type: Number, default: 0 },
  url: { type: String, default: "/api" }
}
```

**Change callbacks:**

```javascript
countValueChanged(value, previousValue) {
  // Called on initialize and when value changes
  this.element.textContent = value
}
```

### Actions

Connect DOM events to controller methods:

**Format:** `event->controller#method`

```erb
<button data-action="click->gallery#next">Next</button>
```

**Event shorthand** (common defaults):
- `<button>`, `<a>` → `click`
- `<form>` → `submit`
- `<input>`, `<textarea>` → `input`
- `<select>` → `change`
- `<details>` → `toggle`

```erb
<%# Equivalent to click->gallery#next %>
<button data-action="gallery#next">Next</button>
```

**Global events:**

```erb
<div data-action="resize@window->gallery#layout">
<div data-action="keydown@document->modal#close">
```

**Keyboard filters:**

```erb
<input data-action="keydown.enter->search#submit">
<input data-action="keydown.esc->modal#close">
<input data-action="keydown.ctrl+s->form#save">
```

**Action options:**

| Option | Effect |
|--------|--------|
| `:stop` | Calls `stopPropagation()` |
| `:prevent` | Calls `preventDefault()` |
| `:self` | Only fires if target matches element |
| `:capture` | Use capture phase |
| `:once` | Remove after first invocation |
| `:passive` | Passive event listener |

```erb
<form data-action="submit->form#save:prevent">
<a data-action="click->link#track:stop">
```

**Action parameters:**

```erb
<button data-action="item#delete"
        data-item-id-param="123"
        data-item-type-param="article">
```

```javascript
delete(event) {
  const { id, type } = event.params
  // id = 123 (Number), type = "article" (String)
}
```

### Classes

Define CSS class names as controller properties:

```javascript
static classes = ["active", "loading"]
```

```erb
<div data-controller="toggle"
     data-toggle-active-class="bg-blue-500"
     data-toggle-loading-class="opacity-50">
```

```javascript
this.activeClass     // "bg-blue-500"
this.hasActiveClass  // true
this.loadingClasses  // ["opacity-50"]
```

## Import Maps (Rails 7+)

```ruby
# config/importmap.rb
pin "application"
pin "@hotwired/turbo-rails", to: "turbo.min.js"
pin "@hotwired/stimulus", to: "stimulus.min.js"
pin_all_from "app/javascript/controllers", under: "controllers"
```

```bash
bin/importmap pin lodash
bin/importmap pin chartkick --from jsdelivr
```

## Additional Resources

### Reference Files

- **`references/stimulus-patterns.md`** - Common Stimulus controller patterns
- **`references/turbo-streams-advanced.md`** - Complex broadcasting scenarios
