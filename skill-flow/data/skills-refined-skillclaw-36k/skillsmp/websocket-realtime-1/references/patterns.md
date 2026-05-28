# WebSocket & Real-time

## Patterns


---
  #### **Name**
Connection Lifecycle Management
  #### **Description**
    Properly handle the WebSocket connection states: connecting, open,
    closing, closed. Each state requires different handling.
    
  #### **Example**
    class WebSocketClient {
      private ws: WebSocket | null = null;
      private reconnectAttempts = 0;
      private maxReconnectAttempts = 5;
      private reconnectDelay = 1000;
    
      connect(url: string) {
        this.ws = new WebSocket(url);
    
        this.ws.onopen = () => {
          console.log('Connected');
          this.reconnectAttempts = 0;
          this.startHeartbeat();
        };
    
        this.ws.onclose = (event) => {
          this.stopHeartbeat();
          if (!event.wasClean) {
            this.scheduleReconnect();
          }
        };
    
        this.ws.onerror = (error) => {
          console.error('WebSocket error:', error);
        };
    
        this.ws.onmessage = (event) => {
          this.handleMessage(JSON.parse(event.data));
        };
      }
    
      private scheduleReconnect() {
        if (this.reconnectAttempts >= this.maxReconnectAttempts) {
          console.error('Max reconnect attempts reached');
          return;
        }
    
        const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts);
        this.reconnectAttempts++;
    
        setTimeout(() => this.connect(this.url), delay);
      }
    }
    
  #### **When**
Any WebSocket implementation

---
  #### **Name**
Heartbeat/Ping-Pong
  #### **Description**
    Keep connections alive and detect stale connections with periodic
    heartbeats. Essential for detecting zombie connections.
    
  #### **Example**
    // Server-side (Node.js with ws)
    const wss = new WebSocket.Server({ port: 8080 });
    
    wss.on('connection', (ws) => {
      ws.isAlive = true;
    
      ws.on('pong', () => {
        ws.isAlive = true;
      });
    });
    
    // Ping all clients every 30 seconds
    const interval = setInterval(() => {
      wss.clients.forEach((ws) => {
        if (!ws.isAlive) {
          return ws.terminate();
        }
        ws.isAlive = false;
        ws.ping();
      });
    }, 30000);
    
    wss.on('close', () => {
      clearInterval(interval);
    });
    
    // Client-side custom heartbeat
    class HeartbeatClient {
      private heartbeatInterval: number | null = null;
      private missedHeartbeats = 0;
      private maxMissedHeartbeats = 3;
    
      startHeartbeat() {
        this.heartbeatInterval = setInterval(() => {
          if (this.missedHeartbeats >= this.maxMissedHeartbeats) {
            this.ws.close();
            return;
          }
    
          this.missedHeartbeats++;
          this.send({ type: 'ping' });
        }, 10000);
      }
    
      handleMessage(msg) {
        if (msg.type === 'pong') {
          this.missedHeartbeats = 0;
        }
      }
    }
    
  #### **When**
Any persistent WebSocket connection

---
  #### **Name**
Room/Channel Management
  #### **Description**
    Organize connections into rooms or channels for targeted broadcasting.
    Users subscribe to specific topics and receive only relevant messages.
    
  #### **Example**
    // Socket.IO room management
    io.on('connection', (socket) => {
      // Join a room
      socket.on('join', (roomId) => {
        socket.join(roomId);
        socket.to(roomId).emit('user-joined', socket.id);
      });
    
      // Leave a room
      socket.on('leave', (roomId) => {
        socket.leave(roomId);
        socket.to(roomId).emit('user-left', socket.id);
      });
    
      // Send to specific room
      socket.on('message', ({ roomId, content }) => {
        io.to(roomId).emit('message', {
          sender: socket.id,
          content,
          timestamp: Date.now()
        });
      });
    });
    
    // Custom room implementation
    class RoomManager {
      private rooms = new Map<string, Set<WebSocket>>();
    
      join(roomId: string, ws: WebSocket) {
        if (!this.rooms.has(roomId)) {
          this.rooms.set(roomId, new Set());
        }
        this.rooms.get(roomId)!.add(ws);
      }
    
      leave(roomId: string, ws: WebSocket) {
        this.rooms.get(roomId)?.delete(ws);
      }
    
      broadcast(roomId: string, message: any, exclude?: WebSocket) {
        const room = this.rooms.get(roomId);
        if (!room) return;
    
        const data = JSON.stringify(message);
        room.forEach((ws) => {
          if (ws !== exclude && ws.readyState === WebSocket.OPEN) {
            ws.send(data);
          }
        });
      }
    }
    
  #### **When**
