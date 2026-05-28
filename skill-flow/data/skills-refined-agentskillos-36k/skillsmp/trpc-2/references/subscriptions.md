# tRPC Subscriptions

Real-time event streaming with WebSockets and Server-Sent Events (SSE).

## Table of Contents

1. [Overview](#overview)
2. [Server-Sent Events (SSE)](#server-sent-events-sse)
3. [WebSocket Setup](#websocket-setup)
4. [Client Configuration](#client-configuration)
5. [Advanced Patterns](#advanced-patterns)

---

## Overview

tRPC subscriptions enable real-time, bidirectional communication. Choose based on your needs:

| Feature | SSE | WebSocket |
|---------|-----|-----------|
| Setup complexity | Simple | More complex |
| Bidirectional | No (server → client) | Yes |
| Reconnection | Built-in | Manual/library |
| Browser support | Excellent | Excellent |
| HTTP/2 multiplexing | Yes | No |

**Recommendation**: Use SSE for most cases; use WebSocket for bidirectional needs.

---

## Server-Sent Events (SSE)

### Server Setup

```typescript
// server/routers/notifications.ts
import { publicProcedure, router } from '../trpc';
import { z } from 'zod';
import { tracked } from '@trpc/server';
import { EventEmitter } from 'events';

// Global event emitter (consider Redis for multi-instance)
const ee = new EventEmitter();

export const notificationRouter = router({
  // Basic subscription
  onNotification: publicProcedure.subscription(async function* ({ signal }) {
    // Listen to events
    const onNotification = (data: Notification) => {
      // Will be yielded to client
    };

    ee.on('notification', onNotification);

    // Cleanup when client disconnects
    signal.addEventListener('abort', () => {
      ee.off('notification', onNotification);
    });

    // Yield events as they come
    for await (const notification of createAsyncIterator(ee, 'notification', signal)) {
      yield notification;
    }
  }),

  // Subscription with tracked events (for reconnection)
  onUpdate: publicProcedure
    .input(z.object({ 
      lastEventId: z.string().optional() 
    }))
    .subscription(async function* ({ input, signal }) {
      // If reconnecting, replay missed events
      if (input.lastEventId) {
        const missedEvents = await db.events.findMany({
          where: { id: { gt: input.lastEventId } },
        });
        for (const event of missedEvents) {
          yield tracked(event.id, event);
        }
      }

      // Continue with live events
      for await (const event of createAsyncIterator(ee, 'update', signal)) {
        yield tracked(event.id, event);
      }
    }),

  // Polling-based subscription (alternative pattern)
  onNewPosts: publicProcedure
    .input(z.object({ channelId: z.string() }))
    .subscription(async function* ({ input, signal }) {
      let lastCheck = new Date();

      while (!signal.aborted) {
        const newPosts = await db.post.findMany({
          where: {
            channelId: input.channelId,
            createdAt: { gt: lastCheck },
          },
        });

        for (const post of newPosts) {
          yield post;
        }

        lastCheck = new Date();
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
    }),
});

// Helper to emit events
export function emitNotification(notification: Notification) {
  ee.emit('notification', notification);
}
```

### AsyncIterator Helper

```typescript
// utils/asyncIterator.ts
export async function* createAsyncIterator<T>(
  emitter: EventEmitter,
  event: string,
  signal: AbortSignal
): AsyncGenerator<T> {
  const queue: T[] = [];
  let resolve: (() => void) | null = null;

  const handler = (data: T) => {
    queue.push(data);
    resolve?.();
  };

  emitter.on(event, handler);
  signal.addEventListener('abort', () => emitter.off(event, handler));

  try {
    while (!signal.aborted) {
      if (queue.length > 0) {
        yield queue.shift()!;
      } else {
        await new Promise<void>(r => { resolve = r; });
        resolve = null;
      }
    }
  } finally {
    emitter.off(event, handler);
  }
}
```

### HTTP Adapter with SSE

```typescript
// server/index.ts
import { createHTTPServer } from '@trpc/server/adapters/standalone';

const server = createHTTPServer({
  router: appRouter,
  createContext,
});

server.listen(3000);
```

---

## WebSocket Setup

### Server Setup

```typescript
// server/wsServer.ts
import { applyWSSHandler } from '@trpc/server/adapters/ws';
import { WebSocketServer } from 'ws';
import { appRouter } from './routers/_app';
import { createContext } from './context';

const wss = new WebSocketServer({ port: 3001 });

const handler = applyWSSHandler({
  wss,
  router: appRouter,
  createContext,
  // Optional: Connection params for auth
  onConnect: (opts) => {
    console.log('Client connected:', opts.client);
  },
  onDisconnect: (opts) => {
    console.log('Client disconnected:', opts.client);
  },
});

// Graceful shutdown
process.on('SIGTERM', () => {
  handler.broadcastReconnectNotification();
  wss.close();
});
```

### WebSocket Subscription Procedure

```typescript
// server/routers/chat.ts
import { observable } from '@trpc/server/observable';

export const chatRouter = router({
  // Using observable pattern (v10 style, still works)
  onMessage: publicProcedure
    .input(z.object({ roomId: z.string() }))
    .subscription(({ input }) => {
      return observable<Message>((emit) => {
        const onMessage = (message: Message) => {
          if (message.roomId === input.roomId) {
            emit.next(message);
          }
        };

        ee.on('message', onMessage);
        
        return () => {
          ee.off('message', onMessage);
        };
      });
    }),

  // Using async generator (v11 style)
  onMessageV11: publicProcedure
    .input(z.object({ roomId: z.string() }))
    .subscription(async function* ({ input, signal }) {
      for await (const message of createAsyncIterator(ee, 'message', signal)) {
        if (message.roomId === input.roomId) {
          yield message;
        }
      }
    }),
});
```

### Combined HTTP + WebSocket Server

```typescript
// server/index.ts
import { createHTTPServer } from '@trpc/server/adapters/standalone';
import { applyWSSHandler } from '@trpc/server/adapters/ws';
import { WebSocketServer } from 'ws';

// HTTP server for queries/mutations
const { server } = createHTTPServer({
  router: appRouter,
  createContext,
});

// WebSocket server for subscriptions
const wss = new WebSocketServer({ server });
applyWSSHandler({ wss, router: appRouter, createContext });

server.listen(3000);
```

---

## Client Configuration

### SSE Client (httpSubscriptionLink)

```typescript
import { createTRPCClient, httpBatchLink, httpSubscriptionLink, splitLink } from '@trpc/client';
import type { AppRouter } from './server/routers/_app';

const trpc = createTRPCClient<AppRouter>({
  links: [
    splitLink({
      condition: (op) => op.type === 'subscription',
      true: httpSubscriptionLink({
        url: 'http://localhost:3000/api/trpc',
      }),
      false: httpBatchLink({
        url: 'http://localhost:3000/api/trpc',
      }),
    }),
  ],
});
```

### WebSocket Client (wsLink)

```typescript
import { createTRPCClient, httpBatchLink, wsLink, splitLink } from '@trpc/client';
import { createWSClient } from '@trpc/client';
import type { AppRouter } from './server/routers/_app';

const wsClient = createWSClient({
  url: 'ws://localhost:3001',
  // Optional: Connection params for auth
  connectionParams: async () => ({
    token: await getAuthToken(),
  }),
  // Reconnection settings
  retryDelayMs: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
});

const trpc = createTRPCClient<AppRouter>({
  links: [
    splitLink({
      condition: (op) => op.type === 'subscription',
      true: wsLink({ client: wsClient }),
      false: httpBatchLink({ url: 'http://localhost:3000/api/trpc' }),
    }),
  ],
});
```

### Using Subscriptions

```typescript
// Vanilla client
const subscription = trpc.chat.onMessage.subscribe(
  { roomId: 'room-1' },
  {
    onData: (message) => {
      console.log('New message:', message);
    },
    onError: (error) => {
      console.error('Subscription error:', error);
    },
    onComplete: () => {
      console.log('Subscription completed');
    },
  }
);

// Unsubscribe when done
subscription.unsubscribe();
```

### React Hook Usage

```tsx
// With @trpc/react-query
function ChatRoom({ roomId }: { roomId: string }) {
  const [messages, setMessages] = useState<Message[]>([]);

  trpc.chat.onMessage.useSubscription(
    { roomId },
    {
      onData: (message) => {
        setMessages((prev) => [...prev, message]);
      },
      onError: (err) => {
        console.error('Subscription error:', err);
      },
    }
  );

  return (
    <div>
      {messages.map((msg) => (
        <div key={msg.id}>{msg.text}</div>
      ))}
    </div>
  );
}
```

---

## Advanced Patterns

### Reconnection with Event Replay

```typescript
// Server
export const eventsRouter = router({
  onEvents: publicProcedure
    .input(z.object({ lastEventId: z.string().optional() }))
    .subscription(async function* ({ input, signal }) {
      // Replay missed events
      if (input.lastEventId) {
        const missed = await db.events.findMany({
          where: { id: { gt: input.lastEventId } },
          orderBy: { id: 'asc' },
        });
        for (const event of missed) {
          yield tracked(event.id, event);
        }
      }

      // Stream new events
      for await (const event of liveEvents(signal)) {
        yield tracked(event.id, event);
      }
    }),
});

// Client - lastEventId is automatically tracked
const subscription = trpc.events.onEvents.subscribe(
  { lastEventId: localStorage.getItem('lastEventId') },
  {
    onData: (event) => {
      localStorage.setItem('lastEventId', event.id);
      handleEvent(event);
    },
  }
);
```

### Subscription with Authentication

```typescript
// Server middleware
const wsAuthMiddleware = middleware(async ({ ctx, next }) => {
  if (!ctx.user) {
    throw new TRPCError({ code: 'UNAUTHORIZED' });
  }
  return next({ ctx: { user: ctx.user } });
});

const protectedSubscription = publicProcedure.use(wsAuthMiddleware);

// Router
export const notificationRouter = router({
  onUserNotifications: protectedSubscription.subscription(
    async function* ({ ctx, signal }) {
      for await (const notification of userNotifications(ctx.user.id, signal)) {
        yield notification;
      }
    }
  ),
});
```

### Broadcast to Specific Users

```typescript
// Server
const userConnections = new Map<string, Set<(data: any) => void>>();

export const notificationRouter = router({
  onNotification: protectedProcedure.subscription(async function* ({ ctx, signal }) {
    const userId = ctx.user.id;
    const callbacks = userConnections.get(userId) ?? new Set();
    
    let resolve: ((data: any) => void) | null = null;
    const queue: Notification[] = [];

    const callback = (data: Notification) => {
      queue.push(data);
      resolve?.(data);
    };

    callbacks.add(callback);
    userConnections.set(userId, callbacks);

    signal.addEventListener('abort', () => {
      callbacks.delete(callback);
      if (callbacks.size === 0) userConnections.delete(userId);
    });

    while (!signal.aborted) {
      if (queue.length > 0) {
        yield queue.shift()!;
      } else {
        await new Promise(r => { resolve = r; });
        resolve = null;
      }
    }
  }),
});

// Helper to send to specific user
export function sendToUser(userId: string, notification: Notification) {
  const callbacks = userConnections.get(userId);
  callbacks?.forEach((cb) => cb(notification));
}
```

### Error Handling in Subscriptions

```typescript
// Server
export const dataRouter = router({
  onData: publicProcedure.subscription(async function* ({ signal }) {
    try {
      for await (const data of dataStream(signal)) {
        yield data;
      }
    } catch (error) {
      // Throwing 5xx errors triggers automatic reconnect
      throw new TRPCError({
        code: 'INTERNAL_SERVER_ERROR',
        message: 'Data stream error',
        cause: error,
      });
    }
  }),
});

// Client
trpc.data.onData.subscribe(undefined, {
  onData: (data) => handleData(data),
  onError: (error) => {
    if (error.data?.code === 'INTERNAL_SERVER_ERROR') {
      // Will automatically reconnect with lastEventId
      console.log('Reconnecting...');
    }
  },
});
```

### Keep-Alive / Heartbeat

```typescript
// Server - send periodic pings
export const healthRouter = router({
  heartbeat: publicProcedure.subscription(async function* ({ signal }) {
    while (!signal.aborted) {
      yield { type: 'ping', timestamp: Date.now() };
      await new Promise(r => setTimeout(r, 30000));
    }
  }),
});

// Or use server config for automatic pings (SSE)
const server = createHTTPServer({
  router: appRouter,
  createContext,
  subscriptions: {
    pingIntervalMs: 30000,
  },
});
```