# Kaizen Structured Outputs

**Feature**: Multi-provider Structured Outputs with 100% schema compliance and intelligent validation
**Response Handling**: Dict responses from providers are automatically detected and handled by strategies
**Compatibility**: Requires Kaizen 0.8.2+, works with both `AsyncSingleShotStrategy` and `SingleShotStrategy`

---

## Overview

Kaizen provides first-class support for structured outputs across multiple providers (OpenAI, Google/Gemini, Azure AI Foundry) with comprehensive type introspection, enabling 100% reliable JSON schema compliance. The framework supports all 10 Python typing patterns with intelligent strict mode validation and automatic fallback for incompatible types.

**Multi-Provider Support (v0.8.2)**: All providers receive the same OpenAI-style `response_format` configuration. Each provider auto-translates to its native parameters:
- **OpenAI**: Uses `response_format` directly
- **Google/Gemini**: Translates to `response_mime_type` + `response_schema`
- **Azure AI Foundry**: Translates to `JsonSchemaFormat`

This guide covers configuration, type system, signature inheritance, and integration patterns.

---

## Quick Start

### Automatic Configuration (Recommended)

**Most users don't need to configure anything!** When you use BaseAgent with a signature, structured outputs are **automatically configured** for supported providers (OpenAI, Google, Azure).

```python
from kaizen.core.base_agent import BaseAgent
from kaizen.signatures import Signature, InputField, OutputField
from kaizen.core.config import BaseAgentConfig

class QASignature(Signature):
    """Simple Q&A signature."""
    question: str = InputField(desc="User question")
    answer: str = OutputField(desc="Answer to the question")
    confidence: float = OutputField(desc="Confidence score 0-1")

# Structured outputs auto-configured - NO provider_config needed!
config = BaseAgentConfig(
    llm_provider="openai",
    model="gpt-4o-2024-08-06"
)

agent = BaseAgent(config=config, signature=QASignature())
result = agent.run(question="What is AI?")

# Response guaranteed to have all fields with correct types
print(result['answer'])       # Always present, always string
print(result['confidence'])   # Always present, always float
```

**How Auto-Configuration Works** (from `workflow_generator.py`):
- When a signature is provided and no `provider_config` is set
- WorkflowGenerator automatically calls `create_structured_output_config()`
- Uses strict mode for OpenAI (100% schema compliance)
- Providers that don't support structured outputs (Ollama, Anthropic) use prompt-based schema enforcement

**When to Use Manual Configuration**:
- Force legacy JSON mode (`strict=False`) instead of strict schema mode
- Override auto-generated schema with a custom one
- Disable structured outputs entirely (rare)

---

### Manual Configuration with Strict Mode

For advanced use cases requiring explicit control:

```python
from kaizen.core.base_agent import BaseAgent
from kaizen.signatures import Signature, InputField, OutputField
from kaizen.core.config import BaseAgentConfig
from kaizen.core.structured_output import create_structured_output_config

class ProductAnalysisSignature(Signature):
    """Structured product analysis."""
    product_description: str = InputField(desc="Product description")  # 'description=' also works
    category: str = OutputField(desc="Product category")
    price_range: str = OutputField(desc="Price range estimate")
    confidence: float = OutputField(desc="Confidence score 0-1")

# Create structured output config (strict mode)
config = BaseAgentConfig(
    llm_provider="openai",
    model="gpt-4o-2024-08-06",
    provider_config=create_structured_output_config(
        signature=ProductAnalysisSignature(),
        strict=True,
        name="product_analysis"
    )
)

# Create agent with structured outputs
agent = BaseAgent(config=config, signature=ProductAnalysisSignature())

# Run with guaranteed schema compliance
result = agent.run(product_description="Wireless noise-cancelling headphones with 30-hour battery")
print(result)
# Output: {'category': 'Electronics', 'price_range': '$200-$400', 'confidence': 0.95}
```

---

## Configuration Modes

### Strict Mode (Recommended)

**100% schema compliance** with gpt-4o-2024-08-06+

