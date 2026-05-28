# Kaizen Signature Programming

Complete guide to signature-based programming with InputField and OutputField for type-safe AI agent I/O.

## What are Signatures?

Signatures define **type-safe inputs and outputs** for AI agents. Think of them as contracts that specify what data an agent accepts and produces.

**Benefits:**
- ✅ Type safety - catch errors at design time
- ✅ Auto-validation - framework validates inputs/outputs
- ✅ Self-documenting - descriptions built into code
- ✅ LLM-friendly - descriptions become prompt context
- ✅ A2A integration - automatic capability card generation

## Basic Signature Pattern

```python
from kaizen.signatures import Signature, InputField, OutputField

class QASignature(Signature):
    """Signature docstring becomes system prompt context."""

    # Input Fields
    question: str = InputField(
        description="User question to answer"
    )
    context: str = InputField(
        description="Additional context if available",
        default=""  # Optional field with default
    )

    # Output Fields
    answer: str = OutputField(
        description="Clear, accurate answer"
    )
    confidence: float = OutputField(
        description="Confidence score between 0.0 and 1.0"
    )
    reasoning: str = OutputField(
        description="Brief explanation of reasoning"
    )
```

## InputField vs OutputField

### InputField - What Agent Receives

```python
# Basic input
prompt: str = InputField(description="User prompt")

# With default (makes field optional)
temperature: float = InputField(
    description="Sampling temperature",
    default=0.7
)

# With validation
max_tokens: int = InputField(
    description="Maximum tokens to generate",
    default=1000,
    ge=1,  # Greater than or equal to 1
    le=4000  # Less than or equal to 4000
)

# Multiple types
context: Union[str, List[str]] = InputField(
    description="Context as string or list of strings"
)
```

### OutputField - What Agent Produces

```python
# Simple output
answer: str = OutputField(description="Agent response")

# Structured output
analysis: dict = OutputField(
    description="Analysis results as JSON object"
)

# Lists
sources: List[str] = OutputField(
    description="List of source citations"
)

# Numeric with constraints
confidence: float = OutputField(
    description="Confidence score",
    ge=0.0,
    le=1.0
)
```

## Field Properties

### Description (Required)

Descriptions are **critical** - they become part of the LLM prompt:

```python
# ❌ BAD - Vague description
answer: str = OutputField(description="The answer")

# ✅ GOOD - Specific, actionable description
answer: str = OutputField(
    description="Concise answer to the user's question, 2-3 sentences maximum"
)
```

### Default Values (Optional Fields)

```python
class MySignature(Signature):
    # Required field (no default)
    question: str = InputField(description="User question")

    # Optional field (with default)
    context: str = InputField(description="Additional context", default="")
    temperature: float = InputField(description="Temperature", default=0.7)
```

### Validation Constraints

```python
from pydantic import Field

class ValidatedSignature(Signature):
    # Numeric constraints
    temperature: float = InputField(
        description="Sampling temperature",
        ge=0.0,  # Greater than or equal
        le=1.0   # Less than or equal
    )

    # String constraints
    answer: str = OutputField(
        description="Answer text",
        min_length=10,  # Minimum length
        max_length=500  # Maximum length
    )

    # Pattern matching
    email: str = InputField(
        description="User email",
        pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$"
    )
```

## Common Signature Patterns

### 1. Question Answering

```python
class QASignature(Signature):
    """Answer questions accurately with confidence scoring."""
    question: str = InputField(description="User question")
    context: str = InputField(description="Relevant context", default="")

    answer: str = OutputField(description="Accurate, concise answer")
    confidence: float = OutputField(description="Confidence 0.0-1.0")
```

### 2. Chain of Thought

```python
class ChainOfThoughtSignature(Signature):
    """Solve problems step-by-step with explicit reasoning."""
    question: str = InputField(description="Problem to solve")

    reasoning_steps: List[str] = OutputField(
        description="List of reasoning steps as JSON array"
    )
    final_answer: str = OutputField(description="Final answer")
```

### 3. Code Generation

```python
class CodeGenerationSignature(Signature):
    """Generate code based on specifications."""
    specification: str = InputField(description="Code requirements")
    language: str = InputField(description="Programming language", default="python")

    code: str = OutputField(description="Generated code")
    explanation: str = OutputField(description="Code explanation")
    test_cases: List[str] = OutputField(description="Example test cases")
```

### 4. Sentiment Analysis

```python
class SentimentSignature(Signature):
    """Analyze sentiment of text."""
    text: str = InputField(description="Text to analyze")

    sentiment: str = OutputField(
        description="Sentiment category: positive, negative, or neutral"
    )
    confidence: float = OutputField(description="Confidence score 0.0-1.0")
    explanation: str = OutputField(description="Brief reasoning")
```

### 5. RAG (Retrieval-Augmented Generation)

