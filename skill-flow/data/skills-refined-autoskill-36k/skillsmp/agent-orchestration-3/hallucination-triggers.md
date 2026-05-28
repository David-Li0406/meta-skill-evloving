# Hallucination Detection Guide for AI Agent Orchestration

## Purpose and Scope

This guide catalogs observable triggers that indicate reasoning failures in AI agent outputs, particularly when orchestrating AI-to-AI delegation. These triggers reveal when agents generate conventional-looking outputs through pattern-matching rather than reasoning about actual problem requirements.

**Target Audience**: AI orchestrators and sub-agents evaluating work quality

**Core Principle**: If output includes elements that (1) cannot be justified with reasoning, (2) have no relation to the task, and (3) have no relation to the outcome, the agent is hallucinating through pattern-matching.

## Trigger Catalog

### Category 1: Assumption Language Triggers

#### Trigger Pattern

Output contains unverified assessment language:

- "I presume"
- "I think"
- "likely"
- "should be"
- "probably"
- "seems like"
- "appears to"
- "must be"
- "guess"
- "assume"

#### Issue Indicator

1. **Unverified assessment made** - Agent bypassed available verification tools
2. **Self-verification steps omitted** - CoVe checklist not followed
3. **Context poisoning active** - Unverified claim now pollutes conversation history
4. **Pattern-matching from training data** - Not research-based reasoning

#### Next Actions

1. **Immediate**: Flag the specific claim containing assumption language
2. **Verify**: Use available tools (Read, Grep, WebFetch) to verify the claim
3. **Correct**: Replace assumption with verified observation or explicit "unverified" marker
4. **Prevent**: If delegating to sub-agent, add explicit verification requirement to task prompt

**Example**:

❌ **Hallucinated**:

```text
The function likely uses async/await based on common patterns in this codebase.
```

✅ **Verified**:

```text
Grep search for "async def" in target file returned 0 matches. Function uses synchronous implementation (lines 45-67).
```

### Category 2: Timeline/Timespan Language

#### Trigger Pattern

Output contains temporal scheduling language inappropriate for AI agent work:

- "Week 1", "Week 2", "Week N"
- "2 hours", "40 hours", specific duration estimates
- "Next sprint", "Sprint 1", sprint planning references
- "Q1 2025", "By end of month", calendar deadlines
- "Phase 1 (January)", temporal phase labels
- Any Gantt chart or timeline visualization for AI agent plans

#### Issue Indicator

1. **Wrong audience model** - Thinking human team with fixed time capacity, not AI agents
2. **Wrong execution model** - Missing that AI work scales arbitrarily with parallelization
3. **Missing actual requirements** - Should specify dependencies, priorities, sync points instead
4. **Borrowed framework hallucination** - Importing human project management conventions

#### Next Actions

1. **Immediate**: Remove all temporal language from plan
2. **Replace with**:
   - Priority ordering (Priority 1, 2, 3 based on importance/dependencies)
   - Explicit dependencies ("depends on Task A completion")
   - Parallelization markers ("can parallelize with Task B")
   - Synchronization checkpoints ("SYNC: review outputs before next fan-out")
3. **Verify**: Ask "Could 50 AI agents complete this in hours? Could 1 agent complete it in days? Then timeline is meaningless."

**Why Critical**: Timelines are fundamentally meaningless for AI agent work because:

- 50 parallel agents complete "Week 1" work in hours
- 1 sequential agent might take days/weeks for same work
- Execution rate depends entirely on chosen parallelization strategy
- AI agents don't have "weeks" - they execute based on task availability

**Example**:

❌ **Hallucinated**:

```markdown
Priority 1 (Week 1):

- Implement authentication
- Add logging

Priority 2 (Week 2):

- Write tests
- Documentation
```

✅ **Correct**:

