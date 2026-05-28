# WebSockets & Real-time

## Patterns

### **Websocket Server**
  #### **Description**
Basic WebSocket server setup
  #### **Example**
    // Node.js with ws library
    import { WebSocketServer, WebSocket } from 'ws';
    import { createServer } from 'http';
    
    const server = createServer();
    const wss = new WebSocketServer({ server });
    
    // Track connected clients
    const clients = new Map<string, WebSocket>();
    
    wss.on('connection', (ws, req) => {
      // Authenticate from query params or headers
      const userId = authenticateFromRequest(req);
      if (!userId) {
        ws.close(4001, 'Unauthorized');
        return;
      }
    
      clients.set(userId, ws);
      console.log(`User ${userId} connected`);
    
      ws.on('message', (data) => {
        try {
          const message = JSON.parse(data.toString());
          handleMessage(userId, message);
        } catch (e) {
          ws.send(JSON.stringify({ error: 'Invalid JSON' }));
        }
      });
    
      ws.on('close', () => {
        clients.delete(userId);
        console.log(`User ${userId} disconnected`);
      });
    
      ws.on('error', (error) => {
        console.error(`WebSocket error for ${userId}:`, error);
      });
    
      // Send initial state
      ws.send(JSON.stringify({ type: 'connected', userId }));
    });
    
    // Broadcast to all clients
    function broadcast(message: object) {
      const data = JSON.stringify(message);
      for (const [, client] of clients) {
        if (client.readyState === WebSocket.OPEN) {
          client.send(data);
        }
      }
    }
    
    // Send to specific user
    function sendToUser(userId: string, message: object) {
      const client = clients.get(userId);
      if (client?.readyState === WebSocket.OPEN) {
        client.send(JSON.stringify(message));
      }
    }
    
    server.listen(3001);
    
### **Websocket Client**
  #### **Description**
Robust WebSocket client with reconnection
  #### **Example**
    // React hook for WebSocket connection
    import { useEffect, useRef, useCallback, useState } from 'react';
    
    interface UseWebSocketOptions {
      url: string;
      onMessage: (data: unknown) => void;
      onConnect?: () => void;
      onDisconnect?: () => void;
      reconnectInterval?: number;
      maxReconnectAttempts?: number;
    }
    
    export function useWebSocket({
      url,
      onMessage,
      onConnect,
      onDisconnect,
      reconnectInterval = 3000,
      maxReconnectAttempts = 10,
    }: UseWebSocketOptions) {
      const wsRef = useRef<WebSocket | null>(null);
      const reconnectCount = useRef(0);
      const reconnectTimer = useRef<NodeJS.Timeout>();
      const [isConnected, setIsConnected] = useState(false);
    
      const connect = useCallback(() => {
        // Clean up existing connection
        if (wsRef.current) {
          wsRef.current.close();
        }
    
        const ws = new WebSocket(url);
    
        ws.onopen = () => {
          setIsConnected(true);
          reconnectCount.current = 0;
          onConnect?.();
        };
    
        ws.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            onMessage(data);
          } catch (e) {
            console.error('Failed to parse message:', e);
          }
        };
    
        ws.onclose = (event) => {
          setIsConnected(false);
          onDisconnect?.();
    
          // Don't reconnect on intentional close
          if (event.code === 1000) return;
    
          // Reconnect with backoff
          if (reconnectCount.current < maxReconnectAttempts) {
            const delay = reconnectInterval * Math.pow(2, reconnectCount.current);
            reconnectCount.current++;
    
            reconnectTimer.current = setTimeout(() => {
              connect();
            }, Math.min(delay, 30000));
          }
        };
    
        ws.onerror = (error) => {
          console.error('WebSocket error:', error);
        };
    
        wsRef.current = ws;
      }, [url, onMessage, onConnect, onDisconnect, reconnectInterval, maxReconnectAttempts]);
    
      const send = useCallback((data: object) => {
        if (wsRef.current?.readyState === WebSocket.OPEN) {
          wsRef.current.send(JSON.stringify(data));
        }
      }, []);
    
      const disconnect = useCallback(() => {
        clearTimeout(reconnectTimer.current);
        wsRef.current?.close(1000);
      }, []);
    
      useEffect(() => {
        connect();
        return () => {
          clearTimeout(reconnectTimer.current);
          wsRef.current?.close(1000);
        };
      }, [connect]);
    
      return { isConnected, send, disconnect };
    }
    
