# Vague Syntax Reference

## Basic Types

```vague
schema Person {
  name: string,
  age: int,
  salary: decimal,
  active: boolean,
  joined: date
}
```

## Let Bindings (Reusable Values)

```vague
// Define reusable superpositions at the top of the file
let teamNames = "Arsenal" | "Chelsea" | "Liverpool" | "Man City"
let statuses = 0.8: "active" | 0.15: "pending" | 0.05: "inactive"

schema Team {
  name: unique teamNames,
  status: statuses
}
```

- Improves readability for long enum lists
- Works with `unique` modifier
- Supports weighted superpositions

## Superposition (Random Choice)

```vague
// Equal weight
status: "draft" | "sent" | "paid"

// Weighted probabilities
status: 0.7: "paid" | 0.2: "pending" | 0.1: "draft"

// Mixed types: range OR field reference
amount: int in 10..500 | invoice.total
amount: 0.7: int in 10..500 | 0.3: invoice.total

// Expression in superposition
remaining: 0.7: (invoice.total - invoice.amount_paid) | 0.3: int in 10..100
```

## Nullable Fields

```vague
nickname: string?           // Shorthand: sometimes null
notes: string | null        // Explicit: equivalent to string?
priority: int | null        // Works with any primitive type
```

## Ranges

```vague
age: int in 18..65
price: decimal in 0.01..999.99
founded: date in 2000..2023
```

## Cardinality (Collections)

```vague
line_items: 1..5 of LineItem    // 1-5 items
employees: 100 of Employee       // Exactly 100
```

## Unique Values

```vague
id: unique int in 1000..9999,       // Ensures no duplicate IDs
code: unique "A" | "B" | "C" | "D"  // Works with superposition too
```

## Private Fields

```vague
schema Person {
  // Private fields are generated and usable in logic, but excluded from output
  age: private int in 0..105,
  age_bracket: age < 18 ? "minor" : age < 65 ? "adult" : "senior"
}
// Output: { "age_bracket": "adult" }  -- no "age" field

schema Product {
  // Can combine with unique
  internal_id: unique private int in 1..10000,
  public_ref: concat("PROD-", internal_id)
}
```

## Constraints

```vague
schema Invoice {
  issued_date: int in 1..20,
  due_date: int in 1..30,

  assume due_date >= issued_date,   // Hard constraint

  assume if status == "paid" {      // Conditional constraint
    amount > 0
  }
}
```

Logical operators: `and`, `or`, `not`

## Cross-Record References

```vague
schema Invoice {
  customer: any of companies,                         // Random from collection
  supplier: any of companies where .active == true,   // Filtered

  // Logical operators in where
  vendor: any of companies where .active == true and .region == "US"
}
```

## Parent References

```vague
schema LineItem {
  currency: ^base_currency   // Inherit from parent schema
}
```

## Computed Fields

```vague
schema Invoice {
  line_items: 1..10 of LineItem,

  // Aggregates
  total: sum(line_items.amount),
  item_count: count(line_items),
  avg_price: avg(line_items.unit_price),
  min_price: min(line_items.unit_price),
  max_price: max(line_items.unit_price),

  // Arithmetic expressions
  tax: round(sum(line_items.amount) * 0.2, 2),
  grand_total: round(sum(line_items.amount) * 1.2, 2)
}
```

## Ternary Expressions

```vague
schema Invoice {
  total: int in 100..500,
  amount_paid: int in 0..0,
  status: amount_paid >= total ? "paid" : "partially-paid"
}

schema Item {
  score: int in 0..100,
  // Nested ternary
  grade: score >= 90 ? "A" : score >= 70 ? "B" : "C"
}

schema Order {
  total: int in 10..200,
  is_member: boolean,
  has_coupon: boolean,
  // Logical operators
  discount: (total >= 100 and is_member) or has_coupon ? 0.15 : 0
}
```

## Dynamic Cardinality

```vague
schema Order {
  size: "small" | "large",
  items: (size == "large" ? 5..10 : 1..3) of LineItem
}

schema Shipment {
  is_bulk: boolean,
  is_priority: boolean,
  packages: (is_bulk and is_priority ? 20..30 : 1..5) of Package
}
```

## Side Effects (then blocks)

Mutate referenced objects after a record is generated:

```vague
schema Payment {
  invoice: any of invoices,
  amount: int in 50..500
}
then {
  invoice.amount_paid += amount,
  invoice.status = invoice.amount_paid >= invoice.total ? "paid" : "partially-paid"
}
```

- Runs once per generated record
- Can only mutate upstream references
- Supports `=` (assignment) and `+=` (compound assignment)

## Refine Blocks (Conditional Field Overrides)

Override field definitions based on conditions - more efficient than constraints:

```vague
schema Player {
  position: "GK" | "DEF" | "MID" | "FWD",
  goals_scored: int in 0..30,
  assists: int in 0..20,
  clean_sheets: int in 0..20
} refine {
  if position == "GK" {
    goals_scored: int in 0..3,
    assists: int in 0..5
  },
  if position == "FWD" {
    clean_sheets: int in 0..3
  }
}
```

- Runs after initial field generation
- Fields are regenerated with new definitions when conditions match
- More efficient than `assume` constraints (generates correct values directly)
- Supports logical operators: `if position == "GK" or position == "DEF" { ... }`

## Datasets

```vague
dataset TestData {
  companies: 100 of Company,
  invoices: 500 of Invoice
}
```

## Dataset-Level Constraints

```vague
dataset TestData {
  invoices: 100 of Invoice,
  payments: 50 of Payment,

  validate {
    sum(invoices.total) >= 100000,
    sum(payments.amount) <= sum(invoices.total),
    count(payments) <= count(invoices),

    // Predicate functions
    all(invoices, .amount_paid <= .total),
    some(invoices, .status == "paid"),
    none(invoices, .total < 0)
  }
}
```

## Negative Testing (Violating Datasets)

```vague
// Normal dataset - satisfies constraints
dataset Valid {
  invoices: 100 of Invoice
}

// Violating dataset - intentionally breaks constraints
dataset Invalid violating {
  bad_invoices: 100 of Invoice
}
```

## OpenAPI Schema Import

```vague
import petstore from "petstore.json"

schema Pet from petstore.Pet {
  age: int in 1..15  // Override or add fields
}

dataset TestData {
  pets: 50 of Pet
}
```
