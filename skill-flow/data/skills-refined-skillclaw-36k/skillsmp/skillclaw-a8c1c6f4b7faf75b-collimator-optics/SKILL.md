---
name: collimator-optics
description: Use this skill when working with the Collimator library for Lean 4 to access and modify nested data structures using profunctor optics like lenses, prisms, and traversals.
---

# Collimator Optics Library

## Overview

Collimator is a profunctor optics library for Lean 4 that provides composable, type-safe access patterns for nested data structures.

## Setup

```lean
import Collimator.Prelude      -- Core optic types and operations
import Collimator.Operators    -- Haskell-style operators
import Collimator.Combinators  -- Advanced combinators
import Collimator.Instances    -- Instances for List, Option, String
open Collimator
open scoped Collimator.Operators  -- Enable operator syntax
```

## Optic Types

| Optic | Focus | Read | Write |
|-------|-------|------|-------|
| `Iso' s a` | Exactly 1 (reversible) | Yes | Yes |
| `Lens' s a` | Exactly 1 | Yes | Yes |
| `Prism' s a` | 0 or 1 (sum types) | Maybe | Yes |
| `AffineTraversal' s a` | 0 or 1 | Maybe | Yes |
| `Traversal' s a` | 0 or more | List | Yes |

## Operators

| Op | Name | Example |
|----|------|---------|
| `^.` | view | `person ^. personName` |
| `^?` | preview | `val ^? _someVariant` |
| `.~` | set | `person & personAge .~ 30` |
| `%~` | over | `person & personAge %~ (· + 1)` |
| `&` | pipe | `x & lens .~ v` |
| `∘` | compose | `outer ∘ inner` |

## Creating Optics

### Lenses (struct fields)

```lean
structure Person where
  name : String
  age : Nat

-- Preferred: use fieldLens% macro
def nameLens : Lens' Person String := fieldLens% Person name
```

### Prisms (sum type constructors)

```lean
inductive JsonValue
  | str : String → JsonValue
  | num : Int → JsonValue

-- Preferred: use ctorPrism% macro
def strPrism : Prism' JsonValue String := ctorPrism% JsonValue.str

-- For Option.some
def somePrism (α : Type) : Prism' (Option α) α := ctorPrism% Option.some
```

## Composition

Optics compose with `∘`. Use `optic%` for type annotations:

```lean
-- Lens ∘ Prism = AffineTraversal
let emailAffine := optic%
  userProfileLens ∘ somePrism Profile ∘ emailLens
  : AffineTraversal' User String

user ^? emailAffine              -- Option String
user & emailAffine %~ toUpper    -- Modify if present
```

## Common Patterns

### Filtering
```lean
[-1, 2, -3, 4] & filteredList (· > 0) %~ (· * 2)  -- [-1, 4, -3, 8]
```

### List operations
```lean
[1, 2, 3] ^? _head                    -- some 1
[1, 2, 3, 4] & taking 2 %~ (· * 10)   -- [10, 20, 3, 4]
```

### Nested Access
```lean
employee ^. (employeeAddress ∘ addressCity)
```

### Chained Updates
```lean
config
  & configHost .~ "localhost"
  & configPort .~ 8080
```

### Conditional via Prism
```lean
if (val ^? _error).isSome then handleError else continue
```

## File Organization

To avoid circular imports:
1. Put structures in `Types.lean`
2. Put `makeLenses` calls in `Optics.lean` (imports Types)
3. Put methods in other files (import Optics)