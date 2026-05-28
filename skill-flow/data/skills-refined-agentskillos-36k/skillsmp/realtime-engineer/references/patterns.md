# Realtime Engineer

## Patterns


---
  #### **Name**
Exponential Backoff with Jitter
  #### **Description**
Reconnection strategy that prevents thundering herd
  #### **When**
Implementing WebSocket reconnection after disconnect
  #### **Example**
    class ReconnectingWebSocket {
      private attempt = 0;
      private maxDelay = 30000;
      private baseDelay = 1000;
    
      private getDelay(): number {
        // Exponential backoff: 1s, 2s, 4s, 8s, 16s, 30s (capped)
        const exponential = Math.min(
          this.maxDelay,
          this.baseDelay * Math.pow(2, this.attempt)
        );
    
        // Add jitter (0-30%) to prevent thundering herd
        const jitter = exponential * 0.3 * Math.random();
    
        return exponential + jitter;
      }
    
      async reconnect(): Promise<void> {
        while (true) {
          try {
            await this.connect();
            this.attempt = 0;  // Reset on success
            return;
          } catch (error) {
            this.attempt++;
            const delay = this.getDelay();
            console.log(`Reconnecting in ${delay}ms (attempt ${this.attempt})`);
            await sleep(delay);
          }
        }
      }
    }
    

---
  #### **Name**
Heartbeat with Server Confirmation
  #### **Description**
Detect dead connections before TCP timeout
  #### **When**
Need faster detection of disconnected clients
  #### **Example**
    // Client side
    class HeartbeatClient {
      private ws: WebSocket;
      private pingInterval: number;
      private pongTimeout: number;
      private missedPongs = 0;
    
      startHeartbeat() {
        this.pingInterval = setInterval(() => {
          if (this.missedPongs >= 3) {
            console.log('Connection dead - 3 missed pongs');
            this.reconnect();
            return;
          }
    
          this.ws.send(JSON.stringify({ type: 'ping', ts: Date.now() }));
          this.missedPongs++;
    
          // Expect pong within 5 seconds
          this.pongTimeout = setTimeout(() => {
            console.log('Pong timeout');
          }, 5000);
        }, 15000);
      }
    
      handlePong() {
        clearTimeout(this.pongTimeout);
        this.missedPongs = 0;
      }
    }
    
    // Server side
    ws.on('message', (msg) => {
      const data = JSON.parse(msg);
      if (data.type === 'ping') {
        ws.send(JSON.stringify({ type: 'pong', ts: data.ts }));
      }
    });
    

---
  #### **Name**
Presence with Tombstones
  #### **Description**
Track online users with graceful disconnection handling
  #### **When**
Showing who is online in collaborative features
  #### **Example**
    interface PresenceState {
      id: string;
      status: 'online' | 'away' | 'offline';
      lastSeen: number;
      cursor?: { x: number; y: number };
    }
    
    class PresenceManager {
      private presence = new Map<string, PresenceState>();
      private tombstoneDelay = 5000;  // Grace period before removal
    
      handleDisconnect(userId: string) {
        const user = this.presence.get(userId);
        if (!user) return;
    
        // Don't remove immediately - use tombstone
        user.status = 'offline';
        user.lastSeen = Date.now();
    
        // Remove after grace period (allows reconnection)
        setTimeout(() => {
          const current = this.presence.get(userId);
          if (current?.status === 'offline') {
            this.presence.delete(userId);
            this.broadcast({ type: 'presence_leave', userId });
          }
        }, this.tombstoneDelay);
      }
    
      handleReconnect(userId: string) {
        const user = this.presence.get(userId);
        if (user?.status === 'offline') {
          // Cancel tombstone - user reconnected
          user.status = 'online';
          user.lastSeen = Date.now();
        }
      }
    }
    

---
  #### **Name**
SSE with Event IDs for Resume
  #### **Description**
Server-Sent Events with reliable delivery
  #### **When**
One-way server-to-client push with recovery needs
  #### **Example**
    // Server (Node.js/Express)
    app.get('/events', (req, res) => {
      res.setHeader('Content-Type', 'text/event-stream');
      res.setHeader('Cache-Control', 'no-cache');
      res.setHeader('Connection', 'keep-alive');
    
      // Check if client is resuming
      const lastEventId = req.headers['last-event-id'];
      if (lastEventId) {
        // Replay missed events from store
        const missed = eventStore.getAfter(lastEventId);
        missed.forEach(event => sendEvent(res, event));
      }
    
      // Send new events
      function sendEvent(res, event) {
        res.write(`id: ${event.id}\n`);
        res.write(`event: ${event.type}\n`);
        res.write(`data: ${JSON.stringify(event.data)}\n\n`);
      }
    
      // Subscribe to new events
      const unsubscribe = eventBus.subscribe(event => {
        sendEvent(res, event);
      });
    
      req.on('close', () => {
        unsubscribe();
      });
    });
    
    // Client
    const eventSource = new EventSource('/events');
    eventSource.onmessage = (event) => {
      // Browser automatically sends Last-Event-ID on reconnect
      console.log('Event:', event.lastEventId, event.data);
    };
    

