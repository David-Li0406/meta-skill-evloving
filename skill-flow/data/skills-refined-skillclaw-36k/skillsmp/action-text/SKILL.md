---
name: action-text
description: This skill should be used when the user asks about "rich text", "Action Text", "Trix editor", "WYSIWYG", "has_rich_text", "content editing", "embedded attachments", "formatted text", "text editor", or needs guidance on implementing rich text editing in Rails applications.
version: 1.0.0
---

# Action Text

Comprehensive guide to rich text content with the Trix editor in Rails.

## Setup

```bash
rails action_text:install
rails db:migrate
```

This creates:
- `active_storage` tables (if not present)
- `action_text_rich_texts` table
- Imports Trix editor and styles

### JavaScript Setup

```javascript
// app/javascript/application.js
import "trix"
import "@rails/actiontext"
```

### Stylesheet Setup

```scss
// app/assets/stylesheets/application.scss
@import "trix/dist/trix";

// Or in application.css
//= require trix
//= require actiontext
```

## Model Configuration

### Basic Rich Text

```ruby
class Article < ApplicationRecord
  has_rich_text :content
end
```

### Multiple Rich Text Fields

```ruby
class Article < ApplicationRecord
  has_rich_text :content
  has_rich_text :summary
  has_rich_text :notes
end
```

### Encrypted Rich Text

```ruby
class Article < ApplicationRecord
  has_rich_text :content, encrypted: true
end
```

## Form Integration

### Basic Form

```erb
<%= form_with model: @article do |form| %>
  <div class="field">
    <%= form.label :title %>
    <%= form.text_field :title %>
  </div>

  <div class="field">
    <%= form.label :content %>
    <%= form.rich_text_area :content %>
  </div>

  <%= form.submit %>
<% end %>
```

### With Placeholder

```erb
<%= form.rich_text_area :content, placeholder: "Write your article here..." %>
```

### With Custom Class

```erb
<%= form.rich_text_area :content, class: "custom-editor", data: { controller: "editor" } %>
```

## Controller Setup

### Strong Parameters

```ruby
class ArticlesController < ApplicationController
  def create
    @article = Article.new(article_params)
    # ...
  end

  private

  def article_params
    params.require(:article).permit(:title, :content)
  end
end
```

## Displaying Content

### Basic Display

```erb
<%# Renders as HTML %>
<%= @article.content %>

<%# With wrapper div %>
<div class="prose">
  <%= @article.content %>
</div>
```

### Plain Text

```erb
<%# Plain text version %>
<%= @article.content.to_plain_text %>

<%# Truncated plain text %>
<%= truncate(@article.content.to_plain_text, length: 200) %>
```

### Checking for Content

```erb
<% if @article.content.present? %>
  <%= @article.content %>
<% else %>
  <p class="empty">No content yet.</p>
<% end %>

<%# Or %>
<% if @article.content.blank? %>
  <p>Write something!</p>
<% end %>
```

## Attachments

### Image Attachments

Action Text automatically handles image attachments through Active Storage:

```ruby
# Images are automatically embedded when pasted or dragged into editor
# They're stored via Active Storage
```

### Custom Attachments

```ruby
# app/models/user.rb
class User < ApplicationRecord
  include ActionText::Attachable

  def to_trix_content_attachment_partial_path
    "users/mention"
  end
end
```

```erb
<%# app/views/users/_mention.html.erb %>
<span class="mention">@<%= user.name %></span>
```

### Embedding Attachments Programmatically

```ruby
# Attach a user mention
article.content = ActionText::Content.new("<div>Hello #{user.attachable_sgid}</div>")

# Using the helper
article.update(content: "<div>Check out #{ActionText::Attachment.from_attachable(user)}</div>")
```

### Attachment Gallery

```erb
<%# Display all attachments from rich text %>
<% @article.content.attachments.each do |attachment| %>
  <% if attachment.attachable.is_a?(ActiveStorage::Blob) %>
    <%= image_tag attachment.attachable.representation(resize_to_limit: [200, 200]) %>
  <% end %>
<% end %>
```

## Customizing Trix

### Toolbar Configuration

```javascript
// app/javascript/controllers/trix_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  connect() {
    // Remove unwanted toolbar buttons
    this.element.addEventListener("trix-initialize", () => {
      const toolbar = this.element.previousElementSibling
      toolbar.querySelector(".trix-button-group--file-tools")?.remove()
    })
  }
}
```

```erb
<div data-controller="trix">
  <%= form.rich_text_area :content %>
</div>
```

### Custom Toolbar

```javascript
// Remove specific buttons
document.addEventListener("trix-initialize", (event) => {
  const toolbar = event.target.toolbarElement

  // Remove file attachment button
  toolbar.querySelector('[data-trix-action="attachFiles"]')?.remove()

  // Remove heading button
  toolbar.querySelector('[data-trix-attribute="heading1"]')?.remove()
})
```

### Adding Custom Buttons

