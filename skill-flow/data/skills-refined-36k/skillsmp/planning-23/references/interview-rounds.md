# Deep Interview Round Templates

## Overview

This document provides detailed templates for each interview round. The planner adjusts depth based on complexity analysis.

## Round Categories

### Round 1: Intent & Scope (All complexities)

**Purpose**: Clarify core goal, define boundaries, and establish success criteria.

```python
AskUserQuestion(questions=[
  {
    "question": "The core goal is X, which direction is closer: Y or Z?",
    "header": "Intent",
    "options": [
      {"label": "Y Direction", "description": "..."},
      {"label": "Z Direction", "description": "..."},
      {"label": "Both", "description": "..."}
    ],
    "multiSelect": False
  },
  {
    "question": "What is the scope of this feature?",
    "header": "Scope",
    "options": [
      {"label": "Minimal Implementation (MVP)", "description": "Core features only"},
      {"label": "Standard Implementation", "description": "Typical level"},
      {"label": "Complete Implementation", "description": "All edge cases included"}
    ],
    "multiSelect": False
  },
  {
    "question": "Relationship with existing code/system?",
    "header": "Integration",
    "options": [
      {"label": "Independent", "description": "No impact on existing code"},
      {"label": "Extension", "description": "Add to existing code"},
      {"label": "Modification", "description": "Existing code changes required"}
    ],
    "multiSelect": False
  },
  {
    "question": "What are the success criteria?",
    "header": "Success",
    "options": [
      {"label": "Tests Pass", "description": "Automated test criteria"},
      {"label": "Manual Verification", "description": "Direct verification"},
      {"label": "Both", "description": "Tests + Manual Verification"}
    ],
    "multiSelect": False
  }
])
```

---

### Round 2: Technical Decisions (standard+)

**Purpose**: Architecture patterns, tech stack, data model, and testing approach.

```python
AskUserQuestion(questions=[
  {
    "question": "What architecture pattern should we use?",
    "header": "Architecture",
    "options": [...],  # Generate from context
    "multiSelect": False
  },
  {
    "question": "What libraries/tech stack to use?",
    "header": "Tech Stack",
    "options": [...],  # Generate from context
    "multiSelect": True  # Multiple selection allowed
  },
  {
    "question": "Data model/schema direction?",
    "header": "Data Model",
    "options": [...],  # Generate from context
    "multiSelect": False
  },
  {
    "question": "Testing strategy? (TDD recommended)",
    "header": "Testing",
    "options": [
      {"label": "TDD (Recommended)", "description": "Write tests first"},
      {"label": "Standard", "description": "Test after implementation"},
      {"label": "Mixed", "description": "TDD for core logic only"}
    ],
    "multiSelect": False
  }
])
```

---

### Round 3: Edge Cases & Error Handling (complex+)

**Purpose**: Error scenarios, concurrency, performance, and security considerations.

```python
AskUserQuestion(questions=[
  {
    "question": "Expected error scenarios and handling approach?",
    "header": "Errors",
    "options": [...],  # Generate from context
    "multiSelect": True
  },
  {
    "question": "Is concurrency/race condition consideration needed?",
    "header": "Concurrency",
    "options": [...],  # Generate from context
    "multiSelect": False
  },
  {
    "question": "Are there performance requirements?",
    "header": "Performance",
    "options": [...],  # Generate from context
    "multiSelect": False
  },
  {
    "question": "What are security considerations?",
    "header": "Security",
    "options": [...],  # Generate from context
    "multiSelect": True
  }
])
```

---

### Round 4: Polish & Integration (massive)

**Purpose**: UI/UX details, observability, documentation, and deployment.

```python
AskUserQuestion(questions=[
  {
    "question": "What are the UI/UX details?",
    "header": "UI/UX",
    "options": [...],  # Generate from context
    "multiSelect": False
  },
  {
    "question": "What are the logging/monitoring requirements?",
    "header": "Observability",
    "options": [...],  # Generate from context
    "multiSelect": True
  },
  {
    "question": "What is the documentation scope?",
    "header": "Documentation",
    "options": [...],  # Generate from context
    "multiSelect": False
  },
  {
    "question": "What is the deployment/rollback strategy?",
    "header": "Deployment",
    "options": [...],  # Generate from context
    "multiSelect": False
  }
])
```

---

### Round 5+: Freeform (User-requested)

**Purpose**: Additional topics based on user request via adaptive check.

```python
# First, ask what topics to explore
AskUserQuestion(questions=[
  {
    "question": "Please select additional areas to discuss",
    "header": "Topics",
    "options": [
      {"label": "Technical Details", "description": "In-depth implementation approach"},
      {"label": "Edge Cases", "description": "Additional exception cases"},
      {"label": "Performance Optimization", "description": "Performance-related decisions"},
      {"label": "Other", "description": "Other topics"}
    ],
    "multiSelect": True
  }
])

# Then ask questions specific to selected topics
```

---

## Adaptive Check (After Each Round)

After completing each round, ask if user wants to continue:

```python
AskUserQuestion(questions=[{
  "question": f"Round {n} complete. Continue?",
  "header": "Continue",
  "options": [
    {"label": "Sufficient", "description": "Proceed to Plan writing"},
    {"label": "Continue", "description": "Proceed to next round"}
  ],
  "multiSelect": False
}])
```

**Behavior**:
- **"Sufficient"** → Exit interview, proceed to Phase 4 (Document Design)
- **"Continue"** → Next round (no upper limit)

---

## Recording Decisions

After each round, record decisions in markdown format for design document:

```markdown
## Interview Round {n}: {Category}

| Question | Answer | Notes |
|----------|--------|-------|
| Intent direction | Y approach | User prefers simplicity |
| Scope | MVP | Phase 2 for extras |
| Testing | TDD | Core logic only |
```

This record will be included in the design document created in Phase 4.

---

## Domain-Specific Question Templates

Based on goal keywords, add relevant questions:

| Goal Contains | Add Questions About |
|--------------|---------------------|
| API, endpoint | Request/Response format, versioning, rate limiting |
| auth, login | Session vs JWT, OAuth providers, MFA |
| database, schema | Migration strategy, indexing, relationships |
| UI, frontend | Component library, state management, routing |
| test, coverage | Unit vs integration, mocking strategy, CI |
| refactor | Breaking changes, migration path, rollback |
| performance | Metrics baseline, caching, lazy loading |
| security | OWASP concerns, audit logging, encryption |
