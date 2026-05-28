# Form Patterns

## Custom Form Builder

```ruby
# app/helpers/tailwind_form_builder.rb
class TailwindFormBuilder < ActionView::Helpers::FormBuilder
  def text_field(method, options = {})
    add_default_classes(options, "input-field")
    wrap_with_label(method) do
      super(method, options)
    end
  end

  def text_area(method, options = {})
    add_default_classes(options, "textarea-field")
    wrap_with_label(method) do
      super(method, options)
    end
  end

  def select(method, choices = nil, options = {}, html_options = {})
    add_default_classes(html_options, "select-field")
    wrap_with_label(method) do
      super(method, choices, options, html_options)
    end
  end

  def submit(value = nil, options = {})
    add_default_classes(options, "btn btn-primary")
    super(value, options)
  end

  private

  def add_default_classes(options, default_classes)
    options[:class] = [default_classes, options[:class]].compact.join(" ")
  end

  def wrap_with_label(method, &block)
    @template.content_tag(:div, class: "form-group") do
      label(method, class: "form-label") + @template.capture(&block) + error_message(method)
    end
  end

  def error_message(method)
    return "" unless object.errors[method].any?

    @template.content_tag(:span, object.errors[method].first, class: "error-message")
  end
end
```

```erb
<%# Usage %>
<%= form_with model: @user, builder: TailwindFormBuilder do |form| %>
  <%= form.text_field :name %>
  <%= form.email_field :email %>
  <%= form.submit %>
<% end %>
```

## Dynamic Nested Forms

```erb
<%# app/views/articles/_form.html.erb %>
<%= form_with model: @article, data: { controller: "nested-form" } do |form| %>
  <%= form.text_field :title %>

  <div id="comments" data-nested-form-target="container">
    <%= form.fields_for :comments do |comment_form| %>
      <%= render "comment_fields", form: comment_form %>
    <% end %>
  </div>

  <%= link_to "Add Comment",
      "#",
      data: {
        action: "click->nested-form#add",
        nested_form_template_value: render("comment_fields", form: form.fields_for(:comments, Comment.new, child_index: "NEW_RECORD"))
      } %>

  <%= form.submit %>
<% end %>

<%# app/views/articles/_comment_fields.html.erb %>
<div class="nested-fields" data-nested-form-target="field">
  <%= form.text_area :body %>
  <%= form.hidden_field :_destroy, value: false, data: { nested_form_target: "destroy" } %>
  <%= link_to "Remove", "#", data: { action: "click->nested-form#remove" } %>
</div>
```

```javascript
// app/javascript/controllers/nested_form_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["container", "field", "destroy"]
  static values = { template: String }

  add(event) {
    event.preventDefault()
    const content = this.templateValue.replace(/NEW_RECORD/g, new Date().getTime())
    this.containerTarget.insertAdjacentHTML("beforeend", content)
  }

  remove(event) {
    event.preventDefault()
    const field = event.target.closest("[data-nested-form-target='field']")
    const destroyInput = field.querySelector("[data-nested-form-target='destroy']")

    if (destroyInput) {
      destroyInput.value = "1"
      field.style.display = "none"
    } else {
      field.remove()
    }
  }
}
```

## Multi-Step Form (Wizard)

```ruby
# app/controllers/registrations_controller.rb
class RegistrationsController < ApplicationController
  STEPS = %w[account profile preferences].freeze

  def new
    @user = User.new
    @step = params[:step] || STEPS.first
  end

  def create
    @user = User.new(user_params)
    @step = params[:step]

    if final_step?
      if @user.save
        redirect_to root_path, notice: "Registration complete!"
      else
        render :new, status: :unprocessable_entity
      end
    else
      if @user.valid?(step_context)
        redirect_to new_registration_path(step: next_step, user: user_params)
      else
        render :new, status: :unprocessable_entity
      end
    end
  end

  private

  def next_step
    STEPS[STEPS.index(@step) + 1]
  end

  def final_step?
    @step == STEPS.last
  end

  def step_context
    @step.to_sym
  end
end
```