```python
from kaizen.core.structured_output import create_structured_output_config

# Strict mode configuration
provider_config = create_structured_output_config(
    signature=MySignature(),
    strict=True,  # Enforces schema compliance
    name="my_response"
)

config = BaseAgentConfig(
    llm_provider="openai",
    model="gpt-4o-2024-08-06",
    provider_config=provider_config
)
```

**Generated Format:**
```python
{
    "type": "json_schema",
    "json_schema": {
        "name": "my_response",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {...},
            "required": [...],
            "additionalProperties": False
        }
    }
}
```

### Legacy Mode (Best-Effort)

**70-85% reliability** with older models or incompatible types

**When to use:**
- Using older OpenAI models (gpt-3.5-turbo, gpt-4, etc.)
- Signature has types incompatible with strict mode (Dict[str, Any], Union)
- You want fallback compatibility across model versions

**How it works:**
- Returns `{"type": "json_object"}` only (no schema parameter)
- Schema enforcement happens via system prompt automatically
- OpenAI returns any valid JSON (not 100% guaranteed to match schema)

```python
# Legacy mode configuration
provider_config = create_structured_output_config(
    signature=MySignature(),
    strict=False,  # Best-effort JSON object mode
    name="my_response"  # Name is ignored in legacy mode
)

config = BaseAgentConfig(
    llm_provider="openai",
    model="gpt-4",  # Works with older models
    provider_config=provider_config
)
```

**Generated Format:**
```python
{
    "type": "json_object"  # Schema enforcement via system prompt
}
```

---

## Response Handling

OpenAI structured outputs return **dict responses** (pre-parsed JSON), not strings. The framework handles this automatically.

### How It Works

```python
# OpenAI returns dict directly (not a string)
response = {"category": "Electronics", "price_range": "$200-$400", "confidence": 0.95}

# Strategies auto-detect dict responses and return them without parsing
result = agent.run(product_description="Wireless headphones")

# Access fields directly - no JSON parsing needed
print(result['category'])      # "Electronics"
print(result['confidence'])    # 0.95
```

**Key Points:**
- Dict responses are detected automatically by `parse_result()` in both strategies
- No code changes needed - transparent to users
- Works with both strict mode and legacy mode
- Both string responses (traditional) and dict responses (structured outputs) work seamlessly

**Comparison:**
```python
# Traditional (string response, needs parsing)
response = '{"category": "..."}'  # String
result = json.loads(response)     # Manual parsing

# Structured Outputs (dict response, pre-parsed)
response = {"category": "..."}    # Dict
result = response                 # Already parsed
```

---

**Strict Mode vs Legacy Mode:**
| Feature | Strict (`strict=True`) | Legacy (`strict=False`) |
|---------|------------------------|-------------------------|
| **Reliability** | 100% schema compliance | 70-85% best-effort |
| **Models** | gpt-4o-2024-08-06+ | All OpenAI models |
| **Format** | `json_schema` with strict:true | `json_object` only |
| **Schema Enforcement** | OpenAI API (constrained sampling) | System prompt (LLM prompt) |
| **Compatible Types** | str, int, float, bool, List[T], Optional[T], Literal, TypedDict | All types including Dict[str, Any], Union |
| **Use Case** | Production (guaranteed structure) | Legacy models or flexible schemas |

---

## Signature Inheritance

**New in v0.6.3**: Child signatures now **MERGE** parent fields instead of replacing them.

### Parent-Child Inheritance

