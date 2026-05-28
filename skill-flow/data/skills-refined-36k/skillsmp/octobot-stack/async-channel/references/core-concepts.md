# Core Concepts

## Channels

Message conduits between components.

```python
from async_channel import Channel

channel = Channel(name="MyChannel")
await channel.start()
```

## Producers

Send messages to channels.

```python
from async_channel import Producer

producer = Producer(channel)
await producer.send({"event": "price_update", "price": 50000})
await producer.run()
```

## Consumers

Receive messages from channels.

```python
from async_channel import Consumer

consumer = Consumer(channel)
async for message in consumer:
    print(f"Got: {message}")
```

## Message Flow

```
Producer → Channel → Consumer(s)
```

Multiple consumers can subscribe to the same channel.
