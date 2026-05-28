---
name: documentation
description: Guide to writing accessible, maintainable, and "evolution-ready" documentation.
---
# Documentation Skill

## 1. The "why", not just the "what"
*   **Bad:** `// Sets i to 0` (Redundant)
*   **Good:** `// Initialize counter to reset retry logic` (Intent)

## 2. README.md Structure
Every app and complex component needs a README.

### Template
```markdown
# [Name]

[One line pitch: What does this do?]

## Overview
[Architecture diagram or explanation of the data flow]

## Setup / Installation
[Prerequisites and commands]

## Usage
[Examples of common tasks]

## Key Concepts
*   **Concept A:** ...
*   **Concept B:** ...
```

## 3. SCL Documentation
Explain the *business validation* behind the schema.

```scl
table order {
  # We use a decimal with 4 digits precision to handle
  # fractional crypto-currency amounts, not just USD.
  required amount, :decimal {
    digits 18
    decimals 8
  }
}
```

## 4. Code Comments (JS/TS)
Use JSDoc to document the "Contract" of functions.

```typescript
/**
 * Calculates the final price including tax and discounts.
 * 
 * @param basePrice - The catalog price
 * @param userRegion - Used to determine tax rate (e.g. EU vs US)
 * @returns Final amount in cents
 */
export function calculateTotal(basePrice: number, userRegion: string): number { ... }
```
