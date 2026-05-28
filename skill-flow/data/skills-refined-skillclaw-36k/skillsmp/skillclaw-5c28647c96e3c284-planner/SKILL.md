---
name: planner
description: Use this skill when you need to create comprehensive, phased implementation plans with sprints and atomic tasks.
---

# Planner Agent

Create detailed, phased implementation plans for bugs, features, or tasks.

## Process

### Phase 0: Research

1. **Investigate the codebase:**
   - Architecture and patterns
   - Similar existing implementations
   - Dependencies and frameworks
   - Related components

2. **Analyze the request:**
   - Core requirements
   - Challenges and edge cases
   - Security/performance/UX considerations

### Phase 1: Clarify Requirements

Use `request_user_input` to resolve ambiguities. Ask up to 10 targeted questions:
- Scope boundaries (in/out of scope)
- Technology/architectural constraints
- Priorities (critical vs nice-to-have)
- Edge case handling
- Success criteria

### Phase 2: Create Plan

#### Structure
- **Overview**: Brief summary and approach
- **Sprints**: Logical phases that build on each other
- **Tasks**: Specific, actionable items within sprints

#### Sprint Requirements
Each sprint must:
- Result in **demoable, runnable, testable** increment
- Build on prior sprint work
- Include demo/verification checklist

#### Task Requirements
Each task must be:
- **Atomic and committable** (small, independent)
- Specific with clear inputs/outputs
- Independently testable
- Include file paths when relevant
- Include dependencies for parallel execution
- Include tests or validation method

**Bad:** "Implement Google OAuth"  
**Good:**
- "Add Google OAuth config to env variables"
- "Install passport-google-oauth20 package"
- "Create OAuth callback route in src/routes/auth.ts"
- "Add Google sign-in button to login UI"

### Phase 3: Save
Save the file.

Generate filename from request:
1. Extract key words
2. Convert to kebab-case
3. Add `-plan.md` suffix

Examples:
- "fix xyz bug" → `xyz-bug-plan.md`
- "implement google auth" → `google-auth-plan.md`

### Phase 4: Gotchas

AFTER it is saved, identify potential issues and edge cases in the plan. Address them proactively. Where could something go wrong? What about the plan is ambiguous? Is there a missing step, dependency, or pitfall?

Use the `request_user_input` to clarify any uncertainties.