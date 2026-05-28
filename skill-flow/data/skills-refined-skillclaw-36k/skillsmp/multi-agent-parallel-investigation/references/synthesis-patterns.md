# Synthesis Patterns

Frameworks for synthesizing findings from 4-6 parallel agent investigations into actionable decision frameworks.

## Phased Decision Framework

Structure agent findings into implementation phases with clear decision gates.

### Template

```markdown
## Summary of Parallel Investigations

**Agent 1 (Role)**: Key findings summary (2-3 sentences)
**Agent 2 (Role)**: Key findings summary
**Agent 3 (Role)**: Key findings summary
**Agent 4 (Role)**: Key findings summary

## Decision Framework

### Phase 1: [Immediate Action] (Priority: HIGH)
**Objective**: [What this phase accomplishes]
**Based on**: [Which agent findings support this]
**Effort**: [Time estimate]
**Impact**: [Expected outcome]
**Recommendation**: [Specific action to take]

### Phase 2: [Next Step] (Priority: MEDIUM)
**Objective**: [What this phase accomplishes]
**Based on**: [Which agent findings support this]
**Effort**: [Time estimate]
**Impact**: [Expected outcome]
**Decision Criteria**: [When to proceed with this phase]

### Phase 3: [Future] (Priority: LOW, Optional)
**Objective**: [What this phase accomplishes]
**Based on**: [Which agent findings support this]
**Effort**: [Time estimate]
**Impact**: [Expected outcome]
**Decision Criteria**: [When to proceed with this phase]

## Total Effort Estimate
- **Phase 1**: X hours
- **Phase 2**: Y hours
- **Phase 3**: Z hours
- **Total**: X+Y+Z hours
```

## Consensus-Building Pattern

When agent findings conflict, use voting or weighted consensus.

### Voting Matrix

| Decision | Agent 1 | Agent 2 | Agent 3 | Agent 4 | Consensus |
|----------|---------|---------|---------|---------|-----------|
| Option A | ✅ Yes  | ❌ No   | ✅ Yes  | ⚠️ Maybe | **3/4 Support** |
| Option B | ❌ No   | ✅ Yes  | ❌ No   | ❌ No   | 1/4 Support |
| Option C | ⚠️ Maybe | ⚠️ Maybe | ⚠️ Maybe | ✅ Yes  | Mixed |

**Consensus Threshold**: >50% for proceed, >75% for high confidence

### Weighted Consensus

When agents have different expertise levels for decision:

```markdown
| Agent | Weight | Recommendation | Weighted Vote |
|-------|--------|----------------|---------------|
| Performance Analyst | 0.3 | Option A | 0.3 |
| API Analyst | 0.25 | Option A | 0.25 |
| Documentation Analyst | 0.2 | Option B | 0 |
| Feasibility Engineer | 0.25 | Option A | 0.25 |
| **Total for Option A** | | | **0.8** |

**Result**: Option A wins with 80% weighted consensus
```

## Trade-off Matrix

Synthesize conflicting priorities into decision matrix.

```markdown
| Solution | Complexity | Cost | Performance | Developer UX | Score |
|----------|------------|------|-------------|--------------|-------|
| Option A | Low (9)    | Low (9) | Medium (5) | High (8)     | **31** |
| Option B | High (3)   | High (3)| High (9)   | Medium (5)   | 20 |
| Option C | Medium (6) | Medium (6)| Low (3)  | Low (3)      | 18 |

Scoring: 1-10 scale, higher is better
**Recommendation**: Option A (highest total score)
```

## Risk-Based Synthesis

Prioritize based on risk mitigation.

```markdown
| Phase | Risk Mitigated | Likelihood | Impact | Priority |
|-------|----------------|------------|--------|----------|
| Phase 1: Documentation | Onboarding friction | HIGH | MEDIUM | **P1** |
| Phase 2: Performance | Slow queries | MEDIUM | HIGH | **P1** |
| Phase 3: CLI Tool | Manual workflow | LOW | LOW | **P2** |

**Priority Levels**:
- **P0**: Critical (blocks progress)
- **P1**: High (addresses likely high-impact risks)
- **P2**: Medium (nice-to-have improvements)
- **P3**: Low (future enhancements)
```

