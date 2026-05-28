---
name: hotwire-turbo-stimulus-patterns
description: Use this skill when implementing JavaScript interactions, real-time updates, or partial page rendering in Ruby on Rails applications with Hotwire, Turbo, and Stimulus.
---

# Hotwire, Turbo & Stimulus Patterns for Rails

This skill provides comprehensive guidance for integrating Hotwire (Turbo + Stimulus) in Ruby on Rails applications, focusing on creating interactive and real-time features.

## Core Principles

1. Use the latest versions based on the Gemfile.
2. Follow Rails conventions and best practices.
3. Utilize official documentation for Turbo and Stimulus.
4. Test JavaScript with RSpec system specs (Capybara + Cuprite).
5. Review existing Stimulus controllers before creating new ones.

## When to Use This Skill

- Creating Stimulus controllers for interactive behaviors.
- Implementing Turbo frames for partial page updates.
- Using Turbo streams for real-time updates.
- Progressive enhancement patterns.
- Form enhancements and validations.

## Quick Reference

| Component       | Purpose                          | Use When                          |
|------------------|----------------------------------|-----------------------------------|
| Stimulus         | JavaScript behaviors             | Adding interactivity to HTML      |
| Turbo Drive      | SPA navigation                   | Default for all links/forms       |
| Turbo Frames     | Partial updates                  | Update part of the page           |
| Turbo Streams    | Multi-target updates             | Update multiple elements           |

## Stimulus Controllers

### Guidelines
- Keep controllers simple and focused.
- Make controllers generic when possible, specific only when needed.
- **Never** have controllers communicate with each other.
- Integrate into ERB templates using Rails conventions.

### Basic Controller Example
```javascript
// app/javascript/controllers/toggle_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["content"]
  static values = { open: Boolean }

  toggle() {
    this.openValue = !this.openValue
  }

  openValueChanged() {
    this.contentTarget.classList.toggle("hidden", !this.openValue)
  }
}
```

### ERB Integration Example
```erb
<div data-controller="toggle" data-toggle-open-value="false">
  <button data-action="toggle#toggle">Toggle</button>
  <div data-toggle-target="content" class="hidden">
    Content here
  </div>
</div>
```

## Turbo Frames

Use Turbo frames for partial page updates without full refreshes.

### Basic Frame Example
```erb
<%= turbo_frame_tag "user_profile" do %>
  <%= render @user %>
<% end %>

<%= link_to "Edit", edit_user_path(@user), data: { turbo_frame: "user_profile" } %>
```

## Turbo Streams

Use Turbo streams for real-time updates from the server.

### Stream Actions Example
```erb
<%# app/views/posts/create.turbo_stream.erb %>
<%= turbo_stream.prepend "posts", @post %>
<%= turbo_stream.update "post_count", Post.count %>
```

## AJAX Requests

Use `request.js` for AJAX when needed:

```javascript
import { get } from "@rails/request.js"

async function loadData() {
  const response = await get("/api/data", { responseKind: "json" })
  if (response.ok) {
    const data = await response.json()
    // handle data
  }
}
```

## Testing

Test Hotwire features with RSpec system specs:

```ruby
RSpec.describe "Posts", type: :system do
  before { driven_by(:cuprite) }

  it "updates post inline with Turbo" do
    post = posts(:published)
    visit post_path(post)

    click_link "Edit"
    fill_in "Title", with: "Updated Title"
    click_button "Save"

    expect(page).to have_content("Updated Title")
    expect(page).to have_current_path(post_path(post)) # No redirect
  end
end
```

## Debugging

### Turbo Events
Listen to Turbo events for debugging:
```javascript
document.addEventListener("turbo:before-fetch-request", (event) => {
  console.log("Turbo request:", event.detail.url)
})
```

### Common Issues
1. **Frame not updating**: Check frame IDs match between source and target.
2. **Streams not working**: Verify `turbo_stream_from` subscription.
3. **Actions not firing**: Check data-action syntax and controller registration.

## Conclusion

This skill provides a structured approach to implementing Hotwire, Turbo, and Stimulus in Rails applications, ensuring best practices and effective patterns for modern web development.