# Agent Examples - Annotated High-Quality Agents

This document provides annotated examples of production-quality agents following v2 architecture patterns.

## Example 1: legal-agent (68/70 Quality Score)

**Why it's excellent**:
- Progressive disclosure (264 lines main + 2 reference docs)
- Temporal awareness with REQUIRED label
- 14 success criteria (specific and measurable)
- 8 self-critique questions (domain-specific)
- Proper tool selection (only what's used)

**Key excerpts**:

```markdown
## Phase 1: Temporal Awareness & Requirements Intake

**Actions**:
1. **Establish Temporal Context** (REQUIRED):
   ```bash
   CURRENT_DATE=$(date '+%Y-%m-%d')
   READABLE_DATE=$(date '+%B %d, %Y')
   ```
```

**Lesson**: REQUIRED label makes temporal awareness unmissable.

```markdown
## Success Criteria

- ✅ Temporal awareness established with current date
- ✅ Legal domain identified (Finnish vs EU vs cross-jurisdiction)
- ✅ Citations validated against Finlex/EUR-Lex APIs
- ✅ All statutes current (not repealed or amended)
- ✅ Bilingual support (Finnish/English) maintained
[14 total - specific and measurable]
```

**Lesson**: Success criteria reference concrete outputs, not vague outcomes.

```markdown
**Reference Documentation**: 
- `/agents/refs/legal-agent-patterns.md` (532 lines)
- `/agents/refs/legal-databases-integration.md` (312 lines)

**Key patterns** (see reference for details):
1. Finnish citation format (HE 309/1993 vp)
2. EU citation format (32016R0679)
3. Cross-reference validation
```

**Lesson**: Main agent stays concise (264 lines), details in references.

---

## Example 2: ceo-orchestrator (244 lines)

**Why it's excellent**:
- Integrated-reasoning integration for complex decisions
- Worker agent registry with estimated durations
- Clear decision tree (when to delegate vs decide)
- 12 success criteria
- 7 self-critique questions

**Key excerpts**:

```markdown
## Decision Tree: Delegate vs Direct Decision

**Delegate to integrated-reasoning** when:
- 8+ decision dimensions
- Strategic importance (multi-project impact)
- High confidence required (>90%)
- Complex trade-offs

**Direct decision** when:
- Simple task (<3 decision points)
- Well-precedented
- Single project impact
```

**Lesson**: Decision trees make multi-mode agents clear.

```markdown
## Worker Agent Registry

**Legal Agent** (`legal-agent`)
- Typical Duration: 2-10 minutes
- Benchmark: Bilingual NDA = 3 min 51 sec
- Use: Legal compliance, contract review, citation validation

**Agent HR Manager** (`agent-hr-manager`)
- Typical Duration: 2-14 minutes
- Benchmark: Agent creation = 2 min 9 sec, skill creation = 14 min 4 sec
```

**Lesson**: Real benchmarks from production use, not guesses.

---

## Example 3: agent-hr-manager (748 lines, Meta-Agent)

**Why it's excellent**:
- Delegates to skill-creator for skill creation (single source of truth)
- Uses integrated-reasoning for 8+ dimension problems
- Quality rubric scoring (0-70 scale)
- 11 self-critique questions
- Deployment to both global + local

**Key excerpts**:

```markdown
### For Skill Creation:

**IMPORTANT**: Delegate to the skill-creator skill for all skill creation tasks.

1. **Invoke skill-creator skill**:
   # The skill-creator skill has comprehensive, up-to-date instructions
```

**Lesson**: Meta-agents delegate to specialized skills rather than duplicate knowledge.

```markdown
## Self-Critique

4. **Skill Delegation**: If creating a skill, did I delegate to skill-creator skill instead of implementing manually?
```

**Lesson**: Self-critique enforces delegation patterns.

---

## Common Patterns Across Excellent Agents

### 1. Temporal Awareness Pattern
```markdown
## Phase 1: [Phase Name] & Temporal Awareness

1. **Establish Temporal Context** (REQUIRED):
   ```bash
   CURRENT_DATE=$(date '+%Y-%m-%d')
   READABLE_DATE=$(date '+%B %d, %Y')
   ```
```

### 2. Specific Success Criteria
✅ GOOD: "Generated report includes 5 sections: summary, findings, evidence, recommendations, confidence score"
❌ BAD: "Agent works correctly"

### 3. Domain-Specific Self-Critique
✅ GOOD: "Did I validate all legal citations against Finlex API?"
❌ BAD: "Did I do a good job?"

### 4. Progressive Disclosure (>250 lines)
```markdown
**Reference Documentation**: `/path/to/refs/agent-patterns.md`

**Key patterns**:
1. Pattern A (CRITICAL)
2. Pattern B (WARNING)
```

### 5. Tool Minimalism
✅ GOOD: `tools: Read, Grep, Write` (only what's used)
❌ BAD: `tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch, Task` (when only Read/Write used)

---

## Anti-Examples (What NOT to Do)

### Bad Example: Missing Temporal Awareness
```markdown
## Phase 1: Requirements Gathering

**Actions**:
1. Understand user needs
2. Identify scope
```
❌ No date checking = documents with wrong dates

### Bad Example: Vague Success Criteria
```markdown
## Success Criteria

- ✅ Task completed
- ✅ Output generated
- ✅ Quality acceptable
```
❌ Can't validate if these are met

### Bad Example: Generic Self-Critique
```markdown
## Self-Critique

1. Did I understand the requirements?
2. Did I complete the task?
3. Is the output good?
```
❌ Applies to every agent, not domain-specific

---

## Quality Score Breakdown

| Agent | Score | Phase | Success | Self-Crit | Disclosure | Tools | Docs | Edge | Notes |
|-------|-------|-------|---------|-----------|------------|-------|------|------|-------|
| legal-agent | 68/70 | 15/15 | 15/15 | 10/10 | 8/10 | 10/10 | 10/10 | 0/10 | Missing edge cases |
| ceo-orchestrator | 64/70 | 15/15 | 14/15 | 9/10 | 10/10 | 10/10 | 6/10 | 0/10 | Could add examples |
| agent-hr-manager | 62/70 | 15/15 | 13/15 | 10/10 | 4/10 | 10/10 | 10/10 | 0/10 | Long (748 lines) |

**Analysis**: Even excellent agents (60+) have room for improvement. Edge case handling is commonly weak (0-2/10 across agents).

---

## Lessons Learned

1. **Temporal awareness is non-negotiable** - REQUIRED label in Phase 1
2. **Success criteria must be measurable** - Specific outputs, not vague goals
3. **Self-critique must be domain-specific** - Not generic questions
4. **Progressive disclosure at 250 lines** - Extract details to references
5. **Tools should match usage** - Only declare what phases use
6. **Edge cases often overlooked** - Explicitly document error handling
7. **Benchmarks beat guesses** - Use real timing data, not estimates
8. **Delegation beats duplication** - Reference skills/patterns, don't copy
