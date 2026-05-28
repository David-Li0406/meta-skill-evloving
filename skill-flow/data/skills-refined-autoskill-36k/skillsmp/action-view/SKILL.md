---
name: action-view
description: This skill should be used when the user asks about "views", "ERB templates", "partials", "layouts", "render", "form_with", "form helpers", "view helpers", "link_to", "content_for", "yield", "collection rendering", "locals", "tag helpers", "asset helpers", "image_tag", "stylesheet_link_tag", or needs guidance on building Rails views and templates.
version: 1.0.0
---

# Action View

Comprehensive guide to Rails views, templates, partials, layouts, and view helpers.

## Templates

### ERB Syntax

```erb
<%# Comment - not rendered %>

<% code %>        <%# Execute Ruby, no output %>
<%= expression %> <%# Output result (escaped) %>
<%== raw_html %>  <%# Output without escaping (use carefully) %>

<%- code -%>      <%# Suppress leading/trailing whitespace %>
```

### Common ERB Patterns

```erb
<%# Conditionals %>
<% if @user.admin? %>
  <span class="badge">Admin</span>
<% end %>

<%# Iteration %>
<% @articles.each do |article| %>
  <article>
    <h2><%= article.title %></h2>
    <p><%= truncate(article.body, length: 100) %></p>
  </article>
<% end %>

<%# Safe output %>
<%= sanitize(@article.body) %>
<%= raw(@trusted_html) %>
```

## Partials

Partials are reusable view fragments. Filename starts with underscore.

### Basic Partial

```erb
<%# app/views/articles/_article.html.erb %>
<article id="<%= dom_id(article) %>">
  <h2><%= article.title %></h2>
  <p><%= article.body %></p>
</article>

<%# Render partial %>
<%= render "article", article: @article %>
<%= render partial: "article", locals: { article: @article } %>
```

### Collection Rendering

```erb
<%# Renders _article.html.erb for each item %>
<%= render @articles %>

<%# Explicit collection %>
<%= render partial: "article", collection: @articles %>

<%# With spacer %>
<%= render partial: "article", collection: @articles, spacer_template: "article_divider" %>

<%# Cached collection %>
<%= render partial: "article", collection: @articles, cached: true %>
```

### Local Variables

```erb
<%# Counter and iteration info available %>
<%# article_counter (0-indexed) %>
<%# article_iteration.first?, .last?, .index, .size %>

<%# Strict locals (Rails 7.1+) %>
<%# locals: (article:, show_author: true) -%>
<article>
  <h2><%= article.title %></h2>
  <% if show_author %>
    <p>By <%= article.author.name %></p>
  <% end %>
</article>
```

### Partial Layouts

```erb
<%# Wrap partial in a layout %>
<%= render partial: "article", layout: "card", locals: { article: @article } %>

<%# app/views/shared/_card.html.erb %>
<div class="card">
  <%= yield %>
</div>
```

## Layouts

### Application Layout

```erb
<%# app/views/layouts/application.html.erb %>
<!DOCTYPE html>
<html>
  <head>
    <title><%= content_for(:title) || "My App" %></title>
    <%= csrf_meta_tags %>
    <%= csp_meta_tag %>
    <%= stylesheet_link_tag "application", "data-turbo-track": "reload" %>
    <%= javascript_importmap_tags %>
    <%= yield :head %>
  </head>
  <body>
    <%= render "shared/header" %>

    <% if notice %>
      <div class="notice"><%= notice %></div>
    <% end %>
    <% if alert %>
      <div class="alert"><%= alert %></div>
    <% end %>

    <main>
      <%= yield %>
    </main>

    <%= render "shared/footer" %>
  </body>
</html>
```

### Content For

```erb
<%# In view %>
<% content_for :title, "My Page Title" %>

<% content_for :head do %>
  <%= stylesheet_link_tag "custom" %>
<% end %>

<% content_for :sidebar do %>
  <nav>Sidebar content</nav>
<% end %>

<%# In layout %>
<%= content_for?(:sidebar) ? yield(:sidebar) : render("default_sidebar") %>
```

### Controller-Specific Layouts

```ruby
class AdminController < ApplicationController
  layout "admin"
end

class ArticlesController < ApplicationController
  layout "article", only: [:show]
  layout :determine_layout

  private

  def determine_layout
    current_user&.admin? ? "admin" : "application"
  end
end
```

## Form Helpers

### form_with

```erb
<%# Model-backed form %>
<%= form_with model: @article do |form| %>
  <%= form.label :title %>
  <%= form.text_field :title %>

  <%= form.label :body %>
  <%= form.text_area :body, rows: 10 %>

  <%= form.label :status %>
  <%= form.select :status, Article::STATUSES %>

  <%= form.submit %>
<% end %>

<%# URL-based form %>
<%= form_with url: search_path, method: :get do |form| %>
  <%= form.text_field :q, placeholder: "Search..." %>
  <%= form.submit "Search" %>
<% end %>
```

### Form Fields

