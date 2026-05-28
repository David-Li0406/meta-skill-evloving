# DSPy Adapters

Adapters bridge DSPy modules with Language Models, handling prompt formatting and output parsing. This guide covers adapter architecture and usage.

## Table of Contents

- [Adapter Overview](#adapter-overview)
- [Adapter Architecture](#adapter-architecture)
- [ChatAdapter](#chatadapter)
- [JSONAdapter](#jsonadapter)
- [Custom Adapters](#custom-adapters)
- [Multi-Provider Configuration](#multi-provider-configuration)

## Adapter Overview

### What are Adapters?

Adapters are the interface layer that transforms DSPy modules/signatures into LM prompts and parses LM responses back into structured data.

### Where Adapters Fit in the System

```
1. User calls DSPy module with inputs
   ↓
2. Module calls dspy.Predict
   ↓
3. Adapter.format() converts signature + inputs → LM messages
   ↓
4. Language Model generates response
   ↓
5. Adapter.parse() converts LM response → structured outputs
   ↓
6. Module returns structured outputs to user
```

### Why Use Adapters?

- **Automatic formatting**: No manual prompt engineering
- **Type validation**: Enforces signature field types
- **Multi-provider support**: Same code works across different LMs
- **Conversation history**: Manages multi-turn conversations
- **Native features**: Enables function calling, citations, etc.

## Adapter Architecture

### Base Adapter Class

```python
import dspy

class dspy.Adapter:
    """
    Base adapter class for bridging DSPy modules with LMs.

    Manages the transformation pipeline from DSPy inputs to LM prompts
    and from LM responses to structured DSPy outputs.
    """

    def format(self, signature, demos, inputs):
        """Format signature + demos + inputs into LM messages."""
        pass

    def parse(self, signature, output):
        """Parse LM output into structured DSPy data."""
        pass
```

### Message Structure

Adapters format messages in recommended structure:

```python
[
    {"role": "system", "content": system_message},
    # Few-shot examples
    {"role": "user", "content": few_shot_example_1_input},
    {"role": "assistant", "content": few_shot_example_1_output},
    # Conversation history
    {"role": "user", "content": history_1_input},
    {"role": "assistant", "content": history_1_output},
    # Current input
    {"role": "user", "content": current_input},
]
```

### System Message Components

System message contains:
1. **Field descriptions**: Purpose of each input/output field
2. **Field structure**: Input vs output field types
3. **Task description**: High-level explanation of what to do

## ChatAdapter

### Basic ChatAdapter Usage

```python
import dspy

# Create signature
signature = dspy.Signature("question -> answer")

# Format system message
system_message = dspy.ChatAdapter().format_system_message(signature)
print(system_message)
```

### System Message Format

```python
system_message = """
You are a helpful assistant.

Your task is to answer the given question.

Input fields:
- question (str): The question to answer

Output fields:
- answer (str): The answer to the question
"""
```

### ChatAdapter in Module

```python
class MyModule(dspy.Module):
    def __init__(self):
        super().__init__()
        # ChatAdapter is used automatically by dspy.Predict
        self.predict = dspy.Predict(MySignature)

    def forward(self, question: str):
        return self.predict(question=question)
```

## JSONAdapter

### JSONAdapter for Structured Output

```python
import dspy

# Create signature with type hints
class StructuredOutput(dspy.Signature):
    question = dspy.InputField(desc="Question to answer")
    answer = dspy.OutputField(desc="Answer to the question")
    confidence: float = dspy.OutputField(desc="Confidence score")
    reasoning: str = dspy.OutputField(desc="Reasoning steps")

# Use JSONAdapter for structured output
module = dspy.Predict(StructuredOutput)
result = module(question="What is the capital of France?")

print(result.answer)
print(result.confidence)
print(result.reasoning)
```

### JSONAdapter Format Method

```python
def format(
    self,
    signature: type[Signature],
    demos: list[dict[str, Any]],
    inputs: dict[str, Any],
) -> list[dict[str, Any]]:
    """
    Format inputs into multi-turn messages.

    Converts DSPy structured input along with few-shot examples and
    conversation history into multiturn messages for the LM.
    """
    # Format system message
    messages = []
    system_message = self.format_system_message(signature)
    messages.append({"role": "system", "content": system_message})

    # Format few-shot examples
    messages.extend(self.format_demos(signature, demos))

    # Format current input
    messages.append({
        "role": "user",
        "content": self.format_user_message_content(signature, inputs)
    })

    return messages
```

## Custom Adapters

### Custom Cache Key Implementation

```python
import dspy
from typing import Dict, Any, Optional
import ujson
from hashlib import sha256

class CustomCache(dspy.clients.Cache):

    def cache_key(
        self,
        request: dict[str, Any],
        ignored_args_for_cache_key: Optional[list[str]] = None
    ) -> str:
        """
        Generate custom cache key.

        This example creates key based solely on messages,
        ignoring other parameters.
        """
        messages = request.get("messages", [])
        return sha256(ujson.dumps(messages, sort_keys=True).encode()).hexdigest()

# Configure custom cache
dspy.cache = CustomCache(
    enable_disk_cache=True,
    enable_memory_cache=True,
    disk_cache_dir=dspy.clients.DISK_CACHE_DIR
)
```

### Custom Adapter for Special Format

```python
class MyCustomAdapter(dspy.Adapter):
    """Custom adapter for special output format."""

    def format_user_message_content(
        self,
        signature,
        inputs,
        main_request=True
    ):
        """Custom input formatting."""
        # Format input as special XML tags
        content = "<input>\n"
        for field_name, field_value in inputs.items():
            content += f"  <{field_name}>{field_value}</{field_name}>\n"
        content += "</input>"
        return content

    def parse(
        self,
        signature,
        output
    ):
        """Custom output parsing."""
        # Parse output from special XML tags
        import xml.etree.ElementTree as ET

        root = ET.fromstring(f"<output>{output}</output>")

        result = {}
        for field in signature.output_fields:
            field_elem = root.find(field)
            if field_elem is not None:
                result[field] = field_elem.text

        return dspy.Prediction(**result)
```

### Using Custom Adapter

```python
# Create module with custom adapter
adapter = MyCustomAdapter()

class MyModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict(
            MySignature,
            adapter=adapter  # Use custom adapter
        )

    def forward(self, input_data):
        return self.predict(input=input_data)
```

## Multi-Provider Configuration

### Configure with LiteLLM

```python
import dspy

# OpenAI
lm = dspy.LM("openai/gpt-4o-mini", api_key="YOUR_KEY")

# Anthropic
lm = dspy.LM("anthropic/claude-3-opus-20240229")

# Together AI
lm = dspy.LM("together_ai/meta-llama/Llama-2-70b-chat-hf")

# General provider (via LiteLLM)
lm = dspy.LM(
    "openai/your-model-name",
    api_key="PROVIDER_API_KEY",
    api_base="YOUR_PROVIDER_URL"
)

# Configure DSPy
dspy.configure(lm=lm)
```

### Switching LMs Globally

```python
import dspy

# Configure LM globally
dspy.configure(lm=dspy.LM('openai/gpt-4o-mini'))
response = qa(question="Test question")
print('GPT-4o-mini:', response.answer)
```

### Switching LMs Locally

```python
import dspy

# Change LM within a context block
with dspy.context(lm=dspy.LM('openai/gpt-3.5-turbo')):
    response = qa(question="Test question")
    print('GPT-3.5-turbo:', response.answer)
```

### Responses API for Advanced Models

```python
import dspy

# Configure DSPy to use Responses API
dspy.configure(
    lm=dspy.LM(
        "openai/gpt-5-mini",
        model_type="responses",
        temperature=1.0,
        max_tokens=16000,
    ),
)
```

## Best Practices

### 1. Use Built-in Adapters

```python
# Good: Use built-in ChatAdapter or JSONAdapter
module = dspy.Predict(MySignature)

# Bad: Don't create custom adapter unless necessary
class MyAdapter(dspy.Adapter):
    pass
```

### 2. Test Adapter Behavior

```python
# Good: Test adapter with sample inputs
adapter = dspy.ChatAdapter()
messages = adapter.format(signature, [], {"input": "test"})
assert len(messages) > 0
assert messages[0]["role"] == "system"

# Bad: Don't skip testing
module = dspy.Predict(MySignature)
result = module(input="test")  # Untested behavior
```

### 3. Handle Parsing Errors

```python
# Good: Handle parsing errors gracefully
class RobustAdapter(dspy.Adapter):
    def parse(self, signature, output):
        try:
            return super().parse(signature, output)
        except Exception as e:
            # Return default values on parse error
            return dspy.Prediction(
                **{field: "" for field in signature.output_fields}
            )
```

### 4. Use Appropriate Adapter for Task

```python
# Good: Use JSONAdapter for structured output
class StructuredModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict(
            StructuredSignature,  # Has type hints
            adapter=dspy.JSONAdapter()
        )

# Bad: Use ChatAdapter for structured output
class BadModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict(StructuredSignature)  # May not enforce types
```

### 5. Document Custom Adapters

```python
# Good: Document custom adapter behavior
class XMLAdapter(dspy.Adapter):
    """
    Adapter for XML-formatted input/output.

    Formats inputs as XML tags and parses outputs from XML tags.

    Example:
        Input: <input><field>value</field></input>
        Output: <output><field>result</field></output>
    """

    def format_user_message_content(self, signature, inputs, main_request=True):
        """Format inputs as XML tags."""
        pass

# Bad: Undocumented custom adapter
class MyAdapter(dspy.Adapter):
    pass
```

## Common Issues and Solutions

### Issue: Adapter Not Parsing Output

**Problem**: Adapter fails to parse LM output

**Solution**:
1. Check LM output format matches expectations
2. Verify signature field types are correct
3. Add error handling in parse() method
4. Test adapter with sample outputs

### Issue: Custom Adapter Not Used

**Problem**: DSPy uses default adapter instead of custom

**Solution**:
1. Verify adapter parameter is passed correctly
2. Check adapter is passed to dspy.Predict, not module
3. Ensure adapter class is defined before use

### Issue: LM Provider Not Supported

**Problem**: Can't configure LM for specific provider

**Solution**:
1. Use LiteLLM format: "provider/model"
2. Set api_base if provider has custom endpoint
3. Check provider is supported by LiteLLM
4. Implement custom LM client if needed

### Issue: Context Manager Not Switching LM

**Problem**: `dspy.context()` not changing LM locally

**Solution**:
1. Ensure LM object is valid
2. Check indentation of context block
3. Verify `with dspy.context(lm=...)` syntax
4. Use thread-safe configuration if needed
