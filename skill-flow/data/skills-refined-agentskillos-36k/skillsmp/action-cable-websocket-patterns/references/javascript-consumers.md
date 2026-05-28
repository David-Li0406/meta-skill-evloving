# JavaScript Action Cable Consumer Patterns

## Consumer Setup

```javascript
// app/javascript/channels/consumer.js
import { createConsumer } from "@rails/actioncable"

export default createConsumer()
```

## Basic Channel Subscription

```javascript
// app/javascript/channels/notifications_channel.js
import consumer from "./consumer"

consumer.subscriptions.create("NotificationsChannel", {
  connected() {
    console.log("Connected to notifications channel")
  },

  disconnected() {
    console.log("Disconnected from notifications channel")
  },

  received(data) {
    console.log("Received:", data)

    switch(data.action) {
      case 'notification_created':
        this.showNotification(data.notification)
        this.updateBadge(data.unread_count)
        break
      case 'count_updated':
        this.updateBadge(data.unread_count)
        break
    }
  },

  // Client-initiated actions
  markAsRead(notificationId) {
    this.perform('mark_as_read', { id: notificationId })
  },

  showNotification(notification) {
    // Display notification in UI
  },

  updateBadge(count) {
    // Update unread count badge
  }
})
```

## Parametrized Channels

```javascript
// app/javascript/channels/chat_channel.js
import consumer from "./consumer"

const roomId = document.getElementById('room-id').value

consumer.subscriptions.create({ channel: "ChatChannel", room_id: roomId }, {
  received(data) {
    if (data.action === 'new_message') {
      this.appendMessage(data.message)
    }
  },

  speak(message) {
    this.perform('speak', { text: message })
  },

  appendMessage(message) {
    const messagesEl = document.getElementById('messages')
    messagesEl.insertAdjacentHTML('beforeend', `
      <div class="message">
        <strong>${message.user.name}:</strong> ${message.text}
      </div>
    `)
  }
})
```

## React Integration

```javascript
// hooks/useActionCable.js
import { useEffect, useRef, useCallback } from 'react'
import consumer from '../channels/consumer'

export function useChannel(channelName, params = {}) {
  const subscriptionRef = useRef(null)
  const handlersRef = useRef({})

  useEffect(() => {
    subscriptionRef.current = consumer.subscriptions.create(
      { channel: channelName, ...params },
      {
        received(data) {
          const handler = handlersRef.current[data.action]
          if (handler) handler(data)
        }
      }
    )

    return () => {
      subscriptionRef.current?.unsubscribe()
    }
  }, [channelName, JSON.stringify(params)])

  const on = useCallback((action, handler) => {
    handlersRef.current[action] = handler
  }, [])

  const perform = useCallback((action, data) => {
    subscriptionRef.current?.perform(action, data)
  }, [])

  return { on, perform }
}

// Usage
function ChatRoom({ roomId }) {
  const { on, perform } = useChannel('ChatChannel', { room_id: roomId })

  useEffect(() => {
    on('new_message', (data) => {
      setMessages(prev => [...prev, data.message])
    })
  }, [on])

  const sendMessage = (text) => {
    perform('speak', { text })
  }
}
```

## Stimulus Controller Integration

```javascript
// app/javascript/controllers/chat_controller.js
import { Controller } from "@hotwired/stimulus"
import consumer from "../channels/consumer"

export default class extends Controller {
  static targets = ["messages", "input"]
  static values = { roomId: Number }

  connect() {
    this.subscription = consumer.subscriptions.create(
      { channel: "ChatChannel", room_id: this.roomIdValue },
      {
        received: this.handleReceived.bind(this)
      }
    )
  }

  disconnect() {
    this.subscription?.unsubscribe()
  }

  handleReceived(data) {
    if (data.action === 'new_message') {
      this.appendMessage(data.message)
    }
  }

  send() {
    const text = this.inputTarget.value
    this.subscription.perform('speak', { text })
    this.inputTarget.value = ''
  }

  appendMessage(message) {
    this.messagesTarget.insertAdjacentHTML('beforeend', `
      <div class="message">${message.text}</div>
    `)
  }
}
```

## Token-Based Authentication

```javascript
// For API clients or mobile apps
import { createConsumer } from "@rails/actioncable"

const token = localStorage.getItem('auth_token')
const consumer = createConsumer(`wss://example.com/cable?token=${token}`)

export default consumer
```
