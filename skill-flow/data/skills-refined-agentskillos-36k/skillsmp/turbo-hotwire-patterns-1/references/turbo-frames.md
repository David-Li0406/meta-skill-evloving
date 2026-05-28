# Turbo Frames Reference

## Basic Frame

```erb
<%# app/views/tasks/index.html.erb %>
<%= turbo_frame_tag "tasks_list" do %>
  <% @tasks.each do |task| %>
    <%= render task %>
  <% end %>

  <%= link_to "Load more", tasks_path(page: @next_page) %>
<% end %>
```

## Frame Navigation

```erb
<%# Links within frame navigate inside frame %>
<%= turbo_frame_tag dom_id(@task) do %>
  <h3><%= @task.title %></h3>
  <%= link_to "Edit", edit_task_path(@task) %>
<% end %>

<%# Edit form replaces frame content %>
<%# app/views/tasks/edit.html.erb %>
<%= turbo_frame_tag dom_id(@task) do %>
  <%= render "form", task: @task %>
<% end %>
```

## Breaking Out of Frame

```erb
<%# Target another frame %>
<%= link_to "Details", task_path(@task), data: { turbo_frame: "task_detail" } %>

<%# Target the whole page %>
<%= link_to "Full Page", task_path(@task), data: { turbo_frame: "_top" } %>
```

## Lazy Loading Frames

```erb
<%# Load content when frame becomes visible %>
<%= turbo_frame_tag "comments",
                    src: task_comments_path(@task),
                    loading: :lazy do %>
  <p>Loading comments...</p>
<% end %>
```

## Frame with Different Source

```erb
<%# Frame that loads from different URL %>
<%= turbo_frame_tag "sidebar",
                    src: sidebar_path,
                    target: "_top" do %>
  <p>Loading sidebar...</p>
<% end %>
```

## Progressive Enhancement

```erb
<!-- Works without JavaScript -->
<turbo-frame id="comments" src="<%= task_comments_path(@task) %>">
  <!-- Fallback content shown during load and without JS -->
  <a href="<%= task_comments_path(@task) %>">View comments</a>
</turbo-frame>
```
