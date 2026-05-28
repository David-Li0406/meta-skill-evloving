# Quality Rubric Explained - 0-70 Scoring System

Detailed breakdown of agent quality scoring across 7 categories.

## Scoring Overview

| Category | Max Points | Weight | Description |
|----------|------------|--------|-------------|
| Phase Structure | 15 | 21% | 3-5 phases with objectives and deliverables |
| Success Criteria | 15 | 21% | 10-16 specific, measurable criteria |
| Self-Critique | 10 | 14% | 6-10 domain-specific questions |
| Progressive Disclosure | 10 | 14% | 150-250 lines or references used |
| Tool Usage | 10 | 14% | Tools match phase usage |
| Documentation | 10 | 14% | Examples, purpose, references |
| Edge Case Handling | 10 | 14% | Error scenarios documented |
| **TOTAL** | **70** | **100%** | Sum of all categories |

**Grading Scale**:
- **60-70**: Excellent (production ready)
- **50-59**: Good (minor improvements)
- **40-49**: Fair (significant work needed)
- **<40**: Poor (major refactoring required)

---

## Category 1: Phase Structure (0-15 pts)

**What it measures**: Quality of agent's workflow organization.

### Scoring Breakdown

**Phase Count (0-10 pts)**:
- 3-5 phases = 10 pts ✅ (optimal)
- 2 phases = 5 pts ⚠️ (too simple)
- 6+ phases = 5 pts ⚠️ (too complex)
- 0-1 phases = 0 pts ❌ (no structure)

**Objectives (0-3 pts)**:
- 80%+ phases have objectives = 3 pts ✅
- 50-79% have objectives = 1 pt ⚠️
- <50% have objectives = 0 pts ❌

**Deliverables (0-2 pts)**:
- 80%+ phases have deliverables = 2 pts ✅
- 50-79% have deliverables = 1 pt ⚠️
- <50% have deliverables = 0 pts ❌

### Examples

**15/15 (Perfect)**:
```markdown
## Phase 1: Static Code Analysis
**Objective**: Scan codebase for leak patterns
**Actions**: [3 specific actions with tools]
**Deliverable**: List of violations with severity ratings

## Phase 2: Runtime Validation
**Objective**: Execute runtime checks
**Actions**: [2 specific actions]
**Deliverable**: Validation results with pass/fail status

## Phase 3: Report Generation
**Objective**: Create audit report
**Actions**: [2 actions]
**Deliverable**: Comprehensive audit report
```
✅ 3 phases, all have objectives and deliverables

**10/15 (Good)**:
```markdown
## Phase 1: Requirements Gathering
**Objective**: Understand user needs
**Actions**: [3 actions]

## Phase 2: Implementation
**Objective**: Build solution
**Actions**: [5 actions]
**Deliverable**: Working implementation

## Phase 3: Testing
**Objective**: Validate quality
**Deliverable**: Test results
```
✅ 3 phases, but Phase 1 missing deliverable

---

## Category 2: Success Criteria (0-15 pts)

**What it measures**: Quality and quantity of completion checkpoints.

### Scoring Breakdown

**Quantity**:
- 10-16 criteria = 15 pts ✅ (optimal)
- 7-9 criteria = 10 pts ⚠️ (acceptable)
- >16 criteria = 10 pts ⚠️ (too many)
- 4-6 criteria = 5 pts ❌ (too few)
- 0-3 criteria = 0 pts ❌ (missing)

**Quality** (assessed subjectively):
- Specific and measurable = full points
- Some vagueness = -2 to -5 pts

### Examples

