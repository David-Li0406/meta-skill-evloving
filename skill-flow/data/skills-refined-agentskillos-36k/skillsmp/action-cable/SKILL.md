---
name: action-cable
description: This skill should be used when the user asks about "WebSockets", "Action Cable", "real-time", "channels", "broadcasting", "streams", "subscriptions", "live updates", "push notifications", "chat features", or needs guidance on implementing real-time features in Rails applications.
version: 1.0.0
---

# Action Cable

Comprehensive guide to real-time WebSocket communication in Rails.

## Server Setup

### Connection

```ruby
# app/channels/application_cable/connection.rb
module ApplicationCable
  class Connection < ActionCable::Connection::Base
    identified_by :current_user

    def connect
      self.current_user = find_verified_user
    end

    private

    def find_verified_user
      if verified_user = User.find_by(id: cookies.encrypted[:user_id])
        verified_user
      else
        reject_unauthorized_connection
      end
    end
  end
end
```

### Channel Generator

```bash
rails generate channel Chat speak
```

Creates:
- `app/channels/chat_channel.rb`
- `app/javascript/channels/chat_channel.js`

## Channels

### Basic Channel

```ruby
# app/channels/chat_channel.rb
class ChatChannel < ApplicationCable::Channel
  def subscribed
    stream_from "chat_#{params[:room_id]}"
  end

  def unsubscribed
    # Cleanup when channel is unsubscribed
  end

  def speak(data)
    Message.create!(
      content: data["message"],
      user: current_user,
      room_id: params[:room_id]
    )
  end
end
```

### Stream Methods

```ruby
class NotificationsChannel < ApplicationCable::Channel
  def subscribed
    # Stream from string identifier
    stream_from "notifications_#{current_user.id}"

    # Stream for model (uses GlobalID)
    stream_for current_user
  end
end

# Broadcasting to stream_for
NotificationsChannel.broadcast_to(user, { type: "alert", message: "Hello!" })
```

### Rejecting Subscriptions

```ruby
class ChatChannel < ApplicationCable::Channel
  def subscribed
    room = Room.find(params[:room_id])

    if room.accessible_by?(current_user)
      stream_for room
    else
      reject
    end
  end
end
```

## Broadcasting

### From Models

```ruby
class Message < ApplicationRecord
  belongs_to :room
  belongs_to :user

  after_create_commit :broadcast_message

  private

  def broadcast_message
    ActionCable.server.broadcast(
      "chat_#{room_id}",
      { message: content, user: user.name, created_at: created_at }
    )
  end
end
```

### From Controllers

```ruby
class MessagesController < ApplicationController
  def create
    @message = current_user.messages.create!(message_params)

    ActionCable.server.broadcast(
      "chat_#{@message.room_id}",
      render_message(@message)
    )

    head :ok
  end

  private

  def render_message(message)
    ApplicationController.renderer.render(
      partial: "messages/message",
      locals: { message: message }
    )
  end
end
```

### From Jobs

```ruby
class BroadcastMessageJob < ApplicationJob
  queue_as :default

  def perform(message)
    ActionCable.server.broadcast(
      "chat_#{message.room_id}",
      message: render_message(message)
    )
  end

  private

  def render_message(message)
    MessagesController.render(
      partial: "messages/message",
      locals: { message: message }
    )
  end
end
```

### With Turbo Streams

```ruby
class Message < ApplicationRecord
  belongs_to :room
  after_create_commit { broadcast_append_to room }
  after_update_commit { broadcast_replace_to room }
  after_destroy_commit { broadcast_remove_to room }
end
```

## Client-Side (JavaScript)

### Subscription

```javascript
// app/javascript/channels/chat_channel.js
import consumer from "./consumer"

consumer.subscriptions.create(
  { channel: "ChatChannel", room_id: roomId },
  {
    connected() {
      console.log("Connected to chat")
    },

    disconnected() {
      console.log("Disconnected from chat")
    },

    received(data) {
      // Called when data is broadcast
      const messagesContainer = document.getElementById("messages")
      messagesContainer.insertAdjacentHTML("beforeend", data.message)
    },

    speak(message) {
      this.perform("speak", { message: message })
    }
  }
)
```

### Consumer Setup

```javascript
// app/javascript/channels/consumer.js
import { createConsumer } from "@rails/actioncable"

export default createConsumer()

// With custom URL
export default createConsumer("/cable")

// With authentication token
export default createConsumer(`/cable?token=${getToken()}`)
```

