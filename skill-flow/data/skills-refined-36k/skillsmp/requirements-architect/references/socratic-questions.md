# Socratic Questioning Framework for PRD Development

Use this framework to sharpen strategic thinking before writing any PRD. Work through each question systematically, documenting answers and challenging assumptions.

---

## Phase 1: Problem Space Analysis

### Question 1: Job-to-Be-Done
**Ask**: What specific job-to-be-done does this solve? Who experiences this problem?

**Follow-up probes**:
- Is this a functional job, emotional job, or social job?
- How frequently does this job arise?
- What triggers the need for this job?
- Who else is involved when this job needs to be done?

**Devil's advocate**: Are you solving the real job or a symptom of a deeper need?

---

### Question 2: Problem Evidence
**Ask**: What evidence exists that this is a real, significant problem?

**Required evidence types**:
- **Quantitative**: Usage data, support tickets, churn analysis, survey scores
- **Qualitative**: User interviews, feedback themes, behavioral observations

**Follow-up probes**:
- How many users are affected?
- What's the financial impact of not solving this?
- How long has this problem existed?
- Is the problem growing or shrinking?

**Devil's advocate**: Is the evidence strong enough, or are we seeing patterns we want to see?

---

### Question 3: Current Solutions
**Ask**: How are users solving this problem today? What's the pain of the status quo?

**Document**:
- Existing workarounds
- Competitor solutions
- Manual processes
- "Do nothing" approach

**Follow-up probes**:
- Why haven't existing solutions worked?
- What do users like about current solutions?
- What would make them switch?

**Devil's advocate**: Is the status quo "good enough"? What would change that?

---

## Phase 2: Strategic Fit Analysis

### Question 4: Company Strategy Alignment
**Ask**: How does this align with company strategy and competitive positioning?

**Evaluate against**:
- Company mission and vision
- Strategic priorities (this quarter/year)
- Competitive differentiation
- Core competencies

**Follow-up probes**:
- Does this strengthen our competitive moat?
- Does this move us toward or away from our vision?
- What would we NOT do if we do this?

**Devil's advocate**: Are we building this because it's strategic, or because it's interesting?

---

### Question 5: Timing
**Ask**: Why is NOW the right time to build this? What's changed?

**Consider**:
- Market timing (customer readiness)
- Technology timing (is it feasible now?)
- Competitive timing (first mover vs fast follower)
- Internal timing (resources, priorities)

**Follow-up probes**:
- What happens if we wait 6 months? 12 months?
- What risks are there in moving now?
- What external factors could change?

**Devil's advocate**: What if we're too early? What if we're too late?

---

### Question 6: Critical Assumptions
**Ask**: What must be true for this to succeed?

**Categories**:
- **User assumptions**: Will they adopt? Will they pay? Will they retain?
- **Technical assumptions**: Can we build it? Will it scale? Will it perform?
- **Business assumptions**: Is the market big enough? Can we compete?

**Follow-up probes**:
- How can we validate each assumption?
- What's the cheapest way to test the riskiest assumption?
- What happens if an assumption is wrong?

**Devil's advocate**: Which assumption are you most uncertain about? What would you do if it's false?

---

## Phase 3: Solution Space Analysis

### Question 7: Alternative Approaches
**Ask**: What are 2-3 fundamentally different approaches to solve this?

**Generate alternatives by varying**:
- Build vs buy vs partner
- Automated vs manual vs hybrid
- Self-serve vs high-touch
- MVP vs full-featured

**For each alternative, document**:
- Pros and cons
- Resource requirements
- Time to value
- Risk profile

**Devil's advocate**: Have you considered the approach you immediately dismissed? Why was it dismissed?

---

### Question 8: Scope Boundaries
**Ask**: What are we explicitly NOT building? What's out of scope?

**Document**:
- Features considered but rejected (and why)
- Adjacent problems we won't solve
- User segments we won't serve
- Quality levels we won't target

**Follow-up probes**:
- Where will we say "no" to customers?
- What edge cases will we not handle?
- What integrations are out of scope?

**Devil's advocate**: Is your scope too narrow to be valuable? Too broad to be achievable?

---

### Question 9: Risk Assessment
**Ask**: What are the main risks? Technical, market, operational?

**Risk categories**:
| Category | Examples |
|----------|----------|
| Technical | Scalability, complexity, dependencies, security |
| Market | Adoption, competition, timing, pricing |
| Operational | Support burden, maintenance, compliance |
| Execution | Team capability, timeline, budget |

**For each risk**:
- Likelihood (L/M/H)
- Impact (L/M/H)
- Mitigation strategy
- Contingency plan

**Devil's advocate**: What's the risk you're most afraid to talk about?

---

## Phase 4: Success Definition

### Question 10: Success Metrics
**Ask**: How will we know this succeeded? What metrics prove value?

**Metric categories**:
- **Leading indicators**: Early signals (Week 1-4)
- **Lagging indicators**: Ultimate outcomes (Month 3+)
- **Quality metrics**: Not just adoption, but quality of adoption

**For each metric, specify**:
- Baseline (where are we today?)
- Target (what's "success"?)
- Stretch goal (what's "great"?)
- Measurement method (how will we track?)

**Devil's advocate**: If we hit these metrics, are we certain we've created value?

---

### Question 11: Phase 1 Definition
**Ask**: What does "good enough" for Phase 1 look like?

**Define MVP by**:
- Minimum features for value delivery
- Acceptable quality thresholds
- Target user segment for initial launch
- Success criteria for Phase 1

**Follow-up probes**:
- What can we defer to Phase 2?
- What's the fastest path to learning?
- What would make us decide to stop vs continue?

**Devil's advocate**: Is your Phase 1 too small to validate anything? Too big to ship quickly?

---

## Usage Instructions

1. **Work through all questions sequentially** - Don't skip, even for "obvious" projects
2. **Document all answers** - Written answers force clarity
3. **Challenge every answer** - Use the devil's advocate prompts
4. **Share findings** - Strategic alignment comes from shared understanding
5. **Revisit during development** - Assumptions may change

## Output Template

After completing this framework, summarize:

```markdown
## Strategic Summary

### Problem Statement
[Concise description of the problem with evidence]

### Strategic Rationale
[Why this, why now, how it fits strategy]

### Key Assumptions (to validate)
1. [Assumption 1]
2. [Assumption 2]
3. [Assumption 3]

### Chosen Approach
[Description of selected approach]

### Out of Scope
[Explicit boundaries]

### Success Metrics
| Metric | Baseline | Target | Measurement |
|--------|----------|--------|-------------|
| ... | ... | ... | ... |

### Top Risks
| Risk | L/I | Mitigation |
|------|-----|------------|
| ... | ... | ... |

### Phase 1 Definition
[MVP scope description]
```
