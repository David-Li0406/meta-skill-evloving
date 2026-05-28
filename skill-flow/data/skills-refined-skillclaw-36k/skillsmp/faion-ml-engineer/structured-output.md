---
id: structured-output
name: "Structured Output"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Structured Output

## Overview

Structured output ensures LLMs return data in consistent, parseable formats like JSON. This is essential for integrating LLM outputs into applications, APIs, and automated pipelines.

## When to Use

- API responses requiring specific format
- Data extraction from unstructured text
- Form filling automation
- Database record generation
- Configuration generation
- Any application needing reliable parsing

## Key Concepts

### Output Format Options

| Method | Reliability | Flexibility | Provider |
|--------|-------------|-------------|----------|
| JSON Mode | High | Medium | OpenAI, Anthropic |
| Structured Outputs | Very High | High | OpenAI |
| Prompt Engineering | Medium | High | All |
| Output Parsers | Medium | High | LangChain |

### JSON Mode vs Structured Outputs

```
JSON Mode: Guarantees valid JSON, but not schema compliance
Structured Outputs: Guarantees both valid JSON AND schema compliance
```

## Implementation

### OpenAI JSON Mode

```python
from openai import OpenAI
import json

client = OpenAI()

def extract_with_json_mode(text: str) -> dict:
    """Extract structured data using JSON mode."""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Extract entities from text. Return JSON with: {entities: [{name, type, context}]}"
            },
            {"role": "user", "content": text}
        ],
        response_format={"type": "json_object"}
    )

    return json.loads(response.choices[0].message.content)

# Usage
result = extract_with_json_mode(
    "Apple CEO Tim Cook announced a new iPhone model at their Cupertino headquarters."
)
# {"entities": [{"name": "Apple", "type": "company", "context": "..."}, ...]}
```

### OpenAI Structured Outputs

```python
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List, Optional

client = OpenAI()

# Define schema with Pydantic
class Entity(BaseModel):
    name: str = Field(description="Entity name")
    type: str = Field(description="Entity type: person, company, location, product")
    confidence: float = Field(ge=0, le=1, description="Confidence score")

class ExtractionResult(BaseModel):
    entities: List[Entity]
    summary: str
    language: str

def extract_structured(text: str) -> ExtractionResult:
    """Extract data with guaranteed schema compliance."""
    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Extract entities and provide a summary."
            },
            {"role": "user", "content": text}
        ],
        response_format=ExtractionResult
    )

    return response.choices[0].message.parsed

# Usage
result = extract_structured(
    "Elon Musk visited Berlin to open a new Tesla factory."
)
print(result.entities[0].name)  # "Elon Musk"
print(result.summary)
```

### Anthropic JSON Output

```python
from anthropic import Anthropic
import json

client = Anthropic()

def extract_with_claude(text: str, schema: dict) -> dict:
    """Extract structured data with Claude."""
    schema_str = json.dumps(schema, indent=2)

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Extract information from the following text and return valid JSON matching this schema:

Schema:
```json
{schema_str}
```

Text:
{text}

Return only valid JSON, no other text."""
            }
        ]
    )

    # Extract JSON from response
    content = response.content[0].text

    # Handle potential markdown code blocks
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0]
    elif "```" in content:
        content = content.split("```")[1].split("```")[0]

    return json.loads(content.strip())

# Schema definition
schema = {
    "type": "object",
    "properties": {
        "product_name": {"type": "string"},
        "price": {"type": "number"},
        "features": {"type": "array", "items": {"type": "string"}},
        "in_stock": {"type": "boolean"}
    },
    "required": ["product_name", "price"]
}

result = extract_with_claude(
    "The new iPhone 15 Pro costs $999 and features a titanium design, A17 chip, and improved camera.",
    schema
)
```

### Function-Based Structured Output

```python
# Using function calling for structured output
def get_structured_response(
    prompt: str,
    schema: dict,
    client,
    model: str = "gpt-4o"
) -> dict:
    """Use function calling to enforce output structure."""
    tools = [{
        "type": "function",
        "function": {
            "name": "return_structured_data",
            "description": "Return the extracted data in structured format",
            "parameters": schema
        }
    }]

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        tools=tools,
        tool_choice={"type": "function", "function": {"name": "return_structured_data"}}
    )

    # Extract function call result
    tool_call = response.choices[0].message.tool_calls[0]
    return json.loads(tool_call.function.arguments)

