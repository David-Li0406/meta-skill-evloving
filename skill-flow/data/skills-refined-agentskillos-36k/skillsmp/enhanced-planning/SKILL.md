---
name: enhanced-planning
description: Upgrade Claude's planning with parallel research, external docs, and systematic flow analysis. Use this skill when entering plan mode for non-trivial features.
---

# Enhanced Planning Skill

When planning non-trivial features, use this enhanced methodology instead of basic exploration.

## When to Use

Automatically apply this skill when:
- User requests a new feature that touches multiple files
- User asks to "plan" something complex
- You're about to enter plan mode for anything beyond a simple fix

## Enhanced Planning Workflow

### Phase 1: Parallel Research (run simultaneously)

Launch 3 research tasks in parallel using the Task tool:

```
Task 1: Codebase Pattern Analysis
- Scan ARCHITECTURE.md, README.md, CONTRIBUTING.md, CLAUDE.md
- Find similar implementations in the codebase (use Grep/Glob)
- Identify naming conventions, file organization patterns
- Check for existing utilities/helpers that could be reused
- Look at test patterns for similar features

Task 2: External Best Practices
- Use WebSearch for "[technology] [feature] best practices 2025"
- Use WebFetch to get official framework documentation
- Find examples from well-regarded open source projects
- Identify security considerations and common pitfalls

Task 3: Dependency/Framework Docs
- Identify which frameworks/libraries will be used
- Fetch current documentation for those dependencies
- Check for version-specific constraints or deprecations
- Find recommended patterns from official sources
```

### Phase 2: User Flow Analysis

After research completes, systematically analyze:

**Happy Paths:**
- Primary user journey from start to finish
- All entry points to the feature
- Success states and confirmations

**Edge Cases & Error States:**
- What happens when X fails?
- Network errors, timeouts, rate limits
- Invalid input, missing data
- Permission denied scenarios
- Concurrent user actions

**User Variations:**
- First-time vs returning user
- Different user roles/permissions
- Mobile vs desktop considerations
- Offline/slow connection handling

**State Management:**
- What state needs to persist?
- How does user resume if interrupted?
- Cleanup on cancellation

### Phase 3: Gap Identification

Before writing the plan, identify:
- [ ] Missing error handling specs
- [ ] Unclear validation rules
- [ ] Unspecified edge cases
- [ ] Security considerations
- [ ] Accessibility requirements
- [ ] Performance implications

Ask clarifying questions using AskUserQuestion for any critical gaps.

### Phase 4: Structured Plan Output

Write the plan using this structure:

```markdown
# [Feature Name] Implementation Plan

## Summary
[1-2 sentence overview]

## Research Findings

### Codebase Patterns
- Similar implementations: [file paths]
- Reusable utilities: [what can be leveraged]
- Conventions to follow: [naming, structure]

### External Best Practices
- [Key recommendation 1 with source]
- [Key recommendation 2 with source]
- Security considerations: [list]

### Framework/Dependency Notes
- [Relevant framework patterns]
- [Version constraints if any]

## User Flows

### Primary Flow
1. User does X
2. System responds with Y
3. ...

### Edge Cases
| Scenario | Expected Behavior |
|----------|------------------|
| [case 1] | [handling] |
| [case 2] | [handling] |

## Implementation Steps

### Step 1: [Component/File]
- What: [description]
- Why: [reasoning]
- Files: [paths]

### Step 2: [Component/File]
...

## Open Questions
- [Any remaining uncertainties]

## Testing Strategy
- [ ] Unit tests for [X]
- [ ] Integration tests for [Y]
- [ ] Edge case coverage for [Z]
```

## Key Principles

1. **Parallel over sequential** - Run research tasks simultaneously
2. **External knowledge matters** - Don't just look at the codebase, fetch current docs
3. **Edge cases upfront** - Identify error states before implementation, not after
4. **Ask don't assume** - Use AskUserQuestion for ambiguities
5. **Cite sources** - Reference file paths and documentation URLs

## Example Invocation

When user says "plan adding user avatars with S3 upload":

1. Launch 3 parallel Task agents for research
2. Wait for all to complete
3. Analyze user flows (upload, view, delete, error cases)
4. Identify gaps (max size? allowed formats? existing users?)
5. Ask clarifying questions if needed
6. Write structured plan to `plans/` directory