```python
from kaizen.signatures import Signature, InputField, OutputField

class BaseConversationSignature(Signature):
    """Parent signature with 6 output fields."""
    conversation_text: str = InputField(desc="The conversation text")

    # Parent fields (6 fields)
    next_action: str = OutputField(desc="Next action to take")
    extracted_fields: dict = OutputField(desc="Extracted fields")
    conversation_context: str = OutputField(desc="Context of conversation")
    user_intent: str = OutputField(desc="User intent")
    system_response: str = OutputField(desc="System response")
    confidence_level: float = OutputField(desc="Confidence level 0-1")

class ReferralConversationSignature(BaseConversationSignature):
    """Child signature that EXTENDS parent with 4 additional fields."""

    # Child fields (4 new fields)
    confidence_score: float = OutputField(desc="Confidence score for referral")
    user_identity_detected: bool = OutputField(desc="Whether user identity detected")
    referral_needed: bool = OutputField(desc="Whether referral is needed")
    referral_reason: str = OutputField(desc="Reason for referral")

# Verify field merging
sig = ReferralConversationSignature()
print(f"Total output fields: {len(sig.output_fields)}")  # 10 (6 from parent + 4 from child)
print(f"Parent fields preserved: {all(f in sig.output_fields for f in ['next_action', 'extracted_fields', 'conversation_context', 'user_intent', 'system_response', 'confidence_level'])}")  # True
print(f"Child fields added: {all(f in sig.output_fields for f in ['confidence_score', 'user_identity_detected', 'referral_needed', 'referral_reason'])}")  # True
```

### Multi-Level Inheritance

```python
class Level1Signature(Signature):
    """Level 1: Base signature."""
    input1: str = InputField(desc="Level 1 input")
    output1: str = OutputField(desc="Level 1 output")

class Level2Signature(Level1Signature):
    """Level 2: Extends Level 1."""
    output2: str = OutputField(desc="Level 2 output")

class Level3Signature(Level2Signature):
    """Level 3: Extends Level 2."""
    output3: str = OutputField(desc="Level 3 output")

# Verify multi-level merging
sig = Level3Signature()
print(f"Total output fields: {len(sig.output_fields)}")  # 3 (1 from each level)
assert "output1" in sig.output_fields  # From Level1
assert "output2" in sig.output_fields  # From Level2
assert "output3" in sig.output_fields  # From Level3
```

### Field Overriding

```python
class ParentSignature(Signature):
    """Parent with default field."""
    input_text: str = InputField(desc="Input text")
    result: str = OutputField(desc="Parent result")

class ChildSignature(ParentSignature):
    """Child overrides parent field."""
    result: str = OutputField(desc="Child result (overridden)")
    extra: str = OutputField(desc="Extra field")

# Verify override behavior
sig = ChildSignature()
print(sig.output_fields["result"]["desc"])  # "Child result (overridden)"
print(len(sig.output_fields))  # 2 (parent field overridden + child extra)
```

---

## Integration with BaseAgent

### Manual Provider Config

```python
from kaizen.core.base_agent import BaseAgent
from kaizen.core.config import BaseAgentConfig

# Option 1: Pass provider_config directly to BaseAgentConfig
config = BaseAgentConfig(
    llm_provider="openai",
    model="gpt-4o-2024-08-06",
    provider_config={
        "type": "json_schema",
        "json_schema": {
            "name": "response",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "answer": {"type": "string", "description": "Answer to question"}
                },
                "required": ["answer"],
                "additionalProperties": False
            }
        }
    }
)

agent = BaseAgent(config=config, signature=MySignature())
```

### Using Helper Function

```python
from kaizen.core.structured_output import create_structured_output_config

# Option 2: Use helper function (recommended)
provider_config = create_structured_output_config(
    signature=MySignature(),
    strict=True,
    name="my_response"
)

config = BaseAgentConfig(
    llm_provider="openai",
    model="gpt-4o-2024-08-06",
    provider_config=provider_config
)

agent = BaseAgent(config=config, signature=MySignature())
```

---

## Supported Models

### OpenAI Structured Outputs (Strict Mode)

**Supported Models** (strict=True):
- `gpt-4o-2024-08-06` (recommended)
- `gpt-4o-mini-2024-07-18`
- Newer models released after August 2024

**Features**:
- 100% schema compliance guaranteed
- Automatic validation and error handling
- Supports complex nested objects, arrays, enums
- `additionalProperties: false` enforced by default

### Legacy JSON Object Mode