# Usage
schema = {
    "type": "object",
    "properties": {
        "sentiment": {"type": "string", "enum": ["positive", "negative", "neutral"]},
        "topics": {"type": "array", "items": {"type": "string"}},
        "urgency": {"type": "integer", "minimum": 1, "maximum": 5}
    },
    "required": ["sentiment", "topics", "urgency"]
}

result = get_structured_response(
    "Analyze this customer feedback: 'I love the product but shipping was slow!'",
    schema,
    client
)
```

### Complex Schema Examples

```python
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Union
from datetime import datetime
from enum import Enum

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    BLOCKED = "blocked"

class Subtask(BaseModel):
    title: str
    estimated_hours: Optional[float] = None
    completed: bool = False

class Task(BaseModel):
    id: Optional[str] = None
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    priority: Priority = Priority.MEDIUM
    status: TaskStatus = TaskStatus.TODO
    due_date: Optional[str] = None
    assignee: Optional[str] = None
    tags: List[str] = []
    subtasks: List[Subtask] = []
    estimated_hours: Optional[float] = Field(None, ge=0)

    @validator('due_date')
    def validate_date(cls, v):
        if v:
            try:
                datetime.strptime(v, '%Y-%m-%d')
            except ValueError:
                raise ValueError('Date must be in YYYY-MM-DD format')
        return v

class ProjectExtraction(BaseModel):
    project_name: str
    tasks: List[Task]
    total_estimated_hours: float
    team_members: List[str]

def extract_project_plan(description: str) -> ProjectExtraction:
    """Extract project plan from natural language description."""
    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a project planning assistant. Extract tasks and project details from the description."
            },
            {"role": "user", "content": description}
        ],
        response_format=ProjectExtraction
    )

    return response.choices[0].message.parsed
```

### Output Parsing with Retry

```python
from typing import TypeVar, Type
import json
from tenacity import retry, stop_after_attempt, retry_if_exception_type

T = TypeVar('T', bound=BaseModel)

class OutputParsingError(Exception):
    """Error parsing LLM output."""
    pass

@retry(
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type((json.JSONDecodeError, OutputParsingError))
)
def parse_with_retry(
    client,
    prompt: str,
    output_class: Type[T],
    model: str = "gpt-4o"
) -> T:
    """Parse LLM output with automatic retry on failure."""
    schema = output_class.model_json_schema()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": f"Return valid JSON matching this schema: {json.dumps(schema)}"
            },
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )

    content = response.choices[0].message.content

    try:
        data = json.loads(content)
        return output_class(**data)
    except Exception as e:
        raise OutputParsingError(f"Failed to parse output: {e}")
```

### Streaming Structured Output

```python
def stream_structured_output(
    client,
    prompt: str,
    model: str = "gpt-4o"
):
    """Stream JSON output with partial parsing."""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Return JSON with streaming support. Output complete JSON object."
            },
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        stream=True
    )

    accumulated = ""

    for chunk in response:
        if chunk.choices[0].delta.content:
            accumulated += chunk.choices[0].delta.content

            # Try to parse partial JSON for progress updates
            try:
                partial = json.loads(accumulated + '"}]}')
                yield {"partial": partial, "complete": False}
            except:
                pass

    # Final complete parse
    yield {"partial": json.loads(accumulated), "complete": True}
```

### Form/Document Extraction

```python
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional

class Address(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None

class ContactInfo(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[Address] = None

class InvoiceItem(BaseModel):
    description: str
    quantity: float
    unit_price: float
    total: float

class Invoice(BaseModel):
    invoice_number: str
    date: str
    due_date: Optional[str] = None
    vendor: ContactInfo
    customer: ContactInfo
    items: List[InvoiceItem]
    subtotal: float
    tax: Optional[float] = None
    total: float
    currency: str = "USD"
    notes: Optional[str] = None

def extract_invoice(text: str) -> Invoice:
    """Extract invoice data from text or OCR output."""
    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Extract invoice information. Calculate totals if not provided."
            },
            {"role": "user", "content": f"Extract invoice data:\n\n{text}"}
        ],
        response_format=Invoice
    )

    return response.choices[0].message.parsed
