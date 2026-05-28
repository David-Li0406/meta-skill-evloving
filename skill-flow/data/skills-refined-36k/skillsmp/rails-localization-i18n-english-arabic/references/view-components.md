# View Components & Templates Reference

## Application Layout with RTL Support

```erb
<%# app/views/layouts/application.html.erb %>
<!DOCTYPE html>
<html lang="<%= I18n.locale %>" dir="<%= text_direction %>">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title><%= yield(:title) || t('app.name') %></title>

  <%# Load RTL stylesheet when needed %>
  <%= stylesheet_link_tag "application", "data-turbo-track": "reload" %>
  <% if rtl? %>
    <%= stylesheet_link_tag "rtl", "data-turbo-track": "reload" %>
  <% end %>

  <%= javascript_importmap_tags %>
</head>
<body class="<%= direction_class %>" data-locale="<%= I18n.locale %>">
  <%= render 'shared/header' %>

  <main class="container">
    <%= render 'shared/flash_messages' %>
    <%= yield %>
  </main>

  <%= render 'shared/footer' %>
</body>
</html>
```

---

## Language Switcher Component

```erb
<%# app/views/shared/_language_switcher.html.erb %>
<div class="language-switcher" data-controller="language-switcher">
  <button type="button"
          class="language-button"
          data-action="click->language-switcher#toggle"
          aria-expanded="false"
          aria-haspopup="true">
    <span class="current-language">
      <%= I18n.t('language_name_native') %>
    </span>
    <svg class="icon" aria-hidden="true"><!-- dropdown icon --></svg>
  </button>

  <ul class="language-menu hidden" role="menu">
    <% I18n.available_locales.each do |locale| %>
      <li role="menuitem">
        <%= link_to switch_locale_path(locale: locale),
                    class: "language-option #{'active' if I18n.locale == locale}",
                    data: { locale: locale } do %>
          <span dir="<%= locale == :ar ? 'rtl' : 'ltr' %>">
            <%= I18n.t('language_name_native', locale: locale) %>
          </span>
          <span class="language-name-english">
            (<%= I18n.t('language_name', locale: locale) %>)
          </span>
        <% end %>
      </li>
    <% end %>
  </ul>
</div>
```

---

## Bidirectional Form Example

```erb
<%# app/views/users/_form.html.erb %>
<%= form_with model: @user, class: "form #{direction_class}" do |f| %>
  <% if @user.errors.any? %>
    <div class="error-summary" role="alert">
      <h3><%= t('activerecord.errors.messages.not_saved',
                 count: @user.errors.count,
                 resource: t('activerecord.models.user.one')) %></h3>
      <ul>
        <% @user.errors.full_messages.each do |message| %>
          <li><%= message %></li>
        <% end %>
      </ul>
    </div>
  <% end %>

  <div class="form-group">
    <%= f.label :email, class: 'form-label' %>
    <%= f.email_field :email,
                      class: 'form-input',
                      dir: 'ltr',  # Email always LTR
                      placeholder: t('placeholders.email'),
                      required: true %>
  </div>

  <div class="form-group">
    <%= f.label :first_name, class: 'form-label' %>
    <%= f.text_field :first_name,
                     class: 'form-input',
                     dir: 'auto',  # Auto-detect direction
                     required: true %>
  </div>

  <div class="form-group">
    <%= f.label :last_name, class: 'form-label' %>
    <%= f.text_field :last_name,
                     class: 'form-input',
                     dir: 'auto',
                     required: true %>
  </div>

  <div class="form-group">
    <%= f.label :phone_number, class: 'form-label' %>
    <%= f.telephone_field :phone_number,
                          class: 'form-input',
                          dir: 'ltr',  # Phone numbers always LTR
                          placeholder: '+966 5X XXX XXXX' %>
  </div>

  <div class="form-group">
    <%= f.label :bio, class: 'form-label' %>
    <%= f.text_area :bio,
                    class: 'form-input',
                    dir: 'auto',
                    rows: 4 %>
  </div>

  <div class="form-actions">
    <%= f.submit t('common.actions.save'), class: 'btn btn-primary' %>
    <%= link_to t('common.actions.cancel'), users_path, class: 'btn btn-secondary' %>
  </div>
<% end %>
```

---

## Route Configuration

```ruby
# config/routes.rb
Rails.application.routes.draw do
  # Locale-scoped routes
  scope "(:locale)", locale: /en|ar/ do
    resources :users
    resources :transactions
    resources :accounts

    root "home#index"
  end

  # API routes (typically not localized in URL)
  namespace :api do
    namespace :v1 do
      resources :users
    end
  end

  # Locale switcher
  get "locale/:locale", to: "locales#switch", as: :switch_locale
end
```

---

## Stimulus Controller for Language Switcher

```javascript
// app/javascript/controllers/language_switcher_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["menu", "button"]

  toggle() {
    this.menuTarget.classList.toggle("hidden")
    const expanded = !this.menuTarget.classList.contains("hidden")
    this.buttonTarget.setAttribute("aria-expanded", expanded)
  }

  close(event) {
    if (!this.element.contains(event.target)) {
      this.menuTarget.classList.add("hidden")
      this.buttonTarget.setAttribute("aria-expanded", "false")
    }
  }

  connect() {
    document.addEventListener("click", this.close.bind(this))
  }

  disconnect() {
    document.removeEventListener("click", this.close.bind(this))
  }
}
```

---

## Flash Messages with RTL Support

```erb
<%# app/views/shared/_flash_messages.html.erb %>
<% flash.each do |type, message| %>
  <div class="flash flash-<%= type %>"
       role="alert"
       dir="<%= text_direction %>">
    <span class="flash-message"><%= message %></span>
    <button type="button"
            class="flash-close"
            data-action="click->flash#dismiss"
            aria-label="<%= t('common.actions.close') %>">
      ×
    </button>
  </div>
<% end %>
```

---

## Data Table with Mixed Directions

```erb
<%# Numbers and dates stay LTR, text follows locale %>
<table class="data-table" dir="<%= text_direction %>">
  <thead>
    <tr>
      <th><%= t('activerecord.attributes.transaction.date') %></th>
      <th><%= t('activerecord.attributes.transaction.description') %></th>
      <th><%= t('activerecord.attributes.transaction.amount') %></th>
    </tr>
  </thead>
  <tbody>
    <% @transactions.each do |transaction| %>
      <tr>
        <td dir="ltr" class="date"><%= l(transaction.date, format: :short) %></td>
        <td dir="auto"><%= transaction.description %></td>
        <td dir="ltr" class="currency"><%= localized_currency(transaction.amount) %></td>
      </tr>
    <% end %>
  </tbody>
</table>
```
