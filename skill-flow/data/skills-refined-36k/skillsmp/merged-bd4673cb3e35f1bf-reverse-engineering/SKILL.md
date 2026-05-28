---
name: reverse-engineering
description: Use this skill to reverse engineer existing code into SDD specification documents, particularly for analyzing legacy code and documenting undocumented systems.
---

# Reverse Engineering to SDD Specification Guide

> **Languages**: [English](../../../../../skills/claude-code/reverse-engineer/SKILL.md) | 繁體中文 | 简体中文

**Version**: 1.1.0  
**Last Updated**: 2026-01-19  
**Applicable Scope**: Claude Code Skills

> **Core Specification**: This skill implements the [reverse engineering standards](../../../core/reverse-engineering-standards.md). Any AI tool can refer to the core specifications for complete methodology documentation.

---

## Purpose

This skill guides you in reverse engineering existing code into SDD (Specification Driven Development) specification documents while strictly adhering to anti-hallucination standards.

## Quick Reference

### Reverse Engineering Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│              Reverse Engineering Workflow                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1️⃣  Code Analysis (AI Automation)                             │
│      ├─ Scan code structure, APIs, data models                 │
│      ├─ Parse existing tests to extract acceptance criteria     │
│      └─ Generate draft specifications (with uncertainty tags)   │
│                                                                 │
│  2️⃣  Human Input (Necessary)                                   │
│      ├─ Write motivation (why this feature is needed)          │
│      ├─ Add risk assessment                                       │
│      └─ Validate dependencies and business context              │
│                                                                 │
│  3️⃣  Review and Confirmation                                     │
│      ├─ Discuss with stakeholders                                │
│      └─ Confirm [Confirmed] / [Inferred] / [Unknown] tags      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Extractable and Non-Extractable Content

| Aspect         | Extractable | Certainty | Notes                          |
|----------------|-------------|-----------|--------------------------------|
| **API Endpoints** | ✅ Yes     | [Confirmed] | Route definitions, HTTP methods |
| **Data Models**   | ✅ Yes     | [Confirmed] | Types, interfaces, structure descriptions |
| **Function Signatures** | ✅ Yes | [Confirmed] | Parameters, return types       |
| **Test Cases**    | ✅ Yes     | [Confirmed] | → Acceptance criteria          |
| **Dependencies**  | ✅ Yes     | [Confirmed] | Package references             |
| **Behavior Patterns** | ⚠️ Partial | [Inferred] | Inferred from code analysis    |
| **Motivation/Why** | ❌ No     | [Unknown] | Requires human input           |
| **Business Context** | ❌ No   | [Unknown] | Requires human input           |
| **Risk Assessment** | ❌ No    | [Unknown] | Requires domain expertise      |
| **Trade-offs**    | ❌ No     | [Unknown] | Lacks historical context       |

## Core Principles

### 1. Anti-Hallucination Compliance

**Key**: This skill must strictly adhere to the [anti-hallucination standards](../../../core/anti-hallucination.md).

#### Certainty Tags

| Tag         | Usage Context                          | Example                               |
|-------------|----------------------------------------|---------------------------------------|
| `[Confirmed]` | Direct evidence from code/tests       | API endpoint in `src/api/users.ts:15` |
| `[Inferred]`  | Reasonable inference from patterns    | "Dependency injection may be used based on constructor patterns" |
| `[Unknown]`   | Cannot be determined from code       | Motivation, business needs            |
| `[Needs Confirmation]` | Requires human validation | Design intent, boundary case handling |

#### Source Annotation

Each extracted item must include source annotations:

```markdown
## API Design

### User Authentication
[Confirmed] POST /api/auth/login endpoint accepts email and password
- [Source: Code] src/controllers/AuthController.ts:25-45
- [Source: Code] src/routes/auth.ts:8

### Session Management
[Inferred] Based on JWT expiration settings, sessions expire after 24 hours
- [Source: Code] src/config/auth.ts:12 - TOKEN_EXPIRY=86400
- [Source: Knowledge] Standard JWT expiration explanation (⚠️ Please verify intent)
```

### 2. Progressive Disclosure

Start with high-level architecture and then drill down:

1. **System Overview**: Entry points, main components
2. **Component Details**: Individual modules and their responsibilities
3. **Implementation Details**: Algorithms, data flows

