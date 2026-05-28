---
name: srp_enforcer
description: Analyzes modules for Single Responsibility Principle violations and proposes splitting plans (Service, Repository, Utils, Controller).
---

# SRP Enforcer Skill

**Goal**: Fix "unclear responsibilities" and adhere to the Single Responsibility Principle (SRP).

## Instructions

Analyze the specified file or module.

### 1. Analysis Criteria

- **Mixed Concerns**: Does the file mix UI logic, business logic, persistence, and utility methods?
- **Size**: Identify classes or functions > 300 lines. Are they doing too much?

### 2. Split Plan (Proposal)

Propose a split plan *before* executing:

- **Service**: Business logic
- **Repository**: Data access
- **Utils**: Helper methods
- **Controller**: Flow control

### 3. Execution (After Confirmation)

- Create new files for the split components.
- Ensure interfaces remain compatible or provide refactoring suggestions for call sites.
- Verify that the original file is significantly smaller and more focused.
