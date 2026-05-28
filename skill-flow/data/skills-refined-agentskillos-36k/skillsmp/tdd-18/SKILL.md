---
name: tdd
description: Guide development following Kent Beck's Test-Driven Development (TDD) using Red → Green → Refactor cycle. Use when writing tests first, implementing features with TDD, need to write failing tests, make tests pass, refactoring after tests pass, following red-green-refactor, fixing defects with tests, or practicing test-driven development methodology.
---

# Test-Driven Development (TDD)

## Instructions
Follow Kent Beck's Test-Driven Development (TDD) methodology precisely using the Red → Green → Refactor cycle.

### Core TDD Principles

#### The TDD Cycle
Always follow: **Red → Green → Refactor**

1. **Red**: Write a failing test
2. **Green**: Write minimal code to make it pass
3. **Refactor**: Improve structure while keeping tests green

### Test Writing Guidelines

#### Writing Tests
- Write the simplest failing test first
- Start by writing a failing test that defines a small increment of functionality
- Use meaningful test names that describe behavior (e.g., "shouldSumTwoPositiveNumbers")
- Make test failures clear and informative
- Write just enough code to make the test pass - no more
- Always write one test at a time

#### Test Execution
- Run tests to confirm they pass (Green)
- Always run all the tests (except long-running tests) each time
- Once tests pass, consider if refactoring is needed
- Repeat the cycle for new functionality

#### Defect Fixing
When fixing a defect:
1. First write an API-level failing test
2. Then write the smallest possible test that replicates the problem
3. Get both tests to pass

### Implementation Guidelines

#### Minimum Implementation
- Implement the minimum code needed to make tests pass
- Use the simplest solution that could possibly work
- Write just enough code to make the test pass - no more

#### Code Quality
- Eliminate duplication ruthlessly
- Express intent clearly through naming and structure
- Make dependencies explicit
- Keep methods small and focused on a single responsibility
- Minimize state and side effects

### Refactoring in TDD

#### When to Refactor
- Refactor only when tests are passing (in the "Green" phase)
- Never refactor when tests are failing

#### How to Refactor
- Use established refactoring patterns with their proper names
- Make one refactoring change at a time
- Run tests after each refactoring step
- Prioritize refactorings that remove duplication or improve clarity

### TDD Workflow

#### Standard Feature Development
1. Write a simple failing test for a small part of the feature
2. Implement the bare minimum to make it pass
3. Run tests to confirm they pass (Green)
4. Make any necessary structural changes, running tests after each change
5. Add another test for the next small increment of functionality
6. Repeat until the feature is complete

### Discipline
- Always write one test at a time
- Make it run
- Improve structure
- Maintain high code quality throughout development

### Commit Standards

Use the `commit-message` skill format for all commits.

Only commit when:
1. ALL tests are passing
2. ALL compiler/linter warnings have been resolved
3. The change represents a single logical unit of work

Use small, frequent commits rather than large, infrequent ones.

## Examples

### Example 1: Simple Calculator Function (Complete TDD Cycle)

#### Step 1: Red - Write Failing Test
```go
// calculator_test.go
package calculator

import "testing"

func TestShouldAddTwoPositiveNumbers(t *testing.T) {
    result := Add(2, 3)
    if result != 5 {
        t.Errorf("Add(2, 3) = %d; want 5", result)
    }
}
```

Run test: ❌ **FAILS** - `Add` function doesn't exist

#### Step 2: Green - Minimum Code to Pass
```go
// calculator.go
package calculator

func Add(a, b int) int {
    return 5  // Hardcoded to pass the specific test
}
```

Run test: ✅ **PASSES**

#### Step 3: Add Another Test (Red)
```go
func TestShouldAddTwoPositiveNumbers(t *testing.T) {
    result := Add(2, 3)
    if result != 5 {
        t.Errorf("Add(2, 3) = %d; want 5", result)
    }
}

func TestShouldAddDifferentNumbers(t *testing.T) {
    result := Add(1, 4)
    if result != 5 {
        t.Errorf("Add(1, 4) = %d; want 5", result)
    }
}
```

Run tests: ❌ **FAILS** - Second test fails

#### Step 4: Implement Real Logic (Green)
```go
func Add(a, b int) int {
    return a + b  // Now properly implements addition
}
```

Run tests: ✅ **ALL PASS**

#### Step 5: Refactor (if needed)
No refactoring needed yet - code is simple and clear.

