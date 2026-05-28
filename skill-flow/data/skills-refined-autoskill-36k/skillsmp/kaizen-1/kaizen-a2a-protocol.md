# Google A2A Protocol

Automatic capability card generation and semantic agent matching.

## Automatic Capability Cards

```python
agent = DataAnalystAgent(config)
card = agent.to_a2a_card()

print(card.agent_name)            # "DataAnalystAgent"
print(card.primary_capabilities)  # Extracted from signature
print(card.domain)                # Auto-inferred: "data_analysis"
```

## Semantic Matching

```python
best_worker = supervisor.select_worker_for_task(
    task="Analyze sales data and create visualization",
    available_workers=[code_expert, data_expert, writing_expert],
    return_score=True
)
# Returns: {"worker": <DataAnalystAgent>, "score": 0.9}
```

**Benefits:**
- ✅ No hardcoded if/else logic
- ✅ Semantic capability matching (0.0-1.0 scores)
- ✅ Zero configuration
- ✅ 100% Google A2A compliant

## References
- **Specialist**: `.claude/agents/frameworks/kaizen-specialist.md` lines 115-165
