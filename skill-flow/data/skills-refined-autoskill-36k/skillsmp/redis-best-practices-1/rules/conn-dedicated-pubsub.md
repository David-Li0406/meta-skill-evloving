---
title: Use Dedicated Connections for Pub/Sub
impact: MEDIUM-HIGH
impactDescription: Pub/Sub blocks connection, can't be shared
tags: connection, pubsub, messaging, architecture
---

## Use Dedicated Connections for Pub/Sub

Use separate, dedicated connections for Pub/Sub subscribers. Once a connection enters subscribe mode, it can only execute subscribe/unsubscribe commands. Sharing a Pub/Sub connection with regular commands will fail or block.

**Why Dedicated Connections:**
- SUBSCRIBE puts connection in special mode
- Can only run SUBSCRIBE, PSUBSCRIBE, UNSUBSCRIBE, PUNSUBSCRIBE, PING, QUIT
- Regular commands (GET, SET, etc.) are not allowed
- Messages arrive asynchronously on the subscribed connection

**Incorrect (sharing Pub/Sub connection):**

```python
import redis
r = redis.Redis()

# Anti-pattern 1: Using same client for subscribe and commands
pubsub = r.pubsub()
pubsub.subscribe('channel1')

# This will fail or behave unexpectedly
r.get('some_key')  # May interfere with pub/sub
r.set('key', 'value')

# Anti-pattern 2: Subscribing in request handler
def handle_request(request):
    pubsub = r.pubsub()
    pubsub.subscribe('updates')
    # Creates new subscription per request - resource leak!

# Anti-pattern 3: Blocking subscribe in main thread
def start_app():
    pubsub = r.pubsub()
    pubsub.subscribe('events')
    for message in pubsub.listen():  # Blocks forever!
        process(message)
    # App can't do anything else
```

**Correct (dedicated Pub/Sub connections):**

```python
import redis
import threading

# Separate clients for regular operations and pub/sub
redis_client = redis.Redis(host='localhost', port=6379)
redis_pubsub = redis.Redis(host='localhost', port=6379)

# Correct 1: Dedicated pubsub in separate thread
class PubSubHandler:
    def __init__(self, channels):
        self.redis = redis.Redis(host='localhost', port=6379)
        self.pubsub = self.redis.pubsub()
        self.channels = channels
        self.thread = None

    def message_handler(self, message):
        if message['type'] == 'message':
            channel = message['channel'].decode()
            data = message['data'].decode()
            print(f"Received on {channel}: {data}")
            # Process message here

    def start(self):
        self.pubsub.subscribe(**{ch: self.message_handler for ch in self.channels})
        self.thread = self.pubsub.run_in_thread(sleep_time=0.001)

    def stop(self):
        if self.thread:
            self.thread.stop()
        self.pubsub.close()

# Usage
handler = PubSubHandler(['notifications', 'updates'])
handler.start()

# Main thread can still use regular Redis client
redis_client.set('key', 'value')
redis_client.get('key')

# Correct 2: Pattern subscription with dedicated connection
def start_pattern_subscriber():
    r = redis.Redis()  # Dedicated connection
    pubsub = r.pubsub()

    # Subscribe to pattern
    pubsub.psubscribe('events:*')

    for message in pubsub.listen():
        if message['type'] == 'pmessage':
            pattern = message['pattern'].decode()
            channel = message['channel'].decode()
            data = message['data'].decode()
            print(f"Pattern {pattern}, Channel {channel}: {data}")

# Run in separate thread
thread = threading.Thread(target=start_pattern_subscriber, daemon=True)
thread.start()

# Correct 3: Async pub/sub with separate connection
import asyncio
import redis.asyncio as redis

async def subscriber(channels):
    """Async subscriber with dedicated connection"""
    r = redis.Redis()
    pubsub = r.pubsub()

    await pubsub.subscribe(*channels)

    async for message in pubsub.listen():
        if message['type'] == 'message':
            await process_message(message)

async def publisher():
    """Publisher uses regular connection"""
    r = redis.Redis()
    while True:
        await r.publish('notifications', 'Hello!')
        await asyncio.sleep(1)

async def main():
    # Run subscriber and publisher concurrently
    await asyncio.gather(
        subscriber(['notifications']),
        publisher()
    )
```

```python
# Correct 4: Publisher pattern (separate from subscribers)
class EventBus:
    def __init__(self):
        # Publisher connection (for sending)
        self.publisher = redis.Redis(host='localhost', port=6379)
        # Subscriber connections (for receiving)
        self.subscribers = {}

    def publish(self, channel, message):
        """Publish message - uses regular connection"""
        self.publisher.publish(channel, message)

    def subscribe(self, channel, callback):
        """Create dedicated subscriber for channel"""
        r = redis.Redis(host='localhost', port=6379)
        pubsub = r.pubsub()
        pubsub.subscribe(channel)

        def listener():
            for msg in pubsub.listen():
                if msg['type'] == 'message':
                    callback(msg['data'])

        thread = threading.Thread(target=listener, daemon=True)
        thread.start()
        self.subscribers[channel] = (pubsub, thread)

    def unsubscribe(self, channel):
        if channel in self.subscribers:
            pubsub, thread = self.subscribers[channel]
            pubsub.unsubscribe(channel)
            pubsub.close()
            del self.subscribers[channel]
```

```javascript
// Node.js - Separate connections for pub/sub
const Redis = require('ioredis');

// Regular operations
const redis = new Redis();

// Dedicated subscriber connection
const subscriber = new Redis();

// Dedicated publisher connection (optional, can share with redis)
const publisher = new Redis();

subscriber.subscribe('notifications', 'updates', (err, count) => {
    console.log(`Subscribed to ${count} channels`);
});

subscriber.on('message', (channel, message) => {
    console.log(`Received ${message} from ${channel}`);
});

// Regular operations on separate connection
await redis.set('key', 'value');
await redis.get('key');

// Publish (can use redis or publisher)
await publisher.publish('notifications', 'Hello!');
```

```go
// Go - Dedicated pub/sub connection
import "github.com/redis/go-redis/v9"

// Regular client
rdb := redis.NewClient(&redis.Options{Addr: "localhost:6379"})

// Dedicated pub/sub (creates separate connection internally)
pubsub := rdb.Subscribe(ctx, "notifications", "updates")

// Receive messages in goroutine
go func() {
    ch := pubsub.Channel()
    for msg := range ch {
        fmt.Printf("Received %s from %s\n", msg.Payload, msg.Channel)
    }
}()

// Regular operations continue
rdb.Set(ctx, "key", "value", 0)

// Publish
rdb.Publish(ctx, "notifications", "Hello!")
```

Reference: [Redis Pub/Sub](https://redis.io/docs/manual/pubsub/)
