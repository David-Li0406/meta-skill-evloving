# Advanced Turbo Streams Patterns

## Broadcasting Strategies

### Direct Model Broadcasts

```ruby
# app/models/message.rb
class Message < ApplicationRecord
  belongs_to :conversation

  # Broadcast to conversation stream
  after_create_commit -> {
    broadcast_append_to conversation,
      target: "messages",
      partial: "messages/message"
  }

  after_update_commit -> {
    broadcast_replace_to conversation
  }

  after_destroy_commit -> {
    broadcast_remove_to conversation
  }
end
```

### Custom Stream Names

```ruby
# Broadcast to user-specific stream
class Notification < ApplicationRecord
  belongs_to :user

  after_create_commit -> {
    broadcast_append_to "notifications_#{user_id}",
      target: "notifications",
      partial: "notifications/notification"
  }
end
```

```erb
<!-- Subscribe to user's notification stream -->
<%= turbo_stream_from "notifications_#{current_user.id}" %>
```

### Conditional Broadcasting

```ruby
class Comment < ApplicationRecord
  after_create_commit :broadcast_comment

  private

  def broadcast_comment
    # Only broadcast public comments
    return unless public?

    broadcast_append_to commentable,
      target: "comments",
      partial: "comments/comment"
  end
end
```

### Multiple Target Broadcasting

```ruby
class Order < ApplicationRecord
  after_update_commit :broadcast_status_change, if: :saved_change_to_status?

  private

  def broadcast_status_change
    # Update order on customer's page
    broadcast_replace_to self

    # Update admin dashboard
    broadcast_replace_to "admin_orders",
      target: dom_id(self, :admin),
      partial: "admin/orders/order_row"

    # Update counters
    broadcast_update_to "admin_dashboard",
      target: "pending_orders_count",
      html: Order.pending.count.to_s
  end
end
```

## Complex UI Updates

### Multiple DOM Operations

```ruby
# app/controllers/comments_controller.rb
def create
  @comment = @article.comments.build(comment_params)

  if @comment.save
    respond_to do |format|
      format.turbo_stream do
        render turbo_stream: [
          # Add comment to list
          turbo_stream.append("comments", partial: "comments/comment", locals: { comment: @comment }),

          # Update comment count
          turbo_stream.update("comment_count", @article.comments.count),

          # Reset form
          turbo_stream.replace("new_comment", partial: "comments/form", locals: { comment: Comment.new }),

          # Show flash message
          turbo_stream.prepend("flash", partial: "shared/flash", locals: { message: "Comment added!" }),

          # Hide empty state if first comment
          (@article.comments.count == 1 ? turbo_stream.remove("no_comments") : nil)
        ].compact
      end
      format.html { redirect_to @article }
    end
  else
    respond_to do |format|
      format.turbo_stream do
        render turbo_stream: turbo_stream.replace(
          "new_comment",
          partial: "comments/form",
          locals: { comment: @comment }
        )
      end
      format.html { render :new }
    end
  end
end
```

### Updating Multiple Frames

```erb
<!-- app/views/tasks/update.turbo_stream.erb -->

<%# Update the task in the list %>
<%= turbo_stream.replace @task %>

<%# Update the sidebar counter %>
<%= turbo_stream.update "tasks_count" do %>
  <%= pluralize(@project.tasks.incomplete.count, "task") %> remaining
<% end %>

<%# Update the progress bar %>
<%= turbo_stream.update "progress_bar" do %>
  <%= render "projects/progress_bar", project: @project %>
<% end %>

<%# Optionally show completion message %>
<% if @project.tasks.incomplete.empty? %>
  <%= turbo_stream.append "notifications" do %>
    <%= render "shared/toast", message: "All tasks complete!" %>
  <% end %>
<% end %>
```

## Real-Time Features

### Chat Application

```ruby
# app/models/message.rb
class Message < ApplicationRecord
  belongs_to :conversation
  belongs_to :sender, class_name: "User"

  after_create_commit :broadcast_message

  private

  def broadcast_message
    conversation.participants.each do |user|
      broadcast_append_to "conversation_#{conversation.id}_user_#{user.id}",
        target: "messages",
        partial: "messages/message",
        locals: { message: self, current_user: user }
    end
  end
end
```