### 3. Test Correspondence Requirements

Extract acceptance criteria from tests:

```javascript
// Test file: src/tests/auth.test.ts
describe('Authentication', () => {
  it('should return 401 for invalid credentials', () => {...});
  it('should issue a JWT token on successful login', () => {...});
  it('should refresh the token before expiration', () => {...});
});
```

Convert to:

```markdown
## Acceptance Criteria
[Inferred] From test analysis (src/tests/auth.test.ts):
- [ ] Return 401 status code for invalid credentials
- [ ] Issue JWT token on successful login
- [ ] Support token refresh before expiration
```

## Workflow Stages

### Stage 1: Code Scanning

**Input**: File path or directory  
**Output**: Code structure analysis

**Actions**:
1. Identify entry points (main functions, API routes, event handlers)
2. Map module dependencies
3. Extract type definitions and interfaces
4. List configuration sources

### Stage 2: Test Analysis

**Input**: Test files  
**Output**: Acceptance criteria candidates

**Actions**:
1. Parse test case names
2. Extract Given-When-Then patterns (if BDD style)
3. Identify boundary conditions
4. Record coverage gaps

### Stage 3: Gap Identification

**Input**: Code + Test Analysis  
**Output**: List of unknown items requiring human input

**Necessary Human Input**:
- [ ] Motivation: Why is this feature being built?
- [ ] User Stories: Who uses this feature? For what purpose?
- [ ] Risks: What could go wrong?
- [ ] Trade-offs: Why choose this approach over alternatives?
- [ ] Out of Scope: Clearly state what is excluded.

### Stage 4: Specification Generation

**Input**: All analysis results  
**Output**: Draft specification document

**Template**: Use [reverse-spec-template.md](../../../templates/reverse-spec-template.md)

### Stage 5: Human Review

**Input**: Draft specification  
**Output**: Verified specification

**Review Checklist**:
- [ ] All `[Confirmed]` items verified for accuracy
- [ ] All `[Inferred]` items validated or corrected
- [ ] All `[Unknown]` items filled by humans
- [ ] Source citations checked
- [ ] Business context added

## Examples

### Example 1: API Endpoint Extraction

**Input Code** (`src/controllers/UserController.ts`):
```typescript
export class UserController {
  @Get('/users/:id')
  @Authorize('admin', 'user')
  async getUser(@Param('id') id: string): Promise<User> {
    return this.userService.findById(id);
  }
}
```

**Extracted Specification**:
```markdown
## API Endpoints

### GET /users/:id
[Confirmed] Retrieve user by ID
- [Source: Code] src/controllers/UserController.ts:3-7

**Authorization**: [Confirmed] Requires 'admin' or 'user' role
- [Source: Code] @Authorize decorator on line 4

**Parameters**:
- `id` (path, required): User identifier [Confirmed]

**Response**: [Confirmed] Returns User object
- [Source: Code] Return type on line 5

**Error Handling**: [Unknown] Error response cannot be clearly determined from code
```

### Example 2: Test Conversion to Standards

**Input Test** (`src/tests/cart.test.ts`):
```typescript
describe('Shopping Cart', () => {
  it('should add item to empty cart', () => {...});
  it('should increase quantity for duplicate items', () => {...});
  it('should not exceed maximum quantity of 99', () => {...});
  it('should calculate total including tax', () => {...});
});
```

**Extracted Acceptance Criteria**:
```markdown
## Acceptance Criteria

[Inferred] From test analysis (src/tests/cart.test.ts):
- [ ] Can add item to empty cart (line 2)
- [ ] Increase quantity for duplicate items (line 3)
- [ ] Maximum quantity limit: 99 items (line 4)
- [ ] Total calculation includes tax (line 5)

[Unknown] Tax calculation rules not specified in tests
[Needs Confirmation] What happens when the cart exceeds 99 items? (Reject or limit?)
```

## Integration with Other Skills

### With /spec (Specification Driven Development)

1. Use `/reverse-spec` to generate reverse engineering specifications
2. Review and fill in `[Unknown]` blocks
3. Use `/spec review` to verify completeness
4. Continue normal SDD workflow for enhancements

### With /tdd (Test Driven Development)

1. Extract existing test patterns
2. Identify test coverage gaps
3. Use `/tdd` to add missing tests
4. Update specifications with new acceptance criteria

