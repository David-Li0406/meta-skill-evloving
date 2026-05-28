# Delegation Patterns

Real-world examples of decomposing complex tasks into subagent teams.

---

## Pattern 1: Full-Stack Feature Implementation

**User Request**: "Add user authentication with login, signup, and profile pages"

### Decomposition

```
Batch 1 (Parallel - Exploration):
├── Explore Agent 1: "Find existing auth patterns, middleware, user models"
├── Explore Agent 2: "Find routing structure, page patterns, form components"
└── Explore Agent 3: "Find test patterns, API endpoint conventions"

Gate: Synthesize findings → Design architecture

Batch 2 (Parallel - Implementation):
├── General Agent 1: "Implement user model and auth middleware" (sonnet)
├── General Agent 2: "Implement login/signup API endpoints" (sonnet)
└── General Agent 3: "Implement frontend pages and forms" (sonnet)

Gate: Synthesize → Integration

Batch 3 (Parallel - Verification):
├── General Agent 1: "Run all tests, fix failures" (haiku)
└── General Agent 2: "Check for security issues in auth code" (sonnet)

Final: Orchestrator synthesizes, reports to user
```

---

## Pattern 2: Bug Investigation & Fix

**User Request**: "Users report 500 errors on checkout"

### Decomposition

```
Batch 1 (Parallel - Investigation):
├── Explore Agent 1: "Search for checkout-related error handling, recent changes"
├── Explore Agent 2: "Find checkout API endpoints, payment integration code"
└── Explore Agent 3: "Search logs/error patterns related to checkout flow"

Gate: Synthesize → Identify root cause

Batch 2 (Sequential - Fix):
└── General Agent: "Fix the identified issue in [specific file:line]" (sonnet)

Batch 3 (Parallel - Verification):
├── General Agent 1: "Run checkout-related tests" (haiku)
└── Explore Agent: "Verify fix doesn't introduce regressions" (haiku)

Final: Orchestrator confirms fix, reports to user
```

---

## Pattern 3: Code Refactoring

**User Request**: "Refactor the API layer to use a consistent error handling pattern"

### Decomposition

```
Batch 1 (Parallel - Analysis):
├── Explore Agent 1: "Find all API endpoints and current error handling" (medium)
├── Explore Agent 2: "Identify error handling inconsistencies" (medium)
└── Explore Agent 3: "Find existing error utilities or middleware" (quick)

Gate: Synthesize → Design consistent pattern

Batch 2 (Parallel - Implementation):
├── General Agent 1: "Refactor endpoints in /api/users/*" (sonnet)
├── General Agent 2: "Refactor endpoints in /api/products/*" (sonnet)
└── General Agent 3: "Refactor endpoints in /api/orders/*" (sonnet)

Batch 3 (Sequential):
└── General Agent: "Update tests to match new error patterns" (sonnet)

Final: Orchestrator verifies consistency
```

---

## Pattern 4: Documentation & Analysis

**User Request**: "Document the entire API and identify gaps"

### Decomposition

```
Batch 1 (Parallel - Discovery):
├── Explore Agent 1: "Find all API routes, controllers, handlers" (very thorough)
├── Explore Agent 2: "Find existing documentation, comments, types" (medium)
└── Explore Agent 3: "Find test files that demonstrate API usage" (medium)

Gate: Synthesize complete API inventory

Batch 2 (Parallel - Documentation):
├── General Agent 1: "Document /api/auth/* endpoints" (haiku)
├── General Agent 2: "Document /api/users/* endpoints" (haiku)
└── General Agent 3: "Document /api/products/* endpoints" (haiku)

Final: Orchestrator combines, identifies gaps, reports
```

---

## Pattern 5: Multi-Service Setup

**User Request**: "Set up Docker Compose with API, database, and Redis"

### Decomposition

```
Batch 1 (Parallel - Research):
├── Explore Agent 1: "Find existing Docker/compose files, port configs"
├── Explore Agent 2: "Find database connection strings, env vars"
└── Explore Agent 3: "Find Redis usage patterns, cache configs"

Gate: Synthesize requirements

Batch 2 (Sequential - Implementation):
└── General Agent: "Create docker-compose.yml with all services" (sonnet)

Batch 3 (Parallel - Verification):
├── General Agent 1: "Validate docker-compose syntax" (haiku)
└── General Agent 2: "Test services start correctly" (haiku)

Final: Orchestrator reports setup complete
```

---

## Pattern 6: Test Suite Creation

**User Request**: "Add comprehensive tests for the payment module"

### Decomposition

```
Batch 1 (Parallel - Analysis):
├── Explore Agent 1: "Find all payment module files, functions, classes"
├── Explore Agent 2: "Find existing test patterns, test utils, mocks"
└── Explore Agent 3: "Identify edge cases, error paths in payment code"

Gate: Synthesize test plan

Batch 2 (Parallel - Implementation):
├── General Agent 1: "Write unit tests for payment models" (sonnet)
├── General Agent 2: "Write integration tests for payment API" (sonnet)
└── General Agent 3: "Write tests for payment error handling" (sonnet)

Batch 3 (Sequential):
└── General Agent: "Run all tests, fix failures" (sonnet)

Final: Orchestrator reports coverage
```

---

## Sizing Guide

| Task Size | Subagents | Batches | Example |
|-----------|-----------|---------|---------|
| Small (1-2 files) | 1-2 | 1 | Fix typo, add comment |
| Medium (3-5 files) | 2-3 | 2 | Add endpoint, fix bug |
| Large (5-15 files) | 3-5 | 2-3 | New feature, refactor |
| XL (15+ files) | 5-8 | 3-4 | Architecture change |

---

## Background Agent Pattern

For long-running tasks, use `run_in_background: true`:

```
1. Launch background agent for test suite
2. Continue with other work (implementation)
3. Check status with AgentOutputTool (block=false)
4. When ready, retrieve results with AgentOutputTool (block=true)
```

This prevents the main session from idling while waiting for results.