```markdown
Priority 1 (Foundational, no dependencies):

- Task A: Implement authentication
  - Dependencies: None
  - Acceptance Criteria: Tests pass, security review approved
  - Can parallelize with: Task B

- Task B: Add logging framework
  - Dependencies: None
  - Acceptance Criteria: Log levels configurable, rotation working
  - Can parallelize with: Task A

SYNC CHECKPOINT 1: Review-Reflect-Revise

- Convergence: Tasks A + B outputs
- Quality Gates: No conflicts in dependencies, patterns consistent
- Proceed only after approval

Priority 2 (Depends on Priority 1 outputs):

- Task C: Write integration tests
  - Dependencies: Task A (auth), Task B (logging)
  - Acceptance Criteria: 80% coverage, all critical paths tested
```

### Category 3: Pseudo-Quantification (Borrowed Rigor)

#### Trigger Pattern

Output contains quantitative artifacts without measurement methodology:

- **Unscaled ratings**: "8.5/10 quality score" without defining scale
- **Unverified metrics**: "70% efficiency improvement" without source citation
- **Fabricated statistics**: "100% consensus (5/5 agents)" without verification
- **Precision without basis**: "9.4/10" suggests false precision
- **ROI percentages**: "60% ROI" without calculation basis

#### Issue Indicator

**Borrowed Rigor Hallucination** (also "Authority Mimicry"):

The model decorates outputs with quantitative artifacts from training corpus WITHOUT:

1. Verifying artifacts are domain-appropriate
2. Establishing measurement methodology
3. Grounding claims in observable evidence
4. Reasoning about whether structure serves actual task

**Core Issue**: Generating what rigorous analysis LOOKS LIKE rather than what rigorous analysis IS.

#### Next Actions

1. **For each quantitative claim, verify**:

   - What observable evidence supports this number?
   - What is the measurement scale/methodology?
   - Can I reproduce this measurement with available tools?

2. **If cannot verify**:

   - Remove the quantification entirely, OR
   - Mark explicitly as estimate: "Estimated at ~70% based on [reasoning]", OR
   - Replace with qualitative assessment: "Significant improvement observed in [specific measurable outcome]"

3. **For ratings (X/10)**:
   - Define objective scale: "Score 1-10 where 1=no tests, 5=basic tests, 10=comprehensive test coverage with edge cases"
   - Provide evidence for rating: "Scored 8/10: has unit tests (lines X-Y), integration tests (lines A-B), missing property-based tests"
   - Better: Replace rating with factual checklist of presence/absence

**Example**:

❌ **Hallucinated**:

```markdown
Code Quality: 8.5/10 Performance: 70% improvement over baseline Test Coverage: Excellent (9/10)
```

✅ **Verified**:

```markdown
Code Quality Assessment:

- ✅ Type hints present (lines 1-450)
- ✅ Docstrings on all public functions
- ✅ No linting errors (ruff check passed)
- ❌ Missing property-based tests
- ❌ No benchmarks for performance claims

Test Coverage: 67% (pytest-cov report, lines 234-890 covered) Performance: Unverified - no baseline measurements found in codebase
```

### Category 4: Incomplete Verification

#### Trigger Pattern

Analysis claims completeness but verification reveals gaps:

- "All agents reviewed" but count doesn't match file count
- "Comprehensive analysis" but files were skipped
- "100% consensus" but actual verification shows disagreement
- "No issues found" without showing verification methodology

#### Issue Indicator

1. **Verification steps skipped** - Agent didn't count/verify completeness
2. **Pattern completion** - Agent generated "feels complete" structure without checking
3. **Assumed coverage** - Trusted incomplete data gathering

#### Next Actions

1. **Count verification**:

   ```claude
   Glob(pattern="path/to/agents/*.md")  # Get actual file list
   # Compare count to agent's claimed coverage
   ```

2. **Coverage verification**:

   - List what WAS analyzed
   - List what SHOULD have been analyzed
   - Identify gaps explicitly

3. **Consensus verification**:
   - Show actual agreement count
   - Show disagreement examples
   - Never claim 100% without showing full verification

**Example**:

❌ **Hallucinated**:

```markdown
Analyzed all 5 agent files with 100% consensus on quality issues.
```

✅ **Verified**:

```markdown
Analysis Coverage:

- Files analyzed: 5 (code-reviewer.md, test-runner.md, refactorer.md, documentation-expert.md, linting-resolver.md)
- Files discovered: 6 (Glob result)
- Missing from analysis: python-portable-script.md
- Coverage: 83% (5/6)

Consensus Assessment:

- Complete agreement: 3/5 files (code-reviewer, test-runner, refactorer)
- Partial agreement: 2/5 files (documentation-expert disagrees on tone, linting-resolver disagrees on auto-fix approach)
- Consensus rate: 60% full agreement, 40% with documented disagreements
```

## Pattern Categories

### Meta-Pattern: Authority Mimicry

**Definition**: Agent generates surface features of authoritative analysis (numbers, timelines, structured frameworks) without underlying verification or domain appropriateness.

**Manifestations**:

- Timeline language (Category 2)
- Pseudo-quantification (Category 3)
- Professional document structure imported from training data
- Frameworks borrowed from human contexts applied to AI contexts

**Detection**: Ask "Does this artifact serve semantic function (describing actual task properties) or aesthetic function (making document look professional)?"

### Meta-Pattern: Context Poisoning

**Definition**: Agent introduces unverified claims into conversation history, creating false foundation for future reasoning.

**Manifestations**:

- Assumption language (Category 1)
- Incomplete verification (Category 4)
- Fabricated metrics that get cited as "established baseline" later

**Detection**: Track assumption language in output. Any unverified claim pollutes context for all subsequent reasoning.

## Correct Alternatives

### For AI Agent Plans

**NEED**:

1. **Priority ordering** - Based on importance and dependencies, not time
2. **Explicit dependencies** - "Depends on Task X" not "After Week 1"
3. **Acceptance criteria per task** - Agent knows objective "done" state
4. **Parallelization markers** - "Can parallelize with Task Y"
5. **Sync checkpoints** - Convergence points for review-reflect-revise cycles
6. **Fan-out/fan-in patterns** - Where parallel work begins and converges

**DO NOT INCLUDE**:

- Timelines, timespans, duration estimates
- Calendar references, sprint labels, temporal phases
- "Week N", "Q1", "Next sprint", "2 hours"

### For Quantitative Claims

**NEED**:

1. **Observable evidence** - Cite specific source
2. **Measurement methodology** - Define how number was derived
3. **Reproducibility** - Show verification steps
4. **Scale definition** - For ratings, define what each point means

**DO NOT INCLUDE**:

- Ratings without scales (8/10 with no criteria)
- Metrics without sources (70% improvement uncited)
- Precision without basis (9.4/10 suggests false rigor)

### For Verification Claims

**NEED**:

1. **Explicit coverage list** - What was checked
2. **Gap identification** - What was skipped/missed
3. **Evidence citations** - Line numbers, file paths, command outputs
4. **Uncertainty markers** - "Unverified", "Estimated", "Based on sample"

**DO NOT INCLUDE**:

- Completeness claims without verification (all, every, 100%)
- Consensus percentages without showing disagreements
- "No issues found" without showing what was checked

## System Prompt Summary

**Compact hallucination detection rules for AI assistant context:**