---
  #### **Name**
Message Ordering with Vector Clocks
  #### **Description**
Ensure causal ordering in distributed updates
  #### **When**
Multiple clients can make concurrent edits
  #### **Example**
    type VectorClock = Map<string, number>;
    
    function increment(clock: VectorClock, nodeId: string): VectorClock {
      const newClock = new Map(clock);
      newClock.set(nodeId, (clock.get(nodeId) || 0) + 1);
      return newClock;
    }
    
    function merge(a: VectorClock, b: VectorClock): VectorClock {
      const merged = new Map(a);
      for (const [node, time] of b) {
        merged.set(node, Math.max(merged.get(node) || 0, time));
      }
      return merged;
    }
    
    function happensBefore(a: VectorClock, b: VectorClock): boolean {
      let atLeastOneLess = false;
      for (const [node, timeA] of a) {
        const timeB = b.get(node) || 0;
        if (timeA > timeB) return false;
        if (timeA < timeB) atLeastOneLess = true;
      }
      // Check nodes in b not in a
      for (const [node, timeB] of b) {
        if (!a.has(node) && timeB > 0) atLeastOneLess = true;
      }
      return atLeastOneLess;
    }
    
    // Usage in message handling
    class OrderedChannel {
      private clock: VectorClock = new Map();
      private pending: Message[] = [];
    
      receive(msg: Message) {
        if (happensBefore(msg.clock, this.clock)) {
          // Old message, already processed
          return;
        }
    
        if (canDeliver(msg.clock, this.clock)) {
          this.deliver(msg);
          this.clock = merge(this.clock, msg.clock);
          this.tryDeliverPending();
        } else {
          this.pending.push(msg);
        }
      }
    }
    

## Anti-Patterns


---
  #### **Name**
Reconnect Immediately
  #### **Description**
Reconnecting instantly after disconnect
  #### **Why**
    When server restarts, all clients reconnect simultaneously. This creates
    a thundering herd that can crash the server again. Each client should
    wait a random delay before reconnecting.
    
  #### **Instead**
Use exponential backoff with jitter (random 0-30% added to delay)

---
  #### **Name**
Polling Disguised as Real-time
  #### **Description**
Using setInterval to poll an API and calling it real-time
  #### **Why**
    Polling wastes bandwidth, battery, and adds latency. 1-second polling
    means 1-second average delay. It also hammers your server with requests
    from every connected client.
    
  #### **Instead**
Use SSE for server-push, WebSocket only if you need bidirectional

---
  #### **Name**
Trusting Connection State
  #### **Description**
Assuming WebSocket connection means messages are delivered
  #### **Why**
    Network can be half-open. Client thinks connected, server thinks connected,
    but messages aren't flowing. Without heartbeats, you won't know until
    TCP timeout (can be minutes).
    
  #### **Instead**
Implement application-level heartbeat with pong confirmation

---
  #### **Name**
Presence Without Grace Period
  #### **Description**
Showing users as offline immediately on disconnect
  #### **Why**
    Users flicker online/offline during network blips. Mobile users switching
    networks appear to leave and rejoin. This creates jarring UX and spams
    presence events.
    
  #### **Instead**
Use tombstones with 5-10 second grace period before showing offline

---
  #### **Name**
Synchronizing Full State
  #### **Description**
Sending complete state on every update instead of deltas
  #### **Why**
    Bandwidth explodes with state size. Race conditions when updates cross.
    Latency increases. For 10 users editing a doc, you're sending 10x the data.
    
  #### **Instead**
Send operations/deltas, use CRDT or OT for conflict resolution

---
  #### **Name**
WebSocket for Everything
  #### **Description**
Using WebSocket when SSE would suffice
  #### **Why**
    WebSocket is bidirectional but complex. Most real-time features only need
    server-to-client push. SSE auto-reconnects, works through proxies better,
    and is simpler to implement.
    
  #### **Instead**
Use SSE for notifications, live feeds, dashboards. WebSocket only for chat, games, collaboration