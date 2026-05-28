# Cost Tracking

Token usage and budget management.

## Built-in Tracking

```python
result = agent.run(question="What is AI?")

# Access cost metrics
tokens = result.get("_tokens", {})
cost = result.get("_cost", 0.0)

print(f"Tokens: {tokens}")
print(f"Cost: ${cost:.4f}")
```

## Custom Budget Management

```python
class BudgetAgent(BaseAgent):
    def __init__(self, config, max_budget: float):
        super().__init__(config=config, signature=MySignature())
        self.max_budget = max_budget
        self.total_cost = 0.0

    def process(self, data: str) -> dict:
        result = self.run(data=data)

        cost = result.get("_cost", 0.0)
        self.total_cost += cost

        if self.total_cost > self.max_budget:
            raise BudgetExceededError(f"Budget exceeded: ${self.total_cost}")

        return result
```

## References
- **Source**: `apps/kailash-kaizen/src/kaizen/core/base_agent.py`