```erb
<%# Text inputs %>
<%= form.text_field :name %>
<%= form.email_field :email %>
<%= form.password_field :password %>
<%= form.telephone_field :phone %>
<%= form.url_field :website %>
<%= form.number_field :quantity, min: 1, max: 100 %>
<%= form.range_field :rating, min: 1, max: 5 %>
<%= form.search_field :q %>
<%= form.text_area :description, rows: 5 %>

<%# Hidden %>
<%= form.hidden_field :status, value: "draft" %>

<%# Checkboxes and radios %>
<%= form.check_box :published %>
<%= form.radio_button :status, "draft" %>
<%= form.radio_button :status, "published" %>

<%# Select %>
<%= form.select :category_id, Category.pluck(:name, :id) %>
<%= form.select :role, %w[admin editor viewer], { include_blank: "Select role" } %>

<%# Collection select %>
<%= form.collection_select :category_id, Category.all, :id, :name %>
<%= form.collection_radio_buttons :status, Status.all, :id, :name %>
<%= form.collection_check_boxes :tag_ids, Tag.all, :id, :name %>

<%# Date/time %>
<%= form.date_field :published_on %>
<%= form.time_field :start_time %>
<%= form.datetime_local_field :event_at %>
<%= form.date_select :birthday %>
<%= form.time_zone_select :time_zone %>

<%# File upload %>
<%= form.file_field :avatar %>
<%= form.file_field :images, multiple: true %>
```

### Nested Forms

```ruby
# Model
class Article < ApplicationRecord
  has_many :comments
  accepts_nested_attributes_for :comments, allow_destroy: true
end
```

```erb
<%= form_with model: @article do |form| %>
  <%= form.text_field :title %>

  <%= form.fields_for :comments do |comment_form| %>
    <%= comment_form.text_area :body %>
    <%= comment_form.check_box :_destroy %>
    <%= comment_form.label :_destroy, "Delete" %>
  <% end %>

  <%= form.submit %>
<% end %>
```

## URL Helpers

```erb
<%# Links %>
<%= link_to "Home", root_path %>
<%= link_to "Article", @article %>
<%= link_to "Edit", edit_article_path(@article) %>
<%= link_to "Delete", @article, method: :delete, data: { turbo_method: :delete, turbo_confirm: "Sure?" } %>

<%# With block %>
<%= link_to article_path(@article) do %>
  <strong><%= @article.title %></strong>
<% end %>

<%# Button (creates form) %>
<%= button_to "Subscribe", subscriptions_path, method: :post %>

<%# Email %>
<%= mail_to "support@example.com" %>
<%= mail_to "support@example.com", "Contact Us", subject: "Help Request" %>

<%# Current page check %>
<%= link_to "Home", root_path, class: ("active" if current_page?(root_path)) %>
```

## Tag Helpers

```erb
<%# Modern tag helper syntax %>
<%= tag.div class: "container" do %>
  <%= tag.h1 @article.title %>
  <%= tag.p @article.body, class: "content" %>
<% end %>

<%# With data attributes %>
<%= tag.div data: { controller: "toggle", action: "click->toggle#switch" } do %>
  Content
<% end %>

<%# Self-closing tags %>
<%= tag.br %>
<%= tag.hr %>
<%= tag.input type: "text", name: "query" %>

<%# class_names / token_list %>
<%= tag.div class: class_names("base", active: @active, hidden: @hidden) %>
```

## Asset Helpers

```erb
<%# Images %>
<%= image_tag "logo.png" %>
<%= image_tag "logo.png", alt: "Logo", class: "logo", size: "100x50" %>
<%= image_tag @user.avatar, fallback: "default_avatar.png" %>

<%# Stylesheets %>
<%= stylesheet_link_tag "application", media: "all" %>
<%= stylesheet_link_tag "print", media: "print" %>

<%# JavaScript %>
<%= javascript_include_tag "application" %>
<%= javascript_importmap_tags %>

<%# Favicon %>
<%= favicon_link_tag "favicon.ico" %>

<%# Video/Audio %>
<%= video_tag "intro.mp4", controls: true, autoplay: false %>
<%= audio_tag "podcast.mp3", controls: true %>
```

## Text Helpers

```erb
<%# Truncate %>
<%= truncate(@article.body, length: 100) %>
<%= truncate(@article.body, length: 100, omission: "... (more)") %>

<%# Excerpt %>
<%= excerpt(@article.body, "Rails", radius: 25) %>

<%# Pluralize %>
<%= pluralize(@comments.count, "comment") %>

<%# Word wrap %>
<%= word_wrap(@text, line_width: 80) %>

<%# Simple format (converts newlines to <br> and paragraphs) %>
<%= simple_format(@article.body) %>

<%# Highlight %>
<%= highlight(@article.body, "Rails") %>
```

## Number Helpers

```erb
<%= number_to_currency(1234.56) %>                    <%# $1,234.56 %>
<%= number_to_currency(1234.56, unit: "€") %>         <%# €1,234.56 %>
<%= number_to_percentage(75.5) %>                     <%# 75.500% %>
<%= number_to_percentage(75.5, precision: 0) %>       <%# 76% %>
<%= number_with_delimiter(12345678) %>                <%# 12,345,678 %>
<%= number_with_precision(111.2345, precision: 2) %>  <%# 111.23 %>
<%= number_to_human(1234567) %>                       <%# 1.23 Million %>
<%= number_to_human_size(1234567) %>                  <%# 1.18 MB %>
<%= number_to_phone(5551234567) %>                    <%# 555-123-4567 %>
```

## Date Helpers

```erb
<%= distance_of_time_in_words(Time.current, 3.days.from_now) %>  <%# about 3 days %>
<%= time_ago_in_words(@article.created_at) %>                    <%# 2 hours ago %>
```

## Sanitization

```erb
<%# Remove dangerous HTML %>
<%= sanitize(@user_input) %>

<%# Allow specific tags %>
<%= sanitize(@content, tags: %w[p br strong em]) %>

<%# Strip all tags %>
<%= strip_tags(@html_content) %>

<%# Strip links but keep text %>
<%= strip_links(@content_with_links) %>
```

## Additional Resources

### Reference Files

- **`references/form-patterns.md`** - Complex form patterns, custom form builders
- **`references/view-helpers.md`** - Creating custom helpers, helper organization
