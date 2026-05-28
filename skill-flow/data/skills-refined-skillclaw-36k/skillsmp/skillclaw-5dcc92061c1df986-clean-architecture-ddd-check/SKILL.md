---
name: clean-architecture-ddd-check
description: Use this skill to validate and implement Clean Architecture and Domain-Driven Design (DDD) principles in your software projects.
---

# Skill body

## Overview

This skill helps ensure that your implementation adheres to Clean Architecture and Domain-Driven Design (DDD) principles. It verifies the consistency between your AIDLC (AI-Driven Life Cycle) documentation and the implementation code, detecting domain model violations early.

## Input Format

You can specify the target for verification when invoking the skill:

```
/clean-architecture-ddd-check
```

Or validate specific files/directories:

```
/clean-architecture-ddd-check --domain-only
/clean-architecture-ddd-check --file src/domain/entities/cart.py
```

## Execution Process

### Step 1: Check Ubiquitous Language Consistency

**Verification Content**:
- Ensure terms defined in `aidlc-docs/construction/unit_01_ai_dialog_public/docs/ubiquitous_language.md` are used correctly in the code.

**Files to Check**:
```bash
# Read the Ubiquitous Language definition
main/aidlc-docs/construction/unit_01_ai_dialog_public/docs/ubiquitous_language.md

# Check terms used in the code
main/backend/src/domain/**/*.py
```

**Check Items**:

#### 1. Core Domain Terms Usage

| Japanese | English | Example in Code |
|----------|---------|------------------|
| 買い目   | BetSelection | `class BetSelection` (Value Object) |
| カート   | Cart | `class Cart` (Entity) |
| カートアイテム | CartItem | `class CartItem` (Entity) |
| 相談セッション | ConsultationSession | `class ConsultationSession` (Aggregate Root) |
| メッセージ | Message | `class Message` (Entity) |
| データフィードバック | DataFeedback | `class DataFeedback` (Value Object) |
| 掛け金フィードバック | AmountFeedback | `class AmountFeedback` (Value Object) |

**Verification Method**:
```bash
# Check if terms are used correctly
grep -r "class BetSelection" main/backend/src/domain/value_objects/
grep -r "class Cart" main/backend/src/domain/entities/
```

**Violation Patterns**:
- ❌ `BettingSelection` (Incorrect term)
- ❌ `ShoppingCart` (Term from a different domain)
- ❌ `OrderItem` (E-commerce term mixed in)

#### 2. Support Domain Terms Usage

| Japanese | English | Handling |
|----------|---------|----------|
| レース   | Race | External data (Read Model) |
| 開催場   | Venue | External data |
| 出走馬   | Runner | External data |
| 騎手     | Jockey | External data |
| オッズ   | Odds | External data |

**Verification Method**:
- Support domain concepts should only be retrieved via ports (e.g., `RaceDataProvider`) and must not be implemented as domain entities.

**Violation Patterns**:
- ❌ `class Race(Entity)` implemented in the domain layer
- ❌ Adding business logic to the `Race` class

### Step 2: Verify Layer Separation

**Directory Structure Check**:
```
main/backend/src/
├── domain/              # Domain layer (business logic)
│   ├── entities/        # Entities (with identifiers)
│   ├── value_objects/   # Value Objects (immutable)
│   ├── services/        # Domain Services
│   ├── ports/           # Interfaces (ports)
│   ├── identifiers/     # Identifiers (ID types)
│   └── enums/           # Enumerations
├── application/         # Application layer (use cases)
│   └── use_cases/
├── infrastructure/      # Infrastructure layer (external system integration)
│   ├── providers/       # Providers (adapters)
│   └── repositories/
└── api/                 # API layer (Lambda handlers)
    └── handlers/
```

**Verification Rules**:
- Ensure that the directory structure adheres to the principles of Clean Architecture, maintaining clear separation of concerns across layers.