```erb
<%# app/views/registrations/new.html.erb %>
<%= render "steps/#{@step}", user: @user %>

<%# app/views/registrations/steps/_account.html.erb %>
<%= form_with model: user, url: registrations_path do |form| %>
  <%= hidden_field_tag :step, "account" %>
  <%= form.email_field :email %>
  <%= form.password_field :password %>
  <%= form.submit "Next" %>
<% end %>
```

## Inline Editing

```erb
<%# Show mode %>
<div id="<%= dom_id(article) %>"
     data-controller="inline-edit">
  <div data-inline-edit-target="display">
    <h2><%= article.title %></h2>
    <%= link_to "Edit", "#", data: { action: "click->inline-edit#showForm" } %>
  </div>

  <div data-inline-edit-target="form" class="hidden">
    <%= form_with model: article,
                  data: { action: "turbo:submit-end->inline-edit#hideForm" } do |form| %>
      <%= form.text_field :title %>
      <%= form.submit "Save" %>
      <%= link_to "Cancel", "#", data: { action: "click->inline-edit#hideForm" } %>
    <% end %>
  </div>
</div>
```

## Search Form with Filters

```erb
<%= form_with url: articles_path, method: :get, data: { turbo_frame: "articles" } do |form| %>
  <div class="search-filters">
    <%= form.text_field :q, placeholder: "Search..." %>

    <%= form.select :status,
        options_for_select([["All", ""], ["Published", "published"], ["Draft", "draft"]], params[:status]),
        {},
        { data: { action: "change->form#submit" } } %>

    <%= form.select :category_id,
        options_from_collection_for_select(Category.all, :id, :name, params[:category_id]),
        { include_blank: "All Categories" },
        { data: { action: "change->form#submit" } } %>

    <%= form.date_field :from_date, value: params[:from_date] %>
    <%= form.date_field :to_date, value: params[:to_date] %>

    <%= form.submit "Search" %>
  </div>
<% end %>

<%= turbo_frame_tag "articles" do %>
  <%= render @articles %>
  <%= paginate @articles %>
<% end %>
```

## File Upload with Preview

```erb
<%= form_with model: @product do |form| %>
  <div data-controller="image-preview">
    <%= form.file_field :image,
        accept: "image/*",
        data: { action: "change->image-preview#preview", image_preview_target: "input" } %>

    <img data-image-preview-target="preview"
         src="<%= @product.image.attached? ? url_for(@product.image) : '' %>"
         class="<%= 'hidden' unless @product.image.attached? %>">
  </div>

  <%= form.submit %>
<% end %>
```

```javascript
// app/javascript/controllers/image_preview_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["input", "preview"]

  preview() {
    const file = this.inputTarget.files[0]
    if (file) {
      const reader = new FileReader()
      reader.onload = (e) => {
        this.previewTarget.src = e.target.result
        this.previewTarget.classList.remove("hidden")
      }
      reader.readAsDataURL(file)
    }
  }
}
```

## Form Objects

```ruby
# app/forms/contact_form.rb
class ContactForm
  include ActiveModel::Model
  include ActiveModel::Attributes

  attribute :name, :string
  attribute :email, :string
  attribute :message, :string
  attribute :newsletter, :boolean, default: false

  validates :name, :email, :message, presence: true
  validates :email, format: { with: URI::MailTo::EMAIL_REGEXP }

  def submit
    return false unless valid?

    ContactMailer.new_inquiry(self).deliver_later
    subscribe_to_newsletter if newsletter

    true
  end

  private

  def subscribe_to_newsletter
    NewsletterSubscription.create(email: email)
  end
end
```

```erb
<%= form_with model: @contact_form, url: contacts_path do |form| %>
  <%= form.text_field :name %>
  <%= form.email_field :email %>
  <%= form.text_area :message %>
  <%= form.check_box :newsletter %>
  <%= form.label :newsletter, "Subscribe to newsletter" %>
  <%= form.submit "Send Message" %>
<% end %>
```