Multi-user features, chat rooms, collaborative editing

---
  #### **Name**
Message Protocol Design
  #### **Description**
    Define a clear message format with types, payloads, and optional
    request/response correlation for bidirectional communication.
    
  #### **Example**
    // Message envelope structure
    interface Message<T = unknown> {
      type: string;           // Message type for routing
      id?: string;            // Correlation ID for request/response
      payload: T;             // Actual data
      timestamp: number;      // Server timestamp
      version?: number;       // Protocol version
    }
    
    // Message types
    type ClientMessage =
      | { type: 'subscribe'; payload: { channel: string } }
      | { type: 'unsubscribe'; payload: { channel: string } }
      | { type: 'message'; payload: { channel: string; content: string } }
      | { type: 'ping'; payload: {} };
    
    type ServerMessage =
      | { type: 'subscribed'; payload: { channel: string } }
      | { type: 'message'; payload: { channel: string; content: string; sender: string } }
      | { type: 'presence'; payload: { channel: string; users: string[] } }
      | { type: 'error'; payload: { code: string; message: string } }
      | { type: 'pong'; payload: {} };
    
    // Server message handler
    function handleMessage(ws: WebSocket, raw: string) {
      let message: ClientMessage;
      try {
        message = JSON.parse(raw);
      } catch {
        ws.send(JSON.stringify({
          type: 'error',
          payload: { code: 'INVALID_JSON', message: 'Invalid JSON' }
        }));
        return;
      }
    
      switch (message.type) {
        case 'subscribe':
          handleSubscribe(ws, message.payload);
          break;
        case 'message':
          handleChatMessage(ws, message.payload);
          break;
        // ...
      }
    }
    
  #### **When**
Any WebSocket application

---
  #### **Name**
Presence System
  #### **Description**
    Track online/offline status of users with proper handling of
    disconnections, reconnections, and stale sessions.
    
  #### **Example**
    class PresenceManager {
      private presence = new Map<string, {
        status: 'online' | 'away' | 'offline';
        lastSeen: number;
        connections: Set<string>;
      }>();
    
      private cleanupInterval: NodeJS.Timer;
    
      constructor() {
        // Clean up stale presence every minute
        this.cleanupInterval = setInterval(
          () => this.cleanupStale(),
          60000
        );
      }
    
      connect(userId: string, connectionId: string) {
        if (!this.presence.has(userId)) {
          this.presence.set(userId, {
            status: 'online',
            lastSeen: Date.now(),
            connections: new Set()
          });
        }
    
        const user = this.presence.get(userId)!;
        user.connections.add(connectionId);
        user.status = 'online';
        user.lastSeen = Date.now();
    
        this.broadcastPresence(userId);
      }
    
      disconnect(userId: string, connectionId: string) {
        const user = this.presence.get(userId);
        if (!user) return;
    
        user.connections.delete(connectionId);
    
        // User still has other connections
        if (user.connections.size > 0) {
          return;
        }
    
        // Delay offline status for reconnection window
        setTimeout(() => {
          const current = this.presence.get(userId);
          if (current && current.connections.size === 0) {
            current.status = 'offline';
            this.broadcastPresence(userId);
          }
        }, 5000);
      }
    
      private cleanupStale() {
        const staleThreshold = Date.now() - 5 * 60 * 1000; // 5 minutes
    
        this.presence.forEach((user, userId) => {
          if (user.lastSeen < staleThreshold && user.connections.size === 0) {
            this.presence.delete(userId);
          }
        });
      }
    }
    
  #### **When**