**15/15 (Perfect)**:
```markdown
## Success Criteria

- ✅ Temporal awareness established with current date
- ✅ Phase 1: 47 potential leak patterns identified
- ✅ Phase 2: Runtime validation completed in <5 seconds
- ✅ All findings validated with code evidence
- ✅ Report includes executive summary (1-2 pages)
- ✅ Report includes technical details with line numbers
- ✅ Confidence level >85% with supporting evidence
- ✅ False positive rate <10%
- ✅ Edge cases documented (missing files, corrupted data)
- ✅ Performance acceptable (<10 min total)
- ✅ Output format matches template
- ✅ All recommendations actionable
[12 total - specific, measurable]
```
✅ 12 criteria, all specific with measurable outcomes

**5/15 (Poor)**:
```markdown
## Success Criteria

- ✅ Task completed
- ✅ Output generated
- ✅ Quality acceptable
```
❌ Only 3 criteria, all vague

---

## Category 3: Self-Critique (0-10 pts)

**What it measures**: Quality of agent's self-awareness questions.

### Scoring Breakdown

- 6-10 questions = 10 pts ✅
- 4-5 questions = 6 pts ⚠️
- 2-3 questions = 3 pts ❌
- 0-1 questions = 0 pts ❌

**Domain specificity bonus/penalty**:
- All domain-specific = +0 pts
- Some generic = -2 pts
- All generic = -5 pts

### Examples

**10/10 (Perfect)**:
```markdown
## Self-Critique

1. **Domain Accuracy**: Did I correctly identify all Kaggle competition leak patterns?
2. **Coverage**: Did I audit ALL feature engineering files, not just the main pipeline?
3. **False Positives**: Could any flagged patterns be safe in this specific context?
4. **False Negatives**: What subtle leak patterns might I have missed (rolling with center=True)?
5. **Confidence Basis**: What evidence supports my 92% confidence level?
6. **Verification**: How can the user independently verify each violation?
7. **Temporal Accuracy**: Did I use correct current date for all timestamps?
[7 questions - all domain-specific]
```
✅ 7 questions, all specific to Kaggle leak auditing

**3/10 (Poor)**:
```markdown
## Self-Critique

1. Did I understand the requirements?
2. Did I complete the task?
3. Is the output good?
```
❌ 3 questions, all generic (apply to any agent)

---

## Category 4: Progressive Disclosure (0-10 pts)

**What it measures**: Appropriate length and use of references.

### Scoring Breakdown

**Length-based**:
- 150-250 lines = 10 pts ✅ (ideal range)
- 100-149 lines = 8 pts ⚠️ (short but okay)
- 251-300 lines + references = 8 pts ⚠️ (okay with refs)
- 251-300 lines, no references = 4 pts ❌ (extract details)
- >300 lines + references = 6 pts ⚠️ (long but acceptable)
- >300 lines, no references = 2 pts ❌ (major refactoring)

### Examples

**10/10 (Perfect)**:
```markdown
# Agent Name (200 lines total)

## Pattern Detection

**Reference Documentation**: `/refs/patterns.md` (500 lines)

**Key patterns** (see reference):
1. Pattern A (CRITICAL)
2. Pattern B (WARNING)
```
✅ 200 lines main, details in references

**4/10 (Poor)**:
```markdown
# Agent Name (350 lines total)

## Pattern Detection

**Pattern A (CRITICAL)**:
[50 lines of detailed pattern explanation]

**Pattern B (WARNING)**:
[50 lines of detailed pattern explanation]

[No references - everything inline]
```
❌ 350 lines, no progressive disclosure

---

## Category 5: Tool Usage (0-10 pts)

**What it measures**: Tool declaration accuracy.

### Scoring Breakdown

- Tools declared = 5 pts
- All tools used = 5 pts
- 1-2 tools unused = 3 pts
- 3+ tools unused = 1 pt

### Examples

**10/10 (Perfect)**:
```yaml
tools: Read, Grep, Write
```
```markdown
## Phase 1
**Actions**:
1. Use Grep to search for patterns
2. Use Read to analyze files
3. Use Write to generate report
```
✅ All 3 declared tools are used

**6/10 (Fair)**:
```yaml
tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch
```
```markdown
## Phase 1
**Actions**:
1. Use Read to load file
2. Use Write to save output
```
❌ Declared 7 tools, only used 2

