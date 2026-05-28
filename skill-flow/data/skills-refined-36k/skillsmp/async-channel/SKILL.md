---
name: async-channel
description: Asynchronous pub/sub messaging system for OctoBot. Enables decoupled component communication via producer/consumer pattern. Use when implementing inter-component messaging or event-driven architectures.
version: 1.0.0
license: MIT
---

# Async-Channel Development

Help developers work with OctoBot's asynchronous messaging system - enabling loose coupling between components.

## References

Consult these resources as needed:
- ./references/core-concepts.md -- Channels, producers, consumers, message flow
- ./references/patterns.md -- Common usage patterns, best practices, examples
- ./references/advanced.md -- Channel hierarchies, filtering, error handling

## Overview

Async-Channel is a **Core Layer** library providing:
- Publisher/subscriber messaging
- Asynchronous message passing
- Multiple consumer support
- Channel hierarchies
- Message filtering
- Backpressure handling

**Layer Position**: Core (foundational, used by all layers)
**Used By**: OctoBot-Trading, OctoBot-Evaluators, OctoBot, all components

## Module Structure

```
async_channel/
├── channels/               # Channel implementations
│   ├── channel.py         # Base channel
│   └── channels.py        # Specialized channels
├── producer.py             # Message producers
├── consumer.py             # Message consumers
└── util/                   # Channel utilities
```

## Key Concepts

### Channels
Message conduits between components:
```python
from async_channel import Channel

channel = Channel()
await channel.run()
```

### Producers
Send messages to channels:
```python
from async_channel import Producer

producer = Producer(channel)
await producer.send({"event": "order_filled", "order_id": "123"})
```

### Consumers
Receive messages from channels:
```python
from async_channel import Consumer

consumer = Consumer(channel)
async for message in consumer:
    print(f"Received: {message}")
```

## Common Tasks

### Basic Pub/Sub
```python
# Create channel
channel = Channel()

# Producer
producer = Producer(channel)
await producer.send({"data": "hello"})

# Consumer
consumer = Consumer(channel)
message = await consumer.get()
print(message)  # {"data": "hello"}
```

### Multiple Consumers
```python
# Multiple consumers on same channel
consumer1 = Consumer(channel)
consumer2 = Consumer(channel)

# Both receive the same messages
await producer.send({"broadcast": "message"})
```

### Filtered Consumers
```python
# Consumer with filter
def price_filter(message):
    return message.get("type") == "price"

consumer = Consumer(channel, filter_func=price_filter)
# Only receives price-related messages
```

## Integration with OctoBot

### Common Channels
```python
# Market data channels
TICKER_CHANNEL = "Ticker"
KLINE_CHANNEL = "Kline"
RECENT_TRADES_CHANNEL = "RecentTrades"

# Trading channels
ORDERS_CHANNEL = "Orders"
TRADES_CHANNEL = "Trades"
BALANCE_CHANNEL = "Balance"
```

### Usage Example
```python
from async_channel import Channel, Producer, Consumer
from octobot_commons.channels_name import ORDERS_CHANNEL

# Create orders channel
orders_channel = Channel(ORDERS_CHANNEL)

# Produce order events
producer = Producer(orders_channel)
await producer.send({
    "event": "order_created",
    "order_id": "123",
    "symbol": "BTC/USDT"
})

# Consume order events
consumer = Consumer(orders_channel)
async for order_event in consumer:
    handle_order(order_event)
```

## Quick Reference

### Import Patterns
```python
from async_channel import Channel, Producer, Consumer
from async_channel.channels import Channels
```

### Lifecycle
```python
# Create and start channel
channel = Channel()
await channel.start()

# Use channel...

# Stop channel
await channel.stop()
```

## Checklist

Before committing changes:
- [ ] Channels properly initialized with `start()`
- [ ] Producers send JSON-serializable messages
- [ ] Consumers properly handle message processing
- [ ] Channels stopped with `stop()` during cleanup
- [ ] Error handling for consumer processing
- [ ] No blocking operations in consumer loops
- [ ] Tests verify message delivery