---
name: hypothesis-elimination
description: Systematic elimination reasoning for diagnosis and debugging. Use when you need to identify THE cause among many possibilities through evidence-based elimination. Ideal for production incidents, bug diagnosis, root cause analysis, and differential diagnosis. Unlike BoT (which explores), HE eliminates. Example: "Server is slow" → Generate 10 hypotheses, design discriminating tests, eliminate 9, confirm 1.
license: MIT
---

# Hypothesis-Elimination Reasoning (HE)

**Purpose**: Systematic identification of root causes through evidence-based elimination. Unlike exploration methodologies (BoT, ToT), HE is designed to NARROW possibilities, not expand them.

## When to Use Hypothesis-Elimination

**✅ Use HE when:**
- Problem has ONE correct answer among many possibilities
- Evidence can discriminate between hypotheses
- Time-critical diagnosis (production incidents, debugging)
- "What caused X?" questions
- Differential diagnosis scenarios

**❌ Don't use HE when:**
- Multiple solutions are equally valid (use BoT)
- Need to optimize among options (use ToT)
- No discriminating evidence available
- Creative/generative problems

**Examples:**
- "Why is the API returning 500 errors?" ✅
- "What's causing memory leaks in production?" ✅
- "Which database should we use?" ❌ (use ToT)
- "What features should we build?" ❌ (use BoT)

---

## Core Methodology: 5-Phase HEDAM Process

### Phase 1: Hypothesis Generation (Diverge)

**Goal**: Generate ALL plausible hypotheses without filtering

**Process:**
1. State the observable symptom precisely
2. Generate hypotheses across ALL relevant categories:
   - Recent changes (code, config, infrastructure)
   - External dependencies (APIs, services, network)
   - Resource exhaustion (memory, CPU, disk, connections)
   - Data issues (corruption, volume, format)
   - Timing/race conditions
   - Security incidents
   - Human error
   - Unknown/novel causes

3. For each hypothesis, note:
   - Mechanism: How would this cause the symptom?
   - Prior probability: Based on frequency in similar situations
   - Discriminating evidence: What would prove/disprove this?

**Template:**
```markdown
## Hypothesis [N]: [Name]
- **Mechanism**: [How this causes the symptom]
- **Prior Probability**: [Low/Medium/High] - [Justification]
- **Supporting Evidence Needed**: [What would increase probability]
- **Eliminating Evidence Needed**: [What would rule this out]
```

**Quantity**: Generate 8-15 hypotheses. If fewer than 8, challenge assumptions.

---

### Phase 2: Evidence Hierarchy Design

**Goal**: Design the most efficient evidence-gathering sequence

**Principle**: Gather DISCRIMINATING evidence first (evidence that eliminates multiple hypotheses)

**Process:**
1. List all potential evidence sources:
   - Logs (application, system, network)
   - Metrics (CPU, memory, latency, error rates)
   - Recent changes (git log, deployment history)
   - Reproduction attempts
   - User reports / patterns
   - External status pages

2. Score each evidence source:
   - **Discrimination Power**: How many hypotheses does this affect? (1-10)
   - **Acquisition Cost**: How long/difficult to obtain? (1-10, lower = easier)
   - **Priority Score**: Discrimination / Cost

3. Rank evidence sources by priority score
4. Design evidence-gathering sequence (highest priority first)

**Example:**
```markdown
| Evidence Source | Discriminates | Cost | Priority |
|-----------------|---------------|------|----------|
| Error logs (last hour) | 8 hypotheses | 2 | 4.0 ⬅️ First |
| Recent deployments | 5 hypotheses | 1 | 5.0 ⬅️ First |
| Memory metrics | 3 hypotheses | 2 | 1.5 |
| Network trace | 4 hypotheses | 6 | 0.67 |
| Full reproduction | 10 hypotheses | 8 | 1.25 |
```

---

### Phase 3: Systematic Elimination

**Goal**: Eliminate hypotheses through evidence, not intuition

**Process:**
For each evidence source (in priority order):

1. **Gather evidence** (read logs, check metrics, etc.)

2. **Update ALL hypotheses**:
   ```markdown
   ### Evidence: [What was found]

   | Hypothesis | Impact | New Status |
   |------------|--------|------------|
   | H1: Memory leak | No memory growth seen | ELIMINATED |
   | H2: DB connection pool | Connection count normal | ELIMINATED |
   | H3: Slow external API | Latency spike at 14:32 | STRENGTHENED |
   | H4: Recent deployment | Deploy at 14:30 | STRENGTHENED |
   ```

