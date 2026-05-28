# Structured Outputs Reference

Type-safe JSON responses with Pydantic (Python) and Zod (TypeScript).

## Zod Helpers (TypeScript)

### zodResponseFormat

Convert Zod schemas for `response_format`:

```typescript
import { zodResponseFormat } from 'dedalus-labs/helpers/zod';
import { z } from 'zod';

const OrderSchema = z.object({
  order_id: z.string(),
  customer: z.object({
    name: z.string(),
    email: z.string(),
  }),
  items: z.array(
    z.object({
      product: z.string(),
      quantity: z.number(),
      price: z.number(),
    })
  ),
  total: z.number(),
});

const result = await client.chat.completions.parse({
  model: 'openai/gpt-4o-mini',
  messages: [{
    role: 'user',
    content: 'Create order: Alice bought 2 laptops at $999 each',
  }],
  response_format: zodResponseFormat(OrderSchema, 'order'),
});

const order = result.choices[0]?.message.parsed;
console.log(`Order ID: ${order?.order_id}`);
console.log(`Items: ${order?.items.length}`);
console.log(`Total: $${order?.total}`);
```

### zodFunction

Define tool schemas with Zod:

```typescript
import { zodFunction } from 'dedalus-labs/helpers/zod';

const weatherTool = zodFunction({
  name: 'get_weather',
  description: 'Get current weather for a location',
  parameters: z.object({
    location: z.string().describe('City name'),
    units: z.enum(['celsius', 'fahrenheit']).default('celsius'),
  }),
  function: async ({ location, units }) => {
    return await fetchWeather(location, units);
  },
});
```

## Pydantic Patterns (Python)

### Nested Models

```python
from pydantic import BaseModel

class Address(BaseModel):
    street: str
    city: str
    country: str

class Customer(BaseModel):
    name: str
    email: str
    address: Address

class Order(BaseModel):
    order_id: str
    customer: Customer
    items: list[str]
    total: float

result = await client.chat.completions.parse(
    model="openai/gpt-4o-mini",
    messages=[{"role": "user", "content": "Create an order for John..."}],
    response_format=Order,
)
```

### Optional Fields

```python
from typing import Optional

class Product(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    tags: list[str] = []
```

### Field Validation

```python
from pydantic import BaseModel, Field

class Review(BaseModel):
    rating: int = Field(ge=1, le=5, description="Rating 1-5")
    text: str = Field(min_length=10, description="Review text")
    verified: bool = False
```

## Streaming Structured Outputs

### Python

```python
async with client.chat.completions.stream(
    model="anthropic/claude-opus-4-5",
    messages=[{"role": "user", "content": "Generate a recipe"}],
    response_format=Recipe,
) as stream:
    async for event in stream:
        if event.type == "content.delta":
            print(event.delta, end="", flush=True)
        elif event.type == "content.done":
            # Partial parse available
            print(f"\nName so far: {event.parsed.name}")
    
    final = await stream.get_final_completion()
    recipe = final.choices[0].message.parsed
```

### TypeScript

```typescript
// Use standard streaming and parse at the end
const result = await runner.run({
  model: 'openai/gpt-4o-mini',
  input: 'Generate a recipe',
  stream: true,
});

// Collect chunks, then parse final result
```

## Provider-Specific Behavior

### Strict Enforcement (Guaranteed)

- `openai/*` - Context-free grammar compilation
- `xai/*` - Native schema validation
- `fireworks_ai/*` - Native validation (select models)
- `deepseek/*` - Native validation (select models)

### Best-Effort (Validate Results)

- `google/*` - Schema forwarded to `generationConfig.responseSchema`
- `anthropic/*` - Prompt-based JSON generation (~85-90% success)

For best-effort providers, always validate:

```python
try:
    result = await client.chat.completions.parse(
        model="anthropic/claude-opus-4-5",
        messages=[...],
        response_format=MySchema,
    )
    data = result.choices[0].message.parsed
except ValidationError:
    # Retry or handle invalid response
    pass
```

## Common Schemas

### Classification

```python
from enum import Enum

class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

class Analysis(BaseModel):
    sentiment: Sentiment
    confidence: float = Field(ge=0, le=1)
    keywords: list[str]
```

### Extraction

```python
class Entity(BaseModel):
    text: str
    type: str  # PERSON, ORG, LOCATION, etc.
    start: int
    end: int

class Extraction(BaseModel):
    entities: list[Entity]
    summary: str
```

### Generation

```python
class BlogPost(BaseModel):
    title: str
    introduction: str
    sections: list[str]
    conclusion: str
    tags: list[str]
```
