---
name: llm-integration-patterns
description: Patterns for LLM integration in GUTTERS. Covers factory usage, prompt engineering, fallbacks, and activity logging.
---

# LLM Integration Patterns

Standard patterns for multi-tier LLM usage in GUTTERS modules.

## Multi-Tier Architecture

GUTTERS uses a tiered LLM approach to balance reasoning quality and cost-efficiency.

| Tier | Model | Purpose | Cost (AUD/1K) |
|------|-------|---------|---------------|
| **PREMIUM** | `anthropic/claude-sonnet-4.5` | User-facing chat, complex synthesis | $0.0046 / $0.0231 |
| **STANDARD** | `anthropic/claude-haiku-4.5` | Classification, background tasks | $0.00038 / $0.0019 |

## LLM Tiered Factory

Always use the tiered factory to ensure correct model selection and cost tracking.

```python
from src.app.core.llm.config import get_premium_llm, get_standard_llm, LLMTier

# 1. Premium: Best for user-facing responses
llm = get_premium_llm()

# 2. Standard: Best for high-volume background tasks (12x cheaper!)
llm = get_standard_llm()

# 3. Dynamic Tier (from config or user preference)
from src.app.core.llm.config import LLMConfig
llm = LLMConfig.get_llm(LLMTier.STANDARD)
```

## Temperature Guidelines

| Task | Temperature | Tier | Why |
|------|-------------|------|-----|
| JSON generation | 0.3-0.5 | Standard | Needs structure consistency |
| Profile Synthesis | 0.7 | Premium | High-fidelity reasoning |
| Conversational probes | 0.7 | Premium | Natural variation |
| Classification | 0.0-0.2 | Standard | Deterministic |

## Prompt Engineering

### JSON Output Pattern
```python
prompt = f"""You are helping determine {field} for {context}.

Requirements:
- Return ONLY valid JSON
- No markdown formatting
- Include all required fields

Return JSON:
{{
    "field1": "...",
    "field2": [...],
    "mappings": {{...}}
}}

Generate now:"""
```

### Parsing JSON from LLM
```python
def _parse_llm_response(content: str) -> dict:
    import json
    
    try:
        # Try markdown block first
        if "```json" in content:
            json_str = content.split("```json")[1].split("```")[0]
        elif "{" in content:
            # Find JSON bounds
            start = content.index("{")
            end = content.rindex("}") + 1
            json_str = content[start:end]
        else:
            raise ValueError("No JSON found")
        
        return json.loads(json_str)
    except Exception:
        # Return minimal fallback
        return {"error": "parse_failed", "raw": content[:200]}
```

## Fallback Pattern

ALWAYS have fallback when LLM fails:

```python
async def generate_with_llm(input_data: InputData) -> Result:
    try:
        response = await llm.ainvoke(prompt)
        result = parse_response(response.content)
        return Result(**result)
        
    except Exception as e:
        logger.warning(f"LLM failed, using fallback: {e}")
        return _fallback_result(input_data)

def _fallback_result(input_data: InputData) -> Result:
    """Template-based fallback when LLM unavailable."""
    return Result(
        content=f"Default for {input_data.type}...",
        source="fallback",
    )
```

## Activity Logging & Cost Tracking (REQUIRED)

Every LLM call MUST be logged with model details and AUD cost estimation.

```python
from src.app.core.llm.config import LLMConfig, LLMTier
from src.app.core.activity.logger import get_activity_logger

logger = get_activity_logger()

# 1. Before call
await logger.log_activity(
    trace_id=trace_id,
    agent="module.component",
    activity_type="llm_call_started",
    details={
        "tier": LLMTier.PREMIUM,
        "purpose": "query_analysis",
    }
)

# 2. After call (calculate and log cost)
tokens_in = len(prompt.split()) * 1.3
tokens_out = len(response.content.split()) * 1.3
cost_aud = LLMConfig.estimate_cost(LLMTier.PREMIUM, int(tokens_in), int(tokens_out), currency="AUD")

await logger.log_llm_call(
    trace_id=trace_id,
    model_id="anthropic/claude-sonnet-4.5",
    prompt=prompt[:500],
    response=response.content[:500],
    duration_ms=duration,
    cost_aud=cost_aud, # Log AUD for user transparency
)
```

## Error Handling

```python
from langchain_core.exceptions import OutputParserException

try:
    response = await llm.ainvoke(prompt)
except OutputParserException as e:
    logger.error(f"LLM output parsing failed: {e}")
    return fallback()
except Exception as e:
    logger.error(f"LLM call failed: {e}")
    # Log to activity
    await logger.log_activity(
        agent="module",
        activity_type="llm_call_failed",
        details={"error": str(e)}
    )
    return fallback()
---

## Multi-Model User Preferences

Allow users to select their preferred LLM for specific high-value interactions.

### Preferred Models (Standardized IDs)
```python
ALLOWED_MODELS = [
    "anthropic/claude-sonnet-4.5",  # Default / Premium
    "anthropic/claude-haiku-4.5",   # Efficient
    "anthropic/claude-3-opus",     # Legacy Premium
]
DEFAULT_MODEL = "anthropic/claude-sonnet-4.5"
```

---

## Embedding Service Pattern

For semantic search and knowledge retrieval, use the `EmbeddingService`.

```python
from src.app.modules.intelligence.vector.embedding_service import EmbeddingService

service = EmbeddingService(api_key=settings.OPENROUTER_API_KEY.get_secret_value())

# Embed text
vector = await service.embed_text("User query or content piece")

# Module-specific helpers
vector = await service.embed_journal_entry(entry)
```

### Best Practices
- **Standardize Dimensions**: Ensure all embeddings in a table use the same model/dimensions.
- **AUD Visibility**: When exposing RAG costs, convert using `LLMConfig.AUD_EXCHANGE_RATE`.

---

## Checklist

- [ ] Use `LLMConfig.get_llm(tier)` or tier-specific factory
- [ ] Set appropriate tier (Premium for user-facing, Standard for background)
- [ ] Set appropriate temperature for task
- [ ] Estimate and log cost in **AUD**
- [ ] Parse JSON with fallback handling
- [ ] Truncate storage fields to prevent JSONB bloat
- [ ] Handle `OutputParserException` specifically
- [ ] Validate any model overrides against standardized IDs