**Supported Models** (strict=False):
- `gpt-4` / `gpt-4-turbo`
- `gpt-3.5-turbo`
- Any model with JSON mode support

**Features**:
- Best-effort schema compliance (70-85%)
- May produce extra fields or incorrect types
- Requires additional validation in application code

### Google Gemini Structured Outputs (v0.8.2)

**Supported Models**:
- `gemini-2.0-flash` (recommended)
- `gemini-1.5-pro`
- `gemini-1.5-flash`

**Features**:
- Auto-translates OpenAI-style `response_format` to native parameters
- Supports both `json_schema` and `json_object` modes
- Translation: `response_mime_type="application/json"` + `response_schema`

**Usage**:
```python
from kaizen.core.base_agent import BaseAgent
from kaizen.core.config import BaseAgentConfig
from kaizen.core.structured_output import create_structured_output_config

config = BaseAgentConfig(
    llm_provider="google",  # or "gemini"
    model="gemini-2.0-flash",
    provider_config=create_structured_output_config(
        signature=MySignature(),
        strict=True,
        name="my_response"
    )
)

agent = BaseAgent(config=config, signature=MySignature())
result = agent.run(input_text="...")  # Returns structured dict
```

### Azure AI Foundry Structured Outputs (v0.8.2)

**Supported Models**:
- `gpt-4o` (recommended)
- `gpt-4o-mini`
- Other Azure-hosted OpenAI models

**Features**:
- Auto-translates OpenAI-style `response_format` to Azure's `JsonSchemaFormat`
- Full `json_schema` support with strict mode
- Enterprise-grade reliability and compliance

**Usage**:
```python
config = BaseAgentConfig(
    llm_provider="azure",
    model="gpt-4o",
    provider_config=create_structured_output_config(
        signature=MySignature(),
        strict=True,
        name="my_response"
    )
)
```

### Provider Support Matrix (v0.8.2)

| Provider | `json_schema` (Strict) | `json_object` (Legacy) | Auto-Translation |
|----------|------------------------|------------------------|------------------|
| **OpenAI** | ✅ Full support | ✅ Full support | N/A (native) |
| **Google/Gemini** | ✅ Full support | ✅ Full support | `response_mime_type` + `response_schema` |
| **Azure AI Foundry** | ✅ Full support | ✅ Full support | `JsonSchemaFormat` |
| **Ollama** | ❌ Not supported | ❌ Not supported | N/A |
| **Anthropic** | ❌ Not supported | ❌ Not supported | N/A |

---

## Type System & Introspection

### Supported Type Patterns (10 Total)

Kaizen's TypeIntrospector provides comprehensive runtime type checking and JSON schema generation for all Python typing constructs:

| Python Type | JSON Schema | Runtime Validation | Strict Mode Compatible |
|-------------|-------------|-------------------|----------------------|
| `str` | `{"type": "string"}` | ✅ | ✅ |
| `int` | `{"type": "integer"}` | ✅ | ✅ |
| `float` | `{"type": "number"}` | ✅ | ✅ |
| `bool` | `{"type": "boolean"}` | ✅ | ✅ |
| `Literal["A", "B"]` | `{"type": "string", "enum": ["A", "B"]}` | ✅ | ✅ |
| `Union[str, int]` | `{"oneOf": [...]}` | ✅ | ⚠️ Not compatible |
| `Optional[str]` | `{"type": "string"}` (not required) | ✅ | ✅ |
| `List[str]` | `{"type": "array", "items": {"type": "string"}}` | ✅ | ✅ |
| `Dict[str, int]` | `{"type": "object", "additionalProperties": {...}}` | ✅ | ⚠️ Not compatible |
| `TypedDict` | `{"type": "object", "properties": {...}}` | ✅ | ✅ |

### TypeIntrospector Class

The TypeIntrospector handles all type-to-schema conversion and runtime validation:

```python
from kaizen.core.type_introspector import TypeIntrospector
from typing import Literal, Optional, List

# Check type compatibility
type_annotation = Literal["A", "B", "C"]
is_literal = TypeIntrospector.is_literal_type(type_annotation)  # True

# Validate value against type
value = "A"
is_valid, error = TypeIntrospector.validate_value_against_type(value, type_annotation)
# (True, None)

# Convert type to JSON schema
schema = TypeIntrospector.type_to_json_schema(type_annotation, "Category field")
# {"type": "string", "enum": ["A", "B", "C"], "description": "Category field"}

# Check strict mode compatibility
compatible, reason = TypeIntrospector.is_strict_mode_compatible(type_annotation)
# (True, "")
```

### Intelligent Strict Mode Validation

OpenAI's strict mode has specific constraints. Kaizen automatically validates types and provides actionable guidance:

**Incompatible Types**:
- `Union[str, int]` - Produces `oneOf` which is not allowed
- `Dict[str, Any]` - Requires `additionalProperties: true` which is not allowed

**Auto-Fallback** (default behavior):
```python
from kaizen.core.structured_output import create_structured_output_config

class FlexibleSignature(Signature):
    """Signature with Dict[str, Any] - incompatible with strict mode."""
    data: Dict[str, Any] = OutputField(desc="Flexible data")

# Auto-fallback to strict=False with clear warning
config = create_structured_output_config(
    signature=FlexibleSignature(),
    strict=True,           # Requests strict mode
    auto_fallback=True     # Automatically falls back if incompatible (default)
)
# Logs: "OpenAI strict mode incompatibility detected: Field 'data' (Dict[str, Any]):
# requires additionalProperties, not allowed in strict mode. Auto-falling back to strict=False mode."

# Result: {"type": "json_object", "schema": {...}}  # Legacy mode
```

**Strict Validation** (raise errors):
```python
# Disable auto-fallback to get validation errors
config = create_structured_output_config(
    signature=FlexibleSignature(),
    strict=True,
    auto_fallback=False  # Raise error instead of fallback
)
# Raises ValueError with recommendations:
# "OpenAI strict mode incompatibility detected:
#   - Field 'data' (Dict[str, Any]): requires additionalProperties, not allowed in strict mode
#
# Recommendations:
#   1. Use strict=False for flexible schemas (70-85% compliance)
#   2. Replace Dict[str, Any] with List[str] or TypedDict
#   3. Replace Union types with separate Optional fields"
```

## Type Mapping

Kaizen automatically converts Python types to JSON schema types:

| Python Type | JSON Schema Type | Notes |
|-------------|------------------|-------|
| `str` | `"string"` | Basic string type |
| `int` | `"integer"` | Whole numbers |
| `float` | `"number"` | Decimal numbers |
| `bool` | `"boolean"` | True/False |
| `dict` | `"object"` | Nested objects (generic) |
| `list` | `"array"` | Arrays of items (generic) |
| `List[str]` | `{"type": "array", "items": {"type": "string"}}` | Typed arrays |
| `Optional[str]` | Not in `required` | Optional fields |
| `Literal["A", "B"]` | `{"type": "string", "enum": ["A", "B"]}` | Enum-like constraints |

### Complex Type Example

```python
from typing import List, Optional

class ComplexSignature(Signature):
    """Signature with complex types."""
    user_id: str = InputField(desc="User ID")

    # Complex output types
    tags: List[str] = OutputField(desc="List of tags")
    metadata: dict = OutputField(desc="Nested metadata object")
    score: float = OutputField(desc="Numeric score")
    is_valid: bool = OutputField(desc="Validation flag")
    notes: Optional[str] = OutputField(desc="Optional notes")

# Generated JSON schema will be:
{
    "type": "object",
    "properties": {
        "tags": {"type": "array", "items": {"type": "string"}},
        "metadata": {"type": "object"},
        "score": {"type": "number"},
        "is_valid": {"type": "boolean"},
        "notes": {"type": "string"}
    },
    "required": ["tags", "metadata", "score", "is_valid"],  # notes is optional
    "additionalProperties": False
}
```

---

## Troubleshooting

