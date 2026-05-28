---
title: Use Pydantic for Validated Deserialization
impact: MEDIUM
impactDescription: combines parsing with validation, prevents invalid data
tags: serial, pydantic, validation, type-safety
---

## Use Pydantic for Validated Deserialization

Raw JSON parsing provides no validation. Pydantic combines deserialization with type validation, catching errors at the boundary.

**Incorrect (no validation, errors propagate):**

```python
import json

def process_order(data: bytes) -> Order:
    parsed = json.loads(data)
    return Order(
        user_id=parsed["user_id"],  # May be missing
        total=parsed["total"],  # May be wrong type
        items=parsed["items"],  # May be malformed
    )
```

**Correct (validated deserialization):**

```python
from pydantic import BaseModel, Field

class OrderItem(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)

class Order(BaseModel):
    user_id: int
    total: float = Field(gt=0)
    items: list[OrderItem] = Field(min_length=1)

def process_order(data: bytes) -> Order:
    return Order.model_validate_json(data)
    # Raises ValidationError with clear messages for invalid data
```

**Benefits:**
- Type coercion (string "123" → int 123)
- Constraint validation (positive numbers, non-empty lists)
- Clear error messages for debugging
- JSON Schema generation for API docs

Reference: [Pydantic documentation](https://docs.pydantic.dev/)