3. **Track elimination count**: Stop when 1-2 hypotheses remain

4. **Avoid confirmation bias**: Actively seek evidence AGAINST remaining hypotheses

**Elimination Criteria:**
- **ELIMINATED**: Evidence directly contradicts mechanism
- **WEAKENED**: Evidence reduces probability but doesn't eliminate
- **UNCHANGED**: Evidence doesn't affect this hypothesis
- **STRENGTHENED**: Evidence increases probability

---

### Phase 4: Confirmation Testing

**Goal**: Confirm the remaining hypothesis through targeted testing

**Process:**
1. For the leading hypothesis, identify:
   - **Prediction**: If this is the cause, what else should we observe?
   - **Test**: How can we verify this prediction?
   - **Expected result**: What confirms the hypothesis?

2. Execute confirmation test

3. Evaluate:
   - **CONFIRMED**: Prediction matched, mechanism verified
   - **PARTIAL**: Some predictions matched, uncertainty remains
   - **REFUTED**: Prediction failed, reopen eliminated hypotheses

**Confirmation Checklist:**
- [ ] Can we reproduce the issue with the identified cause?
- [ ] Does fixing the cause resolve the symptom?
- [ ] Does the timeline match (cause preceded symptom)?
- [ ] Is the mechanism physically/logically possible?

---

### Phase 5: Root Cause Documentation

**Goal**: Document findings for future reference and prevention

**Template:**
```markdown
## Root Cause Analysis: [Issue Title]

### Summary
- **Symptom**: [What was observed]
- **Root Cause**: [Confirmed cause]
- **Mechanism**: [How the cause produced the symptom]
- **Timeline**: [When cause occurred, when symptom appeared]

### Elimination Path
1. Started with [N] hypotheses
2. [Evidence 1] eliminated [X] hypotheses
3. [Evidence 2] eliminated [Y] hypotheses
4. Confirmed via [Test]

### Hypotheses Considered and Eliminated
| Hypothesis | Eliminated By | Key Evidence |
|------------|---------------|--------------|
| H1 | Evidence 1 | [Specific finding] |
| H2 | Evidence 2 | [Specific finding] |

### Prevention
- [ ] [Action to prevent recurrence]
- [ ] [Monitoring to detect earlier]

### Confidence: [X]%
- [Justification for confidence level]
```

---

## Time-Critical Mode (Incident Response)

When time is critical, use accelerated HE:

**5-Minute Triage:**
1. Check last 3 deployments (30 sec)
2. Check external dependency status pages (30 sec)
3. Check error rate spike timing (1 min)
4. Check resource exhaustion (CPU, mem, disk) (1 min)
5. Check for similar recent incidents (1 min)
6. Form top-2 hypotheses (1 min)

**Parallel Elimination:**
- Assign different team members to different evidence sources
- Use chat/war room for real-time hypothesis updates
- Timebox each investigation track (10 min max)

---

## Common Mistakes

1. **Premature Convergence**: Latching onto first plausible hypothesis
   - Fix: Force generation of 8+ hypotheses before investigating

2. **Confirmation Bias**: Seeking evidence FOR favorite hypothesis
   - Fix: Actively try to DISPROVE remaining hypotheses

3. **Ignoring Low-Probability Causes**: Novel causes get eliminated by assumption
   - Fix: Keep "Unknown/Novel" as permanent hypothesis until confirmed

4. **Evidence Tunnel Vision**: Only looking at familiar evidence sources
   - Fix: Use the Evidence Hierarchy Design phase systematically

5. **Incomplete Elimination**: Declaring victory with 3+ hypotheses remaining
   - Fix: Require 1-2 remaining before confirmation phase

---

## Integration with Other Patterns

**HE → SRC**: After identifying root cause, use Self-Reflecting Chain to trace the exact failure path

**BoT → HE**: If problem is "what could go wrong?", use BoT first to generate failure modes, then HE when a failure occurs

**HE → ToT**: After finding root cause, use ToT to evaluate fix options

---

## Confidence Calibration

| Remaining Hypotheses | Max Confidence |
|---------------------|----------------|
| 1 (confirmed) | 90-95% |
| 2 (one leading) | 70-80% |
| 3+ | <60% - need more evidence |
| All eliminated | 0% - missing hypothesis, restart |

---

## Quick Reference

```
HEDAM Process:
H - Hypothesis Generation (8-15 possibilities)
E - Evidence Hierarchy (prioritize discriminating evidence)
D - Discrimination/Elimination (update all hypotheses per evidence)
A - Assertion/Confirmation (test leading hypothesis)
M - Memorialize (document for future)
```