```python
class RAGSignature(Signature):
    """Answer questions using retrieved documents."""
    query: str = InputField(description="User query")
    documents: str = InputField(description="Retrieved documents as JSON")

    answer: str = OutputField(description="Answer based on documents")
    sources: List[str] = OutputField(description="Source document IDs")
    confidence: float = OutputField(description="Answer confidence 0.0-1.0")
```

## Multi-Modal Signatures

### Vision Signature

```python
from kaizen.signatures.multi_modal import ImageField

class VisionSignature(Signature):
    """Analyze images with text questions."""
    image: ImageField = InputField(description="Image to analyze")
    question: str = InputField(description="Question about the image")

    answer: str = OutputField(description="Answer about image content")
    objects_detected: List[str] = OutputField(description="Objects in image")
```

### Audio Signature

```python
from kaizen.signatures.multi_modal import AudioField

class TranscriptionSignature(Signature):
    """Transcribe audio files."""
    audio: AudioField = InputField(description="Audio file to transcribe")
    language: str = InputField(description="Language hint", default=None)

    transcription: str = OutputField(description="Transcribed text")
    duration: float = OutputField(description="Audio duration in seconds")
    language: str = OutputField(description="Detected language")
```

## Enterprise Extensions

### With Audit Trail

```python
class AuditedSignature(Signature):
    """Signature with audit fields."""
    # Inputs
    request: str = InputField(description="User request")

    # Outputs
    response: str = OutputField(description="Agent response")

    # Audit fields
    timestamp: str = OutputField(description="Response timestamp")
    agent_id: str = OutputField(description="Agent identifier")
    session_id: str = OutputField(description="Session identifier")
```

### With Compliance

```python
class ComplianceSignature(Signature):
    """Signature with compliance checking."""
    content: str = InputField(description="Content to check")
    policies: str = InputField(description="Policies as JSON")

    compliant: bool = OutputField(description="Compliance status")
    violations: List[str] = OutputField(description="Policy violations found")
    compliance_score: float = OutputField(description="Score 0.0-1.0")
    recommendations: List[str] = OutputField(description="Fix recommendations")
```

## Signature Usage in BaseAgent

```python
from kaizen.core.base_agent import BaseAgent

class MyAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(config=config, signature=QASignature())

    def ask(self, question: str, context: str = "") -> dict:
        # Signature validates inputs and structures outputs
        result = self.run(question=question, context=context)

        # Result is guaranteed to have signature output fields
        assert "answer" in result
        assert "confidence" in result

        return result
```

## Signature Validation

### Automatic Validation

BaseAgent automatically validates:
- ✅ All required input fields are provided
- ✅ Input types match signature definitions
- ✅ Constraints are satisfied (ge, le, min_length, etc.)
- ✅ Output contains all required fields
- ✅ Output types match signature definitions

### Manual Validation

```python
from kaizen.signatures import SignatureValidator

validator = SignatureValidator()

# Validate inputs
inputs = {"question": "What is AI?", "context": ""}
is_valid, errors = validator.validate_inputs(QASignature(), inputs)

if not is_valid:
    print(f"Validation errors: {errors}")

# Validate outputs
outputs = {"answer": "AI is...", "confidence": 0.9}
is_valid, errors = validator.validate_outputs(QASignature(), outputs)
```

## Advanced: Dynamic Signatures

```python
def create_qa_signature(include_reasoning: bool = True):
    """Factory function to create signatures dynamically."""
    fields = {
        "question": (str, InputField(description="User question")),
        "answer": (str, OutputField(description="Answer")),
    }

    if include_reasoning:
        fields["reasoning"] = (str, OutputField(description="Reasoning"))

    return type("DynamicQASignature", (Signature,), fields)
```

## CRITICAL RULES

**Descriptions:**
- ✅ Be specific and actionable
- ✅ Include format expectations (e.g., "as JSON array")
- ✅ Specify length/range constraints in description
- ❌ Don't use vague descriptions like "the answer"

**Defaults:**
- ✅ Use defaults for optional fields
- ✅ Set sensible defaults (0.7 for temperature, not 0.0)
- ❌ Don't make all fields optional

**Types:**
- ✅ Use specific types (str, int, float, List[str], dict)
- ✅ Use Union for multiple accepted types
- ❌ Don't use generic types like Any unless necessary

**Validation:**
- ✅ Add constraints (ge, le, min_length, max_length)
- ✅ Use patterns for format validation (email, URL, etc.)
- ❌ Don't skip validation for critical fields

## Related Skills

- **kaizen-baseagent-quick** - Using signatures with BaseAgent
- **kaizen-config-patterns** - Configuration with signatures
- **kaizen-multimodal-pitfalls** - Multi-modal signature issues

## References

- **Source**: `apps/kailash-kaizen/src/kaizen/signatures/`
- **Examples**: All agents in `apps/kailash-kaizen/examples/`
- **Tests**: `apps/kailash-kaizen/tests/unit/signatures/`
