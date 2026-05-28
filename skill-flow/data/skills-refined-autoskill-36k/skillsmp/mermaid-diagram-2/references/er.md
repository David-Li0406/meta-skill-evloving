# Entity Relationship Diagram Reference

## Declaration

```
erDiagram
    direction LR  %% Optional: LR, RL, TB, BT
```

## Entities

```
CUSTOMER
ORDER
PRODUCT
```

With attributes:
```
CUSTOMER {
    int id PK
    string name
    string email UK
}
```

## Attribute Modifiers

| Modifier | Meaning |
|----------|---------|
| `PK` | Primary Key |
| `FK` | Foreign Key |
| `UK` | Unique Key |

Combine: `int user_id PK, FK`

Add comments: `string name "Customer full name"`

## Relationships

Syntax: `ENTITY1 ||--o{ ENTITY2 : "label"`

### Cardinality Symbols

| Left | Right | Meaning |
|------|-------|---------|
| `\|o` | `o\|` | Zero or one |
| `\|\|` | `\|\|` | Exactly one |
| `}o` | `o{` | Zero or more |
| `}\|` | `\|{` | One or more |

### Line Types

| Symbol | Type |
|--------|------|
| `--` | Identifying (solid) |
| `..` | Non-identifying (dashed) |

## Common Patterns

```
%% One-to-many
CUSTOMER ||--o{ ORDER : places

%% Many-to-many (via junction)
STUDENT }|--|| ENROLLMENT : has
ENROLLMENT ||--|{ COURSE : for

%% Optional relationship
EMPLOYEE |o--o| PARKING_SPOT : assigned
```

## Example

```mermaid
erDiagram
    CUSTOMER {
        int id PK
        string name
        string email UK
    }

    ORDER {
        int id PK
        int customer_id FK
        date created_at
        decimal total
    }

    ORDER_ITEM {
        int id PK
        int order_id FK
        int product_id FK
        int quantity
    }

    PRODUCT {
        int id PK
        string name
        decimal price
        string category
    }

    CUSTOMER ||--o{ ORDER : places
    ORDER ||--|{ ORDER_ITEM : contains
    PRODUCT ||--o{ ORDER_ITEM : "included in"
```