### Issue: TypeError with Literal type validation

**Cause**: Using older version of Kaizen (< 0.6.5)

**Error**: `TypeError: Subscripted generics cannot be used with class and instance checks`

**Solution**: Upgrade to Kaizen 0.6.5+ (fixed with TypeIntrospector)

```bash
pip install --upgrade kailash-kaizen
```

### Issue: "Workflow parameters ['provider_config'] not declared"

**Cause**: Using older version of Kaizen (< 0.6.3)

**Solution**: Upgrade to Kaizen 0.6.5+

```bash
pip install --upgrade kailash-kaizen
```

### Issue: "Invalid schema: additionalProperties must be false"

**Cause**: Using Dict[str, Any] or similar type incompatible with strict mode

**Solution**: Use auto-fallback (default) or replace with compatible type

```python
# Option 1: Auto-fallback (default, recommended)
config = create_structured_output_config(
    signature,
    strict=True,
    auto_fallback=True  # Automatically uses strict=False if incompatible
)

# Option 2: Use compatible types
class FixedSignature(Signature):
    # Replace Dict[str, Any] with TypedDict
    class MetadataDict(TypedDict):
        field1: str
        field2: int

    metadata: MetadataDict = OutputField(desc="Structured metadata")
```

### Issue: Child signature missing parent fields

**Cause**: Using older version of Kaizen (< 0.6.3)

**Solution**: Upgrade to Kaizen 0.6.5+ (fixed in signature inheritance)

```bash
pip install --upgrade kailash-kaizen
```

### Issue: Custom system prompt ignored

**Cause**: Using older version of Kaizen (< 0.6.5) without callback pattern

**Solution**: Upgrade to Kaizen 0.6.5+ and override `_generate_system_prompt()`

```python
class CustomAgent(BaseAgent):
    def _generate_system_prompt(self) -> str:
        return "Your custom prompt here"
```

### Issue: Model returns extra fields not in schema

**Cause**: Using legacy mode (strict=False) with best-effort compliance

**Solution**: Switch to strict mode with supported model

```python
config = BaseAgentConfig(
    llm_provider="openai",
    model="gpt-4o-2024-08-06",  # Use supported model
    provider_config=create_structured_output_config(signature, strict=True)
)
```

### Issue: "Provider config flattened instead of nested"

**Cause**: Using older version of Kaizen (< 0.6.3) with workflow_generator bug

**Solution**: Upgrade to Kaizen 0.6.3+ (fixed in workflow generator)

---

## API Reference

### `create_structured_output_config()`

Create OpenAI-compatible structured output configuration with intelligent validation.

**Signature:**
```python
def create_structured_output_config(
    signature: Any,
    strict: bool = True,
    name: str = "response",
    auto_fallback: bool = True
) -> Dict[str, Any]
```

**Parameters:**
- `signature` (Signature): Kaizen signature instance to convert to JSON schema
- `strict` (bool): Use strict mode (100% compliance) vs legacy mode (best-effort). Default: `True`
- `name` (str): Schema name for OpenAI API. Default: `"response"`
- `auto_fallback` (bool): Automatically fall back to `strict=False` if types are incompatible with strict mode. Default: `True`

**Returns:**
- `Dict[str, Any]`: Provider config dict for BaseAgentConfig

**Raises:**
- `ValueError`: If `strict=True` but signature has incompatible types and `auto_fallback=False`

**Example:**
```python
from kaizen.core.structured_output import create_structured_output_config

# With auto-fallback (recommended)
provider_config = create_structured_output_config(
    signature=MySignature(),
    strict=True,
    name="my_analysis",
    auto_fallback=True  # Falls back to strict=False if types incompatible
)

# Strict validation (raise errors)
provider_config = create_structured_output_config(
    signature=MySignature(),
    strict=True,
    auto_fallback=False  # Raises ValueError on incompatible types
)
```

### `StructuredOutputGenerator.signature_to_json_schema()`

Convert signature to JSON schema dict.

