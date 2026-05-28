# Accessible ViewComponent Examples

## Accessible Component Base

Base class with common accessibility helpers:

```ruby
# app/components/accessible_component.rb
class AccessibleComponent < ViewComponent::Base
  def unique_id(prefix = "component")
    @unique_id ||= "#{prefix}-#{SecureRandom.hex(4)}"
  end

  def describedby_id
    "#{unique_id}-description"
  end

  def labelledby_id
    "#{unique_id}-label"
  end

  def error_id
    "#{unique_id}-error"
  end

  def aria_attributes(options = {})
    attrs = {}
    attrs["aria-label"] = options[:label] if options[:label]
    attrs["aria-labelledby"] = options[:labelledby] if options[:labelledby]
    attrs["aria-describedby"] = options[:describedby] if options[:describedby]
    attrs["aria-expanded"] = options[:expanded] if options.key?(:expanded)
    attrs["aria-controls"] = options[:controls] if options[:controls]
    attrs["aria-current"] = options[:current] if options[:current]
    attrs["aria-invalid"] = options[:invalid] if options[:invalid]
    attrs
  end
end
```

---

## Accessible Form Input Component

```ruby
# app/components/form_input_component.rb
class FormInputComponent < AccessibleComponent
  def initialize(form:, attribute:, label:, hint: nil, required: false)
    @form = form
    @attribute = attribute
    @label = label
    @hint = hint
    @required = required
  end

  def has_error?
    @form.object.errors[@attribute].any?
  end

  def error_message
    @form.object.errors[@attribute].first
  end

  def input_attributes
    attrs = {
      "aria-describedby": [@hint ? describedby_id : nil, has_error? ? error_id : nil].compact.join(" ").presence,
      "aria-required": @required,
      "aria-invalid": has_error?
    }
    attrs["aria-errormessage"] = error_id if has_error?
    attrs.compact
  end
end
```

```erb
<%# app/components/form_input_component.html.erb %>
<div class="mb-4">
  <%= @form.label @attribute, @label, class: "block text-sm font-medium text-black dark:text-white" %>

  <% if @hint %>
    <p id="<%= describedby_id %>" class="text-sm text-bodydark mt-1">
      <%= @hint %>
    </p>
  <% end %>

  <%= @form.text_field @attribute,
      class: "mt-1 block w-full rounded border-stroke dark:border-strokedark
             bg-transparent px-4 py-2 text-black dark:text-white
             focus:border-primary focus:ring-primary
             #{has_error? ? 'border-danger' : ''}",
      **input_attributes %>

  <% if has_error? %>
    <p id="<%= error_id %>" class="mt-1 text-sm text-danger" role="alert">
      <%= error_message %>
    </p>
  <% end %>
</div>
```

---

## Accessible Modal Component

```ruby
# app/components/modal_component.rb
class ModalComponent < AccessibleComponent
  renders_one :trigger
  renders_one :body

  def initialize(title:)
    @title = title
  end
end
```

```erb
<%# app/components/modal_component.html.erb %>
<div data-controller="modal">
  <%= trigger %>

  <div data-modal-target="dialog"
       role="dialog"
       aria-modal="true"
       aria-labelledby="<%= labelledby_id %>"
       class="fixed inset-0 z-50 hidden"
       data-action="keydown.escape->modal#close">

    <%# Backdrop %>
    <div class="fixed inset-0 bg-black/50"
         data-action="click->modal#close"
         aria-hidden="true"></div>

    <%# Dialog content %>
    <div class="fixed inset-0 flex items-center justify-center p-4"
         data-controller="focus-trap"
         data-focus-trap-target="container"
         data-action="keydown->focus-trap#trapFocus">

      <div class="bg-white dark:bg-boxdark rounded-lg shadow-xl max-w-md w-full p-6">
        <h2 id="<%= labelledby_id %>" class="text-xl font-semibold text-black dark:text-white">
          <%= @title %>
        </h2>

        <button data-action="click->modal#close"
                class="absolute top-4 right-4"
                aria-label="Close dialog">
          <svg aria-hidden="true" class="h-5 w-5">...</svg>
        </button>

        <%= body %>
      </div>
    </div>
  </div>
</div>
```

---

## Accessible Tabs Component

```ruby
# app/components/tabs_component.rb
class TabsComponent < AccessibleComponent
  renders_many :tabs, ->(title:) {
    TabComponent.new(title: title, tabs_id: unique_id)
  }

  class TabComponent < ViewComponent::Base
    def initialize(title:, tabs_id:)
      @title = title
      @tabs_id = tabs_id
    end
  end
end
```

```erb
<%# app/components/tabs_component.html.erb %>
<div data-controller="tabs roving-tabindex">
  <div role="tablist"
       aria-label="<%= @label %>"
       data-action="keydown.right->roving-tabindex#next keydown.left->roving-tabindex#previous">
    <% tabs.each_with_index do |tab, index| %>
      <button role="tab"
              id="<%= unique_id %>-tab-<%= index %>"
              aria-selected="<%= index == 0 %>"
              aria-controls="<%= unique_id %>-panel-<%= index %>"
              data-roving-tabindex-target="item"
              data-tabs-target="tab"
              data-action="click->tabs#select"
              tabindex="<%= index == 0 ? 0 : -1 %>">
        <%= tab.title %>
      </button>
    <% end %>
  </div>

  <% tabs.each_with_index do |tab, index| %>
    <div role="tabpanel"
         id="<%= unique_id %>-panel-<%= index %>"
         aria-labelledby="<%= unique_id %>-tab-<%= index %>"
         data-tabs-target="panel"
         <%= index == 0 ? '' : 'hidden' %>>
      <%= tab %>
    </div>
  <% end %>
</div>
```
