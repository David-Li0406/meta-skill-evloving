# Presence Tracking Implementation

Complete presence tracking with Action Cable and Redis.

## Presence Channel

```ruby
# app/channels/presence_channel.rb
class PresenceChannel < ApplicationCable::Channel
  def subscribed
    reject unless current_user

    @room_id = params[:room_id]
    stream_from "presence_room_#{@room_id}"

    add_user_to_room
  end

  def unsubscribed
    remove_user_from_room
  end

  def heartbeat
    # Client sends periodic heartbeat to indicate still active
    Redis.current.setex(
      "presence:user:#{current_user.id}:room:#{@room_id}",
      30, # 30 second TTL
      Time.current.to_i
    )
  end

  private

  def add_user_to_room
    Redis.current.sadd("room:#{@room_id}:members", current_user.id)

    broadcast_presence_change('user_joined')
  end

  def remove_user_from_room
    Redis.current.srem("room:#{@room_id}:members", current_user.id)
    Redis.current.del("presence:user:#{current_user.id}:room:#{@room_id}")

    broadcast_presence_change('user_left')
  end

  def broadcast_presence_change(action)
    ActionCable.server.broadcast(
      "presence_room_#{@room_id}",
      action: action,
      user: current_user.as_json(only: [:id, :name, :avatar_url]),
      member_ids: room_member_ids,
      member_count: room_member_count
    )
  end

  def room_member_ids
    Redis.current.smembers("room:#{@room_id}:members").map(&:to_i)
  end

  def room_member_count
    Redis.current.scard("room:#{@room_id}:members")
  end
end
```

## Presence Service

```ruby
# app/services/presence_service.rb
class PresenceService
  class << self
    def online_users(room_id)
      member_ids = Redis.current.smembers("room:#{room_id}:members")
      User.where(id: member_ids)
    end

    def user_online?(user, room_id)
      Redis.current.sismember("room:#{room_id}:members", user.id)
    end

    def mark_online(user, room_id = 'global')
      Redis.current.sadd("room:#{room_id}:members", user.id)
      Redis.current.setex("user:#{user.id}:last_seen", 300, Time.current.to_i)
    end

    def mark_offline(user, room_id = 'global')
      Redis.current.srem("room:#{room_id}:members", user.id)
    end

    def cleanup_stale_presence(room_id)
      # Run periodically via Sidekiq
      member_ids = Redis.current.smembers("room:#{room_id}:members")

      member_ids.each do |user_id|
        heartbeat_key = "presence:user:#{user_id}:room:#{room_id}"

        unless Redis.current.exists?(heartbeat_key)
          Redis.current.srem("room:#{room_id}:members", user_id)
        end
      end
    end
  end
end
```

## Cleanup Job

```ruby
# app/jobs/cleanup_stale_presence_job.rb
class CleanupStalePresenceJob < ApplicationJob
  queue_as :low

  def perform
    Room.active.find_each do |room|
      PresenceService.cleanup_stale_presence(room.id)
    end
  end
end

# Schedule with sidekiq-cron or whenever gem
# Every minute: CleanupStalePresenceJob.perform_later
```

## JavaScript Client

```javascript
// app/javascript/controllers/presence_controller.js
import { Controller } from "@hotwired/stimulus"
import consumer from "../channels/consumer"

export default class extends Controller {
  static targets = ["memberList", "memberCount"]
  static values = { roomId: Number }

  connect() {
    this.subscription = consumer.subscriptions.create(
      { channel: "PresenceChannel", room_id: this.roomIdValue },
      {
        connected: () => this.startHeartbeat(),
        disconnected: () => this.stopHeartbeat(),
        received: this.handlePresenceUpdate.bind(this)
      }
    )
  }

  disconnect() {
    this.stopHeartbeat()
    this.subscription?.unsubscribe()
  }

  startHeartbeat() {
    this.heartbeatInterval = setInterval(() => {
      this.subscription.perform('heartbeat')
    }, 15000) // Every 15 seconds
  }

  stopHeartbeat() {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval)
    }
  }

  handlePresenceUpdate(data) {
    switch(data.action) {
      case 'user_joined':
        this.addMember(data.user)
        break
      case 'user_left':
        this.removeMember(data.user.id)
        break
    }

    this.updateMemberCount(data.member_count)
  }

  addMember(user) {
    if (!this.memberListTarget.querySelector(`[data-user-id="${user.id}"]`)) {
      this.memberListTarget.insertAdjacentHTML('beforeend', `
        <div data-user-id="${user.id}" class="member">
          <img src="${user.avatar_url}" alt="${user.name}">
          <span>${user.name}</span>
        </div>
      `)
    }
  }

  removeMember(userId) {
    this.memberListTarget.querySelector(`[data-user-id="${userId}"]`)?.remove()
  }

  updateMemberCount(count) {
    this.memberCountTarget.textContent = count
  }
}
```

## View Template

```erb
<div data-controller="presence"
     data-presence-room-id-value="<%= @room.id %>">

  <div class="member-header">
    <span data-presence-target="memberCount">0</span> online
  </div>

  <div data-presence-target="memberList" class="member-list">
    <%# Members will be added dynamically %>
  </div>
</div>
```
