# Section Checklist

Detailed validation criteria for each section of a design document based on the [Lyft tech spec template](https://eng.lyft.com/how-to-write-awesome-tech-specs-86eea8e45bb9).

## Summary

**Purpose:** Enable readers to decide in 30 seconds if they need to read more.

| Criterion | Pass | Fail |
|-----------|------|------|
| Stands alone | Reader understands project without reading rest of doc | Requires context from other sections |
| Captures what | Names the deliverable or capability | Vague ("improve X") |
| Captures why | States the motivation or problem | Assumes reader knows the problem |
| Captures outcome | Describes end state | Only describes activity |
| Length | 2-4 sentences | A paragraph or more |

**Red flags:**
- Starts with "This document describes..." (meta, not summary)
- Lists technologies without explaining purpose
- Mentions implementation details

## Background

**Purpose:** Provide sufficient context for a new team member to understand why this project exists.

| Criterion | Pass | Fail |
|-----------|------|------|
| Current state | Describes how things work today | Assumes reader knows |
| Pain points | Explains problems with current state | Jumps to solution |
| Why now | Explains timing/urgency | No trigger for the work |
| Sufficient for newcomer | New team member could understand | Requires tribal knowledge |

**Red flags:**
- Only describes the solution, not the problem
- References tickets/issues without explaining them
- Assumes historical context ("as we discussed...")

## Goals

**Purpose:** Define measurable success criteria that the project will be evaluated against.

Goals should be SMART:
- **S**pecific — Clear, unambiguous outcome
- **M**easurable — Quantifiable or verifiable
- **A**chievable — Realistic given constraints
- **R**elevant — Tied to business/user value
- **T**ime-bound — Has a deadline or milestone association

| Criterion | Pass | Fail |
|-----------|------|------|
| Specific | "Reduce checkout latency to <2s p99" | "Improve performance" |
| Measurable | Can verify completion objectively | Subjective ("better UX") |
| Outcome-focused | Describes end state | Describes activity ("implement X") |
| Limited scope | 3-7 goals | 10+ goals (scope creep) |
| No contradictions | Goals are mutually compatible | Goals conflict with each other or Non-Goals |

**Red flags:**
- Goals that are really tasks ("Set up CI/CD")
- Goals that can't be verified ("Clean up the codebase")
- Goals that duplicate Non-Goals with opposite polarity

## Non-Goals

**Purpose:** Explicitly exclude work that readers might assume is in scope.

| Criterion | Pass | Fail |
|-----------|------|------|
| Prevents assumptions | Addresses likely reader expectations | Lists irrelevant exclusions |
| Related to project | Could plausibly be in scope | Unrelated to the domain |
| Not contradicting Goals | Exclusions don't undermine goals | Creates impossible situation |
| Explains why | Brief rationale for exclusion | Just a list with no context |

**Red flags:**
- Non-Goals that contradict Goals ("Goal: Support mobile. Non-Goal: Mobile app")
- Non-Goals that are obviously out of scope (padding the list)
- Missing Non-Goals that will cause scope creep

**Common missing Non-Goals:**
- Migration of existing data
- Backward compatibility with deprecated features
- Performance optimization (if not a goal)
- Documentation updates
- Multi-region/multi-tenant support

## Plan

**Purpose:** Describe the technical approach at an appropriate abstraction level.

| Criterion | Pass | Fail |
|-----------|------|------|
| Abstraction level | C4 Level 1-3 (System/Container/Component) | C4 Level 4 (Code) |
| Approach clarity | Clear what will be built | Vague or hand-wavy |
| Alternatives considered | Explains why this approach vs others | Only one option presented |
| Dependencies identified | External systems/teams called out | Hidden dependencies |
| Risks acknowledged | Known risks and mitigations | Only happy path |

**Appropriate content:**
- System context diagrams
- Container diagrams (what deploys, protocols)
- Component responsibilities and interfaces
- API contracts (request/response shapes)
- Data flow descriptions
- Integration points with external systems

**Inappropriate content (defer to milestone planning):**
- Code snippets or pseudocode
- Class/function designs
- Database schemas (unless Container-level decision)
- Algorithm implementations
- Unit test strategies

**Red flags:**
- No diagrams in a complex system
- Only one approach considered ("we will use X")
- Implementation details masquerading as design

## Milestones

**Purpose:** Break the project into demo-able increments that show progress.

| Criterion | Pass | Fail |
|-----------|------|------|
| Demo-able | Each milestone produces observable output | Internal implementation steps |
| Runnable artifact | Milestone ends with working code | Research or documentation only |
| Incremental value | Each milestone is useful alone | Only final milestone has value |
| Ordered | Dependencies between milestones are clear | Can't determine sequence |
| Realistic scope | Each milestone is achievable | "Boil the ocean" milestone |

**Good milestone pattern:**
- Verb + User-visible outcome: "Users can reset passwords via email"
- Enables demonstration to stakeholders
- Could ship independently if needed

**Bad milestone patterns:**
- Implementation task: "Build password reset service"
- Research: "Investigate auth providers"
- Vague: "Phase 1 complete"
- Too large: "Full feature complete"

**Red flags:**
- Milestones that can't be demoed to a non-technical stakeholder
- All milestones are internal ("set up infrastructure", "write tests")
- Final milestone is the only valuable one

## Measurable Impact

**Purpose:** Define specific metrics that prove the project succeeded.

| Criterion | Pass | Fail |
|-----------|------|------|
| Maps to Goals | Each metric ties to a stated goal | Metrics unrelated to goals |
| Quantifiable | Numbers, percentages, counts | Subjective assessments |
| Baseline stated | Current value known or will be measured | No comparison point |
| Target stated | Success threshold defined | "Improve X" without target |
| Measurable | Can actually collect this data | Aspirational but unmeasurable |

**Good metrics:**
- "Reduce checkout p99 latency from 4s to <2s"
- "Increase signup completion rate from 60% to 80%"
- "Reduce support tickets for password reset by 50%"

**Bad metrics:**
- "Improve user satisfaction" (not quantifiable without survey)
- "Better performance" (no baseline or target)
- "Increase engagement" (too vague)

**Red flags:**
- No metrics for stated goals
- Metrics that can't be measured with current infrastructure
- Vanity metrics that don't indicate success

## Open Questions

**Purpose:** Surface unknowns that could affect the design or implementation.

| Criterion | Pass | Fail |
|-----------|------|------|
| Actually open | Genuine unknowns | Rhetorical questions |
| Categorized | Blocking vs non-blocking | Undifferentiated list |
| Assigned | Owner or decision-maker identified | Orphaned questions |
| Time-bound | When answer is needed | No urgency indicated |

**Blocking questions:** Must be answered before implementation starts
**Non-blocking questions:** Can be resolved during implementation

**Red flags:**
- No open questions (unrealistic confidence)
- All questions are blocking (analysis paralysis)
- Questions that are really decisions in disguise
- Questions without owners

**Common missing questions:**
- "Who approves the API contract?"
- "What happens to existing data during migration?"
- "How will we handle the transition period?"
- "What's the rollback strategy?"