```javascript
// Add custom button to toolbar
document.addEventListener("trix-initialize", (event) => {
  const toolbar = event.target.toolbarElement
  const buttonGroup = toolbar.querySelector(".trix-button-group--block-tools")

  const button = document.createElement("button")
  button.setAttribute("type", "button")
  button.setAttribute("class", "trix-button")
  button.setAttribute("data-trix-attribute", "highlight")
  button.textContent = "Highlight"

  buttonGroup.appendChild(button)
})

// Define the attribute
Trix.config.textAttributes.highlight = {
  tagName: "mark",
  inheritable: true
}
```

### Custom Styles

```scss
// Customize Trix appearance
trix-editor {
  min-height: 300px;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;

  &:focus {
    border-color: #3b82f6;
    outline: none;
  }
}

trix-toolbar {
  background: #f9fafb;
  border-bottom: 1px solid #ddd;
  padding: 0.5rem;
}

// Style the rendered content
.trix-content {
  h1 { font-size: 1.5rem; margin-top: 1rem; }

  blockquote {
    border-left: 3px solid #ddd;
    padding-left: 1rem;
    color: #666;
  }

  pre {
    background: #f4f4f5;
    padding: 1rem;
    border-radius: 4px;
    overflow-x: auto;
  }
}
```

## Event Handling

### JavaScript Events

```javascript
// Listen for content changes
document.addEventListener("trix-change", (event) => {
  const editor = event.target
  console.log("Content changed:", editor.value)
})

// Before paste
document.addEventListener("trix-before-paste", (event) => {
  // Modify paste behavior
})

// Before file accept
document.addEventListener("trix-file-accept", (event) => {
  // Validate file
  const acceptedTypes = ["image/jpeg", "image/png", "image/gif"]
  if (!acceptedTypes.includes(event.file.type)) {
    event.preventDefault()
    alert("Only images are allowed!")
  }

  // Limit file size (5MB)
  if (event.file.size > 5 * 1024 * 1024) {
    event.preventDefault()
    alert("File too large!")
  }
})

// After file attached
document.addEventListener("trix-attachment-add", (event) => {
  const attachment = event.attachment
  if (attachment.file) {
    uploadFile(attachment)
  }
})
```

### Stimulus Controller

```javascript
// app/javascript/controllers/rich_text_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["editor", "counter"]

  connect() {
    this.updateCounter()
  }

  change(event) {
    this.updateCounter()
    this.autoSave()
  }

  updateCounter() {
    const text = this.editorTarget.editor.getDocument().toString()
    this.counterTarget.textContent = `${text.length} characters`
  }

  autoSave() {
    clearTimeout(this.saveTimer)
    this.saveTimer = setTimeout(() => {
      this.save()
    }, 2000)
  }

  save() {
    // Auto-save logic
  }
}
```

## Querying Rich Text

### Search Content

```ruby
# Find articles containing text
Article.joins(:rich_text_content)
       .where("action_text_rich_texts.body LIKE ?", "%search term%")

# Scope for searching
class Article < ApplicationRecord
  has_rich_text :content

  scope :search_content, ->(term) {
    joins(:rich_text_content)
      .where("action_text_rich_texts.body LIKE ?", "%#{term}%")
  }
end
```

### Eager Loading

```ruby
# Avoid N+1 queries
@articles = Article.all.with_rich_text_content

# Multiple rich text fields
@articles = Article.all.with_rich_text_content.with_rich_text_summary

# With embedded images
@articles = Article.all.with_rich_text_content_and_embeds
```

## Testing

### Minitest

```ruby
# test/models/article_test.rb
require "test_helper"

class ArticleTest < ActiveSupport::TestCase
  test "has rich text content" do
    article = Article.new(title: "Test", content: "<p>Hello World</p>")

    assert article.content.present?
    assert_includes article.content.to_plain_text, "Hello World"
  end

  test "content with attachment" do
    article = articles(:one)
    blob = active_storage_blobs(:image)

    article.content.body.attachables << blob
    article.save!

    assert_equal 1, article.content.body.attachments.count
  end
end
```

### System Tests

```ruby
# test/system/articles_test.rb
require "application_system_test_case"

class ArticlesTest < ApplicationSystemTestCase
  test "creating article with rich text" do
    visit new_article_path

    fill_in "Title", with: "My Article"

    # Fill in Trix editor
    find("trix-editor").click.set("This is rich text content")

    click_button "Create Article"

    assert_text "Article was successfully created"
    assert_text "This is rich text content"
  end
end
```

## Security

### Sanitization

Action Text automatically sanitizes content. Customize allowed tags:

```ruby
# config/initializers/action_text.rb
Rails.application.config.after_initialize do
  ActionText::ContentHelper.allowed_tags = %w[
    strong em del a h1 h2 h3 h4 blockquote pre code ul ol li
  ]

  ActionText::ContentHelper.allowed_attributes = %w[
    href class data-*
  ]
end
```

### Content Security

```ruby
# Sanitize on output (additional layer)
<%= sanitize @article.content.to_s, tags: %w[p strong em a], attributes: %w[href] %>
```