```

### Production Structured Output Service

```python
from dataclasses import dataclass
from typing import Type, TypeVar, Optional, Dict, Any
from pydantic import BaseModel, ValidationError
import logging
import json

T = TypeVar('T', bound=BaseModel)

@dataclass
class StructuredOutputConfig:
    max_retries: int = 3
    use_structured_outputs: bool = True  # OpenAI structured outputs
    fallback_to_json_mode: bool = True
    validate_output: bool = True

class StructuredOutputService:
    """Production service for structured LLM outputs."""

    def __init__(
        self,
        client,
        model: str = "gpt-4o",
        config: Optional[StructuredOutputConfig] = None
    ):
        self.client = client
        self.model = model
        self.config = config or StructuredOutputConfig()
        self.logger = logging.getLogger(__name__)

    def extract(
        self,
        prompt: str,
        output_class: Type[T],
        system_prompt: str = ""
    ) -> Optional[T]:
        """Extract structured data from text."""
        for attempt in range(self.config.max_retries):
            try:
                if self.config.use_structured_outputs:
                    result = self._extract_structured(prompt, output_class, system_prompt)
                else:
                    result = self._extract_json_mode(prompt, output_class, system_prompt)

                if self.config.validate_output:
                    # Pydantic validation happens automatically
                    return result

                return result

            except ValidationError as e:
                self.logger.warning(f"Validation error (attempt {attempt + 1}): {e}")
                if attempt == self.config.max_retries - 1:
                    raise
            except json.JSONDecodeError as e:
                self.logger.warning(f"JSON parse error (attempt {attempt + 1}): {e}")
                if attempt == self.config.max_retries - 1:
                    raise

        return None

    def _extract_structured(
        self,
        prompt: str,
        output_class: Type[T],
        system_prompt: str
    ) -> T:
        """Use OpenAI structured outputs."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=messages,
            response_format=output_class
        )

        return response.choices[0].message.parsed

    def _extract_json_mode(
        self,
        prompt: str,
        output_class: Type[T],
        system_prompt: str
    ) -> T:
        """Use JSON mode with schema in prompt."""
        schema = output_class.model_json_schema()

        messages = [
            {
                "role": "system",
                "content": f"{system_prompt}\n\nReturn valid JSON matching: {json.dumps(schema)}"
            },
            {"role": "user", "content": prompt}
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            response_format={"type": "json_object"}
        )

        data = json.loads(response.choices[0].message.content)
        return output_class(**data)

    def batch_extract(
        self,
        items: List[str],
        output_class: Type[T],
        system_prompt: str = ""
    ) -> List[Optional[T]]:
        """Extract from multiple items."""
        results = []
        for item in items:
            try:
                result = self.extract(item, output_class, system_prompt)
                results.append(result)
            except Exception as e:
                self.logger.error(f"Extraction failed: {e}")
                results.append(None)
        return results
```

## Best Practices

1. **Schema Design**
   - Use clear field names
   - Provide descriptions for complex fields
   - Set reasonable defaults
   - Use enums for constrained values

2. **Validation**
   - Use Pydantic for type safety
   - Add custom validators for complex rules
   - Handle validation errors gracefully

3. **Error Handling**
   - Implement retry logic
   - Fall back to JSON mode if structured fails
   - Log parsing failures for debugging

4. **Performance**
   - Cache schemas
   - Use streaming for large outputs
   - Batch similar extractions

5. **Prompt Design**
   - Include schema in system prompt for JSON mode
   - Provide examples for complex structures
   - Be explicit about required vs optional fields

## Common Pitfalls

1. **Over-complex Schemas** - Too many nested levels
2. **Missing Required Fields** - LLM may skip them
3. **No Fallback** - System fails on parse errors
4. **Ignoring Validation** - Trusting raw LLM output
5. **Wrong Types** - Expecting int, getting string
6. **Large Schemas** - Exceed context limits

## References

- [OpenAI Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [JSON Schema](https://json-schema.org/)
