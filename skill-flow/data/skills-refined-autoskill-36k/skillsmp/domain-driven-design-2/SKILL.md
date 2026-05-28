---
name: domain-driven-design
description: Design software architecture around business domain models. Use when starting a new project, creating module structure, defining entities and their relationships, or when the user mentions DDD, domain model, bounded context, aggregates, or business logic architecture.
---

# Domain-Driven Design

Apply DDD principles to create architecture that reflects business reality.

## Workflow

1. **Gather domain context**: Ask the user to describe key business entities, their relationships, and core business rules
2. **Define bounded contexts**: Identify distinct subdomains and their boundaries
3. **Model entities and value objects**: Create domain classes that encapsulate business logic
4. **Establish aggregates**: Group related entities with clear aggregate roots
5. **Generate project structure**: Create directories and files reflecting the domain model

## Prompting for context

When user provides incomplete domain information, ask:

- What are the main entities in your domain? (e.g., Order, Customer, Product)
- What states or statuses do these entities have?
- What business rules govern transitions between states?
- How do entities relate to each other?

## Output structure

```
src/
├── domain/
│   ├── entities/
│   │   └── [entity_name].py
│   ├── value_objects/
│   │   └── [value_object_name].py
│   ├── aggregates/
│   │   └── [aggregate_name].py
│   └── services/
│       └── [domain_service].py
├── application/
│   └── use_cases/
└── infrastructure/
    └── repositories/
```

## Example prompt

User: "Create architecture for an e-commerce system"

Response approach:
1. Ask about key entities (Order, Customer, Product, Cart)
2. Clarify business rules (order lifecycle, inventory management)
3. Generate domain model with entities, value objects, and services
4. Create project structure reflecting bounded contexts

## Entity template

```python
from dataclasses import dataclass
from enum import Enum
from typing import List
from datetime import datetime

class OrderStatus(Enum):
    DRAFT = "draft"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"

@dataclass
class Order:
    id: str
    customer_id: str
    items: List["OrderItem"]
    status: OrderStatus
    created_at: datetime
    
    def confirm(self) -> None:
        if self.status != OrderStatus.DRAFT:
            raise ValueError("Only draft orders can be confirmed")
        if not self.items:
            raise ValueError("Cannot confirm empty order")
        self.status = OrderStatus.CONFIRMED
    
    def ship(self) -> None:
        if self.status != OrderStatus.CONFIRMED:
            raise ValueError("Only confirmed orders can be shipped")
        self.status = OrderStatus.SHIPPED
```

## Key principles

- **Ubiquitous language**: Use business terms in code (not technical jargon)
- **Rich domain model**: Entities contain business logic, not just data
- **Aggregate boundaries**: Protect invariants within aggregate roots
- **Domain events**: Capture significant business occurrences
