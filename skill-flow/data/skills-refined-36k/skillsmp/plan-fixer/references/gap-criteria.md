# Completeness Gap Criteria

This document defines what constitutes a "critical completeness gap" in an implementation plan **optimized for autonomous coding agent execution**.

## Design Principle

Plans are consumed by autonomous coding agents, not humans. Gaps are defined by what would cause an **agent to fail or produce wrong output**.

## What IS a Completeness Gap

### 1. Missing Actionable Instructions

An instruction is missing when an **agent cannot proceed without guessing**:

| Gap Type | Agent Impact |
|----------|--------------|
| Feature mentioned but not specified | Agent will hallucinate implementation |
| Expected behavior undefined | Agent may implement wrong behavior |
| Input/output formats missing | Agent will guess formats |
| File paths not specified | Agent won't know where to write code |

**Examples:**
- "User authentication" → Agent needs: JWT vs session, token expiry, storage location
- "Data validation" → Agent needs: specific rules, error messages, where to validate
- "API endpoint" → Agent needs: method, path, request/response schema

### 2. Unhandled Branches (Edge Cases)

A branch is unhandled when an **agent would fail silently or crash**:

| Gap Type | Agent Impact |
|----------|--------------|
| Error scenarios missing | Agent won't add error handling |
| Boundary conditions undefined | Agent will use arbitrary limits |
| Empty/null states unspecified | Agent may crash on edge inputs |

**Examples:**
- Empty form submission → Agent needs: validation message, prevent submit, or allow?
- API 500 error → Agent needs: retry logic, user message, fallback behavior
- File not found → Agent needs: create file, throw error, or return default?

### 3. Missing Verification Commands

Verification is unclear when an **agent cannot confirm task completion**:

| Gap Type | Agent Impact |
|----------|--------------|
| No `<verify>` command | Agent cannot self-check |
| Vague `<done>` criteria | Agent cannot confirm success |
| No test command | CI/CD cannot validate |

**Examples:**
- ❌ "Should work correctly" → ✅ `npm test -- auth.test.ts`
- ❌ "Fast response" → ✅ "Response time < 200ms" + load test command
- ❌ "Handles errors" → ✅ "Returns 400 for invalid input, 500 logged to Sentry"

## What is NOT a Completeness Gap

These do NOT block agent execution:

### Stylistic Preferences
- Document formatting choices
- Naming conventions (unless ambiguous)
- Section ordering

### Implementation Flexibility
- Algorithm choice (agent can decide)
- Internal code structure
- Variable naming

### "Why" Explanations
- Rationale for decisions (agent doesn't need this)
- Background context (agent derives from code)
- Historical notes

### Nice-to-Haves
- Performance optimizations beyond requirements
- Future enhancement ideas
- Alternative approaches

## Severity Assessment (Agent-Oriented)

A gap is **CRITICAL** if it would cause:

| Severity | Agent Behavior | Example |
|----------|----------------|---------|
| **Blocking** | Agent stops, cannot proceed | "Create the API" (which API? what endpoints?) |
| **Hallucination Risk** | Agent guesses wrong | "Add validation" (what rules?) |
| **Silent Failure** | Agent succeeds but wrong | "Handle errors" (how? what message?) |
| **Unverifiable** | Agent can't confirm done | "Should work" (how to test?) |

A gap is **NOT CRITICAL** if:
- Agent can make a reasonable default choice
- Codebase context provides the answer
- It's explicitly marked as agent's choice

## Gap Identification Checklist (Agent Perspective)

For each `<task>` block, verify:

**Structure:**
- [ ] Has `<name>` - descriptive action
- [ ] Has `<files>` - specific paths (not placeholders)
- [ ] Has `<action>` - numbered steps
- [ ] Has `<verify>` - executable command
- [ ] Has `<done>` - measurable criteria

**Content:**
- [ ] All features have concrete specifications
- [ ] File paths are exact (not `[TBD]` or `path/to/file`)
- [ ] Error handling is specified (what to do, not just "handle errors")
- [ ] Constraints are explicit (`<constraints>` section)
- [ ] Dependencies are identified

**Verification:**
- [ ] `<verify>` is an executable command
- [ ] `<done>` has measurable criteria (numbers, states, assertions)
- [ ] Edge cases have defined behavior
