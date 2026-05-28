---
name: go-interfaces
description: Go interface design patterns and best practices
---

# Interface Design

Master Go's approach to interfaces: implicit satisfaction, consumer-driven design, and composition patterns.

## Route by Concern

- **Accept/return patterns** → see [design/](design/)
  - Accept interfaces, return structs principle
  - When to deviate from the rule

- **Interface pollution** → see [pollution/](pollution/)
  - Detecting unnecessary abstractions
  - Premature interface creation

- **Embedding patterns** → see [embedding/](embedding/)
  - Interface composition techniques
  - Method set expansion

## Quick Check

- [ ] Interface defined by consumer, not producer
- [ ] Keep interfaces small (<5 methods)
- [ ] Return concrete types from functions
- [ ] No interface{} unless truly necessary