```erb
<!-- app/views/conversations/show.html.erb -->
<%= turbo_stream_from "conversation_#{@conversation.id}_user_#{current_user.id}" %>

<div id="messages" class="flex flex-col space-y-2">
  <%= render @conversation.messages, current_user: current_user %>
</div>
```

### Live Notifications

```ruby
# app/services/notification_service.rb
class NotificationService
  def self.notify(user, message, type: :info)
    Turbo::StreamsChannel.broadcast_append_to(
      "notifications_#{user.id}",
      target: "notifications",
      partial: "notifications/toast",
      locals: { message: message, type: type }
    )
  end
end

# Usage anywhere in app
NotificationService.notify(user, "Your export is ready!", type: :success)
```

### Live Dashboard

```ruby
# app/jobs/dashboard_update_job.rb
class DashboardUpdateJob < ApplicationJob
  def perform
    stats = calculate_stats

    Turbo::StreamsChannel.broadcast_update_to(
      "admin_dashboard",
      target: "live_stats",
      partial: "admin/dashboard/stats",
      locals: { stats: stats }
    )
  end

  private

  def calculate_stats
    {
      active_users: User.active.count,
      orders_today: Order.today.count,
      revenue_today: Order.today.sum(:total)
    }
  end
end

# Schedule every minute with your job scheduler
```

## Error Handling

### Handling Failed Broadcasts

```ruby
class Message < ApplicationRecord
  after_create_commit :broadcast_with_retry

  private

  def broadcast_with_retry
    broadcast_append_to conversation,
      target: "messages",
      partial: "messages/message"
  rescue StandardError => e
    Rails.logger.error "Broadcast failed: #{e.message}"
    # Optionally retry later
    BroadcastRetryJob.set(wait: 5.seconds).perform_later(self.id)
  end
end
```

### Graceful Degradation

```ruby
# app/controllers/comments_controller.rb
def create
  @comment = @article.comments.build(comment_params)

  if @comment.save
    respond_to do |format|
      format.turbo_stream
      format.html { redirect_to @article, notice: "Comment added" }
    end
  else
    respond_to do |format|
      format.turbo_stream do
        render turbo_stream: turbo_stream.replace(
          "new_comment",
          partial: "comments/form",
          locals: { comment: @comment }
        ), status: :unprocessable_entity
      end
      format.html { render :new, status: :unprocessable_entity }
    end
  end
end
```

## Performance Considerations

### Debouncing Broadcasts

```ruby
class StockPrice < ApplicationRecord
  after_save :schedule_broadcast

  private

  def schedule_broadcast
    # Debounce: only broadcast once per second
    Rails.cache.fetch("stock_broadcast_#{symbol}", expires_in: 1.second) do
      broadcast_update_to "stock_#{symbol}",
        target: "price_#{symbol}",
        html: price.to_s
      true
    end
  end
end
```

### Batching Updates

```ruby
# Instead of broadcasting for each item
items.each { |item| item.broadcast_update }

# Batch into single broadcast
Turbo::StreamsChannel.broadcast_update_to(
  "inventory",
  target: "items_table",
  partial: "items/table",
  locals: { items: items }
)
```

### Using Morph for Large Updates

```erb
<!-- Use morphing for complex DOM updates -->
<%= turbo_stream.replace "complex_list", method: :morph do %>
  <%= render @items %>
<% end %>
```

## Custom Turbo Stream Actions

```javascript
// app/javascript/application.js
import { Turbo } from "@hotwired/turbo-rails"

// Custom action: redirect
Turbo.StreamActions.redirect = function() {
  Turbo.visit(this.getAttribute("url"))
}

// Custom action: scroll_to
Turbo.StreamActions.scroll_to = function() {
  const target = document.getElementById(this.getAttribute("target"))
  target?.scrollIntoView({ behavior: "smooth" })
}
```

```ruby
# Usage in controller
render turbo_stream: turbo_stream.action(:redirect, url: dashboard_path)
render turbo_stream: turbo_stream.action(:scroll_to, target: "new_comment")
```
