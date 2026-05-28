---
name: dry_optimization
description: Detects duplicate code and logic, suggesting abstractions, high-order functions, or strategy patterns.
---

# DRY Optimization Skill

**Goal**: Eliminate repetition (Don't Repeat Yourself) and improve maintainability.

## Instructions

Analyze the specified directory or source root.

### 1. Analysis Steps

- **Scan**: Look for code blocks with similar logic (not just identical text from copy-paste).
- **Magic Values**: Identify hardcoded magic numbers or strings.

### 2. Refactoring Suggestions

- **Abstraction**: Create higher-order functions or common components to replace repeated logic.
- **Constants**: Extract magic values to a constant file or config.
- **Patterns**: Use Strategy Pattern or Factory Pattern to replace complex `if-else` or `switch` statements.

### 3. Output

- List discovered duplicates (Snippet A vs Snippet B).
- Show the refactored common function code.