### **Server Sent Events**
  #### **Description**
SSE for server-to-client updates
  #### **Example**
    // Server: Next.js API route
    // app/api/events/route.ts
    export async function GET(request: Request) {
      const encoder = new TextEncoder();
    
      const stream = new ReadableStream({
        async start(controller) {
          // Send initial connection message
          controller.enqueue(
            encoder.encode(`data: ${JSON.stringify({ type: 'connected' })}\n\n`)
          );
    
          // Subscribe to updates (e.g., from Redis)
          const subscription = subscribeToUpdates((event) => {
            controller.enqueue(
              encoder.encode(`data: ${JSON.stringify(event)}\n\n`)
            );
          });
    
          // Handle client disconnect
          request.signal.addEventListener('abort', () => {
            subscription.unsubscribe();
            controller.close();
          });
    
          // Heartbeat to keep connection alive
          const heartbeat = setInterval(() => {
            controller.enqueue(encoder.encode(`: heartbeat\n\n`));
          }, 30000);
    
          request.signal.addEventListener('abort', () => {
            clearInterval(heartbeat);
          });
        },
      });
    
      return new Response(stream, {
        headers: {
          'Content-Type': 'text/event-stream',
          'Cache-Control': 'no-cache',
          'Connection': 'keep-alive',
        },
      });
    }
    
    
    // Client: React hook
    export function useSSE(url: string, onMessage: (data: unknown) => void) {
      useEffect(() => {
        const eventSource = new EventSource(url);
    
        eventSource.onmessage = (event) => {
          const data = JSON.parse(event.data);
          onMessage(data);
        };
    
        eventSource.onerror = () => {
          // EventSource automatically reconnects
          console.log('SSE connection error, reconnecting...');
        };
    
        return () => eventSource.close();
      }, [url, onMessage]);
    }
    
### **Presence System**
  #### **Description**
Track online/offline status
  #### **Example**
    // Server: Presence tracking with Redis
    import Redis from 'ioredis';
    
    const redis = new Redis();
    const PRESENCE_KEY = 'presence:online';
    const PRESENCE_TTL = 60; // seconds
    
    // User connects
    async function userOnline(userId: string) {
      await redis.zadd(PRESENCE_KEY, Date.now(), userId);
    
      // Publish presence change
      await redis.publish('presence', JSON.stringify({
        userId,
        status: 'online',
        timestamp: Date.now(),
      }));
    }
    
    // Heartbeat (call every 30s)
    async function heartbeat(userId: string) {
      await redis.zadd(PRESENCE_KEY, Date.now(), userId);
    }
    
    // User disconnects
    async function userOffline(userId: string) {
      await redis.zrem(PRESENCE_KEY, userId);
    
      await redis.publish('presence', JSON.stringify({
        userId,
        status: 'offline',
        timestamp: Date.now(),
      }));
    }
    
    // Get online users
    async function getOnlineUsers(): Promise<string[]> {
      const cutoff = Date.now() - (PRESENCE_TTL * 1000);
      // Remove stale entries
      await redis.zremrangebyscore(PRESENCE_KEY, 0, cutoff);
      // Get current online users
      return redis.zrange(PRESENCE_KEY, 0, -1);
    }
    
    // Check if user is online
    async function isUserOnline(userId: string): Promise<boolean> {
      const score = await redis.zscore(PRESENCE_KEY, userId);
      if (!score) return false;
      return parseInt(score) > Date.now() - (PRESENCE_TTL * 1000);
    }
    
    
    // Client: Show presence
    function UserList({ users }) {
      const [onlineUsers, setOnlineUsers] = useState<Set<string>>(new Set());
    
      useSSE('/api/presence', (event) => {
        if (event.status === 'online') {
          setOnlineUsers(prev => new Set([...prev, event.userId]));
        } else {
          setOnlineUsers(prev => {
            const next = new Set(prev);
            next.delete(event.userId);
            return next;
          });
        }
      });
    
      return (
        <ul>
          {users.map(user => (
            <li key={user.id}>
              <span className={onlineUsers.has(user.id) ? 'online' : 'offline'} />
              {user.name}
            </li>
          ))}
        </ul>
      );
    }
    
### **Typing Indicator**
  #### **Description**
