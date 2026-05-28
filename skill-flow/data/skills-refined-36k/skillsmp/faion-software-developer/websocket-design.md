---
id: websocket-design
name: "WebSocket Design"
domain: DEV
skill: faion-software-developer
category: "development"
---

# WebSocket Design

## Overview

WebSocket design involves implementing bidirectional, real-time communication between clients and servers. This methodology covers connection management, message protocols, scaling strategies, and handling reconnection scenarios.

## When to Use

- Real-time features: chat, notifications, live updates
- Collaborative applications: document editing, whiteboards
- Live data feeds: stock prices, sports scores, gaming
- Reducing polling overhead for frequently changing data
- Server-initiated communication requirements

## Key Principles

- **Connection lifecycle management**: Handle connect, disconnect, reconnect gracefully
- **Heartbeat mechanism**: Detect stale connections proactively
- **Message protocol design**: Structure messages for extensibility
- **Horizontal scaling**: Plan for multiple server instances
- **Graceful degradation**: Fallback to polling when WebSocket unavailable

## Best Practices

### WebSocket Server (FastAPI)

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.websockets import WebSocketState
from typing import Dict, Set, Optional
import asyncio
import json
from dataclasses import dataclass, asdict
from enum import Enum
import logging

class MessageType(str, Enum):
    PING = "ping"
    PONG = "pong"
    SUBSCRIBE = "subscribe"
    UNSUBSCRIBE = "unsubscribe"
    MESSAGE = "message"
    ERROR = "error"
    ACK = "ack"

@dataclass
class WSMessage:
    type: MessageType
    channel: Optional[str] = None
    data: Optional[dict] = None
    id: Optional[str] = None

    def to_json(self) -> str:
        return json.dumps({k: v for k, v in asdict(self).items() if v is not None})

class ConnectionManager:
    def __init__(self):
        # user_id -> WebSocket
        self.active_connections: Dict[str, WebSocket] = {}
        # channel -> Set[user_id]
        self.channel_subscriptions: Dict[str, Set[str]] = {}
        # user_id -> Set[channel]
        self.user_channels: Dict[str, Set[str]] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()

        # Disconnect existing connection for same user
        if user_id in self.active_connections:
            await self.disconnect(user_id)

        self.active_connections[user_id] = websocket
        self.user_channels[user_id] = set()
        logging.info(f"User {user_id} connected")

    async def disconnect(self, user_id: str):
        if user_id not in self.active_connections:
            return

        # Unsubscribe from all channels
        for channel in list(self.user_channels.get(user_id, [])):
            await self.unsubscribe(user_id, channel)

        # Close connection
        ws = self.active_connections.pop(user_id, None)
        self.user_channels.pop(user_id, None)

        if ws and ws.client_state == WebSocketState.CONNECTED:
            await ws.close()

        logging.info(f"User {user_id} disconnected")

    async def subscribe(self, user_id: str, channel: str):
        if channel not in self.channel_subscriptions:
            self.channel_subscriptions[channel] = set()

        self.channel_subscriptions[channel].add(user_id)
        self.user_channels[user_id].add(channel)

        await self.send_to_user(user_id, WSMessage(
            type=MessageType.ACK,
            channel=channel,
            data={"action": "subscribed"}
        ))

    async def unsubscribe(self, user_id: str, channel: str):
        if channel in self.channel_subscriptions:
            self.channel_subscriptions[channel].discard(user_id)
            if not self.channel_subscriptions[channel]:
                del self.channel_subscriptions[channel]

        if user_id in self.user_channels:
            self.user_channels[user_id].discard(channel)

    async def send_to_user(self, user_id: str, message: WSMessage):
        ws = self.active_connections.get(user_id)
        if ws and ws.client_state == WebSocketState.CONNECTED:
            try:
                await ws.send_text(message.to_json())
            except Exception as e:
                logging.error(f"Error sending to {user_id}: {e}")
                await self.disconnect(user_id)

    async def broadcast_to_channel(self, channel: str, message: WSMessage):
        subscribers = self.channel_subscriptions.get(channel, set())
        tasks = [
            self.send_to_user(user_id, message)
            for user_id in subscribers
        ]
        await asyncio.gather(*tasks, return_exceptions=True)

    async def broadcast_all(self, message: WSMessage):
        tasks = [
            self.send_to_user(user_id, message)
            for user_id in self.active_connections
        ]
        await asyncio.gather(*tasks, return_exceptions=True)

