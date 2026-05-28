# Example: Systematic Debugging

**Source**: https://github.com/obra/superpowers/tree/main/skills/systematic-debugging
**Pattern**: Four-phase framework with stopping rules
**Use case**: Ensuring understanding before attempting solutions

## Key Sections from SKILL.md

### The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

### The Four Phases

**Phase 1: Root Cause Investigation**
- Read error messages carefully
- Reproduce consistently
- Check recent changes
- **Gather evidence in multi-component systems** (diagnostic instrumentation)
- Trace data flow (requires root-cause-tracing sub-skill)

**Phase 2: Pattern Analysis**
- Find working examples
- Compare against references
- Identify differences
- Understand dependencies

**Phase 3: Hypothesis and Testing**
- Form single hypothesis
- Test minimally (one variable at a time)
- Verify before continuing

**Phase 4: Implementation**
- Create failing test case (requires test-driven-development sub-skill)
- Implement single fix
- Verify fix
- **If 3+ fixes failed: Question architecture**

### Multi-Component Systems Section

Extensive guidance on adding diagnostic instrumentation:

```bash
# Layer 1: Workflow
echo "=== Secrets available in workflow: ==="
echo "IDENTITY: ${IDENTITY:+SET}${IDENTITY:-UNSET}"

# Layer 2: Build script
echo "=== Env vars in build script: ==="
env | grep IDENTITY || echo "IDENTITY not in environment"
```

### Three-Fix Rule

**If ≥ 3: STOP and question the architecture**

Pattern indicating architectural problem:
- Each fix reveals new shared state/coupling/problem in different place
- Fixes require "massive refactoring"
- Each fix creates new symptoms elsewhere

### Your Human Partner's Signals

Watch for these redirections:
- "Is that not happening?" - You assumed without verifying
- "Will it show us...?" - You should have added evidence gathering
- "Stop guessing" - You're proposing fixes without understanding

### Common Rationalizations Table

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too. |
| "Emergency, no time for process" | Systematic debugging is FASTER than thrashing. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem. |

### Integration with Other Skills

**Required sub-skills:**
- **root-cause-tracing** - REQUIRED when error is deep in call stack
- **test-driven-development** - REQUIRED for creating failing test case

**Complementary skills:**
- defense-in-depth
- condition-based-waiting
- verification-before-completion

## Analysis

**What makes this work**:

1. **Four-phase structure**: Clear gates between phases
2. **Stopping rule**: Three-fix rule prevents infinite attempts
3. **Multi-component guidance**: Diagnostic instrumentation examples
4. **Human partner signals**: Meta-cognitive monitoring
5. **Sub-skill integration**: References other required skills
6. **Phase gates**: Must complete each phase before next

## Unique Features

**Three-Fix Rule**:
After 3 failed fixes, STOP and question architecture. Don't attempt fix #4 without architectural discussion.

**Multi-Component Diagnostic Pattern**:
Detailed examples of adding instrumentation at each layer boundary to identify where systems fail.

**Human Partner Signal Detection**:
Watches for specific phrases that indicate the wrong approach:
- "Is that not happening?"
- "Will it show us...?"
- "Stop guessing"

**Sub-Skill Requirements**:
Explicitly states REQUIRED sub-skills at specific phases:
- Phase 1.5: root-cause-tracing
- Phase 4.1: test-driven-development

**Real-World Impact Section**:
- Systematic approach: 15-30 minutes to fix
- Random fixes approach: 2-3 hours of thrashing
- First-time fix rate: 95% vs 40%

## Pattern Type

**Four-phase methodology** with:
- Clear phase boundaries
- Stopping rules (three-fix rule)
- Sub-skill integration
- Meta-cognitive monitoring (human partner signals)

## Key Takeaways

1. **Stopping rules prevent infinite loops** - Three-fix rule forces rethinking
2. **Phase gates enforce discipline** - Can't skip to Phase 4
3. **Multi-component systems need instrumentation** - Don't guess where it breaks
4. **Sub-skill integration** - Explicitly requires other skills at specific phases
5. **Meta-cognitive monitoring** - Watch for human partner's redirections
6. **Architectural questioning** - Three failures = wrong pattern, not wrong implementation
7. **Evidence gathering first** - Add diagnostic instrumentation before proposing fixes
