---
name: WebSocket Real-time
description: Real-time communication for live poker, chat, and notifications
---

# WebSocket Real-time Skill

## Supabase Realtime (Recommended for Smarter.Poker)

### Subscribe to Table Changes
```javascript
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(url, key);

// Subscribe to changes
const channel = supabase
  .channel('poker-table-123')
  .on(
    'postgres_changes',
    { event: '*', schema: 'public', table: 'game_actions', filter: 'table_id=eq.123' },
    (payload) => {
      console.log('Action:', payload.new);
      handleGameAction(payload.new);
    }
  )
  .subscribe();

// Cleanup
channel.unsubscribe();
```

### Presence (Who's Online)
```javascript
const channel = supabase.channel('online-users');

channel
  .on('presence', { event: 'sync' }, () => {
    const state = channel.presenceState();
    console.log('Online users:', Object.keys(state).length);
  })
  .on('presence', { event: 'join' }, ({ key, newPresences }) => {
    console.log('User joined:', newPresences);
  })
  .on('presence', { event: 'leave' }, ({ key, leftPresences }) => {
    console.log('User left:', leftPresences);
  })
  .subscribe(async (status) => {
    if (status === 'SUBSCRIBED') {
      await channel.track({
        user_id: userId,
        online_at: new Date().toISOString()
      });
    }
  });
```

### Broadcast Messages
```javascript
// Send
channel.send({
  type: 'broadcast',
  event: 'chat_message',
  payload: { userId, message, timestamp: Date.now() }
});

// Receive
channel.on('broadcast', { event: 'chat_message' }, ({ payload }) => {
  addMessage(payload);
});
```

## Custom WebSocket (Socket.io)

### Server Setup
```javascript
import { Server } from 'socket.io';
import { createServer } from 'http';

const httpServer = createServer();
const io = new Server(httpServer, {
  cors: { origin: '*' }
});

io.on('connection', (socket) => {
  console.log('Client connected:', socket.id);
  
  socket.on('join_table', (tableId) => {
    socket.join(`table:${tableId}`);
  });
  
  socket.on('player_action', (action) => {
    io.to(`table:${action.tableId}`).emit('action', action);
  });
  
  socket.on('disconnect', () => {
    console.log('Client disconnected');
  });
});

httpServer.listen(3001);
```

### Client
```javascript
import { io } from 'socket.io-client';

const socket = io('ws://localhost:3001');

socket.on('connect', () => {
  socket.emit('join_table', tableId);
});

socket.on('action', (action) => {
  handleAction(action);
});

// Send action
socket.emit('player_action', {
  tableId,
  playerId,
  action: 'raise',
  amount: 100
});
```

## React Hooks

### useRealtime Hook
```javascript
import { useEffect, useState } from 'react';
import { supabase } from '@/lib/supabase';

export function useRealtime(channel, table, filter) {
  const [data, setData] = useState([]);
  
  useEffect(() => {
    const subscription = supabase
      .channel(channel)
      .on('postgres_changes', 
        { event: '*', schema: 'public', table, filter },
        (payload) => {
          setData(prev => [...prev, payload.new]);
        }
      )
      .subscribe();
    
    return () => subscription.unsubscribe();
  }, [channel, table, filter]);
  
  return data;
}

// Usage
const actions = useRealtime('game-123', 'game_actions', 'game_id=eq.123');
```

### usePresence Hook
```javascript
export function usePresence(channelName, userId) {
  const [onlineUsers, setOnlineUsers] = useState([]);
  
  useEffect(() => {
    const channel = supabase.channel(channelName);
    
    channel
      .on('presence', { event: 'sync' }, () => {
        const state = channel.presenceState();
        setOnlineUsers(Object.values(state).flat());
      })
      .subscribe(async (status) => {
        if (status === 'SUBSCRIBED') {
          await channel.track({ user_id: userId });
        }
      });
    
    return () => channel.unsubscribe();
  }, [channelName, userId]);
  
  return onlineUsers;
}
```

## Best Practices
- Use connection pooling for scalability
- Implement heartbeat/ping for connection health
- Handle reconnection gracefully
- Debounce rapid-fire events
- Use rooms/channels for message routing
- Authenticate WebSocket connections
