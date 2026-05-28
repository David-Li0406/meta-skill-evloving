---
name: code-refactoring
description: Use this skill when improving code quality, modernizing legacy code, or addressing technical debt through systematic refactoring techniques.
---

# Code Refactoring

## Overview

This skill guides systematic code refactoring to improve code quality, maintainability, and design while preserving functionality. Follow the safe refactoring workflow with comprehensive test coverage and incremental changes.

## Refactoring Workflow

### Step 1: Analyze Code and Identify Issues

Examine the codebase to identify code smells and quality issues:

- Long methods or large classes
- Duplicated code blocks or similar logic
- Unclear or misleading names for variables, methods, or classes
- Complex conditional logic or deeply nested structures
- Poor separation of concerns or tight coupling between components

### Step 2: Verify Test Coverage

Before refactoring any code:

1. Check existing test coverage for the code to be refactored.
2. If tests are missing or inadequate, write tests first.
3. Run all tests to establish a baseline (all should pass).
4. Never proceed without adequate test coverage.

### Step 3: Choose Refactoring Technique

Select the appropriate refactoring pattern based on the identified issues:

- **Extract Method/Function**: Break down long methods into smaller, focused ones.
- **Extract Class**: Split large classes with multiple responsibilities.
- **Rename**: Improve clarity with better names.
- **Move Method/Field**: Relocate functionality to more appropriate classes.
- **Replace Conditional with Polymorphism**: Simplify complex conditionals.
- **Introduce Parameter Object**: Group related parameters.
- **Inline Method/Variable**: Remove unnecessary indirection.

### Step 4: Apply Refactoring Incrementally

Make one small change at a time:

1. Apply a single refactoring technique.
2. Run all tests immediately after the change.
3. If tests pass, commit the change.
4. If tests fail, revert and try a different approach.
5. Repeat for each refactoring needed.

**Critical Rules:**

- Never change behavior while refactoring.
- Never refactor and add features simultaneously.
- Use IDE automated refactoring tools when available.
- Keep each refactoring commit small and focused.

### Step 5: Verify and Document

After completing refactorings:

1. Run the full test suite to ensure all tests pass.
2. Check that code quality metrics improved.
3. Review code to confirm readability enhanced.
4. Document significant architectural changes if needed.
5. Create clear commit messages describing refactorings.

## Common Refactoring Scenarios

Guidance is available for:

- Legacy code modernization
- Preparing code for new features
- Performance optimization through refactoring
- Reducing technical debt systematically
- Extracting reusable components

## Best Practices and Quality Guidelines

Follow established principles for high-quality refactoring:

- Apply SOLID principles (Single Responsibility, Open/Closed, etc.).
- Reduce coupling between components.
- Increase cohesion within components.
- Eliminate duplication (DRY principle).
- Maintain consistent coding standards.

## Tools and Automation

Modern IDEs and tools can automate many refactorings safely:

- IDE refactoring features (IntelliJ, VS Code, Visual Studio).
- Static analysis tools for code smell detection.
- Test coverage tools.
- Automated code formatting and linting.

## Refactoring Patterns

### Extract Method

**Before:**
```python
def print_invoice(invoice):
    print("***********************")
    print("**** Invoice ****")
    print("***********************")
    
    # Print details
    print(f"Name: {invoice.customer_name}")
    print(f"Address: {invoice.customer_address}")
    print(f"Total: ${invoice.total}")
```

**After:**
```python
def print_invoice(invoice):
    print_banner()
    print_details(invoice)

def print_banner():
    print("***********************")
    print("**** Invoice ****")
    print("***********************")

def print_details(invoice):
    print(f"Name: {invoice.customer_name}")
    print(f"Address: {invoice.customer_address}")
    print(f"Total: ${invoice.total}")
```

### Replace Conditional with Polymorphism

**Before:**
```python
class Bird:
    def __init__(self, bird_type):
        self.type = bird_type
    
    def fly(self):
        if self.type == "sparrow":
            return "Flying short distances"
        elif self.type == "eagle":
            return "Soaring high"
        elif self.type == "penguin":
            return "Cannot fly"
```

**After:**
```python
from abc import ABC, abstractmethod

class Bird(ABC):
    @abstractmethod
    def fly(self):
        pass

class Sparrow(Bird):
    def fly(self):
        return "Flying short distances"

class Eagle(Bird):
    def fly(self):
        return "Soaring high"

class Penguin(Bird):
    def fly(self):
        return "Cannot fly"
```

## When to Use This Skill

Use this skill when:
- Improving code quality
- Reducing technical debt
- Modernizing legacy code
- Preparing for new features
- Eliminating code smells
- Implementing design patterns
- Optimizing performance
- Improving testability
- Making code more maintainable
- Cleaning up after rapid development