User online status, typing indicators, collaborative features

---
  #### **Name**
Server-Sent Events (SSE)
  #### **Description**
    Use SSE for server-to-client unidirectional streaming. Simpler than
    WebSocket when you don't need client-to-server messages.
    
  #### **Example**
    // Server (Express)
    app.get('/events', (req, res) => {
      res.setHeader('Content-Type', 'text/event-stream');
      res.setHeader('Cache-Control', 'no-cache');
      res.setHeader('Connection', 'keep-alive');
    
      // Send initial data
      res.write(`data: ${JSON.stringify({ type: 'connected' })}\n\n`);
    
      // Keep connection alive
      const heartbeat = setInterval(() => {
        res.write(': heartbeat\n\n');
      }, 30000);
    
      // Subscribe to events
      const handler = (event: any) => {
        res.write(`event: ${event.type}\n`);
        res.write(`data: ${JSON.stringify(event.data)}\n\n`);
      };
    
      eventEmitter.on('notification', handler);
    
      // Cleanup on disconnect
      req.on('close', () => {
        clearInterval(heartbeat);
        eventEmitter.off('notification', handler);
      });
    });
    
    // Client
    const eventSource = new EventSource('/events');
    
    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log('Message:', data);
    };
    
    eventSource.addEventListener('notification', (event) => {
      const data = JSON.parse(event.data);
      showNotification(data);
    });
    
    eventSource.onerror = () => {
      console.log('SSE connection error, will auto-reconnect');
    };
    
  #### **When**
Notifications, live feeds, one-way data streaming

---
  #### **Name**
Scaling with Redis Pub/Sub
  #### **Description**
    Scale WebSocket servers horizontally using Redis for cross-instance
    message broadcasting.
    
  #### **Example**
    import Redis from 'ioredis';
    
    const pub = new Redis();
    const sub = new Redis();
    
    class ScalableWebSocketServer {
      private wss: WebSocket.Server;
      private channels = new Map<string, Set<WebSocket>>();
    
      constructor(port: number) {
        this.wss = new WebSocket.Server({ port });
    
        // Subscribe to Redis channels
        sub.psubscribe('channel:*');
        sub.on('pmessage', (pattern, channel, message) => {
          const channelName = channel.replace('channel:', '');
          this.localBroadcast(channelName, JSON.parse(message));
        });
    
        this.wss.on('connection', (ws) => {
          ws.on('message', (raw) => {
            const msg = JSON.parse(raw.toString());
            this.handleMessage(ws, msg);
          });
        });
      }
    
      subscribe(ws: WebSocket, channel: string) {
        if (!this.channels.has(channel)) {
          this.channels.set(channel, new Set());
        }
        this.channels.get(channel)!.add(ws);
      }
    
      // Broadcast via Redis to all instances
      broadcast(channel: string, message: any) {
        pub.publish(`channel:${channel}`, JSON.stringify(message));
      }
    
      // Local broadcast to connections on this instance
      private localBroadcast(channel: string, message: any) {
        const subs = this.channels.get(channel);
        if (!subs) return;
    
        const data = JSON.stringify(message);
        subs.forEach((ws) => {
          if (ws.readyState === WebSocket.OPEN) {
            ws.send(data);
          }
        });
      }
    }
    
  #### **When**
Multiple server instances, horizontal scaling

---
  #### **Name**
