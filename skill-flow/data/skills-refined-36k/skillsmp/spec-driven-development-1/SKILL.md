---
name: spec-driven-development
description: Develop software from detailed specifications that serve as contracts. Use when building APIs, integrations, complex features with multiple conditions, or when the user provides OpenAPI specs, JSON schemas, detailed requirements, or mentions SDD, specification, contract-first development.
---

# Spec-Driven Development

Use specifications as the source of truth for implementation.

## Workflow

1. **Review specification**: Parse provided spec (OpenAPI, JSON Schema, requirements doc)
2. **Clarify ambiguities**: Ask about unclear edge cases or missing details
3. **Validate spec completeness**: Check for inputs, outputs, errors, constraints
4. **Implement to spec**: Generate code that matches the specification exactly
5. **Verify against spec**: Ensure all requirements are covered

## Specification formats

### OpenAPI/Swagger (for APIs)

```yaml
paths:
  /api/orders:
    post:
      summary: Create new order
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [customer_id, items]
              properties:
                customer_id:
                  type: integer
                items:
                  type: array
                  minItems: 1
                  items:
                    type: object
                    properties:
                      product_id: { type: integer }
                      quantity: { type: integer, minimum: 1 }
      responses:
        '201':
          description: Order created
        '400':
          description: Invalid request
```

### JSON Schema (for data structures)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["name", "email"],
  "properties": {
    "name": { "type": "string", "minLength": 1 },
    "email": { "type": "string", "format": "email" },
    "age": { "type": "integer", "minimum": 0 }
  }
}
```

### Structured requirements (for features)

```
Feature: Order creation

Input:
- customer_id: integer, required
- items: array of {product_id, quantity}, min 1 item

Behavior:
- Verify all products exist in catalog
- Check stock availability for each item
- If any item unavailable → return 400 with list of unavailable items
- Create order in 'draft' status
- Reserve inventory

Output (201):
- order_id: string (UUID)
- total_amount: decimal
- created_at: ISO 8601 timestamp

Errors:
- 400: Invalid input or unavailable items
- 404: Customer not found
```

## Prompting for specification

When user provides incomplete requirements, ask:

- What are the required vs optional fields?
- What are the valid ranges/formats for each field?
- What errors should be returned and when?
- Are there any business rules or constraints?
- What should happen in edge cases?

## Implementation template (FastAPI)

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from uuid import uuid4

class OrderItem(BaseModel):
    product_id: int
    quantity: int = Field(ge=1)

class CreateOrderRequest(BaseModel):
    customer_id: int
    items: List[OrderItem] = Field(min_length=1)

class CreateOrderResponse(BaseModel):
    order_id: str
    total_amount: float
    created_at: datetime

@app.post("/api/orders", response_model=CreateOrderResponse, status_code=201)
async def create_order(request: CreateOrderRequest):
    # Verify customer exists
    customer = await get_customer(request.customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Check product availability
    unavailable = await check_availability(request.items)
    if unavailable:
        raise HTTPException(
            status_code=400, 
            detail={"unavailable_items": unavailable}
        )
    
    # Create order
    order = await create_order_record(request)
    
    return CreateOrderResponse(
        order_id=str(uuid4()),
        total_amount=order.total,
        created_at=datetime.utcnow()
    )
```

## Verification checklist

After implementation, verify:

- [ ] All required fields validated
- [ ] All optional fields handled with defaults
- [ ] All error cases return correct status codes
- [ ] Response matches specified schema
- [ ] Edge cases documented in spec are handled
- [ ] Business rules enforced

## Best practices

- **Spec is the contract**: Implementation must match spec exactly
- **Clarify before coding**: Resolve ambiguities upfront
- **Generate from spec when possible**: Use OpenAPI generators for boilerplate
- **Keep spec updated**: Sync changes between spec and implementation
- **Test against spec**: Validation tests should verify spec compliance
