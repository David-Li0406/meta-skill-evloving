# View Helpers Guide

## Creating Custom Helpers

### Application Helper

```ruby
# app/helpers/application_helper.rb
module ApplicationHelper
  def page_title(title = nil)
    if title.present?
      content_for(:title) { title }
    end
    content_for(:title) || "My Application"
  end

  def flash_class(type)
    case type.to_sym
    when :notice, :success then "alert-success"
    when :alert, :error then "alert-danger"
    when :warning then "alert-warning"
    else "alert-info"
    end
  end

  def avatar_for(user, size: 40)
    if user.avatar.attached?
      image_tag user.avatar.variant(resize_to_limit: [size, size]),
                class: "avatar",
                alt: user.name
    else
      image_tag "default_avatar.png",
                size: "#{size}x#{size}",
                class: "avatar",
                alt: user.name
    end
  end

  def active_link_to(name, path, options = {})
    classes = options.delete(:class) || ""
    classes += " active" if current_page?(path)
    link_to name, path, options.merge(class: classes.strip)
  end

  def time_ago(time)
    return "never" if time.nil?
    "#{time_ago_in_words(time)} ago"
  end
end
```

### Domain-Specific Helpers

```ruby
# app/helpers/articles_helper.rb
module ArticlesHelper
  def article_status_badge(article)
    status_classes = {
      "published" => "badge-success",
      "draft" => "badge-secondary",
      "archived" => "badge-warning"
    }

    tag.span article.status.humanize,
             class: "badge #{status_classes[article.status]}"
  end

  def reading_time(article)
    words_per_minute = 200
    words = article.body.split.size
    minutes = (words / words_per_minute.to_f).ceil
    "#{minutes} min read"
  end

  def article_meta(article)
    parts = []
    parts << "by #{article.author.name}" if article.author
    parts << time_ago(article.published_at) if article.published?
    parts << "#{article.comments_count} comments" if article.comments_count > 0
    parts.join(" • ")
  end

  def truncated_body(article, length: 200)
    truncate(strip_tags(article.body), length: length)
  end
end
```

### Formatting Helpers

```ruby
# app/helpers/formatting_helper.rb
module FormattingHelper
  def format_money(amount, currency: "USD")
    return "Free" if amount.zero?
    number_to_currency(amount, unit: currency_symbol(currency))
  end

  def format_percentage(value, precision: 1)
    number_to_percentage(value, precision: precision)
  end

  def format_date(date, format: :long)
    return "N/A" if date.nil?
    l(date, format: format)
  end

  def format_datetime(datetime)
    return "N/A" if datetime.nil?
    datetime.strftime("%B %d, %Y at %I:%M %p")
  end

  def format_file_size(bytes)
    number_to_human_size(bytes)
  end

  def format_phone(number)
    number_to_phone(number, area_code: true)
  end

  private

  def currency_symbol(currency)
    { "USD" => "$", "EUR" => "€", "GBP" => "£" }[currency] || currency
  end
end
```

## Presenters / Decorators

### Basic Presenter

```ruby
# app/presenters/article_presenter.rb
class ArticlePresenter
  include ActionView::Helpers::TextHelper
  include ActionView::Helpers::UrlHelper
  include Rails.application.routes.url_helpers

  def initialize(article, view_context)
    @article = article
    @h = view_context
  end

  delegate :title, :body, :published?, :created_at, to: :@article

  def status_badge
    @h.tag.span status.humanize, class: "badge badge-#{status_class}"
  end

  def formatted_date
    @h.l(@article.created_at, format: :long)
  end

  def truncated_body(length: 200)
    truncate(@article.body, length: length)
  end

  def author_link
    return "Unknown" unless @article.author
    @h.link_to @article.author.name, @h.user_path(@article.author)
  end

  def edit_link
    @h.link_to "Edit", @h.edit_article_path(@article), class: "btn btn-sm"
  end

  private

  def status
    @article.status
  end

  def status_class
    { "published" => "success", "draft" => "secondary" }[status] || "info"
  end
end
```

```erb
<%# Usage in view %>
<% presenter = ArticlePresenter.new(@article, self) %>
<h1><%= presenter.title %></h1>
<%= presenter.status_badge %>
<p>By <%= presenter.author_link %> on <%= presenter.formatted_date %></p>
<%= presenter.truncated_body %>
```

### Using Draper Gem

```ruby
# app/decorators/article_decorator.rb
class ArticleDecorator < Draper::Decorator
  delegate_all

  def status_badge
    h.tag.span status.humanize, class: "badge badge-#{status_class}"
  end

  def published_on
    return "Not published" unless published_at
    published_at.strftime("%B %d, %Y")
  end

  def author_name
    author&.name || "Anonymous"
  end

  private

  def status_class
    { "published" => "success", "draft" => "warning" }[status] || "secondary"
  end
end

# Controller
def show
  @article = Article.find(params[:id]).decorate
end
```

## View Components

```ruby
# app/components/card_component.rb
class CardComponent < ViewComponent::Base
  def initialize(title:, footer: nil)
    @title = title
    @footer = footer
  end
end
```

```erb
<%# app/components/card_component.html.erb %>
<div class="card">
  <div class="card-header">
    <h3><%= @title %></h3>
  </div>
  <div class="card-body">
    <%= content %>
  </div>
  <% if @footer %>
    <div class="card-footer">
      <%= @footer %>
    </div>
  <% end %>
</div>
```

```erb
<%# Usage %>
<%= render CardComponent.new(title: "User Profile") do %>
  <p><%= @user.name %></p>
  <p><%= @user.email %></p>
<% end %>
```

## Helper Organization Best Practices

### Keep Helpers Focused

```ruby
# Good: Specific, single-purpose helpers
module DateHelper
  def relative_date(date)
    # ...
  end
end

module MoneyHelper
  def format_price(amount)
    # ...
  end
end

# Include in ApplicationHelper or specific controllers
class ApplicationController < ActionController::Base
  helper DateHelper
  helper MoneyHelper
end
```

### Testing Helpers

```ruby
# test/helpers/articles_helper_test.rb
require "test_helper"

class ArticlesHelperTest < ActionView::TestCase
  test "reading_time calculates correctly" do
    article = Article.new(body: "word " * 400)
    assert_equal "2 min read", reading_time(article)
  end

  test "article_status_badge returns correct HTML" do
    article = Article.new(status: "published")
    result = article_status_badge(article)

    assert_includes result, "badge-success"
    assert_includes result, "Published"
  end
end
```

## Common Patterns

### Conditional CSS Classes

```ruby
def nav_link_class(path)
  class_names("nav-link", active: current_page?(path))
end

def button_classes(variant: :primary, size: :md, disabled: false)
  class_names(
    "btn",
    "btn-#{variant}",
    "btn-#{size}",
    disabled: disabled
  )
end
```

### Icon Helpers

```ruby
def icon(name, options = {})
  css_class = options.delete(:class)
  tag.i(class: "bi bi-#{name} #{css_class}".strip, **options)
end

def icon_with_text(icon_name, text)
  tag.span do
    concat icon(icon_name)
    concat " "
    concat text
  end
end
```

### Meta Tag Helpers

```ruby
def meta_tags(title:, description: nil, image: nil)
  tags = []
  tags << tag.title(title)
  tags << tag.meta(name: "description", content: description) if description
  tags << tag.meta(property: "og:title", content: title)
  tags << tag.meta(property: "og:description", content: description) if description
  tags << tag.meta(property: "og:image", content: image) if image
  safe_join(tags)
end
```