Optimistic Updates with Reconciliation
  #### **Description**
    Apply changes immediately on client, then reconcile with server
    response. Handle conflicts gracefully.
    
  #### **Example**
    class RealtimeDocument {
      private localVersion = 0;
      private serverVersion = 0;
      private pendingChanges: Change[] = [];
    
      applyLocalChange(change: Change) {
        // Apply immediately
        this.localVersion++;
        change.localVersion = this.localVersion;
    
        this.applyChange(change);
        this.pendingChanges.push(change);
    
        // Send to server
        this.ws.send(JSON.stringify({
          type: 'change',
          payload: change,
          baseVersion: this.serverVersion
        }));
      }
    
      handleServerMessage(msg: ServerMessage) {
        if (msg.type === 'change-accepted') {
          // Remove from pending
          this.pendingChanges = this.pendingChanges.filter(
            c => c.localVersion !== msg.localVersion
          );
          this.serverVersion = msg.serverVersion;
        }
    
        if (msg.type === 'change-rejected') {
          // Rollback and replay
          this.rollbackToServerState(msg.serverState);
          this.replayPendingChanges();
        }
    
        if (msg.type === 'remote-change') {
          // Transform pending changes against remote
          this.pendingChanges = this.pendingChanges.map(
            c => this.transform(c, msg.change)
          );
    
          // Apply remote change
          this.applyChange(msg.change);
          this.serverVersion = msg.serverVersion;
        }
      }
    }
    
  #### **When**
Collaborative editing, real-time sync with conflict resolution

## Anti-Patterns


---
  #### **Name**
No Reconnection Strategy
  #### **Description**
Not handling connection drops and not implementing reconnection
  #### **Why**
    WebSocket connections WILL drop. Mobile networks, laptop sleep, server
    restarts, load balancer timeouts - all cause disconnections. Without
    reconnection, users see a broken app.
    
  #### **Instead**
    Implement exponential backoff reconnection:
    - Start with short delay (1s)
    - Double delay on each attempt (2s, 4s, 8s...)
    - Cap at max delay (30s)
    - Reset on successful connection
    - Show connection status to user
    

---
  #### **Name**
Unbounded Message Buffers
  #### **Description**
Queueing messages without limits when connection is down
  #### **Why**
    If connection drops and you buffer all messages, memory grows unbounded.
    When connection restores, sending all buffered messages can overwhelm
    server or cause stale data issues.
    
  #### **Instead**
    - Set max buffer size
    - Drop oldest messages when full
    - Consider which messages are time-sensitive
    - Maybe just resync state on reconnection instead of replaying
    

---
  #### **Name**
No Message Validation
  #### **Description**
Trusting client messages without validation
  #### **Why**
    Clients can send anything. Malformed JSON, wrong types, malicious
    payloads. Trusting client input causes crashes and security issues.
    
  #### **Instead**
    Validate every message:
    - Parse JSON in try/catch
    - Validate message schema (Zod, Joi)
    - Authenticate message sender
    - Rate limit per connection
    - Sanitize any user-generated content
    

---
  #### **Name**
Blocking Event Loop
  #### **Description**
Doing heavy work in WebSocket message handlers
  #### **Why**
    Node.js event loop is single-threaded. Heavy computation in message
    handlers blocks all connections. Latency spikes, timeouts, dropped
    connections.
    
  #### **Instead**
    Keep handlers fast:
    - Offload heavy work to worker threads
    - Use message queues for processing
    - Respond immediately, process async
    - Set reasonable timeouts
    

---
  #### **Name**
No Heartbeat
  #### **Description**
Relying on TCP keepalive alone to detect dead connections
  #### **Why**
    TCP keepalive is too slow and unreliable. Proxies and load balancers
    may not forward keepalives. Dead connections stay "open" for minutes.
    
  #### **Instead**
    Implement application-level heartbeat:
    - Server pings clients every 30s
    - Client responds with pong
    - Close connections that miss 2-3 heartbeats
    - Client can also ping server
    

---
  #### **Name**
Broadcasting to All Connections
  #### **Description**
Sending every message to every connected client
  #### **Why**
    Doesn't scale. With 10,000 connections, every message causes 10,000
    sends. Server CPU spikes, clients get irrelevant messages.
    
  #### **Instead**
    Use rooms/channels:
    - Clients subscribe to relevant channels
    - Broadcast only to channel subscribers
    - Use pub/sub for multi-server broadcast
    - Consider message filtering server-side
    