---

## Category 6: Documentation (0-10 pts)

**What it measures**: Presence of supporting documentation.

### Scoring Breakdown

- Examples section = 3 pts
- Description in frontmatter = 3 pts
- Purpose statement = 2 pts
- References to external docs = 2 pts

### Examples

**10/10 (Perfect)**:
```yaml
description: Clear one-sentence description. Use when [trigger]. Examples: "Find X", "Analyze Y"
```
```markdown
**Purpose**: [2 sentences on what this agent does]

## Examples

### Example 1: Simple Task
[Concrete example]

### Example 2: Complex Task
[Concrete example]

**Reference Documentation**:
- `/refs/patterns.md`
- `/refs/api-reference.md`
```
✅ All 4 components present

---

## Category 7: Edge Case Handling (0-10 pts)

**What it measures**: Error handling and boundary conditions.

### Scoring Breakdown

- 10+ edge case mentions = 10 pts ✅
- 5-9 mentions = 7 pts ⚠️
- 2-4 mentions = 4 pts ⚠️
- 0-1 mentions = 0 pts ❌

**Edge case keywords**: error, fail, exception, missing, invalid, empty, null, timeout, boundary

### Examples

**10/10 (Perfect)**:
```markdown
## Edge Cases

**Missing Files**:
- If input file doesn't exist, log error and skip
- Continue processing remaining files

**Invalid Data**:
- If CSV malformed, attempt partial parse
- Report which rows failed

**Timeout**:
- If API call exceeds 30s, retry with exponential backoff
- Max 3 retries, then fail gracefully

**Empty Input**:
- If no patterns found, return empty list (not error)
- Log warning for user awareness

**Boundary Conditions**:
- Handle files >1GB by streaming
- Handle 0-byte files without crashing
```
✅ 11 edge case scenarios documented

**0/10 (Poor)**:
```markdown
[No edge case handling mentioned]
```
❌ No error handling documented

---

## How to Improve Scores

### From <40 to 40-49 (Fair)
1. Add phase structure (3-5 phases) = +10 pts
2. Add 10 success criteria = +10 pts
3. Add 6 self-critique questions = +6 pts
**Total**: +26 pts minimum

### From 40-49 to 50-59 (Good)
1. Improve success criteria specificity = +3-5 pts
2. Add edge case handling = +7-10 pts
3. Add documentation/examples = +5-7 pts
**Total**: +15-22 pts

### From 50-59 to 60+ (Excellent)
1. Refine self-critique to be domain-specific = +2-4 pts
2. Add temporal awareness pattern = (not scored, but critical)
3. Optimize line count with progressive disclosure = +2-4 pts
4. Remove unused tools from frontmatter = +2 pts
5. Add comprehensive edge case handling = +3 pts
**Total**: +9-13 pts

---

## Real Agent Scores

| Agent | Total | Phase | Success | Critique | Disclosure | Tools | Docs | Edge |
|-------|-------|-------|---------|----------|------------|-------|------|------|
| legal-agent | 68/70 | 15 | 15 | 10 | 8 | 10 | 10 | 0 |
| ceo-orchestrator | 64/70 | 15 | 14 | 9 | 10 | 10 | 6 | 0 |
| agent-hr-manager | 62/70 | 15 | 13 | 10 | 4 | 10 | 10 | 0 |

**Common weakness**: Edge case handling (0-2/10 across all agents)

**Common strength**: Phase structure (15/15 in all agents)

---

## Validation Command

```bash
~/.claude/skills/agent-creator/scripts/validate_agent.py /path/to/agent.md
```

**Output**:
- Detailed score breakdown per category
- Specific recommendations for improvement
- Pass/fail based on 60-point threshold

---

**Remember**: Quality > Quantity. A 65/70 agent with strong domain specificity beats a 70/70 agent with generic patterns.
