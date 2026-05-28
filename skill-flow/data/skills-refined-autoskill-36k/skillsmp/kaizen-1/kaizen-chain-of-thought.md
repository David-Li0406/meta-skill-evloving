# Chain of Thought Pattern

CoT pattern with step-by-step reasoning.

## Signature

```python
class ChainOfThoughtSignature(Signature):
    question: str = InputField(description="Question to reason about")
    thoughts: str = OutputField(description="Step-by-step reasoning as JSON list")
    final_answer: str = OutputField(description="Final answer")
```

## Agent

```python
class CoTAgent(BaseAgent):
    def reason(self, question: str) -> dict:
        result = self.run(question=question)
        thoughts = self.extract_list(result, "thoughts", default=[])
        return {"thoughts": thoughts, "reasoning_steps": len(thoughts)}
```

## References
- **Specialist**: `.claude/agents/frameworks/kaizen-specialist.md` lines 215-227
- **Examples**: `apps/kailash-kaizen/examples/1-single-agent/chain-of-thought/`