**Signature:**
```python
@staticmethod
def signature_to_json_schema(signature: Any) -> Dict[str, Any]
```

**Parameters:**
- `signature` (Signature): Kaizen signature instance

**Returns:**
- `Dict[str, Any]`: JSON schema dict with properties, required fields, and type mappings

**Example:**
```python
from kaizen.core.structured_output import StructuredOutputGenerator

schema = StructuredOutputGenerator.signature_to_json_schema(MySignature())
print(schema)
# {'type': 'object', 'properties': {...}, 'required': [...]}
```

---

## Best Practices

1. **Use Strict Mode with Auto-Fallback for Production**
   - Guarantees 100% schema compliance when types are compatible
   - Auto-fallback provides graceful degradation for incompatible types
   - Clear warnings guide you to fix type issues
   ```python
   config = create_structured_output_config(
       signature,
       strict=True,
       auto_fallback=True  # Recommended
   )
   ```

2. **Choose Compatible Types for Strict Mode**
   - ✅ Use: `Literal`, `Optional`, `List[T]`, `TypedDict`, basic types
   - ⚠️ Avoid: `Union[T, U]` (except `Optional`), `Dict[str, Any]`
   - Use TypeIntrospector to validate compatibility:
   ```python
   compatible, reason = TypeIntrospector.is_strict_mode_compatible(field_type)
   if not compatible:
       print(f"Warning: {reason}")
   ```

3. **Design Signatures First**
   - Define clear, typed signatures before implementation
   - Use inheritance to share common fields across agents
   - Leverage Python type hints for automatic schema generation
   - Validate types early with TypeIntrospector

4. **Test Inheritance Chains**
   - Verify child signatures merge all parent fields
   - Check field overriding behavior matches expectations
   - Use multi-level inheritance for complex domain models
   - Test that all 10 typing patterns work correctly

5. **Handle Optional Fields**
   - Use `Optional[Type]` for optional fields
   - Optional fields won't be in `required` list
   - Model may return None or omit optional fields

6. **Use Extension Points for Custom Prompts**
   - Override `_generate_system_prompt()` for domain-specific instructions
   - Callback pattern ensures your overrides are used
   - No circular dependencies or complex setup needed

7. **Validate Complex Types**
   - Test nested objects and arrays with real data
   - Verify typed lists (List[str]) generate correct schemas
   - Use TypeIntrospector.validate_value_against_type() in tests
   - Catch schema generation issues early

---

## Examples

### Example 1: Customer Support Agent

```python
from kaizen.core.base_agent import BaseAgent
from kaizen.signatures import Signature, InputField, OutputField
from kaizen.core.config import BaseAgentConfig
from kaizen.core.structured_output import create_structured_output_config
from typing import List

class SupportTicketSignature(Signature):
    """Structured support ticket analysis."""
    ticket_text: str = InputField(desc="Customer support ticket text")

    category: str = OutputField(desc="Ticket category (technical, billing, feature_request)")
    priority: str = OutputField(desc="Priority level (low, medium, high, urgent)")
    sentiment: str = OutputField(desc="Customer sentiment (positive, neutral, negative)")
    action_items: List[str] = OutputField(desc="List of action items for support team")
    estimated_resolution_hours: int = OutputField(desc="Estimated hours to resolve")

# Create agent with structured outputs
config = BaseAgentConfig(
    llm_provider="openai",
    model="gpt-4o-2024-08-06",
    provider_config=create_structured_output_config(
        signature=SupportTicketSignature(),
        strict=True,
        name="support_analysis"
    )
)

agent = BaseAgent(config=config, signature=SupportTicketSignature())

# Process ticket with guaranteed schema compliance
result = agent.run(
    ticket_text="My payment failed but I was still charged! This is the third time this month. Please fix ASAP!"
)

print(result)
# {
#     'category': 'billing',
#     'priority': 'urgent',
#     'sentiment': 'negative',
#     'action_items': ['Verify payment status', 'Process refund if duplicate charge', 'Investigate recurring payment issue'],
#     'estimated_resolution_hours': 2
# }
```