```text
HALLUCINATION DETECTION TRIGGERS:

1. ASSUMPTION LANGUAGE: "likely", "probably", "I think", "seems like", "appears to", "should be", "must be", "presume", "guess", "assume"
   → Indicates unverified assessment, context poisoning active
   → MUST verify claim with tools or mark "unverified"

2. TIMELINE/TIMESPAN: "Week N", "X hours", "Sprint N", "Q1", "By [date]", any temporal scheduling
   → Indicates wrong execution model for AI agents (work scales with parallelization, not time)
   → MUST replace with: priority ordering, dependencies, sync checkpoints, parallelization markers

3. PSEUDO-QUANTIFICATION: Ratings without scales, metrics without sources, statistics without verification, precision without basis
   → Indicates "borrowed rigor" - mimicking authoritative analysis without underlying verification
   → MUST provide: measurement methodology, observable evidence, or remove quantification

4. INCOMPLETE VERIFICATION: Completeness claims without count verification, consensus percentages without disagreement examples
   → Indicates verification steps skipped
   → MUST show: what was checked, what was skipped, explicit coverage gaps

CORE PRINCIPLE: If output element (1) cannot be justified with reasoning, (2) has no relation to task, (3) has no relation to outcome → hallucination via pattern-matching

CORRECT STRUCTURES:
- AI agent plans: priorities + dependencies + acceptance criteria + sync checkpoints (NO timelines)
- Quantitative claims: evidence + methodology + scale definition (NO unverified metrics)
- Verification: coverage list + gaps + citations (NO assumed completeness)
```

## Examples: Anti-Pattern vs Correct Pattern

### Example 1: Agent Comparative Analysis

❌ **Hallucinated (Borrowed Rigor)**:

```markdown
## Agent Quality Assessment

| Agent         | Quality Score | Coverage  |
| ------------- | ------------- | --------- |
| code-reviewer | 9.4/10        | Excellent |
| test-runner   | 8.0/10        | Good      |
| refactorer    | 8.5/10        | Very Good |

Overall: 100% consensus (5/5 agents) on quality improvements needed.

Implementation Timeline:

- Week 1: High priority fixes
- Week 2: Medium priority enhancements
- Week 3: Documentation updates

Estimated ROI: 70% efficiency improvement
```

**Issues**:

- Unscaled ratings (9.4/10 - what does each point mean?)
- Uncounted consensus (5/5 - were there actually 5 agents?)
- Timeline language (Week 1, 2, 3 - meaningless for AI agents)
- Unverified metric (70% - source? calculation?)
- Qualitative labels without criteria (Excellent, Good - measured how?)

✅ **Correct (Verified)**:

```markdown
## Agent Quality Assessment

Files analyzed: 5 of 6 discovered (83% coverage)

- code-reviewer.md (analyzed)
- test-runner.md (analyzed)
- refactorer.md (analyzed)
- documentation-expert.md (analyzed)
- linting-resolver.md (analyzed)
- python-portable-script.md (NOT analyzed - discovered during verification)

Quality Findings:

**code-reviewer.md**:

- ✅ Has verification checklist (lines 45-67)
- ✅ Includes code examples (lines 89-123)
- ✅ References CLAUDE.md rules (line 23)
- ❌ Missing acceptance criteria specification
- ❌ No sync checkpoint guidance

**test-runner.md**:

- ✅ Defines tool list explicitly (line 12)
- ✅ Has error handling section (lines 78-91)
- ❌ Lacks parallelization strategy
- ❌ No coverage verification methodology

Consensus Assessment:

- Full agreement on issue categories: 3/5 files
- Partial agreement (minor disagreements): 2/5 files
- Files with disagreements: documentation-expert.md (tone preferences differ), linting-resolver.md (auto-fix vs manual-fix approaches differ)

Priority Ordering (Based on Dependencies):

Priority 1 (Foundational, no dependencies):

- Add acceptance criteria templates to all agents
  - Dependencies: None
  - Can parallelize: Yes (independent agent files)
  - Acceptance: Each agent has "Task Complete When" section

Priority 2 (Depends on P1):

- Add sync checkpoint guidance
  - Dependencies: Acceptance criteria templates (P1)
  - Can parallelize: Yes (after P1 complete)
  - Acceptance: Agent prompts reference when to pause for review

SYNC CHECKPOINT: Review P1+P2 outputs for consistency before proceeding

Efficiency impact: Unverified - no baseline task completion measurements exist in current data
```

### Example 2: Implementation Plan

❌ **Hallucinated (Timeline Language)**:

