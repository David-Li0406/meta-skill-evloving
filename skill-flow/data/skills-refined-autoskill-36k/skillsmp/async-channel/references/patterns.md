# Usage Patterns

## Basic Pub/Sub

```python
channel = Channel()
producer = Producer(channel)
consumer = Consumer(channel)

await producer.send({"data": "hello"})
message = await consumer.get()
```

## Multiple Consumers

```python
consumer1 = Consumer(channel)
consumer2 = Consumer(channel)

# Both receive messages
await producer.send({"broadcast": "message"})
```

## Filtered Messages

```python
def filter_prices(msg):
    return msg.get("type") == "price"

consumer = Consumer(channel, filter_func=filter_prices)
```

## Error Handling

```python
async for message in consumer:
    try:
        await process(message)
    except Exception as e:
        logger.error(f"Failed: {e}")
```
