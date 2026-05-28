# Kaizen UX Helpers

Convenience methods for result extraction, memory management, and defensive parsing in Kaizen agents.

## UX Improvements Overview

Kaizen provides **convenience methods** to eliminate boilerplate:
- `extract_*()` - Defensive result parsing (list, dict, float, str)
- `write_to_memory()` - Concise shared memory writes
- Config auto-extraction - No manual BaseAgentConfig creation

**Code Reduction**: ~40-60% less boilerplate in agent methods.

## Extract Methods

### extract_list()

Extract lists from agent results with defensive parsing:

```python
from kaizen.core.base_agent import BaseAgent

class MyAgent(BaseAgent):
    def process(self, input_data: str) -> dict:
        result = self.run(input_field=input_data)

        # OLD WAY (verbose, error-prone)
        field_raw = result.get("items", "[]")
        try:
            items = json.loads(field_raw) if isinstance(field_raw, str) else field_raw
            if not isinstance(items, list):
                items = []
        except:
            items = []

        # NEW WAY (one line, defensive)
        items = self.extract_list(result, "items", default=[])

        return {"items": items, "count": len(items)}
```

**Parameters:**
- `result` (dict): Agent execution result
- `key` (str): Field name to extract
- `default` (list): Default value if extraction fails

**Returns:** List or default value

**Handles:**
- ✅ Missing keys
- ✅ JSON strings (`"[1, 2, 3]"`)
- ✅ Already-parsed lists
- ✅ Invalid JSON
- ✅ Non-list values

### extract_dict()

Extract dictionaries with defensive parsing:

```python
class MyAgent(BaseAgent):
    def process(self, data: str) -> dict:
        result = self.run(data=data)

        # Extract metadata as dict
        metadata = self.extract_dict(result, "metadata", default={})

        # Safe access to nested values
        timestamp = metadata.get("timestamp", "unknown")
        author = metadata.get("author", "anonymous")

        return {"metadata": metadata, "timestamp": timestamp}
```

**Parameters:**
- `result` (dict): Agent execution result
- `key` (str): Field name to extract
- `default` (dict): Default value if extraction fails

**Handles:**
- ✅ Missing keys
- ✅ JSON strings (`'{"key": "value"}'`)
- ✅ Already-parsed dicts
- ✅ Invalid JSON
- ✅ Non-dict values

### extract_float()

Extract numeric values with type coercion:

```python
class MyAgent(BaseAgent):
    def analyze(self, text: str) -> dict:
        result = self.run(text=text)

        # Extract numeric scores
        confidence = self.extract_float(result, "confidence", default=0.0)
        quality_score = self.extract_float(result, "quality_score", default=0.0)

        # Validate ranges
        confidence = max(0.0, min(1.0, confidence))  # Clamp to [0, 1]

        return {
            "confidence": confidence,
            "quality_score": quality_score,
            "is_high_quality": quality_score > 0.8
        }
```

**Parameters:**
- `result` (dict): Agent execution result
- `key` (str): Field name to extract
- `default` (float): Default value if extraction fails

**Handles:**
- ✅ Missing keys
- ✅ String numbers (`"0.95"`)
- ✅ Integer values (auto-converts to float)
- ✅ Invalid formats
- ✅ NaN/Infinity

### extract_str()

Extract strings with safe conversion:

```python
class MyAgent(BaseAgent):
    def process(self, question: str) -> dict:
        result = self.run(question=question)

        # Extract string fields
        answer = self.extract_str(result, "answer", default="No answer available")
        reasoning = self.extract_str(result, "reasoning", default="")

        # Clean up whitespace
        answer = answer.strip()

        return {"answer": answer, "reasoning": reasoning}
```

**Parameters:**
- `result` (dict): Agent execution result
- `key` (str): Field name to extract
- `default` (str): Default value if extraction fails

**Handles:**
- ✅ Missing keys
- ✅ Non-string values (converts to string)
- ✅ None values
- ✅ Numeric values
- ✅ Objects with `__str__()`

## Memory Helpers

### write_to_memory()

Concise method to write to SharedMemoryPool:

```python
from kaizen.memory.shared_memory import SharedMemoryPool

class MyAgent(BaseAgent):
    def __init__(self, config, shared_memory: SharedMemoryPool, agent_id: str):
        super().__init__(config=config, signature=MySignature())
        self.shared_memory = shared_memory
        self.agent_id = agent_id

    def process(self, data: str) -> dict:
        result = self.run(data=data)

        # OLD WAY (verbose)
        if self.shared_memory:
            self.shared_memory.write_insight({
                "agent_id": self.agent_id,
                "content": json.dumps(result),
                "tags": ["processing"],
                "importance": 0.9
            })

        # NEW WAY (concise, auto-serializes)
        self.write_to_memory(
            content=result,  # Auto-serialized to JSON
            tags=["processing"],
            importance=0.9
        )

        return result
```

**Parameters:**
- `content` (any): Content to write (auto-serialized if dict/list)
- `tags` (list): Tags for categorization
- `importance` (float): Importance score 0.0-1.0

**Features:**
- ✅ Auto-serializes dicts/lists to JSON
- ✅ Checks if shared_memory is available
- ✅ Adds agent_id automatically
- ✅ Safe no-op if memory not configured
- ✅ Handles serialization errors gracefully

### read_from_memory()

Read relevant insights from shared memory:

```python
class MyAgent(BaseAgent):
    def process_with_context(self, query: str) -> dict:
        # Read relevant context from shared memory
        context_insights = self.read_from_memory(
            tags=["research", "analysis"],
            exclude_own=True,  # Don't read own insights
            limit=5
        )

        # Extract content from insights
        context_texts = [
            insight.get("content", "")
            for insight in context_insights
        ]

        # Use context in agent execution
        result = self.run(
            query=query,
            context="\n".join(context_texts)
        )

        return result
```

## Pattern: Complete Agent with Helpers

```python
from kaizen.core.base_agent import BaseAgent
from kaizen.signatures import Signature, InputField, OutputField
from kaizen.memory.shared_memory import SharedMemoryPool
from dataclasses import dataclass

class AnalysisSignature(Signature):
    text: str = InputField(description="Text to analyze")

    sentiment: str = OutputField(description="Sentiment category")
    confidence: float = OutputField(description="Confidence score")
    keywords: List[str] = OutputField(description="Key terms as JSON array")
    metadata: dict = OutputField(description="Metadata as JSON object")

@dataclass
class AnalysisConfig:
    llm_provider: str = "openai"
    model: str = "gpt-4"
    temperature: float = 0.3

class AnalysisAgent(BaseAgent):
    def __init__(
        self,
        config: AnalysisConfig,
        shared_memory: SharedMemoryPool = None,
        agent_id: str = "analyzer"
    ):
        super().__init__(config=config, signature=AnalysisSignature())
        self.shared_memory = shared_memory
        self.agent_id = agent_id

    def analyze(self, text: str) -> dict:
        result = self.run(text=text)

        # Use extract helpers for defensive parsing
        sentiment = self.extract_str(result, "sentiment", default="neutral")
        confidence = self.extract_float(result, "confidence", default=0.0)
        keywords = self.extract_list(result, "keywords", default=[])
        metadata = self.extract_dict(result, "metadata", default={})

        # Validate and clean
        confidence = max(0.0, min(1.0, confidence))
        keywords = [k.strip().lower() for k in keywords if k.strip()]

        # Write to shared memory
        self.write_to_memory(
            content={
                "text": text[:100],  # First 100 chars
                "sentiment": sentiment,
                "confidence": confidence,
                "keywords": keywords
            },
            tags=["analysis", sentiment],
            importance=confidence
        )

        return {
            "sentiment": sentiment,
            "confidence": confidence,
            "keywords": keywords,
            "metadata": metadata
        }
```

## Benefits: Code Reduction

### Without Helpers (Verbose)

```python
def process(self, data: str) -> dict:
    result = self.run(data=data)

    # Manual list extraction (12 lines)
    items_raw = result.get("items", "[]")
    try:
        items = json.loads(items_raw) if isinstance(items_raw, str) else items_raw
        if not isinstance(items, list):
            items = []
    except:
        items = []

    # Manual dict extraction (12 lines)
    metadata_raw = result.get("metadata", "{}")
    try:
        metadata = json.loads(metadata_raw) if isinstance(metadata_raw, str) else metadata_raw
        if not isinstance(metadata, dict):
            metadata = {}
    except:
        metadata = {}

    # Manual memory write (10 lines)
    if self.shared_memory:
        try:
            self.shared_memory.write_insight({
                "agent_id": self.agent_id,
                "content": json.dumps(result),
                "tags": ["processing"],
                "importance": 0.9
            })
        except:
            pass

    return {"items": items, "metadata": metadata}
```

**Total: 34 lines**

### With Helpers (Concise)

```python
def process(self, data: str) -> dict:
    result = self.run(data=data)

    # Extract helpers (2 lines)
    items = self.extract_list(result, "items", default=[])
    metadata = self.extract_dict(result, "metadata", default={})

    # Memory helper (1 line)
    self.write_to_memory(content=result, tags=["processing"], importance=0.9)

    return {"items": items, "metadata": metadata}
```

**Total: 5 lines (85% reduction)**

## Error Handling

All helpers handle errors gracefully:

```python
# Safe with missing keys
result = {}
items = self.extract_list(result, "nonexistent", default=[])  # Returns []

# Safe with invalid JSON
result = {"items": "[invalid json"}
items = self.extract_list(result, "items", default=[])  # Returns []

# Safe with wrong types
result = {"confidence": "not a number"}
conf = self.extract_float(result, "confidence", default=0.0)  # Returns 0.0

# Safe with no memory configured
self.write_to_memory(content="data", tags=["test"])  # No-op, no error
```

## CRITICAL RULES

**ALWAYS:**
- ✅ Use extract_*() for agent results
- ✅ Provide sensible defaults
- ✅ Use write_to_memory() for shared memory
- ✅ Validate extracted values after extraction

**NEVER:**
- ❌ Manual JSON parsing (use extract_*())
- ❌ Verbose write_insight() (use write_to_memory())
- ❌ Skip validation after extraction
- ❌ Assume fields exist in results

## Related Skills

- **kaizen-baseagent-quick** - BaseAgent with helpers
- **kaizen-config-patterns** - Config auto-extraction
- **kaizen-shared-memory** - Memory management patterns

## References

- **Source**: `apps/kailash-kaizen/src/kaizen/core/base_agent.py`
- **Specialist**: `.claude/agents/frameworks/kaizen-specialist.md` lines 249-298
