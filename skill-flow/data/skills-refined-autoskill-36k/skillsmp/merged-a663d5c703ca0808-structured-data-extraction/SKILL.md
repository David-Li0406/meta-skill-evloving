---
name: structured-data-extraction
description: Use this skill when you need to extract structured data from LLM responses using Pydantic models and validation, supporting multiple LLM providers.
---

# Structured Data Extraction with Instructor

## When to Use This Skill

Use this skill when you need to:
- **Extract structured data** from LLM responses reliably.
- **Validate outputs** against Pydantic schemas automatically.
- **Retry failed extractions** with automatic error handling.
- **Parse complex JSON** with type safety and validation.
- **Stream partial results** for real-time processing.
- **Support multiple LLM providers** with consistent API.

## Installation

```bash
pip install instructor
```

## Quick Start

### Basic Example: Extract User Data

```python
import instructor
from pydantic import BaseModel
from openai import OpenAI

# Define output structure
class User(BaseModel):
    name: str
    age: int

# Create instructor client
client = instructor.from_openai(OpenAI())

# Extract structured data
user = client.chat.completions.create(
    model="gpt-4o",
    response_model=User,
    messages=[{"role": "user", "content": "John is 25 years old"}]
)

print(user.name)  # "John"
print(user.age)   # 25
```

## Pydantic Models

### Basic Models

```python
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Task(BaseModel):
    title: str = Field(description="Task title")
    description: str = Field(description="Detailed description")
    priority: Priority = Field(description="Task priority level")
    due_date: Optional[str] = Field(None, description="Due date in YYYY-MM-DD format")
    tags: List[str] = Field(default_factory=list, description="Related tags")
```

### Nested Models

```python
class Address(BaseModel):
    street: str
    city: str
    country: str
    postal_code: str

class Person(BaseModel):
    name: str
    email: str
    address: Address
    phone_numbers: List[str]
```

## Validation

### Field Validators

```python
from pydantic import field_validator

class SearchQuery(BaseModel):
    query: str
    filters: List[str]

    @field_validator('query')
    @classmethod
    def query_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Query cannot be empty")
        return v.strip()
```

### Model Validators

```python
from pydantic import model_validator

class DateRange(BaseModel):
    start_date: str
    end_date: str

    @model_validator(mode='after')
    def validate_dates(self):
        if self.start_date > self.end_date:
            raise ValueError("Start date must be before end date")
        return self
```

## Automatic Retrying

Instructor retries automatically when validation fails, providing error feedback to the LLM.

```python
user = client.chat.completions.create(
    model="gpt-4o",
    response_model=User,
    max_retries=3,
    messages=[{"role": "user", "content": "Extract user info"}]
)
```

## Streaming

Stream partial results for real-time processing.

```python
from instructor import Partial

class Report(BaseModel):
    title: str
    sections: List[str]
    summary: str

for partial in client.chat.completions.create_partial(
    model="gpt-4o",
    response_model=Report,
    messages=[{"role": "user", "content": "Write a report on AI trends"}],
):
    print(partial)  # Partial[Report] with available fields
```

## Iterable Extraction

```python
class Product(BaseModel):
    name: str
    price: float
    category: str

products = client.chat.completions.create_iterable(
    model="gpt-4o",
    response_model=Product,
    messages=[{"role": "user", "content": "Extract products: ..."}]
)

for product in products:
    print(product)
```

## Provider Configuration

### Anthropic

```python
import instructor
from anthropic import Anthropic

client = instructor.from_anthropic(Anthropic())

user = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    response_model=User,
    messages=[{"role": "user", "content": "John is 25"}]
)
```

### Local Models (Ollama)

```python
client = instructor.from_openai(
    OpenAI(base_url="http://localhost:11434/v1", api_key="ollama"),
    mode=instructor.Mode.JSON
)

user = client.chat.completions.create(
    model="llama3.1",
    response_model=User,
    messages=[{"role": "user", "content": "John is 25"}]
)
```

## Advanced Patterns

### Chain of Thought

```python
class Reasoning(BaseModel):
    chain_of_thought: str
    answer: str

result = client.chat.completions.create(
    model="gpt-4o",
    response_model=Reasoning,
    messages=[{"role": "user", "content": "What is 25 * 47?"}]
)
```

### Classification

```python
class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

class SentimentAnalysis(BaseModel):
    text: str
    sentiment: Sentiment
    confidence: float = Field(ge=0, le=1)

analysis = client.chat.completions.create(
    model="gpt-4o",
    response_model=SentimentAnalysis,
    messages=[{"role": "user", "content": "Analyze: 'I love this product!'"}]
)
```

## Resources

- [Instructor Documentation](https://python.useinstructor.com/)
- [Instructor GitHub](https://github.com/jxnl/instructor)
- [Examples](https://python.useinstructor.com/examples/)