## Confidence Level Aggregation

Synthesize agent confidence into overall recommendation.

```markdown
| Agent | Finding | Confidence |
|-------|---------|------------|
| API Analyst | HTTP range requests supported | HIGH (95%) |
| Performance Analyst | Queries complete in <3 sec | MEDIUM (70%) |
| Documentation Analyst | Current docs rated 7.5/10 | HIGH (90%) |
| Feasibility Engineer | CLI tool buildable in 4 hours | LOW (50%) |

**Overall Confidence**: HIGH for Phase 1 (documentation), MEDIUM for Phase 2 (performance optimization), LOW for Phase 3 (CLI tool)

**Recommendation**: Proceed with Phase 1 immediately (high confidence), defer Phase 3 until Phase 1 validated
```

## 80/20 Synthesis

Identify solution that solves 80% of problem with 20% of effort.

```markdown
## Problem Coverage Analysis

| Solution | Problem Coverage | Implementation Effort | ROI Ratio |
|----------|------------------|----------------------|-----------|
| Documentation improvements | 80% | 2 hours | **40% per hour** |
| Remote query optimization | 15% | 4 hours | 3.75% per hour |
| CLI tool | 5% | 6 hours | 0.83% per hour |

**Recommendation**: Implement documentation improvements first (highest ROI), evaluate need for other solutions based on user feedback
```

## Integration Strategy

When agents identify complementary solutions, structure implementation order.

```markdown
## Solution Stack

**Foundation** (Build First):
- API endpoint evaluation (Agent 1 finding)
- Performance benchmarking (Agent 2 finding)

**Core Functionality** (Build Second):
- Documentation quick-start (Agent 3 finding)
- Example code samples

**Enhancements** (Build Later):
- CLI tool (Agent 4 finding)
- Browser UI (deferred pending user feedback)

**Integration Points**:
1. Documentation references API endpoints from Agent 1 findings
2. Examples use performance-optimized patterns from Agent 2 benchmarks
3. CLI tool (if built) reuses code from examples
```

## Success Criteria Synthesis

Combine agent findings into measurable success criteria.

```markdown
## Success Criteria (from 4-agent investigation)

**Functional** (Agent 1 + 4):
- ✅ API endpoints available OR remote query method documented
- ✅ Working code examples (copy-paste ready)
- ✅ Installation steps clear (<5 minutes)

**Performance** (Agent 2):
- ✅ Query latency <3 seconds (cold start)
- ✅ Bandwidth efficiency (range requests, not full download)
- ✅ Rate limits acceptable (>1000 queries/hour)

**Usability** (Agent 3):
- ✅ Documentation rating >8/10
- ✅ Time-to-first-query <60 seconds
- ✅ No placeholder URLs or TODOs

**Validation Method**:
- Test with 3 external developers (not on team)
- Measure time from documentation discovery to successful query
- Collect qualitative feedback on ease-of-use
```

## Decision Summary Template

```markdown
## Investigation Summary

**Question**: [Original question investigated]

**Agent Findings**:
1. **[Agent 1 Role]**: [Key finding in 1 sentence]
2. **[Agent 2 Role]**: [Key finding in 1 sentence]
3. **[Agent 3 Role]**: [Key finding in 1 sentence]
4. **[Agent 4 Role]**: [Key finding in 1 sentence]

**Consensus**: [What agents agreed on]

**Conflicts**: [What agents disagreed on and why]

**Recommended Approach**: [Synthesized solution based on findings]

**Implementation Plan**:
- **Phase 1** (Immediate): [Action] - [Effort] - [Based on which agent findings]
- **Phase 2** (Next): [Action] - [Effort] - [Decision criteria]
- **Phase 3** (Future): [Action] - [Effort] - [Decision criteria]

**Success Criteria**: [Measurable outcomes]

**Validation Plan**: [How to test the recommended approach]
```