```markdown
Sprint 1 (2 weeks):

- Setup development environment (8 hours)
- Implement core features (40 hours)
- Write initial tests (16 hours)

Sprint 2 (2 weeks):

- Integration testing (20 hours)
- Documentation (12 hours)
- Code review cycles (8 hours)

Total: 4 weeks, 104 hours estimated effort
```

**Issues**:

- Sprint language (AI agents don't have sprints)
- Hour estimates (meaningless - could be 50 parallel agents or 1 sequential)
- Calendar timespan (4 weeks - arbitrary for AI work)
- Missing: dependencies, acceptance criteria, sync points, parallelization strategy

✅ **Correct (Dependency-Based)**:

```markdown
Implementation Plan

Priority 1 (Foundational - no dependencies):

Task A: Setup development environment

- Dependencies: None
- Acceptance Criteria:
  - Python 3.11+ available via uv
  - Pre-commit hooks installed and passing
  - Test framework (pytest) executable
- Can parallelize with: Task B, Task C

Task B: Implement authentication module

- Dependencies: None (self-contained)
- Acceptance Criteria:
  - Unit tests pass (>90% coverage)
  - Type hints validated (mypy clean)
  - Security review checklist completed
- Can parallelize with: Task A, Task C

Task C: Implement logging framework

- Dependencies: None (self-contained)
- Acceptance Criteria:
  - Log levels configurable
  - Rotation working (tested)
  - No conflicts with existing logging
- Can parallelize with: Task A, Task B

SYNC CHECKPOINT 1: Convergence and Review

- Wait for: Tasks A, B, C all complete
- Review: Integration compatibility (do B and C conflict?)
- Quality gates: All acceptance criteria met, no cross-module issues
- Proceed to Priority 2 only after approval

Priority 2 (Integration - depends on P1):

Task D: Integration testing

- Dependencies: Tasks A (environment), B (auth), C (logging)
- Acceptance Criteria:
  - Auth + logging integration tested
  - End-to-end scenarios pass
  - No regression in P1 acceptance tests
- Can parallelize with: Task E

Task E: API documentation

- Dependencies: Task A (environment), Task B (auth module)
- Acceptance Criteria:
  - All public APIs documented
  - Examples executable and tested
  - Docstrings validated (pydocstyle clean)
- Can parallelize with: Task D

SYNC CHECKPOINT 2: Final Review

- Wait for: Tasks D, E complete
- Review: Documentation accuracy, test coverage completeness
- Quality gates: Production readiness checklist
```

## Verification Protocol

When reviewing agent output for hallucinations:

1. **Scan for trigger language**:

   - Ctrl+F for assumption words: "likely", "probably", "think", "seems", "appears"
   - Ctrl+F for timeline words: "week", "sprint", "hour", "Q1", "month"
   - Look for unscaled numbers: "X/10", "X% improvement", statistics

2. **For each trigger found**:

   - Identify the claim being made
   - Ask: "What observable evidence supports this?"
   - Verify using available tools or mark as unverified
   - Replace or remove the hallucinated content

3. **For completeness claims**:

   - Count what was analyzed vs what exists
   - List gaps explicitly
   - Never claim 100%/all/every without showing verification

4. **For AI agent plans**:
   - Remove all temporal language
   - Add: priorities, dependencies, acceptance criteria, sync checkpoints
   - Verify: Does this work with 1 agent sequentially? 50 agents in parallel?

## References

This guide distills insights from reasoning failure analysis in AI-to-AI delegation contexts. Triggers are designed to catch pattern-matching from training data rather than domain-appropriate reasoning.

**Related Documentation**:

- `~/.claude/CLAUDE.md` - Global rules including timeline prohibition, verification protocol
- `./CLAUDE.md` - Skill creation verification requirements
- Self-verification principles: Hypothesis → Prediction → Experimentation → Verification → Conclusion

**Core Rules Referenced**:

- "The model must never state timelines or estimates for task completion - this is a red-flag for hallucination"
- "The model must distinguish verified information from reasonable assumptions"
- "The model must forbid unverified technical details, cargo-cult patterns, and hidden uncertainty"
