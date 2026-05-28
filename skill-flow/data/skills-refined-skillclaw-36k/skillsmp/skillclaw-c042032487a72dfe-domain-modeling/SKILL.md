---
name: domain-modeling
description: Use this skill when you need to model domain concepts in software, particularly in the context of domain-driven design (DDD).
---

# Domain Modeling

> **Layer 2: Design Choices**

## Core Question

**What is this concept's role in the domain?**

Before modeling in code, understand:
- Is it an Entity (identity matters) or Value Object (interchangeable)?
- What invariants must be maintained?
- Where are the aggregate boundaries?

---

## Domain Concept → Rust Pattern

| Domain Concept | Rust Pattern | Ownership Implication |
|----------------|--------------|----------------------|
| Entity | struct + Id | Owned, unique identity |
| Value Object | struct + Clone/Copy | Shareable, immutable |
| Aggregate Root | struct owns children | Clear ownership tree |
| Repository | trait | Abstracts persistence |
| Domain Event | enum | Captures state changes |
| Service | impl block / free fn | Stateless operations |

---

## Thinking Prompt

Before creating a domain type:

1. **What's the concept's identity?**
   - Needs unique identity → Entity (Id field)
   - Interchangeable by value → Value Object (Clone/Copy)

2. **What invariants must hold?**
   - Always valid → private fields + validated constructor
   - Transition rules → type state pattern

3. **Who owns this data?**
   - Single owner (parent) → owned field
   - Shared reference → Arc/Rc
   - Weak reference → Weak

---

## Trace Up ↑

To domain constraints (Layer 3):

```
"How should I model a Transaction?"
    ↑ Ask: What domain rules govern transactions?
    ↑ Check: domain-fintech (audit, precision requirements)
    ↑ Check: Business stakeholders (what invariants?)
```

| Design Question | Trace To | Ask |
|-----------------|----------|-----|
| Entity vs Value Object | domain-* | What makes two instances "the same"? |
| Aggregate boundaries | domain-* | What must be consistent together? |
| Validation rules | domain-* | What business rules apply? |

---

## Trace Down ↓

To implementation (Layer 1):

```
"Model as Entity"
    ↓ m01-ownership: Owned, unique
    ↓ m05-type-driven: Newtype for Id

"Model as Value Object"
    ↓ m01-ownership: Clone/Copy OK
    ↓ m05-type-driven: Validate at construction

"Model as Aggregate"
    ↓ m01-ownership: Parent owns children
    ↓ m02-resource: Consider Rc for shared within aggregate
```

---

## Quick Reference

| DDD Concept | Rust Pattern | Example |
|-------------|--------------|---------|
| Entity      | struct + Id  |         |
| Value Object| struct + Clone/Copy |   |
| Aggregate Root | struct owns children | |
| Repository   | trait        |         |
| Domain Event | enum         |         |
| Service      | impl block / free fn | |