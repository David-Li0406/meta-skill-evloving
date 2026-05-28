---
name: problem-solving
description: Structured problem-solving methodology. Activates for planning, design, debugging, or complex multi-step tasks. Use for systematic analysis and evidence-based reasoning.
allowed-tools: ["shell", "read_file", "apply_patch", "update_plan"]
metadata:
  short-description: Systematic problem-solving approach
---

# Problem-Solving Methodology

**Read these references:**
- `references/methodology.md` - 5-phase problem-solving framework (detailed)
- `references/behavior.md` - Critical thinking and evidence-based reasoning
- `references/decomposition.md` - Breaking problems into subproblems
- `references/parallelization.md` - Identifying parallel execution opportunities

## Instructions

Apply the 5-phase problem-solving framework from AGENT.md and references:

### Phase 1: Understand (Decompose)
- Gather all requirements and constraints
- Identify unknowns and dependencies
- Restate the problem to confirm understanding
- Ask clarifying questions if needed
- Read relevant code/documentation

### Phase 2: Plan (Strategize)
- Design approach from first principles
- Make scope decisions (what's in/out)
- Identify opportunities for parallelization
- Break complex work into TODO items per task-management.md
- Consider multiple solutions, pick best one

### Phase 3: Execute (Implement)
- Work through TODO list systematically
- Update task status in real-time (exactly ONE in_progress)
- Validate incrementally - don't save all verification for the end
- Document decisions as you go
- Apply critical thinking throughout

### Phase 4: Verify (Validate)
- Sanity check first: "Is this actually good/correct?"
- Run mechanical verification (tests, lint, build)
- Fix issues immediately, re-verify
- Don't proceed until verification passes
- Use evidence to confirm correctness

### Phase 5: Reflect (Learn)
- What worked well? What didn't?
- Were estimates accurate?
- Would a different approach have been better?
- (This is internal reflection - share selectively)

All guidance from AGENT.md Task Tracking section also applies.