app = FastAPI()
manager = ConnectionManager()

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            msg_type = message.get("type")

            if msg_type == MessageType.PING:
                await manager.send_to_user(user_id, WSMessage(type=MessageType.PONG))

            elif msg_type == MessageType.SUBSCRIBE:
                channel = message.get("channel")
                if channel:
                    await manager.subscribe(user_id, channel)

            elif msg_type == MessageType.UNSUBSCRIBE:
                channel = message.get("channel")
                if channel:
                    await manager.unsubscribe(user_id, channel)

            elif msg_type == MessageType.MESSAGE:
                channel = message.get("channel")
                if channel:
                    await manager.broadcast_to_channel(channel, WSMessage(
                        type=MessageType.MESSAGE,
                        channel=channel,
                        data=message.get("data"),
                        id=message.get("id")
                    ))

    except WebSocketDisconnect:
        await manager.disconnect(user_id)
    except Exception as e:
        logging.error(f"WebSocket error for {user_id}: {e}")
        await manager.disconnect(user_id)
```

### Scaling with Redis Pub/Sub

```python
import redis.asyncio as redis
import asyncio
import json
from typing import Callable

class DistributedConnectionManager(ConnectionManager):
    """Connection manager that syncs across multiple server instances."""

    def __init__(self, redis_url: str = "redis://localhost:6379"):
        super().__init__()
        self.redis_url = redis_url
        self.redis: Optional[redis.Redis] = None
        self.pubsub: Optional[redis.client.PubSub] = None

    async def start(self):
        self.redis = await redis.from_url(self.redis_url)
        self.pubsub = self.redis.pubsub()
        asyncio.create_task(self._listen_to_redis())

    async def stop(self):
        if self.pubsub:
            await self.pubsub.close()
        if self.redis:
            await self.redis.close()

    async def _listen_to_redis(self):
        """Listen for messages from other server instances."""
        await self.pubsub.psubscribe("ws:channel:*")

        async for message in self.pubsub.listen():
            if message["type"] != "pmessage":
                continue

            channel = message["channel"].decode().replace("ws:channel:", "")
            data = json.loads(message["data"])

            # Deliver to local subscribers only
            await self._local_broadcast(channel, WSMessage(**data))

    async def _local_broadcast(self, channel: str, message: WSMessage):
        """Broadcast to subscribers connected to this instance."""
        subscribers = self.channel_subscriptions.get(channel, set())
        tasks = [
            self.send_to_user(user_id, message)
            for user_id in subscribers
            if user_id in self.active_connections
        ]
        await asyncio.gather(*tasks, return_exceptions=True)

    async def broadcast_to_channel(self, channel: str, message: WSMessage):
        """Broadcast via Redis to all server instances."""
        await self.redis.publish(
            f"ws:channel:{channel}",
            message.to_json()
        )

    async def subscribe(self, user_id: str, channel: str):
        await super().subscribe(user_id, channel)
        # Track subscription in Redis for cross-instance awareness
        await self.redis.sadd(f"ws:subscribers:{channel}", user_id)

    async def unsubscribe(self, user_id: str, channel: str):
        await super().unsubscribe(user_id, channel)
        await self.redis.srem(f"ws:subscribers:{channel}", user_id)
```

### Client Implementation (TypeScript)

```typescript
interface WSMessage {
  type: 'ping' | 'pong' | 'subscribe' | 'unsubscribe' | 'message' | 'error' | 'ack';
  channel?: string;
  data?: unknown;
  id?: string;
}

type MessageHandler = (message: WSMessage) => void;

class WebSocketClient {
  private ws: WebSocket | null = null;
  private url: string;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;
  private pingInterval: number | null = null;
  private handlers: Map<string, Set<MessageHandler>> = new Map();
  private messageQueue: WSMessage[] = [];
  private isConnected = false;

  constructor(url: string) {
    this.url = url;
  }

  connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(this.url);

      this.ws.onopen = () => {
        console.log('WebSocket connected');
        this.isConnected = true;
        this.reconnectAttempts = 0;
        this.startPingInterval();
        this.flushMessageQueue();
        resolve();
      };

      this.ws.onclose = (event) => {
        console.log('WebSocket closed:', event.code, event.reason);
        this.isConnected = false;
        this.stopPingInterval();
        this.handleReconnect();
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        reject(error);
      };