### With /bdd (Behavior Driven Development)

1. Convert extracted acceptance criteria to Gherkin format
2. Use `/bdd` to formalize scenarios
3. Validate scenarios with stakeholders

## Complete Reverse Engineering Pipeline

The reverse engineering skill supports a complete SDD → BDD → TDD pipeline:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        Complete Reverse Engineering Pipeline              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Code + Tests                                                         │
│        │                                                                │
│        ▼                                                                │
│   /reverse-spec                                                         │
│        │                                                                │
│        └─→ Generate SPEC-XXX with acceptance criteria                   │
│                │                                                        │
│                ▼                                                        │
│   /reverse-bdd                                                          │
│        │                                                                │
│        ├─→ AC → Gherkin scenario conversion                              │
│        ├─→ List-style automatic conversion to Given-When-Then          │
│        └─→ Generate .feature files                                      │
│                │                                                        │
│                ▼                                                        │
│   /reverse-tdd                                                          │
│        │                                                                │
│        ├─→ Analyze existing unit tests                                   │
│        └─→ Generate coverage reports and gaps                           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Pipeline Commands

| Command          | Input         | Output         | Purpose                          |
|------------------|---------------|----------------|----------------------------------|
| `/reverse-spec`  | Code directory | SPEC-XXX.md    | Extract requirements from code   |
| `/reverse-bdd`   | SPEC file     | .feature file   | Convert AC to Gherkin scenarios  |
| `/reverse-tdd`   | .feature file  | Coverage report | Map scenarios to unit tests      |

### Usage Example

```bash
# Step 1: Reverse engineer code into SDD specification
/reverse-spec src/auth/

# Step 2: Convert acceptance criteria to BDD scenarios
/reverse-bdd specs/SPEC-AUTH.md

# Step 3: Analyze test coverage of BDD scenarios
/reverse-tdd features/auth.feature
```

### Detailed Guides

- [BDD Extraction Workflow](./bdd-extraction.md) - Detailed guide for AC → Gherkin conversion
- [TDD Analysis Workflow](./tdd-analysis.md) - Detailed guide for BDD → TDD coverage analysis

## Anti-Patterns to Avoid

### ❌ Don't Do This

1. **Fabricate Motivation**
   - Incorrect: "This feature was built to improve user experience."
   - Correct: "[Unknown] Motivation requires human input."

2. **Assume Requirements**
   - Incorrect: "The system needs SSO support."
   - Correct: "[Needs Confirmation] SSO settings found in code - is this a requirement?"

3. **Speculate on Unread Code**
   - Incorrect: "PaymentService handles Stripe integration."
   - Correct: "[Unknown] PaymentService functionality - needs to read src/services/PaymentService.ts."

4. **Present Options Without Uncertainty Tags**
   - Incorrect: "Code uses Redis for caching."
   - Correct: "[Confirmed] Redis client configured in src/config/cache.ts:5."

## Best Practices

### Should Do

- ✅ Read all relevant files before making statements
- ✅ Tag each statement with certainty levels
- ✅ Include source citations with file:line references
- ✅ Clearly list items requiring human input
- ✅ Retain original code comments for context

### Should Not Do

- ❌ Assume motivation or business context
- ❌ Present inferences as confirmed facts
- ❌ Skip source annotations
- ❌ Generate specifications for unread code
- ❌ Fill in `[Unknown]` blocks without human input

---

## Configuration Detection

This skill will automatically detect project settings:

1. Check for the existence of a `specs/` directory
2. Check for SDD tools (OpenSpec, Spec Kit)
3. Detect testing frameworks used for extracting acceptance criteria
4. Identify code patterns (MVC, DDD, etc.)

---

## Related Standards

- [Specification Driven Development](../../../core/spec-driven-development.md)
- [Anti-Hallucination Guidelines](../../../core/anti-hallucination.md)
- [Code Review Checklist](../../../core/code-review-checklist.md)

---

## Version History

| Version | Date       | Changes                          |
|---------|------------|----------------------------------|
| 1.1.0   | 2026-01-19 | Added BDD/TDD pipeline integration |
| 1.0.0   | 2026-01-19 | Initial release                  |

---

## License

This skill is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

**Source**: [universal-dev-standards](https://github.com/AsiaOstrich/universal-dev-standards)