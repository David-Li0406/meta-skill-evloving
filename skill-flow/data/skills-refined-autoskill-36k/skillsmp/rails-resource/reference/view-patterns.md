# View Patterns

Tailwind CSS patterns from existing views (posts/, job_posts/).

## index.html.erb Template

```erb
<div class="min-h-screen bg-background pb-20">
  <header class="sticky top-0 bg-background/95 backdrop-blur-sm border-b border-border z-40">
    <div class="max-w-screen-xl mx-auto px-4 py-4">
      <h1 class="text-2xl font-bold">Resource Names</h1>
      <p class="text-sm text-muted-foreground">Description</p>
    </div>
  </header>

  <main class="max-w-screen-xl mx-auto px-4 py-6">
    <div class="space-y-4">
      <% @resource_names.each do |resource| %>
        <article class="bg-card rounded-xl p-6 border border-border hover:border-muted-foreground/20 transition-colors">
          <!-- Content -->
        </article>
      <% end %>
    </div>
  </main>
</div>

<%= render "shared/bottom_nav" %>
```

## _form.html.erb Template

```erb
<%= form_with(model: resource, class: "space-y-6") do |form| %>
  <% if resource.errors.any? %>
    <div class="bg-destructive/10 border border-destructive rounded-lg p-4">
      <h2 class="text-sm font-semibold text-destructive mb-2">
        <%= pluralize(resource.errors.count, "error") %> 발생:
      </h2>
      <ul class="list-disc list-inside text-sm text-destructive/80">
        <% resource.errors.full_messages.each do |message| %>
          <li><%= message %></li>
        <% end %>
      </ul>
    </div>
  <% end %>

  <div class="space-y-2">
    <%= form.label :title, class: "block text-sm font-medium" %>
    <%= form.text_field :title, class: "w-full rounded-lg border border-input bg-background px-3 py-2" %>
  </div>

  <div class="space-y-2">
    <%= form.label :content, class: "block text-sm font-medium" %>
    <%= form.text_area :content, rows: 4, class: "w-full rounded-lg border border-input bg-background px-3 py-2" %>
  </div>

  <div class="flex gap-3">
    <%= form.submit "저장", class: "inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90" %>
    <%= link_to "취소", :back, class: "inline-flex items-center justify-center rounded-md border border-input bg-background px-4 py-2 text-sm font-medium hover:bg-accent" %>
  </div>
<% end %>
```

## Key Tailwind Classes

**Layout**: `min-h-screen`, `max-w-screen-xl`, `mx-auto`, `px-4`
**Cards**: `bg-card`, `rounded-xl`, `p-6`, `border border-border`
**Spacing**: `space-y-4`, `space-y-6`, `gap-3`
**Typography**: `text-2xl`, `font-bold`, `text-muted-foreground`
**Buttons**: `bg-primary`, `text-primary-foreground`, `hover:bg-primary/90`
**Forms**: `rounded-lg`, `border border-input`, `bg-background`
**Errors**: `bg-destructive/10`, `text-destructive`
