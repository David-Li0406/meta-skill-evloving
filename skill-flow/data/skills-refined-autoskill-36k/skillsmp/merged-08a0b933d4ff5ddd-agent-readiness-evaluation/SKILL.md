---
name: agent-readiness-evaluation
description: Use this skill to evaluate a codebase's readiness for autonomous agent execution and provide tailored recommendations based on best practices for agent-friendliness.
---

# Agent Readiness Evaluation

Evaluate how well a codebase supports autonomous agent execution based on established principles for agent-friendliness and provide tailored recommendations.

## Core Philosophy

Most agent failures are due to system design failures rather than model failures. This evaluation checks whether the infrastructure enables true autonomy: agents that run unattended, isolated, reproducible, and bounded by system constraints rather than human intervention.

## Evaluation Process

### Phase 1: Gather Evidence

Explore the codebase for indicators across key principles. Key files to examine include:

**Environment & Isolation:**
- `Dockerfile`, `docker-compose.yml`, `.devcontainer/`
- CI configurations (`.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`)

**Dependencies & State:**
- Lockfiles (e.g., `package-lock.json`, `yarn.lock`)
- Database configurations, migration files, seed scripts

**Execution & Interfaces:**
- CLI entry points, `bin/` scripts
- API definitions, background job configurations

**Quality & Monitoring:**
- Test suites, logging configurations, cost tracking setups

### Phase 2: Score Each Principle

Score each principle (0-3) based on evidence found:

| Principle | What to Look For |
|-----------|------------------|
| Sandbox Everything | Ephemeral environments, container support |
| No External DB Dependencies | Local DB setup, migrations in code |
| Clean Environment | Fresh environments, no accumulated state |
| Session-Independent Execution | Capability to run without user sessions |
| Outcome-Based Instructions | Clear acceptance criteria, minimal procedural coupling |
| Direct Low-Level Interfaces | CLI-first tools, minimal abstraction layers |
| Minimal Framework Overhead | Simple interfaces, no heavy orchestration |
| Explicit State Persistence | Writable workspace for intermediate results |
| Early Benchmarks | Measurable quality criteria, automated verification |
| Cost Planning | Resource limits, usage tracking |
| Verifiable Output | Automated validation, clear exit codes |
| Infrastructure-Bounded Permissions | Least-privilege, no runtime prompts |

### Phase 3: Generate Recommendations

For each principle scoring below 2, provide:

1. **Current State**: What exists today
2. **Gap**: What's missing for autonomous execution
3. **Recommendation**: Specific, actionable improvement
4. **Priority**: High/Medium/Low based on impact and effort

## Output Format

```markdown
# Agent-Ready Evaluation Report

**Overall Score: X/36** (Y%)
**Rating: [Excellent|Good|Needs Work|Not Agent-Ready]**

## Summary
[2-3 sentence assessment of overall agent-readiness]

## Principle Scores

| Principle | Score | Evidence |
|-----------|-------|----------|
| Sandbox Everything | X/3 | [brief evidence] |
| No External DB Dependencies | X/3 | [brief evidence] |
| ... | ... | ... |

## Top 3 Improvements

1. **[Highest impact improvement]**
   - Current state: ...
   - Recommendation: ...
   - Impact: ...

2. **[Second improvement]**
   ...

3. **[Third improvement]**
   ...

## Strengths
- [What the codebase does well for agents]

## Detailed Findings
[Optional: deeper analysis of specific areas]
```

## Rating Scale

- **30-36 (83-100%)**: Excellent - Ready for autonomous agent execution
- **24-29 (67-82%)**: Good - Minor improvements needed
- **18-23 (50-66%)**: Needs Work - Significant gaps to address
- **0-17 (<50%)**: Not Agent-Ready - Major architectural changes needed

## Quick Checks

If time is limited, prioritize these high-signal indicators:

1. **Dockerfile exists?** → Sandboxing potential
2. **Lockfiles present?** → Reproducibility
3. **No external DB in default config?** → Isolation
4. **CLI scripts in bin/ or Makefile?** → Direct interfaces
5. **Tests with assertions?** → Verifiable output