### Dynamic Subscriptions

```javascript
// Subscribe dynamically
const subscription = consumer.subscriptions.create(
  { channel: "ChatChannel", room_id: 123 },
  {
    received(data) {
      console.log(data)
    }
  }
)

// Unsubscribe
subscription.unsubscribe()

// Perform action
subscription.perform("speak", { message: "Hello" })
```

## Configuration

### Cable Configuration

```yaml
# config/cable.yml
development:
  adapter: async

test:
  adapter: test

production:
  adapter: redis
  url: <%= ENV.fetch("REDIS_URL") { "redis://localhost:6379/1" } %>
  channel_prefix: myapp_production
```

### Routes

```ruby
# config/routes.rb
Rails.application.routes.draw do
  mount ActionCable.server => "/cable"
end
```

### Allowed Origins

```ruby
# config/environments/production.rb
config.action_cable.allowed_request_origins = [
  "https://example.com",
  /https:\/\/.*\.example\.com/
]

# Or allow all (not recommended for production)
config.action_cable.disable_request_forgery_protection = true
```

### Redis Adapter

```ruby
# Gemfile
gem "redis"

# config/cable.yml
production:
  adapter: redis
  url: <%= ENV["REDIS_URL"] %>
  channel_prefix: myapp_production
```

## Common Patterns

### Presence Tracking

```ruby
class AppearanceChannel < ApplicationCable::Channel
  def subscribed
    stream_from "appearance_channel"
    current_user.appear
  end

  def unsubscribed
    current_user.disappear
  end

  def appear(data)
    current_user.appear(on: data["appearing_on"])
  end

  def away
    current_user.away
  end
end
```

### Typing Indicators

```ruby
class TypingChannel < ApplicationCable::Channel
  def subscribed
    stream_from "typing_#{params[:room_id]}"
  end

  def typing
    ActionCable.server.broadcast(
      "typing_#{params[:room_id]}",
      { user_id: current_user.id, name: current_user.name }
    )
  end

  def stopped_typing
    ActionCable.server.broadcast(
      "typing_#{params[:room_id]}",
      { user_id: current_user.id, stopped: true }
    )
  end
end
```

### Room-Based Chat

```ruby
class RoomChannel < ApplicationCable::Channel
  def subscribed
    @room = Room.find(params[:room_id])
    stream_for @room

    # Notify others user joined
    broadcast_user_joined
  end

  def unsubscribed
    broadcast_user_left if @room
  end

  def speak(data)
    message = @room.messages.create!(
      user: current_user,
      content: data["message"]
    )

    RoomChannel.broadcast_to(@room, {
      type: "message",
      message: render_message(message)
    })
  end

  private

  def broadcast_user_joined
    RoomChannel.broadcast_to(@room, {
      type: "user_joined",
      user: { id: current_user.id, name: current_user.name }
    })
  end

  def broadcast_user_left
    RoomChannel.broadcast_to(@room, {
      type: "user_left",
      user: { id: current_user.id }
    })
  end

  def render_message(message)
    ApplicationController.renderer.render(
      partial: "messages/message",
      locals: { message: message }
    )
  end
end
```

## Testing

### Channel Tests

```ruby
# test/channels/chat_channel_test.rb
require "test_helper"

class ChatChannelTest < ActionCable::Channel::TestCase
  test "subscribes to room stream" do
    subscribe room_id: 1

    assert subscription.confirmed?
    assert_has_stream "chat_1"
  end

  test "rejects without room_id" do
    subscribe

    assert subscription.rejected?
  end
end
```

### Connection Tests

```ruby
# test/channels/application_cable/connection_test.rb
require "test_helper"

class ApplicationCable::ConnectionTest < ActionCable::Connection::TestCase
  test "connects with valid user" do
    user = users(:one)
    cookies.encrypted[:user_id] = user.id

    connect

    assert_equal user, connection.current_user
  end

  test "rejects connection without user" do
    assert_reject_connection { connect }
  end
end
```

### Broadcast Tests

```ruby
# test/models/message_test.rb
require "test_helper"

class MessageTest < ActiveSupport::TestCase
  test "broadcasts on create" do
    room = rooms(:one)

    assert_broadcast_on("chat_#{room.id}", hash_including(message: "Hello")) do
      Message.create!(room: room, user: users(:one), content: "Hello")
    end
  end
end
```
