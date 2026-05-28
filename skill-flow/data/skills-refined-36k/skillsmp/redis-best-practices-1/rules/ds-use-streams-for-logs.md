---
title: Use Streams for Event Logs and Messaging
impact: HIGH
impactDescription: persistent messaging with consumer groups, at-least-once delivery
tags: data-structures, streams, events, messaging, pub-sub
---

## Use Streams for Event Logs and Messaging

Use Redis Streams for event sourcing, activity logs, and reliable messaging. Streams provide persistent, append-only logs with consumer groups for distributed processing, explicit message acknowledgment, and at-least-once delivery semantics.

**When to use Streams vs Lists vs Pub/Sub:**
- **Streams**: Persistent messages, consumer groups, replay capability, acknowledgments
- **Lists**: Simple queues, no need for consumer groups or replay
- **Pub/Sub**: Fire-and-forget, no persistence, real-time only

**Incorrect (using Pub/Sub or Lists for persistent messaging):**

```python
import redis
r = redis.Redis()

# Anti-pattern 1: Pub/Sub for persistent messaging
# Messages are lost if no subscriber is listening!
r.publish("events", '{"type": "order_created", "id": 123}')
# If consumer is down, message is gone forever

# Anti-pattern 2: List without consumer groups
# Only one consumer can process each message
# No acknowledgment tracking
r.lpush("events", '{"type": "order_created", "id": 123}')
job = r.rpop("events")  # If process crashes, job is lost

# Anti-pattern 3: Polling for new events
while True:
    events = r.lrange("events", last_index, -1)
    # Must track position manually, no consumer group support
```

**Correct (using Streams):**

```python
import redis
r = redis.Redis()

# Add events to stream (returns auto-generated ID like "1234567890123-0")
event_id = r.xadd("events:orders", {
    "type": "order_created",
    "order_id": "12345",
    "customer_id": "cust_789",
    "total": "99.99"
})
print(f"Event ID: {event_id}")  # e.g., b'1704067200000-0'

# Add with custom ID (use * for auto-generate)
r.xadd("events:orders", {"type": "order_paid", "order_id": "12345"}, id="*")

# Read events (simple, from beginning)
events = r.xrange("events:orders", "-", "+")  # All events
events = r.xrange("events:orders", "-", "+", count=10)  # First 10

# Read events from specific ID onwards
events = r.xrange("events:orders", "1704067200000-0", "+")

# Read new events only (blocking)
# ">" means only new messages not yet delivered
events = r.xread({"events:orders": "$"}, block=5000)  # Block 5 seconds
```

```python
# Consumer Groups - distributed processing with acknowledgments
import redis
r = redis.Redis()

STREAM = "events:orders"
GROUP = "order-processors"
CONSUMER = "worker-1"

# Create consumer group (run once, idempotent with mkstream)
try:
    r.xgroup_create(STREAM, GROUP, id="0", mkstream=True)
except redis.ResponseError as e:
    if "BUSYGROUP" not in str(e):
        raise  # Group already exists is OK

# Read messages for this consumer group
# ">" means only messages never delivered to any consumer in this group
messages = r.xreadgroup(
    GROUP,
    CONSUMER,
    {STREAM: ">"},
    count=10,
    block=5000  # Block for 5 seconds if no messages
)

# Process messages
for stream_name, stream_messages in messages:
    for message_id, fields in stream_messages:
        try:
            # Process the event
            print(f"Processing {message_id}: {fields}")

            # Acknowledge successful processing
            r.xack(STREAM, GROUP, message_id)
        except Exception as e:
            # Don't ack - message will be re-delivered
            print(f"Failed to process {message_id}: {e}")

# Check pending messages (not yet acknowledged)
pending = r.xpending(STREAM, GROUP)
print(f"Pending messages: {pending}")

# Claim stuck messages (from dead consumers)
# Messages pending > 60 seconds, move to this consumer
stuck = r.xautoclaim(STREAM, GROUP, CONSUMER, min_idle_time=60000, start_id="0")
```

```python
# Full worker implementation
import redis
import signal
import sys

r = redis.Redis()
running = True

def shutdown(signum, frame):
    global running
    running = False

signal.signal(signal.SIGTERM, shutdown)
signal.signal(signal.SIGINT, shutdown)

STREAM = "events:orders"
GROUP = "order-processors"
CONSUMER = f"worker-{os.getpid()}"

# Ensure group exists
try:
    r.xgroup_create(STREAM, GROUP, id="0", mkstream=True)
except redis.ResponseError:
    pass

while running:
    # First, check for pending messages (recovery)
    pending = r.xreadgroup(GROUP, CONSUMER, {STREAM: "0"}, count=10)

    # Then read new messages
    if not pending or not pending[0][1]:
        messages = r.xreadgroup(GROUP, CONSUMER, {STREAM: ">"}, count=10, block=1000)
    else:
        messages = pending

    if messages:
        for _, stream_messages in messages:
            for msg_id, fields in stream_messages:
                try:
                    process_event(fields)
                    r.xack(STREAM, GROUP, msg_id)
                except Exception as e:
                    log_error(f"Failed: {msg_id}", e)
```

```javascript
// Node.js
const redis = require('redis');
const client = redis.createClient();

// Add to stream
await client.xAdd('events:orders', '*', {
    type: 'order_created',
    order_id: '12345'
});

// Create consumer group
try {
    await client.xGroupCreate('events:orders', 'processors', '0', { MKSTREAM: true });
} catch (e) {
    // Group exists
}

// Read with consumer group
const messages = await client.xReadGroup('processors', 'worker-1', [
    { key: 'events:orders', id: '>' }
], { COUNT: 10, BLOCK: 5000 });

// Acknowledge
await client.xAck('events:orders', 'processors', messageId);
```

Reference: [Redis Streams](https://redis.io/docs/data-types/streams/)
