# Turbo Streams Reference

## Stream Actions

```erb
<%# Append to container %>
<%= turbo_stream.append "tasks" do %>
  <%= render @task %>
<% end %>

<%# Prepend to container %>
<%= turbo_stream.prepend "tasks" do %>
  <%= render @task %>
<% end %>

<%# Replace specific element %>
<%= turbo_stream.replace dom_id(@task) do %>
  <%= render @task %>
<% end %>

<%# Update contents (not replace element) %>
<%= turbo_stream.update "task_count" do %>
  <%= @tasks.count %>
<% end %>

<%# Remove element %>
<%= turbo_stream.remove dom_id(@task) %>

<%# Before/After %>
<%= turbo_stream.before dom_id(@task) do %>
  <div class="alert">Task updated!</div>
<% end %>

<%= turbo_stream.after dom_id(@task) do %>
  <div class="related">Related tasks...</div>
<% end %>
```

---

## Stream Response from Controller

```ruby
# app/controllers/tasks_controller.rb
class TasksController < ApplicationController
  def create
    @task = current_account.tasks.build(task_params)

    respond_to do |format|
      if @task.save
        format.turbo_stream  # Renders create.turbo_stream.erb
        format.html { redirect_to @task }
      else
        format.turbo_stream do
          render turbo_stream: turbo_stream.replace(
            "task_form",
            partial: "form",
            locals: { task: @task }
          )
        end
        format.html { render :new }
      end
    end
  end

  def destroy
    @task = current_account.tasks.find(params[:id])
    @task.destroy

    respond_to do |format|
      format.turbo_stream { render turbo_stream: turbo_stream.remove(dom_id(@task)) }
      format.html { redirect_to tasks_path }
    end
  end
end
```

```erb
<%# app/views/tasks/create.turbo_stream.erb %>
<%= turbo_stream.prepend "tasks" do %>
  <%= render @task %>
<% end %>

<%= turbo_stream.replace "task_form" do %>
  <%= render "form", task: Task.new %>
<% end %>

<%= turbo_stream.update "tasks_count" do %>
  <%= current_account.tasks.count %>
<% end %>
```

---

## Broadcast Streams (Real-time)

```ruby
# app/models/task.rb
class Task < ApplicationRecord
  after_create_commit -> { broadcast_prepend_to "tasks" }
  after_update_commit -> { broadcast_replace_to "tasks" }
  after_destroy_commit -> { broadcast_remove_to "tasks" }

  # Or with custom stream name
  after_create_commit -> {
    broadcast_prepend_to [account, "tasks"],
                         target: "tasks_list",
                         partial: "tasks/task"
  }
end
```

```erb
<%# Subscribe to stream in view %>
<%= turbo_stream_from @account, "tasks" %>

<div id="tasks_list">
  <%= render @tasks %>
</div>
```

---

## Error Response Handling

```ruby
# app/controllers/concerns/turbo_streamable_errors.rb
module TurboStreamableErrors
  extend ActiveSupport::Concern

  included do
    rescue_from ActiveRecord::RecordNotFound, with: :handle_not_found
    rescue_from StandardError, with: :handle_error
  end

  private

  def handle_not_found(exception)
    respond_to do |format|
      format.turbo_stream {
        render turbo_stream: turbo_stream.replace(
          "flash",
          partial: "shared/flash",
          locals: { message: "Record not found", type: "error" }
        ), status: :not_found
      }
      format.html { redirect_to root_path, alert: "Record not found" }
    end
  end

  def handle_error(exception)
    Rails.logger.error(exception.message)

    respond_to do |format|
      format.turbo_stream {
        render turbo_stream: turbo_stream.replace(
          "flash",
          partial: "shared/flash",
          locals: { message: "An error occurred", type: "error" }
        ), status: :internal_server_error
      }
      format.html { redirect_to root_path, alert: "An error occurred" }
    end
  end
end
```

---

## Form Validation with Streams

```ruby
# app/controllers/tasks_controller.rb
def create
  @task = Task.new(task_params)

  respond_to do |format|
    if @task.save
      format.turbo_stream {
        render turbo_stream: [
          turbo_stream.prepend("tasks", partial: "tasks/task", locals: { task: @task }),
          turbo_stream.replace("task_form", partial: "tasks/form", locals: { task: Task.new })
        ]
      }
    else
      format.turbo_stream {
        render turbo_stream: turbo_stream.replace(
          "task_form",
          partial: "tasks/form",
          locals: { task: @task }
        ), status: :unprocessable_entity
      }
    end
  end
end
```

```erb
<!-- app/views/tasks/_form.html.erb -->
<%= turbo_frame_tag "task_form" do %>
  <%= form_with model: task do |f| %>
    <div class="field">
      <%= f.label :title %>
      <%= f.text_field :title, class: task.errors[:title].any? ? 'error' : '' %>
      <% if task.errors[:title].any? %>
        <span class="error-message"><%= task.errors[:title].first %></span>
      <% end %>
    </div>

    <%= f.submit %>
  <% end %>
<% end %>
```
