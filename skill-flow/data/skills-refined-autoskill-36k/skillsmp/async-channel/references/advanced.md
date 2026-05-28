# Advanced Topics

## Channel Hierarchies

Create parent-child channel relationships.

## Backpressure

Handle slow consumers:
```python
consumer = Consumer(channel, max_queue_size=100)
```

## Custom Channels

Extend Channel class for specialized behavior.

## Performance

- Use filtering to reduce message processing
- Batch messages when possible
- Monitor channel queue sizes
