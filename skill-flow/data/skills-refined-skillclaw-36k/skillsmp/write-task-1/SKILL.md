---
name: write-task
description: Guide users through writing effective task definitions for plan-forge. Use when user wants help writing a task, needs a task template, is preparing input for plan-forge, or asks "how do I write a good task for planning?"
---

# Write Task Skill

Help users write task definitions that result in high-quality plans (score >= 0.80).

## Task Template

```
Task: [Short, descriptive title]

Objective: [One clear sentence - what needs to be accomplished]

Success Criteria:
- [Specific, testable outcome 1]
- [Specific, testable outcome 2]

Constraints:
- [Explicit limitation or requirement]

Context:
- Existing patterns: [file paths to follow]
- Related code: [file paths]
- Build/test commands: [commands]
```

## Five Qualities

| Quality | Good | Bad |
|---------|------|-----|
| **Specific** | "Add JWT auth to /api/login" | "Add authentication" |
| **Grounded** | "Follow pattern in src/auth/session.rs" | "Use best practices" |
| **Testable** | "All tests in tests/auth/ pass" | "Works correctly" |
| **Deterministic** | "Create files X, Y, Z" | "Create files as needed" |
| **Scoped** | "Only modify src/api/, no DB changes" | "Update auth system" |

## Workflow

1. **Ask for the objective** - What does the user want to accomplish?
2. **Identify affected files** - Search codebase for relevant patterns
3. **Define success criteria** - What proves it works?
4. **Add constraints** - What's out of scope?
5. **Output formatted task** - Use template above

## Anti-Patterns to Flag

- **Vague**: "Improve error handling" → Ask: "Which component? What errors?"
- **Conditional**: "Maybe add validation" → Rewrite: "Add validation to X"
- **Unbounded**: "Refactor the codebase" → Ask: "Which specific area?"
- **Untestable**: "Make it better" → Ask: "How will we verify success?"

## Quality Checks to Anticipate

Plans must pass these checks (score threshold: 0.80):

| Check | Penalty | Task Mitigation |
|-------|---------|-----------------|
| Q-001 Missing runbook | -0.25 | Clear executable steps |
| Q-002 No grounding gate | -0.25 | Reference existing files |
| Q-004 Vague language | -0.10 each | Use deterministic language |
| V-001 No tests | Critical | Mention testing requirements |

## Example Output

When user says: "Help me write a task for adding a health check endpoint"

Generate:

```
Task: Add Health Check Endpoint

Objective: Create a /api/health endpoint that returns server status for monitoring.

Success Criteria:
- GET /api/health returns 200 with {"status": "ok", "version": "X.Y.Z"}
- Endpoint responds in <50ms
- Added to API documentation

Constraints:
- No authentication required on this endpoint
- Use existing router pattern in src/api/routes.rs

Context:
- Follow pattern in src/api/status.rs
- Add tests to tests/api/health_test.rs
```
