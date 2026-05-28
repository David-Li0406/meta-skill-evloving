---
name: code-review
description: Reviews code changes for bugs, style issues, and best practices. Use when looking for errors or improving code quality.
---

# Code Review Skill

When reviewing code, systematically check the following areas:

## 1. Correctness & Logic

- **Boundary Conditions**: Are edge cases (empty lists, None values, zero division) handled?
- **Error Handling**: Are exceptions caught specifically? (No bare `except:`).
- **Type Safety**: Do function signatures match their usage?

## 2. Architecture & Design

- **Single Responsibility**: Does the function/class do one thing?
- **Coupling**: Are dependencies manageable? (e.g., UI code shouldn't import low-level processors directly if possible).
- **Resource Management**: Are files and GPU memory released properly? (Look for `try...finally` or context managers).

## 3. Style & Conventions

- **Naming**: Do names reflect intent? (e.g., `pnm_adjacency` vs `adjacency`).
- **Docstrings**: Are complex logic blocks explained?
- **Imports**: Are imports grouped and sorted?

## 4. Performance (Specific to CT/Volume Data)

- **Vectorization**: Is `numpy`/`cupy` used instead of explicit loops?
- **Memory**: Are large arrays copied unnecessarily?
- **GPU Usage**: Is generic `try-import` used for optional GPU backends?

## Output Format

Provide feedback in a structured list:

- **Severity**: [Critical/Major/Minor]
- **File**: [Filename]
- **Issue**: [Description]
- **Suggestion**: [Proposed Fix]