Show when users are typing
  #### **Example**
    // Server: Typing indicator with debounce
    const typingUsers = new Map<string, NodeJS.Timeout>();
    
    function handleTypingStart(roomId: string, userId: string) {
      // Clear existing timeout
      const existing = typingUsers.get(`${roomId}:${userId}`);
      if (existing) clearTimeout(existing);
    
      // Broadcast typing start
      broadcastToRoom(roomId, {
        type: 'typing_start',
        userId,
      });
    
      // Auto-stop after 3 seconds of no activity
      const timeout = setTimeout(() => {
        handleTypingStop(roomId, userId);
      }, 3000);
    
      typingUsers.set(`${roomId}:${userId}`, timeout);
    }
    
    function handleTypingStop(roomId: string, userId: string) {
      const timeout = typingUsers.get(`${roomId}:${userId}`);
      if (timeout) {
        clearTimeout(timeout);
        typingUsers.delete(`${roomId}:${userId}`);
      }
    
      broadcastToRoom(roomId, {
        type: 'typing_stop',
        userId,
      });
    }
    
    
    // Client: Typing indicator component
    function TypingIndicator({ roomId }) {
      const [typingUsers, setTypingUsers] = useState<string[]>([]);
      const { send } = useWebSocket();
    
      // Handle incoming typing events
      useEffect(() => {
        // Subscribed via WebSocket...
      }, []);
    
      // Debounced typing notification
      const inputRef = useRef<HTMLInputElement>(null);
      const lastTypingRef = useRef(0);
    
      const handleInput = () => {
        const now = Date.now();
        if (now - lastTypingRef.current > 1000) {
          send({ type: 'typing_start', roomId });
          lastTypingRef.current = now;
        }
      };
    
      const handleBlur = () => {
        send({ type: 'typing_stop', roomId });
      };
    
      if (typingUsers.length === 0) return null;
    
      return (
        <div className="typing-indicator">
          {typingUsers.length === 1
            ? `${typingUsers[0]} is typing...`
            : typingUsers.length === 2
            ? `${typingUsers[0]} and ${typingUsers[1]} are typing...`
            : `${typingUsers.length} people are typing...`}
        </div>
      );
    }
    
### **Scaling With Redis**
  #### **Description**
Scale WebSockets with Redis pub/sub
  #### **Example**
    // Each server subscribes to Redis channels
    import { WebSocketServer } from 'ws';
    import Redis from 'ioredis';
    
    const pub = new Redis();
    const sub = new Redis();
    
    // Local clients on this server
    const localClients = new Map<string, WebSocket>();
    
    // Subscribe to Redis for cross-server messages
    sub.subscribe('broadcast', 'user-messages');
    
    sub.on('message', (channel, message) => {
      const data = JSON.parse(message);
    
      if (channel === 'broadcast') {
        // Send to all local clients
        for (const [, ws] of localClients) {
          if (ws.readyState === WebSocket.OPEN) {
            ws.send(message);
          }
        }
      } else if (channel === 'user-messages') {
        // Send to specific user if they're on this server
        const client = localClients.get(data.userId);
        if (client?.readyState === WebSocket.OPEN) {
          client.send(JSON.stringify(data.payload));
        }
      }
    });
    
    // When a message needs to go to all servers
    function broadcast(message: object) {
      pub.publish('broadcast', JSON.stringify(message));
    }
    
    // When a message needs to go to a specific user
    function sendToUser(userId: string, payload: object) {
      pub.publish('user-messages', JSON.stringify({ userId, payload }));
    }
    
    
    // Connection handling
    wss.on('connection', (ws, req) => {
      const userId = authenticate(req);
      localClients.set(userId, ws);
    
      ws.on('close', () => {
        localClients.delete(userId);
      });
    });
    

## Anti-Patterns

### **No Reconnection**
  #### **Description**
Not handling connection drops
  #### **Wrong**
new WebSocket(url) with no reconnection logic
  #### **Right**
Implement exponential backoff reconnection
### **Shared State**
  #### **Description**
Storing connections in memory with multiple servers
  #### **Wrong**
const clients = new Map() with load balancer
  #### **Right**
Use Redis pub/sub for cross-server communication
### **Sync In Handler**
  #### **Description**
Blocking operations in message handler
  #### **Wrong**
await heavyDatabaseQuery() in onmessage
  #### **Right**
Queue work, respond immediately if possible
### **Auth After Connect**
  #### **Description**
Authenticating after WebSocket is established
  #### **Wrong**
ws.onopen = () => ws.send({ token })
  #### **Right**
Pass token in connection URL or headers