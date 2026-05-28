# Streaming Responses

Real-time output streaming.

## Concept

Stream LLM responses token-by-token for better UX.

## Implementation

```python
class StreamingAgent(BaseAgent):
    async def stream_response(self, question: str):
        async for token in self.strategy.stream(
            self.signature,
            {"question": question},
            self.config
        ):
            yield token
```

## References
- **Examples**: `apps/kailash-kaizen/examples/1-single-agent/streaming-chat/`