### Example 2: User Validation with Refactoring

#### Red - Write Failing Test
```go
// user_validator_test.go
package validator

import "testing"

func TestShouldValidateEmailFormat(t *testing.T) {
    validator := NewUserValidator()

    tests := []struct {
        email string
        want  bool
    }{
        {"user@example.com", true},
        {"invalid-email", false},
    }

    for _, tt := range tests {
        got := validator.ValidateEmail(tt.email)
        if got != tt.want {
            t.Errorf("ValidateEmail(%q) = %v; want %v", tt.email, got, tt.want)
        }
    }
}
```

Run test: ❌ **FAILS**

#### Green - Minimum Implementation
```go
// user_validator.go
package validator

import "strings"

type UserValidator struct{}

func NewUserValidator() *UserValidator {
    return &UserValidator{}
}

func (v *UserValidator) ValidateEmail(email string) bool {
    return strings.Contains(email, "@")  // Simplest check
}
```

Run test: ✅ **PASSES**

#### Add More Tests (Red)
```go
func TestShouldValidateEmailFormat(t *testing.T) {
    validator := NewUserValidator()

    tests := []struct {
        email string
        want  bool
    }{
        {"user@example.com", true},
        {"invalid-email", false},
        {"@example.com", false},
        {"user@", false},
    }

    for _, tt := range tests {
        got := validator.ValidateEmail(tt.email)
        if got != tt.want {
            t.Errorf("ValidateEmail(%q) = %v; want %v", tt.email, got, tt.want)
        }
    }
}
```

Run test: ❌ **FAILS** - Last two cases fail

#### Improve Implementation (Green)
```go
func (v *UserValidator) ValidateEmail(email string) bool {
    if !strings.Contains(email, "@") {
        return false
    }
    parts := strings.Split(email, "@")
    return len(parts) == 2 && parts[0] != "" && parts[1] != ""
}
```

Run test: ✅ **ALL PASS**

#### Refactor - Extract Method
```go
// Structural change - extract to improve readability
func (v *UserValidator) ValidateEmail(email string) bool {
    if !v.hasAtSymbol(email) {
        return false
    }
    return v.hasLocalAndDomain(email)
}

func (v *UserValidator) hasAtSymbol(email string) bool {
    return strings.Contains(email, "@")
}

func (v *UserValidator) hasLocalAndDomain(email string) bool {
    parts := strings.Split(email, "@")
    return len(parts) == 2 && parts[0] != "" && parts[1] != ""
}
```

Run test: ✅ **ALL PASS** - Behavior unchanged, structure improved

### Example 3: Fixing a Defect

#### Step 1: Write API-Level Failing Test
```go
// Bug report: CalculateDiscount returns wrong value for 100% discount
func TestShouldCalculateFullDiscount(t *testing.T) {
    order := Order{Total: 100, DiscountPercent: 100}
    got := CalculateOrderTotal(order)
    want := 0

    if got != want {
        t.Errorf("CalculateOrderTotal(%v) = %d; want %d", order, got, want)
    }
}
```

Run test: ❌ **FAILS** - Returns -100 instead of 0

#### Step 2: Write Smallest Test Replicating Problem
```go
func TestShouldHandlePercentageCalculation(t *testing.T) {
    got := CalculateDiscount(100, 100)
    want := 100

    if got != want {
        t.Errorf("CalculateDiscount(100, 100) = %d; want %d", got, want)
    }
}
```

Run test: ❌ **FAILS**

#### Step 3: Fix the Bug
```go
// Before (buggy)
func CalculateDiscount(total int, percent int) int {
    return total - (total * percent / 100)
}

// After (fixed)
func CalculateDiscount(total int, percent int) int {
    return total * percent / 100  // Returns discount amount, not final price
}

func CalculateOrderTotal(order Order) int {
    discount := CalculateDiscount(order.Total, order.DiscountPercent)
    finalTotal := order.Total - discount
    if finalTotal < 0 {
        return 0
    }
    return finalTotal
}
```

Run tests: ✅ **BOTH PASS**

### Key Patterns in Examples

1. **Always write test first** - Never write production code without a failing test
2. **Make smallest possible change** - Don't solve future problems
3. **Run tests after every change** - Immediate feedback
4. **Refactor only when green** - Safe to restructure
5. **One test at a time** - Focus on single behavior
6. **Separate commits** - Structural vs behavioral changes
