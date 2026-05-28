# enhanced-planning

Upgraded planning workflow with parallel research, external documentation, and systematic user flow analysis.

## Quick Start

Use for non-trivial features (3+ files, new integrations, architectural changes).

When entering plan mode for something complex:
1. Launch 3 parallel research agents
2. Analyze user flows systematically
3. Identify gaps and ask clarifying questions
4. Write structured plan with research findings

## How It Works

```
                    ┌─────────────────────────────────┐
                    │     Feature Request Received    │
                    └───────────────┬─────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        ▼                           ▼                           ▼
┌───────────────┐          ┌───────────────┐          ┌───────────────┐
│  Codebase     │          │   External    │          │  Framework    │
│  Patterns     │          │ Best Practices│          │    Docs       │
│               │          │               │          │               │
│ - Similar code│          │ - WebSearch   │          │ - Version info│
│ - Conventions │          │ - WebFetch    │          │ - Constraints │
│ - Reusables   │          │ - Open source │          │ - Patterns    │
└───────┬───────┘          └───────┬───────┘          └───────┬───────┘
        │                          │                          │
        └──────────────────────────┼──────────────────────────┘
                                   ▼
                    ┌─────────────────────────────────┐
                    │     User Flow Analysis          │
                    │  - Happy paths                  │
                    │  - Edge cases                   │
                    │  - Error states                 │
                    └───────────────┬─────────────────┘
                                    ▼
                    ┌─────────────────────────────────┐
                    │     Gap Identification          │
                    │  - Missing specs                │
                    │  - Clarifying questions         │
                    └───────────────┬─────────────────┘
                                    ▼
                    ┌─────────────────────────────────┐
                    │     Structured Plan Output      │
                    └─────────────────────────────────┘
```

## The Four Phases

### Phase 1: Parallel Research
Launch 3 Task agents simultaneously:

| Agent | Focus |
|-------|-------|
| Codebase Patterns | Similar implementations, naming conventions, reusable utilities |
| External Best Practices | WebSearch for current docs, open source examples, security considerations |
| Framework Docs | Version constraints, recommended patterns, deprecations |

### Phase 2: User Flow Analysis
Systematically analyze:
- **Happy paths**: Primary user journey, entry points, success states
- **Edge cases**: Failures, timeouts, rate limits, invalid input
- **User variations**: First-time vs returning, roles, devices, offline
- **State management**: Persistence, resume on interrupt, cleanup

### Phase 3: Gap Identification
Before writing the plan:
- Missing error handling specs
- Unclear validation rules
- Unspecified edge cases
- Security considerations
- Accessibility requirements
- Performance implications

Use AskUserQuestion for critical gaps.

### Phase 4: Structured Plan Output
```markdown
# [Feature] Implementation Plan

## Summary
[1-2 sentences]

## Research Findings
### Codebase Patterns
### External Best Practices
### Framework Notes

## User Flows
### Primary Flow
### Edge Cases

## Implementation Steps
### Step 1: [Component]
- What:
- Why:
- Files:

## Open Questions
## Testing Strategy
```

## When to Use

Apply enhanced planning when:
- Feature touches 3+ files
- New integrations or APIs
- Architectural changes
- User explicitly asks to "plan" something complex

Skip for:
- Simple bug fixes
- Single-file changes
- Well-defined small tasks

## For Claude Code

When entering plan mode for non-trivial features:

1. **Launch 3 parallel Task agents** for research (codebase, external, framework)
2. **Wait for all to complete** before proceeding
3. **Analyze user flows** (happy paths, edge cases, error states)
4. **Identify gaps** and ask clarifying questions via AskUserQuestion
5. **Write structured plan** with research findings, flows, steps, questions, testing strategy