### Example 2: Multi-Level Inheritance

```python
class BaseAnalysisSignature(Signature):
    """Base analysis for all document types."""
    document_text: str = InputField(desc="Document text to analyze")

    summary: str = OutputField(desc="Document summary")
    key_points: List[str] = OutputField(desc="Key points extracted")

class FinancialAnalysisSignature(BaseAnalysisSignature):
    """Financial document analysis extends base."""
    revenue: float = OutputField(desc="Revenue amount")
    expenses: float = OutputField(desc="Expenses amount")
    profit_margin: float = OutputField(desc="Profit margin percentage")

class QuarterlyReportSignature(FinancialAnalysisSignature):
    """Quarterly report extends financial analysis."""
    quarter: str = OutputField(desc="Fiscal quarter (Q1, Q2, Q3, Q4)")
    year: int = OutputField(desc="Fiscal year")
    growth_rate: float = OutputField(desc="YoY growth rate percentage")

# Create agent with multi-level signature
sig = QuarterlyReportSignature()
print(f"Total fields: {len(sig.output_fields)}")  # 8 fields (2 base + 3 financial + 3 quarterly)

config = BaseAgentConfig(
    llm_provider="openai",
    model="gpt-4o-2024-08-06",
    provider_config=create_structured_output_config(sig, strict=True)
)

agent = BaseAgent(config=config, signature=sig)
```

---

## Extension Points

### Custom System Prompts

Override the default system prompt generation in BaseAgent subclasses using the callback pattern:

```python
from kaizen.core.base_agent import BaseAgent

class CustomPromptAgent(BaseAgent):
    """Agent with custom system prompt."""

    def _generate_system_prompt(self) -> str:
        """Override to provide custom prompt logic."""
        return """You are a medical assistant AI.

IMPORTANT: Always advise users to consult a doctor for medical decisions.

Your role is to provide general health information only, not diagnoses."""

# The callback pattern automatically uses your custom prompt
agent = CustomPromptAgent(config=config, signature=signature)
# WorkflowGenerator receives _generate_system_prompt as callback
# Custom prompt is used in workflow generation
```

**How It Works**:
1. BaseAgent passes `_generate_system_prompt` method as callback to WorkflowGenerator
2. WorkflowGenerator calls the callback when building workflows
3. Your override is used instead of the default signature-based prompt
4. No circular dependencies - clean callback pattern

**Use Cases**:
- Domain-specific instructions (medical, legal, financial)
- Compliance requirements (disclaimers, safety warnings)
- Custom formatting preferences
- Integration with external prompt management systems

---

## Version History

### v0.6.5 (Current)
- ✅ TypeIntrospector: Comprehensive type introspection for all 10 Python typing patterns
- ✅ Intelligent strict mode validation with auto-fallback for incompatible types
- ✅ Extension point callback pattern for custom system prompts
- ✅ Literal type validation fix (no more TypeError crashes)
- ✅ Clear error messages with actionable recommendations
- ✅ Zero breaking changes (100% backward compatible)

### v0.6.3
- ✅ OpenAI Structured Outputs API support (strict mode)
- ✅ Signature inheritance field merging (MERGE not REPLACE)
- ✅ provider_config nested dict preservation
- ✅ LLMAgentNode provider_config parameter support

### v0.6.2 (Legacy)
- ❌ No OpenAI Structured Outputs support
- ❌ Signature inheritance replaced parent fields
- ❌ provider_config blocked by workflow validation
- ❌ Literal type validation crashes

---

## Further Reading

- [Kaizen BaseAgent Architecture](../../apps/kailash-kaizen/docs/guides/baseagent-architecture.md)
- [Signature Programming Guide](../../apps/kailash-kaizen/docs/guides/signature-programming.md)
- [OpenAI Structured Outputs Documentation](https://platform.openai.com/docs/guides/structured-outputs)
- [Kaizen Configuration Guide](../../apps/kailash-kaizen/docs/reference/configuration.md)