      this.ws.onmessage = (event) => {
        const message: WSMessage = JSON.parse(event.data);
        this.handleMessage(message);
      };
    });
  }

  private handleMessage(message: WSMessage) {
    if (message.type === 'pong') {
      return; // Heartbeat response
    }

    // Notify channel-specific handlers
    if (message.channel) {
      const handlers = this.handlers.get(message.channel);
      handlers?.forEach(handler => handler(message));
    }

    // Notify global handlers
    const globalHandlers = this.handlers.get('*');
    globalHandlers?.forEach(handler => handler(message));
  }

  private startPingInterval() {
    this.pingInterval = window.setInterval(() => {
      this.send({ type: 'ping' });
    }, 30000);
  }

  private stopPingInterval() {
    if (this.pingInterval) {
      clearInterval(this.pingInterval);
      this.pingInterval = null;
    }
  }

  private handleReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('Max reconnection attempts reached');
      return;
    }

    const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts);
    this.reconnectAttempts++;

    console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`);

    setTimeout(() => {
      this.connect().catch(console.error);
    }, delay);
  }

  private flushMessageQueue() {
    while (this.messageQueue.length > 0) {
      const message = this.messageQueue.shift();
      if (message) {
        this.send(message);
      }
    }
  }

  send(message: WSMessage) {
    if (this.isConnected && this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    } else {
      this.messageQueue.push(message);
    }
  }

  subscribe(channel: string, handler: MessageHandler) {
    if (!this.handlers.has(channel)) {
      this.handlers.set(channel, new Set());
    }
    this.handlers.get(channel)!.add(handler);

    this.send({ type: 'subscribe', channel });

    return () => {
      this.handlers.get(channel)?.delete(handler);
      if (this.handlers.get(channel)?.size === 0) {
        this.send({ type: 'unsubscribe', channel });
        this.handlers.delete(channel);
      }
    };
  }

  disconnect() {
    this.stopPingInterval();
    this.maxReconnectAttempts = 0; // Prevent reconnection
    this.ws?.close(1000, 'Client disconnect');
  }
}

// Usage
const ws = new WebSocketClient('wss://api.example.com/ws/user123');

await ws.connect();

const unsubscribe = ws.subscribe('chat:room-1', (message) => {
  console.log('Received:', message);
});

ws.send({
  type: 'message',
  channel: 'chat:room-1',
  data: { text: 'Hello!' }
});

// Later
unsubscribe();
ws.disconnect();
```

### Room-based Chat Implementation

```python
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class ChatMessage(BaseModel):
    room_id: str
    user_id: str
    username: str
    content: str
    timestamp: datetime = None

    def __init__(self, **data):
        if data.get('timestamp') is None:
            data['timestamp'] = datetime.utcnow()
        super().__init__(**data)

class ChatRoom:
    def __init__(self, room_id: str, manager: ConnectionManager):
        self.room_id = room_id
        self.manager = manager
        self.messages: list[ChatMessage] = []
        self.max_history = 100

    async def join(self, user_id: str):
        await self.manager.subscribe(user_id, f"chat:{self.room_id}")

        # Send recent history
        await self.manager.send_to_user(user_id, WSMessage(
            type=MessageType.MESSAGE,
            channel=f"chat:{self.room_id}",
            data={
                "action": "history",
                "messages": [m.dict() for m in self.messages[-50:]]
            }
        ))

    async def leave(self, user_id: str):
        await self.manager.unsubscribe(user_id, f"chat:{self.room_id}")

    async def send_message(self, message: ChatMessage):
        self.messages.append(message)
        if len(self.messages) > self.max_history:
            self.messages = self.messages[-self.max_history:]

        await self.manager.broadcast_to_channel(
            f"chat:{self.room_id}",
            WSMessage(
                type=MessageType.MESSAGE,
                channel=f"chat:{self.room_id}",
                data={
                    "action": "new_message",
                    "message": message.dict()
                }
            )
        )

# Room manager
class ChatRoomManager:
    def __init__(self, connection_manager: ConnectionManager):
        self.rooms: Dict[str, ChatRoom] = {}
        self.connection_manager = connection_manager

    def get_or_create_room(self, room_id: str) -> ChatRoom:
        if room_id not in self.rooms:
            self.rooms[room_id] = ChatRoom(room_id, self.connection_manager)
        return self.rooms[room_id]
```

## Anti-patterns

- **No heartbeat**: Stale connections consume resources
- **Unbounded connections**: No limit per user or globally
- **No authentication**: WebSocket upgrades should be authenticated
- **Large messages**: Consider chunking or using HTTP for large payloads
- **Blocking operations**: Async handlers should not block
- **No reconnection logic**: Clients must handle disconnections
- **Missing error handling**: Silent failures are hard to debug

## References

- [WebSocket API - MDN](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [FastAPI WebSockets](https://fastapi.tiangolo.com/advanced/websockets/)
- [Socket.io Documentation](https://socket.io/docs/v4/)
- [RFC 6455 - WebSocket Protocol](https://datatracker.ietf.org/doc/html/rfc6455)
