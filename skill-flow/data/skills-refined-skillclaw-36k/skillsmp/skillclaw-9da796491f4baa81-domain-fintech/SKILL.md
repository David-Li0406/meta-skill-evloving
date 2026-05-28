---
name: domain-fintech
description: Use this skill when building fintech applications that require precise financial calculations and compliance with audit trails.
---

# FinTech Domain

> **Layer 3: Domain Constraints**

## Domain Constraints → Design Implications

| Domain Rule | Design Constraint | Rust Implication |
|-------------|-------------------|------------------|
| Audit trail | Immutable records | Arc<T>, no mutation |
| Precision | No floating point | rust_decimal |
| Consistency | Transaction boundaries | Clear ownership |
| Compliance | Complete logging | Structured tracing |
| Reproducibility | Deterministic execution | No race conditions |

---

## Critical Constraints

### Financial Precision

```
RULE: Never use f64 for money
WHY: Floating point loses precision
RUST: Use rust_decimal::Decimal
```

### Audit Requirements

```
RULE: All transactions must be immutable and traceable
WHY: Regulatory compliance, dispute resolution
RUST: Arc<T> for sharing, event sourcing pattern
```

### Consistency

```
RULE: Money can't disappear or appear
WHY: Double-entry accounting principles
RUST: Transaction types with validated totals
```

---

## Trace Down ↓

From constraints to design (Layer 2):

```
"Need immutable transaction records"
    ↓ m09-domain: Model as Value Objects
    ↓ m01-ownership: Use Arc for shared immutable data

"Need precise decimal math"
    ↓ m05-type-driven: Newtype for Currency/Amount
    ↓ rust_decimal: Use Decimal type

"Need transaction boundaries"
    ↓ m12-lifecycle: RAII for transaction scope
    ↓ m09-domain: Aggregate boundaries
```

---

## Key Crates

| Purpose | Crate |
|---------|-------|
| Decimal math | rust_decimal |
| Date/time | chrono, time |
| UUID | uuid |
| Serialization | serde |
| Validation | validator |

## Design Patterns

| Pattern | Purpose | Implementation |
|---------|---------|----------------|
| Currency newtype | Type safety | `struct Amount(Decimal);` |
| Transaction | Atomic operations | Event sourcing |
| Audit log | Traceability | Structured logging with trace IDs |
| Ledger | Double-entry | Debit/credit balance |

## Code Pattern: Currency Type

```rust
use rust_decimal::Decimal;

#[derive(Clone, Debug, PartialEq)]
pub struct Amount {
    value: Decimal,
    currency: Currency,
}

impl Amount {
    pub fn new(value: Decimal, currency: Currency) -> Self {
        Self { value, currency }
    }

    pub fn add(&self, other: &Amount) -> Amount {
        // Implementation for adding two Amounts
    }
}
```